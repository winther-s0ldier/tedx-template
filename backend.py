import os
from datetime import datetime
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field

app = FastAPI(title="TEDx Invitation Generator API")

# --- Models ---

class InvitationRequest(BaseModel):
    speaker_name: str = Field(..., example="Jane Doe")
    why_you: str = Field(..., example="Your expertise in AI ethics is unparalleled.")
    reply_date: str = Field(..., example="2026-03-01")

# --- Utilities ---

def get_date_suffix(day: int) -> str:
    """Returns the ordinal suffix for a given day."""
    if 11 <= day <= 13:
        return "th"
    return {1: "st", 2: "nd", 3: "rd"}.get(day % 10, "th")

def format_ordinal_date(date_str: str) -> str:
    """Formats ISO date string to '1st March, 2026' style."""
    try:
        dt = datetime.fromisoformat(date_str)
        day = dt.day
        suffix = get_date_suffix(day)
        # Format: "1st March, 2026"
        return dt.strftime(f"{day}{suffix} %B, %Y")
    except ValueError:
        return date_str

# --- Routes ---

@app.get("/health")
def health_check():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

@app.post("/generate", response_class=HTMLResponse)
async def generate_invitation(payload: InvitationRequest):
    template_path = "template.html"
    
    if not os.path.exists(template_path):
        raise HTTPException(status_code=500, detail="HTML template file not found on server.")

    try:
        # 1. Read the template
        with open(template_path, "r", encoding="utf-8") as f:
            template_content = f.read()

        # 2. Format the date
        formatted_date = format_ordinal_date(payload.reply_date)

        # 3. Perform replacements
        final_html = template_content.replace("{{SpeakerName}}", payload.speaker_name)
        final_html = final_html.replace("{{WhyYouContent}}", payload.why_you)
        final_html = final_html.replace("{{ReplyDate}}", formatted_date)

        return final_html

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)