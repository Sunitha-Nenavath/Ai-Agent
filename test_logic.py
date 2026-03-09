import os
from dotenv import load_dotenv

load_dotenv()

from resume_parser import extract_text_from_pdf
from ai_engine import analyze_resume

try:
    print("Testing analyze_resume directly...")
    res = analyze_resume("Test resume with React and Node.js skills")
    print(res)
except Exception as e:
    import traceback
    traceback.print_exc()

