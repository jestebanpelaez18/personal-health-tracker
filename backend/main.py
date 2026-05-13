from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import io
import zipfile
import xml.etree.ElementTree as ET

try:
    from backend.azure_storage import upload_records_to_blob
except ModuleNotFoundError:
    from azure_storage import upload_records_to_blob

APPLE_HEALTH_EXPORT_PATH = "apple_health_export/export.xml"


class HealthRecord(BaseModel):
    type: str
    value: str | None
    unit: str | None
    start_date: str | None
    end_date: str | None
    source: str | None


class AppleHealthUploadResponse(BaseModel):
    status: str
    total_records: int
    blob_name: str
    sample: list[HealthRecord]


def _normalize_record_type(record_type: str) -> str:
    return (
        record_type
        .replace("HKQuantityTypeIdentifier", "")
        .replace("HKCategoryTypeIdentifier", "")
    )


def _parse_apple_health_records(xml_file) -> list[HealthRecord]:
    records = []
    for _, elem in ET.iterparse(xml_file, events=("start",)):
        if elem.tag == "Record":
            records.append(
                HealthRecord(
                    type=_normalize_record_type(elem.get("type", "")),
                    value=elem.get("value"),
                    unit=elem.get("unit"),
                    start_date=elem.get("startDate"),
                    end_date=elem.get("endDate"),
                    source=elem.get("sourceName"),
                )
            )
            elem.clear()
    return records


def _extract_records_from_zip(contents: bytes) -> list[HealthRecord]:
    try:
        with zipfile.ZipFile(io.BytesIO(contents)) as zf:
            if APPLE_HEALTH_EXPORT_PATH not in zf.namelist():
                raise HTTPException(
                    status_code=400,
                    detail="Invalid Apple Health export - export.xml not found",
                )
            with zf.open(APPLE_HEALTH_EXPORT_PATH) as xml_file:
                return _parse_apple_health_records(xml_file)
    except zipfile.BadZipFile as exc:
        raise HTTPException(status_code=400, detail="Invalid ZIP file") from exc


app = FastAPI(
    title="Personal Health Tracker",
    description="AI-powered health analytics for hybrid athletes",
    version="0.1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def health_check():
    return {"status": "ok", "message": "Personal Health Tracker API running"}


@app.post("/upload/apple-health", response_model=AppleHealthUploadResponse)
async def upload_apple_health(file: UploadFile = File(...)) -> AppleHealthUploadResponse:
    if not file.filename or not file.filename.lower().endswith(".zip"):
        raise HTTPException(status_code=400, detail="File must be a ZIP file")

    contents = await file.read()
    records = _extract_records_from_zip(contents)

    blob_name = upload_records_to_blob(
        records=[r.model_dump() for r in records],
        user_id="juan"
    )

    return AppleHealthUploadResponse(
        status="success",
        total_records=len(records),
        blob_name=blob_name,
        sample=records[:3],
    )