# TripCraft Deployment Guide

## 1) Deploy Backend (Render)

1. Push this repo to GitHub.
2. Go to Render -> New -> Web Service.
3. Connect your GitHub repo.
4. Configure:
   - Root Directory: `backend`
   - Runtime: `Python 3`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn app:app --host 0.0.0.0 --port $PORT`
5. Deploy and copy the backend URL, for example:
   - `https://tripcraft-backend.onrender.com`
6. Check it:
   - `https://tripcraft-backend.onrender.com/`

## 2) Deploy Frontend (Vercel)

1. Go to Vercel -> New Project.
2. Import the same GitHub repo.
3. Configure:
   - Root Directory: `ai-demo-frontend`
   - Framework Preset: `Create React App`
4. Add environment variable before deploy:
   - `REACT_APP_API_BASE_URL` = your backend URL
   - Example: `https://tripcraft-backend.onrender.com`
5. Deploy.

## 3) If Frontend Was Already Deployed

1. Open your Vercel project -> Settings -> Environment Variables.
2. Add or update:
   - `REACT_APP_API_BASE_URL`
3. Redeploy the latest build.

## 4) CORS

Backend currently allows all origins (`allow_origins=["*"]`), so Vercel frontend can call it directly.

## 5) Local Development Note

If no `REACT_APP_API_BASE_URL` is set, frontend defaults to:
- `http://127.0.0.1:8000`
