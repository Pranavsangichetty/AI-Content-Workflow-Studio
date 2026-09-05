# AI Content Workflow Studio - Deployment & Recruiter Release Checklist

Follow this pre-flight checklist before submitting your prototype and repository to the hiring team.

---

### 1. Local Pre-Flight Verification
- [x] Application launches without error via `streamlit run app.py`.
- [x] All 6 unit tests pass via `python -m unittest test_app.py`.
- [x] Demo Mode executes with zero API keys configured.
- [x] All 4 Starter Templates load and execute completely:
  - [x] LinkedIn Post
  - [x] Blog Article
  - [x] Marketing Copy
  - [x] Resume Improvement
- [x] Node Library actions verified:
  - [x] Adding nodes to pipeline.
  - [x] Reordering nodes up and down.
  - [x] Removing nodes.
  - [x] Resetting to default pipeline.
  - [x] Clearing canvas.
- [x] Guardrails verified:
  - [x] Empty brief displays friendly alert.
  - [x] Empty canvas displays friendly alert.
- [x] Exports tested:
  - [x] Plain Text (.txt) download.
  - [x] Markdown (.md) audit trail download.

---

### 2. Secret & Repository Sanitization
- [x] `.gitignore` excludes `.env`, `secrets.toml`, `.venv/`, and Python cache artifacts.
- [x] No hardcoded API keys exist in `app.py`, `workflow_engine.py`, or documentation.
- [x] No absolute Windows paths (`C:\Users\...`) exist in committed files.
- [x] `requirements.txt` contains only lightweight, pure-Python packages (`streamlit`, `google-genai`).

---

### 3. GitHub Repository Setup
1. Initialize git in the project root:
   ```bash
   git init
   git branch -M main
   ```
2. Stage and commit all files:
   ```bash
   git add .
   git commit -m "feat: production-ready AI Content Workflow Studio MVP"
   ```
3. Create a public repository on GitHub named `AI_Content_Workflow_Studio`.
4. Link remote and push:
   ```bash
   git remote add origin https://github.com/<your-username>/AI-Content-Workflow-Studio.git
   git push -u origin main
   ```

---

### 4. Streamlit Community Cloud Deployment
1. Log in to [share.streamlit.io](https://share.streamlit.io/).
2. Click **"New app"**.
3. Select your repository: `<your-username>/AI-Content-Workflow-Studio`.
4. Branch: `main`.
5. Main file path: `app.py`.
6. *(Optional)* Under **Advanced settings > Secrets**, configure `GEMINI_API_KEY = "your-key"` if live Gemini calls are desired. If omitted, the app will deploy in functional Demo Simulation Mode.
7. Click **"Deploy!"**.

---

### 5. Final Recruiter Submission Bundle
Provide the recruiter with:
1. **Live Prototype URL:** `https://<your-app-name>.streamlit.app`
2. **GitHub Repository URL:** `https://github.com/<your-username>/AI-Content-Workflow-Studio`
3. **Product Highlights:**
   - Sequential, composable node pipeline (Analyze, Generate, Critique, Rewrite, Output).
   - Granular intermediate inspection and auditability.
   - Deterministic Demo Mode simulation for testing without an API key, with Gemini integration and graceful fallback.
