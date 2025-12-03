# 🚀 Smart Document Reader — Open Source AI Version  
A fully offline, end-to-end **Intelligent Document Processing (IDP)** microservice built using:

- **FastAPI** (ASGI)
- **EasyOCR**
- **PyMuPDF**
- **Ollama (Local LLM)**
- **FAISS Vector Search**
- **Sentence Transformers (Embeddings)**
- **ReportLab**

This system reads real-world documents (PDF/JPG), extracts text using OCR, parses structured fields via local LLMs, stores results in SQLite, and supports semantic search using vector embeddings.

---

# 🌟 Key Features

### ✔ 1. End-to-end Offline Document Intelligence  
Zero cloud, zero API keys → privacy-safe.  
Uses **Ollama**, **EasyOCR**, **SQLite**, **FAISS**, **PyMuPDF**.

### ✔ 2. Supports Multiple Document Types  
- Bank statements  
- Invoices  
- Loan agreements  
- Generic documents  
- JPG, PNG, JPEG, PDF

### ✔ 3. LLM-based Structured Extraction  
Uses local LLM (llama3.2) to extract fields like:

```json
{
  "accountNumber": "...",
  "period": "...",
  "avgBalance": 52300.45,
  "status": "verified",
  "confidence": 0.90
}
```

### ✔ 4. Semantic Search with FAISS  
Search documents by **meaning** (not keywords):

```
payment
late fees
loan principal
invoice total
```

### ✔ 5. Synthetic Document Generator  
Creates realistic synthetic PDFs using:
- Ollama → generate fake document text
- ReportLab → convert text → PDF

No real data required for testing.

---

# 🧱 Architecture Overview

```
          +----------------------------+
          |        /api/generate       |
          |     (Synthetic PDF)        |
          +-------------+--------------+
                        |
                        v
+-----------+    +------------+    +---------------------+
|  Upload   |    |   OCR      |    |   LLM Extraction    |
| PDF/JPG   | -> | EasyOCR    | -> | Local Ollama LLM    |
+-----------+    +------------+    +---------------------+
                        |
                        v
              +-------------------+
              |  SQLite Storage   |
              +-------------------+
                        |
                        v
              +-------------------+
              |  Embeddings Store |
              | FAISS + metadata  |
              +-------------------+
                        |
                        v
              +-------------------+
              |   /api/search     |
              +-------------------+
```

---

# 📂 Project Structure

```
smart-doc-reader/
│── main.py                    # FastAPI app: OCR → LLM → DB → FAISS
│── ocr_utils.py               # EasyOCR + PyMuPDF processing
│── extractors.py              # Local LLM JSON extraction
│── embeddings_store.py        # FAISS vector search engine
│── gen_synthetic_pdf.py       # Synthetic PDF generator
│── records.db                 # SQLite storage
│── embeddings/                # FAISS + metadata index
│── sample_data/               # Synthetic documents
```

---

# ⚙️ Installation

### 1. Clone the repo
```bash
git clone <repo-url>
cd smart-doc-reader
```

### 2. Install Python dependencies
```bash
pip install fastapi uvicorn python-multipart easyocr pymupdf faiss-cpu sentence-transformers reportlab numpy
```

### 3. Install Ollama (Required)
Download from: https://ollama.com/download

Pull the model:
```bash
ollama pull llama3.2
```

---

# ▶️ Running the Server

```bash
uvicorn main:app --reload --port 8000
```

Open docs UI:
```
http://localhost:8000/docs
```

---

# 🧪 API Usage

---

## 📌 1. Upload & Process a Document  
**POST /api/verify**

Uploads a PDF/JPG → OCR → LLM → Storage → Embeddings

### Sample curl
```bash
curl -X POST "http://localhost:8000/api/verify?doc_type=statement" \
     -F "file=@myfile.pdf"
```

### Sample Response
```json
{
  "id": "93b0b3fa-fc8d...",
  "filename": "statement.pdf",
  "doc_type": "statement",
  "full_text": "Account Number...",
  "extracted_fields": {
    "accountNumber": "12345",
    "period": "Jan-Mar 2024",
    "avgBalance": 52000.5,
    "status": "verified",
    "confidence": 0.91
  }
}
```

---

## 📌 2. Generate Synthetic PDF  
**GET /api/generate?kind=invoice**

Creates a realistic fake invoice using LLM + ReportLab.

Response:
```json
{
  "generated_pdf": "sample_data/synth_invoice_a92d3c.pdf"
}
```

---

## 📌 3. Semantic Search  
**GET /api/search?q=payment**

Searches documents using vector similarity.

Example output:
```json
[
  {
    "distance": 1.03,
    "meta": {
      "doc_id": "93b0b3fa...",
      "filename": "synth_loan_agreement.pdf",
      "preview": "LOAN AGREEMENT ..."
    }
  }
]
```

---

# 💡 Key Creative Extensions

This project goes **far beyond** the assignment requirements:

### ⭐ Full offline LLM extraction using Ollama  
### ⭐ Semantic vector search (FAISS + MPNet embeddings)  
### ⭐ Synthetic PDF generator  
### ⭐ Automatic PDF-to-image rendering (PyMuPDF)  
### ⭐ Robust JSON extractor with error fallback  
### ⭐ Metadata-based document indexing  
### ⭐ Async/non-blocking FastAPI architecture  
### ⭐ Support for BOTH PDFs and Images (JPG/PNG)  

These additions showcase:
- AI engineering skills  
- System design capability  
- Creativity and problem-solving  

---

# 🏁 Final Notes

This microservice is:

- fully open-source  
- privacy-safe  
- extendable  
- ready for real-world integration  

You can easily add:
- new document types  
- analytics  
- dashboards  
- RAG/Q&A  
- audit logging  
- hybrid search  

---

# 👤 Author  
*Marimuthu*  
AI / Automation Engineer  
Smart Document Processing + LLM Systems

