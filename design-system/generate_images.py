#!/usr/bin/env python3
"""L'Amour theme image generator + Shopify uploader.

Generates missing theme images via Gemini image model, uploads them to Shopify
using the staged-upload flow, and writes CDN URLs to shopify_cdn_urls.json.

Dependencies:
    pip install google-genai requests python-dotenv

Auth:
    - Gemini: uses ADC via Vertex AI — run `gcloud auth application-default login`
      GCP_PROJECT_ID and GCP_LOCATION are read from .env
    - Shopify: uses SHOPIFY_CLIENT_ID + SHOPIFY_CLIENT_SECRET from .env via
      OAuth client_credentials grant — token is fetched automatically at runtime.
      Token is valid for 24 h; no manual shpat_ token required.
"""

import json
import mimetypes
import os
import time
from pathlib import Path

import requests
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv(Path(__file__).parent.parent / ".env")

# ── Config ────────────────────────────────────────────────────────────────────

SHOPIFY_STORE     = os.environ["SHOPIFY_STORE"]          # 0b8499-39.myshopify.com
SHOPIFY_CLIENT_ID = os.environ["SHOPIFY_CLIENT_ID"]
SHOPIFY_CLIENT_SECRET = os.environ["SHOPIFY_CLIENT_SECRET"]
GCP_PROJECT  = os.environ.get("GCP_PROJECT_ID")
# gemini-3-pro-image-preview is a global model — must use "global", not a regional endpoint
GCP_LOCATION = os.environ.get("GCP_LOCATION", "global")
CDN_FILE   = Path(__file__).parent / "shopify_cdn_urls.json"
OUTPUT_DIR = Path(__file__).parent / "_generated"

MODEL = "gemini-3-pro-image-preview"


# ── Shopify auth ──────────────────────────────────────────────────────────────

def get_shopify_token() -> str:
    """Exchange client credentials for a 24-hour Admin API access token."""
    resp = requests.post(
        f"https://{SHOPIFY_STORE}/admin/oauth/access_token",
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        data={
            "grant_type":    "client_credentials",
            "client_id":     SHOPIFY_CLIENT_ID,
            "client_secret": SHOPIFY_CLIENT_SECRET,
        },
        timeout=15,
    )
    resp.raise_for_status()
    token = resp.json().get("access_token")
    if not token:
        raise RuntimeError(f"No access_token in response: {resp.text}")
    print(f"  Shopify token obtained (expires in ~24 h)")
    return token

# ── Image specs ───────────────────────────────────────────────────────────────
# Only images NOT already in shopify_cdn_urls.json. Prompts match the L'Amour
# visual language: dark, editorial, signature pink (#f597b1), luxury fragrance.

IMAGES = [
    {
        "filename": "about-1.png",
        "aspect_ratio": "4:3",
        "prompt": (
            "Elegant lifestyle photograph of a woman's wrist holding a luxury perfume bottle, "
            "warm golden-hour light, marble surface, dried rose petals, "
            "editorial beauty photography, muted warm tones with soft pink highlights, "
            "photorealistic, shallow depth of field"
        ),
    },
    {
        "filename": "about-2.jpg",
        "aspect_ratio": "4:3",
        "prompt": (
            "Cinematic product photograph of a luxury perfume bottle on dark velvet, "
            "single dramatic studio light, deep shadows, soft pink rim light, "
            "premium beauty editorial style, desaturated except for a warm pink glow, "
            "ultra high resolution, photorealistic"
        ),
    },
    {
        "filename": "prod2_4c233e08-bf96-4885-a3fb-22272fd1aaf6.png",
        "aspect_ratio": "3:4",
        "prompt": (
            "Luxury fragrance promotion card visual, elegant Chanel-style perfume bottle, "
            "dark near-black background, radial pink glow from bottom-left, "
            "fine mist particles, editorial fashion photography, "
            "photorealistic, deep blacks, signature pink accent #f597b1"
        ),
    },
    {
        "filename": "prod3_c54ae2c8-96e5-4020-a0ae-0a4fceb3391e.png",
        "aspect_ratio": "3:4",
        "prompt": (
            "Masculine luxury fragrance promotion card, sleek angular Hugo Boss-style "
            "dark glass perfume bottle, dark charcoal background, blue-grey to pink gradient "
            "accent light, dramatic single-source lighting, product photography, photorealistic"
        ),
    },
    {
        "filename": "image_29258.jpg",
        "aspect_ratio": "16:9",
        "prompt": (
            "Luxury beauty brand editorial wide shot, curated flatlay of five perfume bottles "
            "on glossy black surface, overhead angle, minimal composition, "
            "soft pink backlight glow, premium lifestyle photography, "
            "high key contrast, photorealistic"
        ),
    },
    {
        "filename": "image_86248.jpg",
        "aspect_ratio": "16:9",
        "prompt": (
            "Extreme macro close-up of a luxury perfume bottle atomizer, "
            "chrome and frosted glass details, shallow depth of field, "
            "warm bokeh background with pink and gold tones, "
            "editorial beauty photography, photorealistic, ultra-sharp foreground"
        ),
    },
]

# ── Gemini client ─────────────────────────────────────────────────────────────

def build_client() -> genai.Client:
    # Always use ADC via Vertex AI — no API key needed
    return genai.Client(vertexai=True, project=GCP_PROJECT, location=GCP_LOCATION)


def generate_image(client: genai.Client, spec: dict) -> tuple[bytes, str]:
    """Return (image_bytes, mime_type) for the given image spec."""
    print(f"  Generating via {MODEL}…")

    contents = [
        types.Content(
            role="user",
            parts=[types.Part.from_text(text=spec["prompt"])],
        )
    ]

    config = types.GenerateContentConfig(
        image_config=types.ImageConfig(
            aspect_ratio=spec["aspect_ratio"],
            image_size="2K",
        ),
        response_modalities=["IMAGE", "TEXT"],
    )

    image_bytes: bytes | None = None
    mime_type = "image/png"

    for chunk in client.models.generate_content_stream(
        model=MODEL,
        contents=contents,
        config=config,
    ):
        if not chunk.parts:
            continue
        part = chunk.parts[0]
        if part.inline_data and part.inline_data.data:
            image_bytes = part.inline_data.data
            mime_type   = part.inline_data.mime_type or mime_type
        elif chunk.text:
            print(f"    model note: {chunk.text[:120]}")

    if not image_bytes:
        raise RuntimeError(f"No image data returned for {spec['filename']}")

    return image_bytes, mime_type


# ── Shopify upload flow ───────────────────────────────────────────────────────

def _gql(token: str, query: str, variables: dict | None = None) -> dict:
    graphql_url = f"https://{SHOPIFY_STORE}/admin/api/2026-04/graphql.json"
    resp = requests.post(
        graphql_url,
        headers={
            "Content-Type": "application/json",
            "X-Shopify-Access-Token": token,
        },
        json={"query": query, "variables": variables or {}},
        timeout=30,
    )
    resp.raise_for_status()
    body = resp.json()
    if "errors" in body:
        raise RuntimeError(f"GraphQL errors: {body['errors']}")
    return body.get("data") or {}


def staged_upload_create(token: str, filename: str, mime_type: str) -> dict:
    data = _gql(
        token,
        """
        mutation stagedUploadsCreate($input: [StagedUploadInput!]!) {
          stagedUploadsCreate(input: $input) {
            stagedTargets {
              url
              resourceUrl
              parameters { name value }
            }
            userErrors { field message }
          }
        }
        """,
        {
            "input": [{
                "filename":   filename,
                "mimeType":   mime_type,
                "httpMethod": "POST",
                "resource":   "FILE",
            }]
        },
    )
    errors  = data["stagedUploadsCreate"]["userErrors"]
    targets = data["stagedUploadsCreate"]["stagedTargets"]
    if errors:
        raise RuntimeError(f"stagedUploadsCreate errors: {errors}")
    if not targets:
        raise RuntimeError("stagedUploadsCreate returned no targets")
    return targets[0]


