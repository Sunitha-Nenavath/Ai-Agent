from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from resume_parser import extract_text_from_pdf
from ai_engine import analyze_resume, get_skill_gaps, generate_roadmap, chat_with_mentor
from models import UserProfile, ChatMessage, SkillGapRequest
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return {"message": "Vidyaguide AI Backend Running"}


@app.post("/api/resume-analysis")
async def resume_analysis_endpoint(file: UploadFile = File(...)):
    temp_file = f"temp_{file.filename}"
    try:
        with open(temp_file, "wb") as f:
            f.write(await file.read())

        resume_text = extract_text_from_pdf(temp_file)
        if not resume_text or len(resume_text.strip()) == 0:
            raise HTTPException(status_code=400, detail="Could not extract text from the provided PDF. Please ensure it is a valid text-based PDF.")

        ai_result = analyze_resume(resume_text)
        if "error" in ai_result:
             raise HTTPException(status_code=500, detail=f"AI Analysis failed: {ai_result['error']}")
             
        return ai_result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if os.path.exists(temp_file):
            os.remove(temp_file)


@app.post("/api/skill-gap")
async def skill_gap_endpoint(request: SkillGapRequest):
    result = get_skill_gaps(request.current_skills, request.target_role)
    if "error" in result and "rate limit" in result["error"].lower():
        raise HTTPException(status_code=429, detail=result["error"])
    elif "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])
    return result


@app.post("/api/roadmap")
async def roadmap_endpoint(profile: UserProfile):
    result = generate_roadmap(profile.dict())
    if "error" in result and "rate limit" in result["error"].lower():
        raise HTTPException(status_code=429, detail=result["error"])
    elif "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])
    return result


@app.post("/api/chat")
async def chat_endpoint(chat: ChatMessage):
    response_text = chat_with_mentor(chat.message, chat.history)
    if "rate limit" in response_text.lower():
         raise HTTPException(status_code=429, detail=response_text)
    return {"response": response_text}
