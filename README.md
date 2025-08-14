# 📐 CAD PDF Analyzer & Chatbot

This project provides two interfaces for working with CAD drawing PDFs:

1. **Web App (Flask)** – Upload a CAD PDF to extract text and automatically generate a concise engineering summary using a local LLM.
2. **Interactive Chatbot (Gradio)** – Upload a CAD PDF, verify measurements, and interact with an AI assistant that answers questions based on extracted data and diagrams.

---

## 🚀 Features

- **PDF Text Extraction** – Uses `PyMuPDF` for native text extraction from CAD PDFs.
- **OCR Support** – Falls back to `pytesseract` for scanned or image-based PDFs.
- **Image Extraction** – Extracts embedded diagrams from PDF files.
- **Measurement Parsing & Verification** – Detects dimensions in mm/cm/m/in and verifies formula-based expressions.
- **Local LLM Integration** – Works with Ollama-hosted models (e.g., `llama3`, `phi`) for summaries and Q&A.
- **Gradio App** – Upload + chatbot interaction.  
    
  

---

## 📂 Project Structure
```
cad_llm_model
├── cad_pdf_chatbot.py               # Gradio chatbot for Q&A & measurement checks        
├── extractor.py                     # CAD PDF extractor with OCR fallback
├── llm_wrapper.py                   # LLM summary generation logic
└── requirements.txt                 # Python dependencies                      
```
---

## 🛠 Installation

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/adityawalture/CAD-pdf-chatbot.git
cd cad_llm_model
```

### 2️⃣ Create a virtual environment
```bash
python -m venv venv
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate      # Windows
```
### 3️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

---

## ⚙️ Setup Requirements

- **Python 3.9+**
- **Poppler** for PDF-to-image conversion  
  - Windows: [Download Poppler](https://github.com/oschwartz10612/poppler-windows/releases/)  
  - macOS: `brew install poppler`
- **Tesseract OCR** for extracting text from diagrams  
  - Windows: [Download Tesseract](https://github.com/UB-Mannheim/tesseract/wiki)  
  - macOS: `brew install tesseract`
- **Ollama** running locally for LLM inference  
  - Install from: [https://ollama.ai](https://ollama.ai)  
  - Example models:  
    ```bash
    ollama pull llama3
    ollama pull phi
    ```

---

## ▶️ Usage

### Gradio Chatbot (PDF Q&A & Measurement Verification)**
```bash
python cad_pdf_chatbot.py
```
- **Tab 1**: Upload CAD PDF → Extract text & diagrams → Verify measurements  
- **Tab 2**: Chat with AI assistant using the extracted context

<!-- ---

## 🎥 Demo Video


<video width="720" controls>
  <source src="screen_recording/cad_bot_demo.mp4" type="video/mp4">
  Your browser does not support the video tag.
</video> -->

---

## 🔍 Key Functionalities

- **Measurement Verification**  
  - Detects values like `1200 mm`, `45 cm`, `2 m`
  - Checks expressions like `101.6P x 24 = 2438.4`
- **Question Answering**  
  - Ask design-related queries (dimensions, purpose, materials, etc.)
- **OCR Fallback**  
  - Automatically processes image-based CAD PDFs

---

## ⚠️ Notes

- Ensure **Poppler** and **Tesseract** are installed and paths are correctly set in `cad_pdf_chatbot.py`.
- Ollama server must be running before starting apps:
```bash
ollama serve
```
- Large PDFs may take longer to process due to OCR.

---
