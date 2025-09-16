# Club Member Management API

## Overview

This is a FastAPI backend project for managing club members using a Supabase PostgreSQL database. It supports adding, retrieving, updating, and deleting club members. The API ensures unique emails and returns JSON responses.

## Features

- Add new club members (POST /members)
- Retrieve all members (GET /members)
- Update members by ID (PUT /members/{id})
- Delete members by ID (DELETE /members/{id})
- Email uniqueness validation

## Tech Stack

- Python 3.10+
- FastAPI
- Supabase (PostgreSQL)
- Uvicorn
- Postman
- Deployment on Render.com

## Getting Started

### Prerequisites

- Python 3.10 or higher
- Supabase account with a PostgreSQL project
- Git and GitHub account

### Installation

1. Clone the repo:

git clone https://github.com/Sanjana1117/club_member_management.git
cd club


2. Create and activate a virtual environment:

python -m venv venv

Windows
.\venv\Scripts\activate

macOS/Linux
source venv/bin/activate


3. Install dependencies:

pip install -r requirements.txt


4. Create a `.env` file with your Supabase credentials:

SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_api_key

5. Run locally:
uvicorn main:app --reload

Access the API at [http://localhost:8000]

## API Endpoints

- Get all members:  
  https://club-member-management.onrender.com/members

- Update or delete member by ID:  
  https://club-member-management.onrender.com/members/{id}


## Deployment

The backend is deployed on Render:  
[https://club-member-management.onrender.com](https://club-member-management.onrender.com)

