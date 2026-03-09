import os
from resume_parser import extract_text_from_pdf
from ai_engine import analyze_resume

try:
    print("Testing extract_text_from_pdf directly...")
    file_name = "temp_NENAVATH SUNITHA Final resume_2026.pdf"
    text = extract_text_from_pdf(file_name)
    print(f"Extracted Text Length: {len(text)}")
    print("\nTesting analyze_resume with extracted text...")
    res = analyze_resume(text)
    print("Analyze result keys:", list(res.keys()))
except Exception as e:
    import traceback
    traceback.print_exc()
