# AI Presentation to Notes Converter

A terminal-based AI-powered tool that converts PowerPoint, PDF, TXT, images, and general document formats into detailed, well-structured notes. The program supports OCR for extracting text from images, LaTeX rendering for mathematical formulas, and intelligent directory organization for storing generated notes.

## Description

This project takes presentation or document files and uses AI to generate clean, structured notes. It can handle text-based content, embedded images, scanned documents, and mathematical formulas. The program can automatically summarize the presentation, generate a contextual title, and decide the most relevant location within a `Notes/` directory structure — creating new subdirectories as necessary.

## Getting Started

### Dependencies

- Python 3.9+
- Works on macOS, Windows, and Linux
- Required Python libraries:
  - `openai>=1.0.0`
  - `python-pptx`
  - `python-docx`
  - `pdfplumber`
  - `pytesseract`
  - `Pillow`
  - `PyMuPDF` (`fitz`)
  - `markdown2`
  - `reportlab`
  - `latex2mathml`
  - `pypandoc`

### Installing

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/ai-presentation-notes.git
   cd ai-presentation-notes
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Set your OpenAI API key:

   ```bash
   export OPENAI_API_KEY="your_api_key_here"  # macOS/Linux
   setx OPENAI_API_KEY "your_api_key_here"    # Windows
   ```

4. Ensure Tesseract OCR is installed:
   - **macOS (Homebrew)**:
     ```bash
     brew install tesseract
     ```
   - **Windows**: [Download Tesseract](https://github.com/UB-Mannheim/tesseract/wiki)
   - **Linux**:
     ```bash
     sudo apt install tesseract-ocr
     ```

### Executing program

- Place your files into the `input_files/` directory.
- Run the program:
  ```bash
  python main.py path/to/file.pptx
  ```
- Output will be saved under the intelligently chosen `Notes/` subdirectory:
  ```
  Notes/
  ├── Math/
  │   ├── Algebra/
  │   │   └── Generated notes for Quadratic Equations.md
  ├── CS/
  │   ├── Machine_Learning/
  │   │   └── Generated notes for Neural Networks Basics.md
  ```

### Example Run

```bash
python main.py "Algebra_101.pptx"
```

### Help

If OCR is not working, ensure Tesseract OCR is installed and accessible via your system PATH.

```bash
tesseract --version
```

If LaTeX rendering is incorrect, check that `pypandoc` and `latex2mathml` are properly installed.

### Authors

Keith Yao

### Version History

- 0.2

  - Added OCR support for images and PDFs
  - Added LaTeX formula rendering as inline images in output files
  - Intelligent directory placement of generated notes

- 0.1
  - Initial release with PPTX, PDF, TXT parsing and AI note generation
