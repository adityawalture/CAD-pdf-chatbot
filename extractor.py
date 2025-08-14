import io
from pathlib import Path
from typing import Union
import fitz  # PyMuPDF
from pdf2image import convert_from_bytes
from PIL import Image
import pytesseract

class CADPDFExtractor:
    def __init__(self, ocr_if_empty: bool = True, ocr_lang: str = "eng"):
        self.ocr_if_empty = ocr_if_empty
        self.ocr_lang = ocr_lang

    def _ocr_pages(self, pdf_bytes: bytes) -> str:
        text_chunks = []
        for page_img in convert_from_bytes(pdf_bytes, dpi=300):
            buf = io.BytesIO()
            page_img.save(buf, format="PNG")
            buf.seek(0)
            text_chunks.append(
                pytesseract.image_to_string(Image.open(buf), lang=self.ocr_lang)
            )
        return "\n".join(text_chunks)

    def extract_text(self, source: Union[str, Path, bytes, io.BytesIO]) -> str:
        if isinstance(source, (str, Path)):
            pdf_bytes = Path(source).read_bytes()
        elif isinstance(source, io.BytesIO):
            pdf_bytes = source.getvalue()
        elif isinstance(source, (bytes, bytearray)):
            pdf_bytes = bytes(source)
        else:
            raise TypeError("Unsupported source type for PDF extractor.")

        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
        text_buffer = [page.get_text() for page in doc]
        combined = "\n".join(text_buffer).strip()

        if not combined and self.ocr_if_empty:
            combined = self._ocr_pages(pdf_bytes)
        return combined