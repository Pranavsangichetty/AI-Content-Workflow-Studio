# AI Content Workflow Studio

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://ai-content-workflow-studio-2uws6rnshanmeoixp3daxw.streamlit.app/)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg?logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.38%2B-FF4B4B.svg?logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Google Gemini](https://img.shields.io/badge/Google%20Gemini-Pro%20%2F%20Flash-4285F4.svg?logo=google&logoColor=white)](https://ai.google.dev/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A production-grade, composable AI workflow studio built with Streamlit. Instead of relying on a single prompt-and-chat interface, **AI Content Workflow Studio** decomposes content operations into modular, inspectable micro-steps (Analyze, Outline, Generate, Critique, Rewrite, Output).

---

## 🌐 Live Demo

🚀 **Experience the live workflow studio deployed on Streamlit Community Cloud:**
👉 **[Launch Live Demo](https://ai-content-workflow-studio-2uws6rnshanmeoixp3daxw.streamlit.app/)**

---

## The Product Mindset: Why Workflows Beat Chatbots

Standard chatbots suffer from three fundamental flaws in professional content production:
1. **Cognitive Overload:** Forcing one LLM prompt to research, draft, edit, and format leads to hallucination and bland, generic output.
2. **Black Box Execution:** If a single prompt produces a poor output, the creator has to rewrite the entire prompt without knowing where reasoning failed.
3. **Lack of Repeatability:** Quality cannot be automated, measured, or handed off to teammates without a structured pipeline.

**AI Content Workflow Studio** solves this with **Composable Sequential Pipelines**:
- **Granular Control:** Creators can insert, reorder, or remove nodes based on the target asset.
- **Auditability:** Creators can inspect each intermediate transformation (e.g., comparing the raw draft against the editorial critique and final rewrite).
- **Deterministic Demo Simulation:** Runs with template-based mock responses out of the box so reviewers can test the workflow interface, pipeline reordering, and intermediate steps without needing an API key or running a local LLM.

---

## Architecture & How It Works

The workflow execution pipeline operates as a directed sequential processing chain:

```text
+---------------------------------------------------------------------------------------+
|                               AI CONTENT WORKFLOW STUDIO                              |
+---------------------------------------------------------------------------------------+
|  Top Navigation: Brand Title, Subtitle, Demo Mode Indicator, GitHub Repository Link  |
+---------------------------------------------------------------------------------------+
|  Hero Section: Visual Pipeline Rail & High-level Value Proposition                   |
+---------------------------------------------------------------------------------------+
|  1. Define Your Content                                                               |
|     [Brief Text Area: What do you want to create?]   [Audience, Tone, Run Button]     |
+---------------------------------------------------------------------------------------+
|  2. Build Your Workflow                                                               |
|     [Available Nodes Panel]        |        [Active Workflow Canvas (Compact)]        |
|     + Input, Analyze, Outline...   |        Row 1: [ Input ]   [ Analyze ]   [ Gen ]  |
|     + Generate, Critique, Rewrite  |        Row 2: [ Critique ][ Rewrite ]  [ Output]|
|     + Output                       |        (Reorder Up/Down & Remove Controls)       |
|     [Template Loaders / Reset]     |                                                  |
+---------------------------------------------------------------------------------------+
|  3. Execution & Results                                                               |
|     [Tab: Workflow Steps]                    [Tab: Final Output]                      |
|     - Step Checkpoints (latency, source)     - Ready Deliverable Display              |
|     - Intermediate transformations diffs     - Export as Plain Text (.TXT)            |
|     - Token usage & diagnostic logs          - Export as Markdown (.MD)               |
+---------------------------------------------------------------------------------------+
|  Bottom Call-to-Action: Ready to create something amazing? -> Start Creating          |
+---------------------------------------------------------------------------------------+
```

### Execution Flow
1. **Context Initialization (`Input`):** Captures the user's brief, target audience, tone, and platform constraints into an execution context.
2. **Sequential Node Processing:** Each node receives the accumulated state from prior nodes and applies its specialized system prompt and role.
3. **State Accumulation:** Transformed text, reasoning checkpoints, execution latencies, and provider source tags are appended to the run history.
4. **Final Assembly (`Output`):** Polishes and prepares the final deliverable with zero markdown artifacts or stray scaffolding.

---

## Available Workflow Nodes

| Node Name | Category | Description | Primary Role |
| :--- | :--- | :--- | :--- |
| **Input** | Foundation | Captures initial brief, target audience, tone, and context parameters. | Context ingest & validation |
| **Analyze** | Strategy | Evaluates angles, target audience psychographics, hooks, and content objectives. | Strategic breakdown |
| **Outline** | Strategy | Generates a structured multi-part outline with logical progression. | Structural blueprinting |
| **Generate** | Creation | Drafts the initial long-form or short-form content asset based on the blueprint. | Primary content creation |
| **Critique** | Refinement | Reviews the generated draft critically for clarity, fluff, tone alignment, and impact. | Editorial QA & review |
| **Rewrite** | Refinement | Polishes, tightens, and refines the draft using the critique feedback. | Optimization & revision |
| **Output** | Deliverable | Formats the final deliverable for publication and enables instant download. | Production polish & export |

---

## Pre-built Workflow Templates

The studio includes 4 one-click verified templates tailored to specific production workflows:

1. **LinkedIn Post:**
   - *Pipeline:* `Input` → `Generate` → `Critique` → `Rewrite` → `Output`
   - *Focus:* Punchy hooks, line breaks for scannability, strong takeaways, professional networking tone.
2. **Blog Article:**
   - *Pipeline:* `Input` → `Outline` → `Generate` → `Critique` → `Rewrite` → `Output`
   - *Focus:* In-depth educational structure, H2/H3 hierarchy, comprehensive coverage, clear actionable takeaways.
3. **Marketing Copy:**
   - *Pipeline:* `Input` → `Generate` → `Critique` → `Rewrite` → `Output`
   - *Focus:* Conversion-focused frameworks (AIDA, PAS), compelling value propositions, and strong call-to-actions.
4. **Resume Improvement:**
   - *Pipeline:* `Input` → `Analyze` → `Rewrite` → `Output`
   - *Focus:* Action verbs, quantified impact metrics, ATS optimization, and executive phrasing.

---

## Deterministic Fallback & Demo Mode

- **Demo Simulation Mode:** When no API key is provided, the application operates in a deterministic simulation mode using a rule-based mock engine. It produces structured mock transformations tailored to the user's brief, audience, and tone. This allows reviewers to explore the UI, inspect intermediate steps, and test node reordering without requiring an API key or local model weights. Note: Demo mode is a deterministic simulation and does not run an offline LLM.
- **Graceful Fallback:** When live Gemini mode is enabled, unexpected API failures (such as quota limits, invalid keys, or network disconnects) are caught. The engine falls back to the deterministic simulation mode, clearly labeling each affected step in the diagnostics tab.
- **Immediate Evaluation:** Reviewers can explore the workflow studio immediately without needing an API key or account setup.

---

## Google Gemini Integration

When configured with a Google Gemini API key:
- **SDK:** Official `google-genai` Python SDK (`Client(api_key=...)`).
- **Model Support:** Defaults to `gemini-2.5-flash` for high-throughput, low-latency node execution. Also supports `gemini-1.5-pro` and `gemini-1.5-flash`.
- **In-Memory Session Handling:** User-entered API keys are held in memory in Streamlit session state (`st.session_state`) during the active browser session and are not written to local disk or logged.
- **Environment & Secret Discovery:** Supports loading keys from Streamlit `st.secrets["GEMINI_API_KEY"]`, environment variable `GEMINI_API_KEY`, or local `.env`.

---

## Tech Stack

- **Frontend & App Framework:** [Streamlit](https://streamlit.io/) (Single-service Python web framework)
- **AI / LLM Engine:** [Google GenAI SDK](https://github.com/googleapis/python-genai) (`google-genai>=1.0.0`)
- **Styling:** Custom Vanilla CSS with dark SaaS design language (deep navy palette, rounded cards, sleek borders, zero emoji clutter)
- **Runtime:** Python 3.10+ (Tested on Python 3.10, 3.11, 3.12, 3.13)
- **Testing:** Python standard library `unittest`

---

## Project Structure

```text
AI_Content_Workflow_Studio/
├── app.py                      # Main Streamlit SaaS application (vertically stacked dark UI)
├── workflow_engine.py          # Modular workflow engine, Gemini caller & demo generator
├── requirements.txt            # Pinned, lightweight dependencies
├── test_app.py                 # Automated unit tests for engine, templates, and fallback
├── DEPLOYMENT_CHECKLIST.md     # Production release and verification checklist
├── README.md                   # Complete architectural & operational documentation
├── .gitignore                  # Git ignore rules for secrets, virtual environments, and cache
└── .env.example                # Template for optional local environment variables
```

---

## Local Setup & Installation

### Prerequisites
- Python 3.10, 3.11, 3.12, or 3.13
- Git

### 1. Clone the Repository
```bash
git clone https://github.com/<your-username>/AI-Content-Workflow-Studio.git
cd AI-Content-Workflow-Studio
```

### 2. Create and Activate a Virtual Environment
**On macOS/Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

**On Windows (PowerShell):**
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the Application
```bash
streamlit run app.py
```
The application will launch locally at `http://localhost:8501`.

---

## Environment Variables

The application runs fully without any environment variables. If you wish to enable Gemini by default:

1. Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```
2. Set your Google Gemini API key:
   ```env
   GEMINI_API_KEY=your_gemini_api_key_here
   GEMINI_MODEL=gemini-2.5-flash
   ```

*Note: Never commit your `.env` file. It is excluded by `.gitignore`.*

---

## How to Use the Studio

1. **Step 1 — Define Your Content:**
   - Enter your content idea or draft into the brief area.
   - Select your target audience (e.g., Tech Founders, General Public, Students).
   - Choose your desired tone (e.g., Professional, Authoritative, Casual, Persuasive).
2. **Step 2 — Configure the Pipeline:**
   - Choose a starter template (e.g., LinkedIn Post, Blog Article) or build a custom chain.
   - Click node chips from the **Available Nodes** panel to add steps.
   - Use the **Up** / **Down** reorder buttons and **Remove** controls on the canvas cards.
3. **Step 3 — Run & Inspect:**
   - Click **Run Studio Pipeline**.
   - Monitor real-time step progress and per-node execution time.
   - Inspect intermediate drafts, critiques, and revisions under the **Workflow Steps** tab.
4. **Step 4 — Export:**
   - Switch to the **Final Output** tab to preview your deliverable.
   - Click **Download Plain Text (.txt)** or **Download Markdown Report (.md)**.

---

## Automated Testing

The repository contains an automated test suite verifying node execution, starter templates, deterministic outputs, and Gemini fallback.

Run tests using:
```bash
python -m unittest test_app.py
```

Expected output:
```text
......
----------------------------------------------------------------------
Ran 6 tests in ~1.8s

OK
```

---

## Known Limitations & Future Roadmap

### Current Limitations
- **Sequential Execution:** Nodes currently execute in strict linear sequence; branching (parallel multi-agent review) is planned for future releases.
- **Single-Session Memory:** Execution history resets when the browser tab is refreshed (persisting state across sessions would require an external database).

### Future Roadmap
- [ ] Multi-agent debate loops (automatic 2-round critique-and-revise cycles).
- [ ] Export directly to publishing integrations (e.g., Ghost, Medium, LinkedIn API).
- [ ] Custom system prompt editor for individual canvas nodes.
- [ ] Pipeline serialization to JSON for importing and sharing custom workflows.

---

## License & Author

Developed by **Sangeetha S** as a demonstration of production-grade AI agentic workflows and product architecture.

Licensed under the [MIT License](LICENSE).
