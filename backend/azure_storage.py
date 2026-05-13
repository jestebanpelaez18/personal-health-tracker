from azure.storage.blob import BlobServiceClient
from datetime import datetime
from pathlib import Path
import json
import os
from typing import Any
from dotenv import load_dotenv

# Prefer backend/.env for backend runtime, with project-root fallback.
backend_env = Path(__file__).with_name(".env")
root_env = Path(__file__).parent.parent / ".env"
if backend_env.exists():
    load_dotenv(dotenv_path=backend_env)
elif root_env.exists():
    load_dotenv(dotenv_path=root_env)

CONNECTION_STRING = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
CONTAINER_NAME = os.getenv("AZURE_CONTAINER_NAME", "health-data")


def upload_records_to_blob(records: list[dict[str, Any]], user_id: str) -> str:
    """Upload health records to Azure Blob Storage and return the created blob name."""

    if not CONNECTION_STRING:
        raise ValueError("AZURE_STORAGE_CONNECTION_STRING is not configured.")

    if "AccountName=" not in CONNECTION_STRING or "AccountKey=" not in CONNECTION_STRING:
        raise ValueError(
            "AZURE_STORAGE_CONNECTION_STRING is invalid. "
            "Expected full Azure connection string format."
        )

    blob_service = BlobServiceClient.from_connection_string(CONNECTION_STRING)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    blob_name = f"{user_id}/apple_health_{timestamp}.json"

    blob_client = blob_service.get_blob_client(
        container=CONTAINER_NAME,
        blob=blob_name
    )

    payload = json.dumps(records)
    blob_client.upload_blob(payload, overwrite=True)

    print(f"Uploaded {len(records)} records to {blob_name}")
    return blob_name