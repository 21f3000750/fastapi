# main.py
import json
import os
from typing import List, Optional

from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Enable CORS for all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["GET"],  # Allows only GET requests
    allow_headers=["*"],  # Allows all headers
)

# Load marks data
marks_data = []
# Construct the full path to marksdata.json
# On Vercel, the root of your deployment is where main.py resides,
# so marksdata.json should be directly accessible.
json_path = os.path.join(os.path.dirname(__file__), 'q-vercel-python.json')

try:
    with open(json_path, 'r') as f:
        marks_data = json.load(f)
except FileNotFoundError:
    print(f"Error: q-vercel-python.json not found at {json_path}. Please ensure it's in the same directory as main.py.")
    # In a production app, you might want to exit or handle this more gracefully.
    # For Vercel, if the file isn't found during deployment, the app might not start correctly.
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}. Check file format.")

# Create a dictionary for efficient lookup
name_to_marks = {item['name']: item['marks'] for item in marks_data}

class MarksResponse(BaseModel):
    marks: List[Optional[int]]

@app.get("/api", response_model=MarksResponse)
async def get_marks(name: List[str] = Query(...)):
    """
    Returns the marks for the given student names.
    If a name is not found, its mark will be None.
    """
    response_marks = []
    for student_name in name:
        response_marks.append(name_to_marks.get(student_name, None))
    return {"marks": response_marks}
