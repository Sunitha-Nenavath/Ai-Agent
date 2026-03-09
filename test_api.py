import requests

url = 'http://localhost:8000/api/resume-analysis'

try:
    with open("temp_NENAVATH SUNITHA Final resume 1_2026.pdf", "rb") as f:
        files = {'file': ('resume.pdf', f, 'application/pdf')}
        print("Sending real PDF to backend API...")
        response = requests.post(url, files=files)
        print("Status Code:", response.status_code)
        print("Response Body:", response.text)
except Exception as e:
    print("Error:", e)
