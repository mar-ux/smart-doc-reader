# gen_synthetic_pdf.py
import os
import uuid
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from extractors import call_ollama

def generate_pdf(text: str, out_path: str):
    c = canvas.Canvas(out_path, pagesize=letter)
    for i, line in enumerate(text.splitlines()):
        c.drawString(40, 750 - i*15, line[:120])
    c.save()

def generate_synthetic(kind="statement"):
    prompt = f"""
Generate a synthetic {kind} document as plain text.
Use realistic formatting and amounts.
Do NOT include any JSON. Output clean text only.
"""
    out = call_ollama(prompt)
    filename = f"sample_data/synth_{kind}_{uuid.uuid4().hex[:6]}.pdf"
    os.makedirs("sample_data", exist_ok=True)
    generate_pdf(out, filename)
    return filename
