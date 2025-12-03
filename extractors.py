# extractors.py
import re
import json
import subprocess
from typing import Dict


def call_ollama(prompt: str, model: str = "llama3.2"):
    import subprocess

    process = subprocess.Popen(
        ["ollama", "run", model],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=False  # RAW bytes (important!)
    )

    out, err = process.communicate(prompt.encode("utf-8"))

    # Decode safely
    try:
        return out.decode("utf-8", errors="ignore")
    except:
        return out.decode("latin-1", errors="ignore")


def llm_extract(text: str, doc_type: str):
    schema = {
        "statement": ["accountNumber", "period", "avgBalance", "status", "confidence"],
        "invoice": ["invoiceNumber", "totalAmount", "status", "confidence"],
        "loan_agreement": ["loanNumber", "principal", "status", "confidence"],
        "generic": ["summary", "keyValues", "confidence"],
    }

    prompt = f"""
You are a JSON extractor. Input is OCR text from a {doc_type} document.

Return ONLY valid JSON with fields:
{schema.get(doc_type, schema["generic"])}

If something is missing, return null.

OCR TEXT:
{text}
"""

    response = call_ollama(prompt)
    try:
        json_start = response.find("{")
        json_end = response.rfind("}") + 1
        clean_json = response[json_start:json_end]
        return json.loads(clean_json)
    except:
        return {"status": "unverified", "confidence": 0.0}

def extract_fields_from_text(text: str, doc_type="statement"):
    return llm_extract(text, doc_type)
