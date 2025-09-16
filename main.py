from fastapi import FastAPI, status, Path
from fastapi.responses import JSONResponse
from pydantic import BaseModel, EmailStr
from dotenv import load_dotenv
import os
from supabase import create_client, Client

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI()

# Get Supabase credentials from .env
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Debug env loading
print("Supabase URL:", SUPABASE_URL)
print("Supabase Key:", SUPABASE_KEY)

# Create Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Pydantic models for request validation
class Member(BaseModel):
    name: str
    email: EmailStr
    domain: str

class UpdateDomain(BaseModel):
    domain: str

@app.get("/")
def root():
    return {"message": "Club Member Management API is running!"}

@app.get("/members")
def get_members():
    try:
        response = supabase.table('club_members').select("*").execute()
        if response.data is None:
            return JSONResponse(status_code=500, content={"success": False, "message": "Database returned no data"})
        return {"success": True, "data": response.data}
    except Exception as e:
        return JSONResponse(status_code=500, content={"success": False, "message": f"Exception: {str(e)}"})

@app.post("/members")
def add_member(member: Member):
    try:
        existing = supabase.table('club_members').select('*').eq('email', member.email).execute()
        print("Existing check response:", existing)  # Debug print
        print("Existing data:", existing.data)      # Debug print

        if existing.data and len(existing.data) > 0:
            return JSONResponse(status_code=400, content={"success": False, "message": "Email already exists"})
        
        insert_response = supabase.table('club_members').insert({
            "name": member.name,
            "email": member.email,
            "domain": member.domain
        }).execute()
        print("Insert response:", insert_response)  # Debug print

        if insert_response.data is None:
            return JSONResponse(status_code=500, content={"success": False, "message": "Failed to add member"})
        
        return JSONResponse(status_code=status.HTTP_201_CREATED, content={"success": True, "data": insert_response.data})
    except Exception as e:
        return JSONResponse(status_code=500, content={"success": False, "message": f"Exception: {str(e)}"})

@app.put("/members/{id}")
def update_member_domain(id: str = Path(..., description="The UUID of the member to update"), update: UpdateDomain = None):
    try:
        existing = supabase.table('club_members').select('*').eq('id', id).execute()
        if not existing.data or len(existing.data) == 0:
            return JSONResponse(status_code=404, content={"success": False, "message": "Member not found"})

        update_response = supabase.table('club_members').update({"domain": update.domain}).eq('id', id).execute()

        if update_response.data is None or len(update_response.data) == 0:
            return JSONResponse(status_code=500, content={"success": False, "message": "Failed to update member"})

        return JSONResponse(status_code=200, content={"success": True, "data": update_response.data})
    
    except Exception as e:
        return JSONResponse(status_code=500, content={"success": False, "message": f"Exception: {str(e)}"})

@app.delete("/members/{id}")
def delete_member(id: str = Path(..., description="The UUID of the member to delete")):
    try:
        existing = supabase.table('club_members').select('*').eq('id', id).execute()
        if not existing.data or len(existing.data) == 0:
            return JSONResponse(status_code=404, content={"success": False, "message": "Member not found"})

        delete_response = supabase.table('club_members').delete().eq('id', id).execute()

        if delete_response.data is None or len(delete_response.data) == 0:
            return JSONResponse(status_code=500, content={"success": False, "message": "Failed to delete member"})

        return JSONResponse(status_code=200, content={"success": True, "message": "Member deleted successfully"})
    
    except Exception as e:
        return JSONResponse(status_code=500, content={"success": False, "message": f"Exception: {str(e)}"})
