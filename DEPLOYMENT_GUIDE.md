# 🚀 Deploying Project Dwight to Cloud

This guide walks you through deploying Project Dwight so anyone can test it via shareable links.

## Architecture

```
┌─────────────────────┐        ┌─────────────────────┐
│   Frontend (Vercel) │  ───▶  │  Backend (Railway)  │
│   Static HTML/JS    │        │  FastAPI + FAISS    │
│   FREE              │        │  $5 free credits    │
└─────────────────────┘        └─────────────────────┘
                                        │
                                        ▼
                               ┌─────────────────────┐
                               │     Groq API        │
                               │   (Free Tier)       │
                               └─────────────────────┘
```

---

## Step 1: Deploy Backend to Railway

### 1.1 Push Code to GitHub

First, make sure your latest code is pushed:

```bash
cd c:\Users\SauravPayal\project\Dwight
git add .
git commit -m "Prepare for cloud deployment"
git push origin main
```

### 1.2 Create Railway Account

1. Go to [railway.app](https://railway.app)
2. Sign up with GitHub (recommended for easy integration)
3. You get $5 free credits (enough for testing)

### 1.3 Deploy from GitHub

1. Click **"New Project"**
2. Select **"Deploy from GitHub Repo"**
3. Find and select: `Monkey-D-luffy-beep/Dwight---The-ChatBot----International-Freight-Forwarding`
4. **IMPORTANT**: Set the root directory to `backend`

### 1.4 Configure Environment Variables

In Railway dashboard, go to **Variables** tab and add:

| Variable | Value |
|----------|-------|
| `GROQ_API_KEY` | Your Groq API key from https://console.groq.com |
| `GROQ_MODEL` | `llama-3.1-8b-instant` |
| `EMBEDDING_MODEL` | `all-MiniLM-L6-v2` |
| `SIMILARITY_THRESHOLD` | `0.15` |
| `PORT` | `8000` |

### 1.5 Configure Deploy Settings

1. Go to **Settings** tab
2. Set **Root Directory**: `backend`
3. Set **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`

### 1.6 Generate Domain

1. Go to **Settings** → **Networking** → **Generate Domain**
2. You'll get a URL like: `https://dwight-backend-production.up.railway.app`
3. **Copy this URL** - you'll need it for the frontend!

### 1.7 Test Backend

Visit: `https://YOUR-RAILWAY-URL/health`

You should see:
```json
{"status": "healthy", "message": "Dwight is ready to assist!"}
```

---

## Step 2: Deploy Frontend to Vercel

### 2.1 Update Frontend API URL

Edit `frontend/script.js` and update `API_BASE_URL`:

```javascript
const CONFIG = {
    API_BASE_URL: 'https://YOUR-RAILWAY-URL-HERE.up.railway.app',  // ← Put your Railway URL here
    ENDPOINTS: {
        CHAT: '/api/chat',
        ...
    }
};
```

Push the change:
```bash
git add frontend/script.js
git commit -m "Update API URL for production"
git push origin main
```

### 2.2 Create Vercel Account

1. Go to [vercel.com](https://vercel.com)
2. Sign up with GitHub
3. Completely FREE for static sites

### 2.3 Deploy from GitHub

1. Click **"Add New Project"**
2. Import your GitHub repo
3. **Framework Preset**: Other
4. **Root Directory**: `frontend`
5. Click **Deploy**

### 2.4 Get Your Live URL

Vercel will give you a URL like:
- `https://dwight-chatbot.vercel.app`

**Share this link with testers!** 🎉

---

## Step 3: Test Everything

1. Open your Vercel URL in a browser
2. Click the chat widget
3. Ask: "What services does Tiger Logistics offer?"
4. You should get a proper response!

---

## Troubleshooting

### "I'm unable to connect right now"
- Check if Railway backend is running (visit `/health`)
- Verify `API_BASE_URL` in frontend matches your Railway URL
- Check browser console (F12) for CORS errors

### CORS Errors
The backend has CORS configured for all origins (`*`). If you still see CORS errors:
1. Check Railway logs for errors
2. Make sure backend started successfully

### Slow First Response
- First request after idle may take 20-30 seconds (cold start)
- Subsequent requests should be fast (~2 seconds)

### Railway Credits Running Out
- $5 gives ~500 hours of small instance
- To save credits: pause the service when not testing
- Consider upgrading for production use

---

## Quick Reference

| Service | URL |
|---------|-----|
| Backend (Railway) | `https://YOUR-RAILWAY-URL.up.railway.app` |
| Frontend (Vercel) | `https://YOUR-VERCEL-URL.vercel.app` |
| Health Check | `https://YOUR-RAILWAY-URL.up.railway.app/health` |

---

## Updating After Deployment

Just push to GitHub - both Railway and Vercel will auto-redeploy:

```bash
git add .
git commit -m "Your changes"
git push origin main
```

Railway and Vercel both watch your GitHub repo and redeploy automatically! 🚀
