#!/usr/bin/env python3
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

SHOPIFY_STORE     = os.environ["SHOPIFY_STORE"]
SHOPIFY_CLIENT_ID = os.environ["SHOPIFY_CLIENT_ID"]
SHOPIFY_CLIENT_SECRET = os.environ["SHOPIFY_CLIENT_SECRET"]
GCP_PROJECT  = os.environ.get("GCP_PROJECT_ID")
GCP_LOCATION = os.environ.get("GCP_LOCATION", "global")
CDN_FILE   = Path(__file__).parent / "shopify_cdn_urls.json"
OUTPUT_DIR = Path(__file__).parent / "_generated"

MODEL = "gemini-3-pro-image-preview"

def get_shopify_token() -> str:
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
    return resp.json()["access_token"]

IMAGES = [
    {
        "filename": "cat_parfum.png",
        "aspect_ratio": "1:1",
        "prompt": "Luxury perfume bottle on dark marble surface, single dramatic studio light, warm golden-hour light, editorial beauty photography, photorealistic, signature pink #f496b0 accents",
    },
    {
        "filename": "cat_gesicht.png",
        "aspect_ratio": "1:1",
        "prompt": "Luxury face cream jar on dark velvet, soft pink rim light, water ripples, minimalist editorial beauty, photorealistic",
    },
    {
        "filename": "cat_haare.png",
        "aspect_ratio": "1:1",
        "prompt": "Luxury hair care bottle with smooth flowing liquid texture, elegant lighting, dark background, signature pink hue #f496b0, photorealistic",
    },
    {
        "filename": "cat_koerper.png",
        "aspect_ratio": "1:1",
        "prompt": "Elegant body lotion bottle, luxury spa aesthetic, dark moody lighting, gentle mist, photorealistic",
    },
    {
        "filename": "cat_makeup.png",
        "aspect_ratio": "1:1",
        "prompt": "Luxury makeup compact and lipstick, elegant composition, dark dramatic lighting, pink powder texture floating, photorealistic",
    },
    {
        "filename": "cat_gesundheit.png",
        "aspect_ratio": "1:1",
        "prompt": "Premium wellness supplements in elegant dark amber glass jar, sophisticated lighting, warm pink glow, photorealistic",
    },
    {
        "filename": "cat_baby.png",
        "aspect_ratio": "1:1",
        "prompt": "Luxury gentle baby care bottle, soft gentle lighting, dark background but warm, minimal, photorealistic",
    },
    {
        "filename": "cat_tools.png",
        "aspect_ratio": "1:1",
        "prompt": "Premium makeup brushes and beauty blender, sleek dark handles, dramatic lighting, signature pink accent, photorealistic",
    }
]

def build_client() -> genai.Client:
    return genai.Client(vertexai=True, project=GCP_PROJECT, location=GCP_LOCATION)

def generate_image(client: genai.Client, spec: dict) -> tuple[bytes, str]:
    contents = [types.Content(role="user", parts=[types.Part.from_text(text=spec["prompt"])])]
    config = types.GenerateContentConfig(
        image_config=types.ImageConfig(aspect_ratio=spec["aspect_ratio"], image_size="2K"),
        response_modalities=["IMAGE", "TEXT"],
    )
    image_bytes = None
    mime_type = "image/png"
    for chunk in client.models.generate_content_stream(model=MODEL, contents=contents, config=config):
        if not chunk.parts: continue
        part = chunk.parts[0]
        if part.inline_data and part.inline_data.data:
            image_bytes = part.inline_data.data
            mime_type = part.inline_data.mime_type or mime_type
    if not image_bytes: raise RuntimeError(f"No image data returned for {spec['filename']}")
    return image_bytes, mime_type

def _gql(token: str, query: str, variables: dict | None = None) -> dict:
    resp = requests.post(
        f"https://{SHOPIFY_STORE}/admin/api/2024-04/graphql.json",
        headers={"Content-Type": "application/json", "X-Shopify-Access-Token": token},
        json={"query": query, "variables": variables or {}},
        timeout=30,
    )
    resp.raise_for_status()
    body = resp.json()
    if "errors" in body: raise RuntimeError(f"GraphQL errors: {body['errors']}")
    return body.get("data") or {}

def staged_upload_create(token: str, filename: str, mime_type: str) -> dict:
    data = _gql(
        token,
        """mutation stagedUploadsCreate($input: [StagedUploadInput!]!) { stagedUploadsCreate(input: $input) { stagedTargets { url resourceUrl parameters { name value } } userErrors { field message } } }""",
        {"input": [{"filename": filename, "mimeType": mime_type, "httpMethod": "POST", "resource": "FILE"}]}
    )
    return data["stagedUploadsCreate"]["stagedTargets"][0]

def upload_to_staged_url(target: dict, image_bytes: bytes, filename: str, mime_type: str) -> str:
    params = {p["name"]: p["value"] for p in target["parameters"]}
    resp = requests.post(target["url"], data=params, files={"file": (filename, image_bytes, mime_type)}, timeout=180)
    resp.raise_for_status()
    return target["resourceUrl"]

def file_create(token: str, resource_url: str, filename: str) -> str:
    data = _gql(
        token,
        """mutation fileCreate($files: [FileCreateInput!]!) { fileCreate(files: $files) { files { ... on MediaImage { id } ... on GenericFile { id } } } }""",
        {"files": [{"originalSource": resource_url, "filename": filename, "contentType": "IMAGE"}]}
    )
    return data["fileCreate"]["files"][0]["id"]

def poll_cdn_url_by_id(token: str, file_id: str) -> str:
    query = """query getFileById($id: ID!) { node(id: $id) { ... on MediaImage { image { url } } ... on GenericFile { url } } }"""
    for _ in range(15):
        data = _gql(token, query, {"id": file_id})
        node = data.get("node") or {}
        image = node.get("image") or {}
        url = image.get("url") or node.get("url")
        if url: return url
        time.sleep(4.0)
    raise RuntimeError(f"CDN URL for {file_id} not available")

def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    cdn_urls = json.loads(CDN_FILE.read_text()) if CDN_FILE.exists() else {}
    token = get_shopify_token()
    client = build_client()
    for spec in IMAGES:
        filename = spec["filename"]
        if filename in cdn_urls:
            print(f"Skipping {filename}")
            continue
        print(f"Generating {filename}...")
        image_bytes, mime_type = generate_image(client, spec)
        ext = mimetypes.guess_extension(mime_type) or ".png"
        (OUTPUT_DIR / (Path(filename).stem + ext)).write_bytes(image_bytes)
        target = staged_upload_create(token, filename, mime_type)
        resource_url = upload_to_staged_url(target, image_bytes, filename, mime_type)
        file_id = file_create(token, resource_url, filename)
        cdn_url = poll_cdn_url_by_id(token, file_id)
        cdn_urls[filename] = cdn_url
        CDN_FILE.write_text(json.dumps(cdn_urls, indent=2) + "\n")
        print(f"Uploaded {filename}: {cdn_url}")

if __name__ == "__main__":
    main()
