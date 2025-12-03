Dev notes / extensions:

- Vector Search:
  - Save embeddings of `raw_text` or extracted fields using a small local embedding model (or OpenAI embeddings).
  - Use FAISS to add vector search and find similar statements or previously-verified documents.

- Multi-doc types:
  - Add small config of per-doc-type rules (loan_agreement, invoice, statement).
  - For invoices parse vendor, invoice number, total_due.

- Confidence:
  - Combine OCR engine confidence (if available), presence of keyword anchors, and LLM self-reported confidence.

- Testing:
  - Unit test extractors with multiple synthetic variants.
  - Run OCR with altered image resolution / noise to test robustness.

- Security:
  - Rate-limit file uploads.
  - Sanitize exposed text before sending to external LLMs.
