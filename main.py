# main.py (FULL OPEN-SOURCE VERSION)

import io
import uuid
import sqlite3
from fastapi import FastAPI, UploadFile, File, Query
from fastapi.responses import JSONResponse
#custom
from ocr_utils import extract_images_from_pdf, ocr_image_bytes
from extractors import extract_fields_from_text
from embeddings_store import EmbeddingsStore
from gen_synthetic_pdf import generate_synthetic

DB_PATH = "records.db"

app = FastAPI(title="Smart Document Reader - Open Source Version")

# ---------------------------------------------------------
#  DB INITIALIZATION
# ---------------------------------------------------------
def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
    CREATE TABLE IF NOT EXISTS documents (
        id TEXT PRIMARY KEY,
        filename TEXT,
        doc_type TEXT,
        raw_text TEXT,
        extracted_json TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    conn.commit()
    conn.close()

init_db()

# ---------------------------------------------------------
#  VECTOR EMBEDDING STORE (FAISS + MiniLM)
# ---------------------------------------------------------
emb_store = EmbeddingsStore()

def save_record(doc_id, filename, doc_type, raw_text, extracted):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        INSERT INTO documents (id, filename, doc_type, raw_text, extracted_json)
        VALUES (?, ?, ?, ?, ?)
    """, (
        doc_id, filename, doc_type, raw_text[:15000], str(extracted)
    ))
    conn.commit()
    conn.close()

# ---------------------------------------------------------
#  API: VERIFY DOCUMENT
# ---------------------------------------------------------
@app.post("/api/verify")
async def verify_document(
    file: UploadFile = File(...),
    doc_type: str = Query("statement", description="statement | invoice | loan_agreement | generic")
):
    content = await file.read()
    filename = file.filename.lower()

    # -----------------------------
    # PDF → IMAGES → OCR TEXT
    # -----------------------------
    if filename.endswith(".pdf"):
        images = extract_images_from_pdf(content)
    else:
        images = [content]

    ocr_text = ""
    for img_bytes in images:
        ocr_text += ocr_image_bytes(img_bytes) + "\n"

    # -----------------------------
    # LLM EXTRACTION (Ollama)
    # -----------------------------
    extracted = extract_fields_from_text(ocr_text, doc_type)

    # -----------------------------
    # Store to DB
    # -----------------------------
    doc_id = str(uuid.uuid4())
    save_record(doc_id, filename, doc_type, ocr_text, extracted)

    # -----------------------------
    # Add to vector index
    # -----------------------------
    emb_store.add(doc_id, ocr_text, filename)

    return JSONResponse({
        "id": doc_id,
        "filename": filename,
        "doc_type": doc_type,
        "full_text": ocr_text,  # FULL DOCUMENT TEXT
        "extracted_fields": extracted
    })

    #return JSONResponse({
    #"id": doc_id,
    #"filename": filename,
    #"doc_type": doc_type,
    #"extracted": extracted
    #})
# ---------------------------------------------------------
#  API: GENERATE SYNTHETIC DOCUMENT (via Ollama)
# ---------------------------------------------------------
@app.get("/api/generate")
def generate(kind: str = "statement"):
    generated_path = generate_synthetic(kind)
    return {"generated_pdf": generated_path}

# ---------------------------------------------------------
#  API: SEMANTIC SEARCH
# ---------------------------------------------------------
@app.get("/api/search")
def search_documents(q: str, k: int = 5):
    return emb_store.search(q, k)

# ---------------------------------------------------------
#  ROOT ENDPOINT
# ---------------------------------------------------------
@app.get("/")
def root():
    return {
        "message": "Smart Document Reader (Open Source Version)",
        "endpoints": [
            "/api/verify",
            "/api/generate",
            "/api/search",
            "/docs"
        ]
    }
