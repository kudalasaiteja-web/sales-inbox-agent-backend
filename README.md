# Sales Inbox Agent

An AI-powered email triage system that classifies inbound sales emails and routes
them to the correct team member, built for the FDE Intern Challenge.

## Live URLs

- **Frontend**: https://sales-inbox-agent-frontend.vercel.app
- **Backend API**: https://sales-inbox-agent-backend.onrender.com
- **API docs**: https://sales-inbox-agent-backend.onrender.com/docs
- **Backend repo**: https://github.com/kudalasaiteja-web/sales-inbox-agent-backend
- **Frontend repo**: https://github.com/kudalasaiteja-web/sales-inbox-agent-frontend

> Note: the backend runs on Render's free tier, which spins down after ~15
> minutes of inactivity. The first request after idle time may take 30-50
> seconds to respond while it wakes up — this is expected, not a bug.

## Stack

- **Backend**: Python, FastAPI, MongoDB Atlas
- **AI**: Google Gemini (`gemini-flash-latest`)
- **Frontend**: React (Vite)
- **Deployment**: Render (backend), Vercel (frontend)

See `DECISIONS.md` for the reasoning behind these choices, and `EVALS.md` for
routing accuracy results.

## Running locally

### Prerequisites
- Python 3.10+
- Node.js (LTS)
- A MongoDB Atlas connection string (free tier)
- A Google Gemini API key (from https://aistudio.google.com/apikey)

### Backend setup

```bash
cd backend
python -m venv venv
venv\Scripts\activate        # Windows
pip install -r requirements.txt
```

Copy `.env.example` to `.env` and fill in your own values:
