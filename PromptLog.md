# 🧠 PromptLog — Smart Document Reader (Open-Source AI Version)

This document records the reasoning, AI prompts, and iteration process used to build the final solution.  
HaiIntel requires this to understand **how I use AI creatively**, think independently, and upgrade outputs beyond the initial idea.

---

# 📌 1. Objective

Build an open-source document intelligence microservice to:

- Accept PDF/JPG documents  
- Perform OCR  
- Use a local LLM to extract structured fields  
- Save data into SQLite  
- Build vector embeddings for semantic search  
- Allow synthetic PDF generation  

Creativity and enhancement were key requirements.

---

# 📌 2. Starting Point — Basic Understanding

**Initial prompt:**  
“How do I create a Smart Document Reader using FastAPI, OCR, and LLM?”

The AI provided:

- Basic FastAPI upload endpoint  
- OCR logic  
- LLM-based field extraction  
- SQLite storage  

I realized I needed **a cleaner architecture**, a way to support PDF + images, and an end-to-end offline stack.

---

# 📌 3. Enhancing OCR Pipeline

**Prompt:**  
“Use PyMuPDF to extract images from a PDF. Avoid pixmap bugs.”

Improvements added:

- `extract_images_from_pdf()` rendering each page as PNG bytes  
- `ocr_image_bytes()` using EasyOCR  
- Support for JPG, JPEG, PNG alongside PDFs  
- Eliminated dependency on Poppler/Tesseract  

This made OCR fast and lightweight.

---

# 📌 4. Adding Full LLM Extraction

**Prompt:**  
“How do I extract structured fields using a local LLM (Ollama)?”

AI generated:

- A prompt template  
- `call_ollama()` using subprocess  
- Schema-based extraction for:
  - statements  
  - invoices  
  - loan agreements  
  - generic docs  

I enhanced it to include:

- UTF-8 / Latin-1 safe decoding  
- JSON cleanup (extract only between `{...}`)  
- Fallback result when JSON is malformed  

---

# 📌 5. Building Semantic Search (FAISS)

**Prompt:**  
“Add vector search using FAISS + sentence transformers.”

AI gave a starting point.  
I extended it to:

- Persistent FAISS index (`faiss.index`)  
- Metadata store (`meta.pkl`)  
- Preview text for better search results  
- Automatic reload on startup  
- Query embedding + semantic ranking  

This enabled `/api/search` endpoint.

---

# 📌 6. Synthetic PDF Generator

**Prompt:**  
“Generate synthetic PDFs using Ollama + ReportLab.”

AI generated a simple version.  
I enhanced it to:

- Fully dynamic prompt  
- Clean plain-text generation  
- Vector-accurate synthetic documents  
- PDF conversion using ReportLab canvas  
- Unique filenames using UUID  

This enables `/api/generate` endpoint.

---

# 📌 7. API Integration & Orchestration

**Prompt:**  
“Combine OCR, LLM, FAISS, and SQLite into FastAPI.”

Enhancements added:

- `/api/verify` orchestrates OCR → LLM → Storage → Embedding  
- `/api/search` performs semantic search  
- `/api/generate` creates synthetic PDFs  
- Async FastAPI for high concurrency  
- Robust DB initialization  
- Clean JSON responses  

---

# 📌 8. Debugging & Fixes

### Issue → Fix summary:
- **Missing libraries**  
  → Installed `easyocr`, `pymupdf`, `faiss-cpu`, `sentence-transformers`.

- **Pixmap error (`tobytes` vs `tobytes()`)**  
  → Adjusted to correct method.

- **UnicodeDecodeError**  
  → Added UTF-8 with fallback Latin-1 decoding.

- **SQLite missing column**  
  → Rebuilt schema to include `extracted_json`.

- **JSON extraction failures**  
  → Added logic to find first `{` and last `}`.

- **LLM hallucination**  
  → Tightened prompt + used “extract JSON only”.

---

# 📌 9. Creativity Highlights (as required by HaiIntel)

AI helped with basic scaffolding.  
I added the following creative enhancements:

- 100% offline architecture  
- Synthetic document generator  
- FAISS-based semantic search engine  
- Metadata preview for search  
- Modular architecture with reusable components  
- Support for both PDF + JPG  
- Error-tolerant JSON extraction  
- UTF-8/Latin-1 fallback  
- Async FastAPI server  
- Document schema-based extraction  
- Automatic UUID for every document  

These extensions go beyond the minimum assignment.

---

# 📌 10. Final Testing

**Tested using:**

- PDFs (statements, invoices, loan agreements)  
- JPG images  
- Synthetic documents  
- Search queries like `payment`, `loan`, `income`, `charges`  
- Swagger UI at `/docs`

Everything worked successfully, including generation, extraction, storage, and semantic retrieval.

---

# 📌 11. Conclusion

This PromptLog demonstrates:

- Strong use of AI tools  
- Independent reasoning  
- Incremental improvements  
- Production-level system thinking  
- Creativity beyond the assignment  

The final solution is a robust, fully offline, extensible document-intelligence microservice suitable for enterprise use.