def upload_to_staged_url(target: dict, image_bytes: bytes, filename: str, mime_type: str) -> str:
    params = {p["name"]: p["value"] for p in target["parameters"]}
    for attempt in range(3):
        try:
            resp = requests.post(
                target["url"],
                data=params,
                files={"file": (filename, image_bytes, mime_type)},
                timeout=180,
            )
            resp.raise_for_status()
            return target["resourceUrl"]
        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout) as exc:
            if attempt == 2:
                raise
            print(f"    upload attempt {attempt + 1} failed ({exc.__class__.__name__}), retrying…")
            time.sleep(5)


def file_create(token: str, resource_url: str, filename: str) -> str:
    """Create file in Shopify Files and return its GID."""
    data = _gql(
        token,
        """
        mutation fileCreate($files: [FileCreateInput!]!) {
          fileCreate(files: $files) {
            files { ... on MediaImage { id } ... on GenericFile { id } }
            userErrors { field message }
          }
        }
        """,
        {
            "files": [{
                "originalSource": resource_url,
                "filename":       filename,
                "contentType":    "IMAGE",
            }]
        },
    )
    errors = data["fileCreate"]["userErrors"]
    if errors:
        raise RuntimeError(f"fileCreate errors: {errors}")
    files = data["fileCreate"]["files"]
    if not files:
        raise RuntimeError("fileCreate returned no files")
    return files[0]["id"]


def poll_cdn_url_by_id(token: str, file_id: str, retries: int = 15, delay: float = 4.0) -> str:
    """Poll by file GID so we always get the freshly uploaded file, not an older same-named one."""
    query = """
    query getFileById($id: ID!) {
      node(id: $id) {
        ... on MediaImage { image { url } }
        ... on GenericFile { url }
      }
    }
    """
    for attempt in range(retries):
        data  = _gql(token, query, {"id": file_id})
        node  = data.get("node") or {}
        image = node.get("image") or {}
        url   = image.get("url") or node.get("url")
        if url:
            return url
        print(f"    waiting for CDN… ({attempt + 1}/{retries})")
        time.sleep(delay)
    raise RuntimeError(f"CDN URL for {file_id} not available after {retries} attempts")


def upload_image(token: str, image_bytes: bytes, filename: str, mime_type: str) -> str:
    print(f"  Uploading to Shopify…")
    target       = staged_upload_create(token, filename, mime_type)
    resource_url = upload_to_staged_url(target, image_bytes, filename, mime_type)
    file_id      = file_create(token, resource_url, filename)
    cdn_url      = poll_cdn_url_by_id(token, file_id)
    return cdn_url


# ── Main ──────────────────────────────────────────────────────────────────────

def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    cdn_urls: dict = json.loads(CDN_FILE.read_text()) if CDN_FILE.exists() else {}

    # Fetch Shopify token once at startup
    token = get_shopify_token()

    client = build_client()
    print(f"Gemini client ready ({MODEL})\n")

    for spec in IMAGES:
        filename = spec["filename"]

        if filename in cdn_urls:
            print(f"[skip] {filename} — already in cdn_urls")
            continue

        print(f"\n[{filename}]")

        # Generate
        image_bytes, mime_type = generate_image(client, spec)

        # Save locally for inspection
        ext       = mimetypes.guess_extension(mime_type) or ".png"
        local_out = OUTPUT_DIR / (Path(filename).stem + ext)
        local_out.write_bytes(image_bytes)
        print(f"  Saved locally → {local_out.relative_to(Path.cwd())}")

        # Upload
        cdn_url = upload_image(token, image_bytes, filename, mime_type)
        cdn_urls[filename] = cdn_url
        print(f"  ✓ {cdn_url}")

        # Write incrementally so a crash doesn't lose previous work
        CDN_FILE.write_text(json.dumps(cdn_urls, indent=2) + "\n")

    print(f"\nAll done. {CDN_FILE} updated with {len(cdn_urls)} entries.")


if __name__ == "__main__":
    main()
