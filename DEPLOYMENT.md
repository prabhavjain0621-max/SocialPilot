# SocialPilot Deployment Guide (Render + Vercel)

This guide walks you through deploying **SocialPilot**:
- **Backend & Database**: Deployed on [Render](https://render.com) (FastAPI + Managed PostgreSQL).
- **Frontend**: Deployed on [Vercel](https://vercel.com) (React 18 + Vite SPA).

---

## Prerequisites
1. A [GitHub](https://github.com) account with your project pushed to a repository.
2. A free [Render account](https://render.com).
3. A free [Vercel account](https://vercel.com).

---

## Phase 1: Push Changes to GitHub

Commit and push all recent deployment configurations to your GitHub repository:

```bash
git add .
git commit -m "Configure deployment for Render and Vercel"
git push origin main
```

---

## Phase 2: Deploy Backend & Database on Render

You can deploy using either the **Automated Blueprint (Recommended)** or **Manual Setup**.

### Option A: Automated Blueprint (Fastest — 2 clicks)
1. Go to your [Render Dashboard](https://dashboard.render.com/).
2. Click **New +** in the top right and select **Blueprint**.
3. Connect your GitHub repository (`socialpilot`).
4. Render will automatically detect [`render.yaml`](./render.yaml) and configure:
   - **Database**: `socialpilot-db` (PostgreSQL)
   - **Web Service**: `socialpilot-api` (FastAPI + Uvicorn)
5. Click **Apply**. Render will provision your database, run migrations, and launch your API.

---

### Option B: Manual Setup on Render
If you prefer creating services manually:

#### Step 1: Create PostgreSQL Database
1. In Render, click **New +** > **PostgreSQL**.
2. **Name**: `socialpilot-db`
3. **Database**: `socialpilot`
4. **User**: `socialpilot_user`
5. **Plan**: Free
6. Click **Create Database**.
7. Once created, copy the **Internal Database URL** (or External Connection String).

#### Step 2: Create Web Service
1. Click **New +** > **Web Service**.
2. Connect your GitHub repository.
3. Configure the settings:
   - **Name**: `socialpilot-api`
   - **Root Directory**: `backend`
   - **Environment**: `Python`
   - **Region**: Same as your database (e.g., Oregon or Frankfurt)
   - **Branch**: `main`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `bash start.sh`
   - **Plan**: Free

#### Step 3: Add Environment Variables in Render
In your Web Service under the **Environment** tab, add:

| Key | Value / Description |
|---|---|
| `DATABASE_URL` | *Paste your Render PostgreSQL connection string* |
| `SECRET_KEY` | *Any random 32+ character secret string* |
| `CORS_ORIGINS` | `http://localhost:5173,https://your-socialpilot.vercel.app` |
| `FRONTEND_URL` | `https://your-socialpilot.vercel.app` *(update after Phase 3)* |
| `PUBLIC_BASE_URL` | `https://socialpilot-api.onrender.com` *(your Render Web Service URL)* |
| `GEMINI_API_KEY` | *(Optional) Your Google Gemini API Key for AI post generation* |
| `GEMINI_MODEL` | `gemini-2.0-flash` |
| `REDIS_URL` | *(Optional) Upstash or Render Redis URL if using Celery scheduler* |

4. Click **Create Web Service**. Wait for the build to finish.
5. Copy your live backend URL (e.g., `https://socialpilot-api.onrender.com`).
   - Test it by visiting `https://socialpilot-api.onrender.com/health` in your browser. It should return `{"status":"ok"}`.

---

## Phase 3: Deploy Frontend on Vercel

1. Log in to [Vercel](https://vercel.com).
2. Click **Add New...** > **Project**.
3. Select your GitHub repository (`socialpilot`) and click **Import**.
4. In the **Configure Project** screen:
   - **Project Name**: `socialpilot` (or custom name)
   - **Framework Preset**: `Vite`
   - **Root Directory**: Click **Edit** and choose `new_frontend`
   - **Build Command**: `npm run build` (default)
   - **Output Directory**: `dist` (default)
5. Expand **Environment Variables** and add:

| Key | Value |
|---|---|
| `VITE_API_URL` | `https://socialpilot-api.onrender.com` *(your Render service URL, no trailing slash)* |

6. Click **Deploy**.
7. Vercel will install dependencies, build the TypeScript bundle, and provide your live URL (e.g., `https://socialpilot.vercel.app`).

---

## Phase 4: Final Connection & Verification

### 1. Update Frontend URL in Render
Once you have your Vercel URL (e.g. `https://socialpilot.vercel.app`):
1. Go back to Render > `socialpilot-api` > **Environment**.
2. Set:
   - `FRONTEND_URL`: `https://socialpilot.vercel.app`
   - `CORS_ORIGINS`: `http://localhost:5173,https://socialpilot.vercel.app`
3. Click **Save Changes**. Render will automatically redeploy with the updated config.

### 2. Update Social Media OAuth Redirect URIs
If you are using OAuth integrations for social channels, update your developer app consoles with your live Render backend URL:

- **LinkedIn**: `https://<YOUR_RENDER_URL>/auth/linkedin/callback`
- **YouTube**: `https://<YOUR_RENDER_URL>/auth/youtube/callback`
- **Instagram**: `https://<YOUR_RENDER_URL>/auth/instagram/callback`
- **Facebook**: `https://<YOUR_RENDER_URL>/auth/facebook/callback`
- **X (Twitter)**: `https://<YOUR_RENDER_URL>/auth/x/callback`

---

## Deployment Architecture Summary

```
                       ┌────────────────────────────┐
                       │   Vercel (new_frontend)    │
                       │ https://socialpilot.vercel │
                       └─────────────┬──────────────┘
                                     │
                     HTTPS REST API / JSON Web Tokens
                                     │
                                     ▼
                       ┌────────────────────────────┐
                       │    Render (backend API)    │
                       │ https://socialpilot-api    │
                       └──────┬──────────────┬──────┘
                              │              │
              PostgreSQL Pool │              │ Static Uploads
                              ▼              ▼
                     ┌────────────────┐ ┌───────────────┐
                     │ PostgreSQL DB  │ │ /media folder │
                     └────────────────┘ └───────────────┘
```
