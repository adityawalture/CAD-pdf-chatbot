# cad_pdf_chatbot.py

import fitz  # PyMuPDF
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
import re
import requests
from PIL import Image
from pdf2image import convert_from_path
import gradio as gr
import tempfile

# --- Step 1: Extract all text from the PDF ---
def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    full_text = ""
    for page in doc:
        full_text += page.get_text()
    return full_text

# --- Step 2: Extract images (diagrams) from the PDF ---
def extract_images_from_pdf(pdf_path):
    return convert_from_path(pdf_path, dpi=300, poppler_path=r'C:\poppler-24.08.0\Library\bin')

# --- Step 3: Run OCR to get text (measurements) from diagrams ---
def extract_text_from_images(images):
    diagram_text = ""
    for img in images:
        text = pytesseract.image_to_string(img)
        diagram_text += text + "\n"
    return diagram_text

# --- Step 4: Extract measurements using regex ---
def extract_measurements(text):
    return re.findall(r'\d+\.?\d*\s?(mm|cm|m|in)', text)

# --- Step 5: Compare index table values to diagram values ---
def compare_measurements(index_list, diagram_text):
    extracted = extract_measurements(diagram_text)
    matched = [val for val in index_list if val in extracted]
    missing = list(set(index_list) - set(matched))
    return matched, missing

# --- Step 6: Verify formulas like '101.6P x 24 = 2438.4' ---
def verify_measurement_expressions(text):
    issues = []
    pattern = re.compile(r"(\d+\.?\d*)P\s*x\s*(\d+)\s*=\s*(\d+\.?\d*)")
    matches = pattern.findall(text)

    for base, count, expected in matches:
        base = float(base)
        count = int(count)
        expected = float(expected)
        calculated = round(base * count, 1)
        if abs(calculated - expected) > 0.1:
            issues.append(f"❌ Mismatch: {base}P x {count} = {expected} (calculated {calculated})")
        else:
            issues.append(f"✅ Verified: {base}P x {count} = {expected}")
    return "\n".join(issues)

# --- Step 7: Ask question to local LLM using Ollama ---
def ask_local_llm(question, context):
    prompt = f"{context}\n\nUser: {question}\nAssistant:"
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={"model": "llama3", "prompt": prompt, "stream": False}
        )
        response.raise_for_status()  # Raise if HTTP error
        result = response.json()
        return result.get("response", "❌ Error: No 'response' key returned from LLM.")
    except requests.exceptions.RequestException as e:
        return f"❌ Request error: {str(e)}"
    except Exception as e:
        return f"❌ Unexpected error: {str(e)}"

# --- Global variables to store context ---
index_text = ""
diagram_text = ""
verify_report = ""

# --- Step 8: Gradio Chatbot Interface ---
def upload_pdf(file):
    global index_text, diagram_text, verify_report
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(file)  # fixed from file.read() to file
        tmp_path = tmp.name

    # Step 1: Extract text
    index_text = extract_text_from_pdf(tmp_path)

    # Step 2: Extract diagrams
    images = extract_images_from_pdf(tmp_path)

    # Step 3: OCR
    diagram_text = extract_text_from_images(images)

    # Step 4: Verify formulas
    verify_report = verify_measurement_expressions(index_text)

    return "✅ PDF processed. You can now ask questions."

def chatbot_response(message, history):
    context = f"Index Table Text:\n{index_text}\n\nExtracted Measurements from Diagrams:\n{diagram_text}\n\nVerification Report:\n{verify_report}"
    return ask_local_llm(message, context)

iface = gr.Interface(
    fn=upload_pdf,
    inputs=gr.File(type="binary", label="Upload CAD PDF"),
    outputs="text",
    title="📐 CAD PDF Extractor & Verifier"
)

chat = gr.ChatInterface(fn=chatbot_response, title="🤖 CAD PDF Assistant Chatbot")

demo = gr.TabbedInterface([iface, chat], ["Upload PDF", "Chatbot"])

if __name__ == "__main__":
    demo.launch()