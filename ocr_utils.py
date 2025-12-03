# ocr_utils.py
import fitz  #(PyPDF2)
import easyocr

reader = easyocr.Reader(['en'], gpu=False)

def extract_images_from_pdf(pdf_bytes: bytes):
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    images = []
    for page in doc:
        pix = page.get_pixmap(dpi=200)
        images.append(pix.tobytes("png"))
    return images

def ocr_image_bytes(image_bytes: bytes) -> str:
    result = reader.readtext(image_bytes, detail=0)
    return "\n".join(result)
