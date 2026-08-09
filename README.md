**candidate_id**: sai.teja@gmail.com

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


GEMINI_API_KEY=your_key_here
MONGODB_URI=your_connection_string_here

Run the server:
```bash
uvicorn main:app --reload
```
Backend runs at `http://127.0.0.1:8000`. Interactive docs at `/docs`.

### Frontend setup

```bash
cd frontend
npm install
npm run dev
```
Frontend runs at `http://localhost:5173`.

> Note: `App.jsx` currently points `API_BASE` at the deployed Render URL. To
> test against a local backend instead, change `API_BASE` to
> `http://127.0.0.1:8000` and make sure the backend's CORS `allow_origins`
> includes `http://localhost:5173`.

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| POST | `/tasks` | Create a task |
| GET | `/tasks?candidate_id=...` | List tasks, with optional filters |
| PATCH | `/tasks/{task_id}` | Update a task |
| DELETE | `/tasks/{task_id}` | Delete a task |
| GET | `/users` | List team roster |
| POST | `/ingest` | Ingest a batch of emails, classify, and create/update tasks |
| GET | `/api/tasks` | Frontend-facing task list |
| GET | `/api/stats` | Task counts by assignee/category/priority |
| POST | `/api/chat` | Natural-language Q&A over stored task data |

## Testing

- `python test_routing.py` — runs the routing engine against known trap cases
- `python run_eval.py` — runs the full labeled evaluation set (see `EVALS.md`)
- `python test_ingest.py` — sends `inbox.json` through the live `/ingest` endpoint

## Project files

- `main.py` — FastAPI app and all endpoints
- `routing.py` — Gemini prompt and classification logic
- `database.py` — MongoDB connection
- `models.py` — Pydantic request/response models
- `eval_set.py` / `run_eval.py` — evaluation harness
- `DECISIONS.md` — design decisions and tradeoffs
- `EVALS.md` — evaluation methodology and results