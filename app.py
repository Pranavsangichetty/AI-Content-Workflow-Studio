import streamlit as st
import time
from workflow_engine import (
    run_workflow,
    NODE_LIBRARY,
    DEFAULT_WORKFLOW,
    TEMPLATES,
    get_api_key,
)

# -----------------------------------------------------------------------------
# Page Configuration
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="AI Content Workflow Studio",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# -----------------------------------------------------------------------------
# Custom Premium Dark AI SaaS Styling
# -----------------------------------------------------------------------------
st.markdown(
    """
<style>
    /* Full Page Dark Navy / Blue-Black Background */
    .stApp {
        background:
            radial-gradient(circle at 12% 15%, rgba(67, 56, 202, 0.16), transparent 32%),
            radial-gradient(circle at 88% 18%, rgba(147, 51, 234, 0.14), transparent 32%),
            radial-gradient(circle at 50% 85%, rgba(14, 165, 233, 0.10), transparent 42%),
            linear-gradient(135deg, #07111f 0%, #0b1326 50%, #11102a 100%) !important;
        color: #f8fafc;
        font-family: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    }

    /* Container Constraints & Spacing */
    .block-container {
        padding-top: 1.5rem !important;
        padding-bottom: 3.5rem !important;
        max-width: 1380px !important;
    }

    /* Hide default Streamlit header and footer elements */
    header[data-testid="stHeader"] {
        background: transparent !important;
    }
    footer {
        visibility: hidden !important;
    }

    /* Gradient Typography Utilities */
    .gradient-text {
        background: linear-gradient(135deg, #60a5fa 0%, #a78bfa 50%, #c084fc 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        display: inline-block;
    }
    .eyebrow {
        font-size: 0.75rem;
        text-transform: uppercase;
        letter-spacing: 0.15em;
        font-weight: 700;
        color: #818cf8;
        margin-bottom: 0.4rem;
    }

    /* Glassmorphism Section Cards */
    .saas-card {
        background: rgba(13, 20, 36, 0.72);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 20px;
        padding: 1.8rem 2.2rem;
        margin-bottom: 2rem;
        box-shadow: 0 16px 36px -12px rgba(0, 0, 0, 0.6);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
    }

    .saas-card-header {
        margin-bottom: 1.4rem;
        border-bottom: 1px solid rgba(255, 255, 255, 0.06);
        padding-bottom: 1rem;
    }
    .saas-card-header h2 {
        font-size: 1.45rem;
        font-weight: 700;
        margin: 0;
        color: #ffffff;
        letter-spacing: -0.02em;
    }
    .saas-card-header p {
        font-size: 0.9rem;
        color: #94a3b8;
        margin: 0.35rem 0 0 0;
    }

    /* Top Navigation Header */
    .top-nav {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 1rem 0 1.6rem 0;
        margin-bottom: 0.5rem;
        border-bottom: 1px solid rgba(255, 255, 255, 0.07);
        flex-wrap: wrap;
        gap: 1rem;
    }
    .nav-brand-title {
        font-size: 1.5rem;
        font-weight: 800;
        margin: 0;
        letter-spacing: -0.02em;
        color: #ffffff;
    }
    .nav-brand-sub {
        font-size: 0.82rem;
        color: #94a3b8;
        margin: 0.2rem 0 0 0;
        letter-spacing: 0.03em;
    }
    .nav-status-group {
        display: flex;
        align-items: center;
        gap: 1rem;
        flex-wrap: wrap;
    }
    .status-badge {
        display: inline-flex;
        align-items: center;
        gap: 0.45rem;
        padding: 0.4rem 0.85rem;
        border-radius: 9999px;
        font-size: 0.8rem;
        font-weight: 600;
        letter-spacing: 0.02em;
    }
    .status-badge-demo {
        background: rgba(14, 165, 233, 0.12);
        color: #38bdf8;
        border: 1px solid rgba(14, 165, 233, 0.28);
    }
    .status-badge-live {
        background: rgba(34, 197, 94, 0.12);
        color: #4ade80;
        border: 1px solid rgba(34, 197, 94, 0.28);
    }
    .status-dot {
        width: 7px;
        height: 7px;
        border-radius: 50%;
        display: inline-block;
    }
    .dot-cyan { background: #38bdf8; box-shadow: 0 0 8px #38bdf8; }
    .dot-green { background: #4ade80; box-shadow: 0 0 8px #4ade80; }

    .nav-link-btn {
        display: inline-flex;
        align-items: center;
        gap: 0.4rem;
        color: #cbd5e1;
        text-decoration: none;
        font-size: 0.82rem;
        font-weight: 500;
        padding: 0.4rem 0.9rem;
        border-radius: 8px;
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        transition: all 0.2s ease;
    }
    .nav-link-btn:hover {
        background: rgba(255, 255, 255, 0.1);
        color: #ffffff;
        border-color: rgba(255, 255, 255, 0.2);
    }

    /* Hero Section */
    .hero-card {
        background:
            radial-gradient(circle at 85% 30%, rgba(99, 102, 241, 0.15), transparent 45%),
            rgba(13, 20, 36, 0.72);
        border: 1px solid rgba(255, 255, 255, 0.09);
        border-radius: 22px;
        padding: 2.4rem 2.8rem;
        margin-bottom: 2rem;
        display: grid;
        grid-template-columns: 1.3fr 1fr;
        gap: 2.5rem;
        align-items: center;
        box-shadow: 0 20px 40px -15px rgba(0, 0, 0, 0.7);
    }
    @media (max-width: 960px) {
        .hero-card {
            grid-template-columns: 1fr;
            padding: 1.8rem;
            gap: 1.8rem;
        }
    }
    .hero-headline {
        font-size: 2.3rem;
        font-weight: 800;
        line-height: 1.15;
        margin: 0.3rem 0 0.85rem 0;
        letter-spacing: -0.03em;
        color: #ffffff;
    }
    .hero-copy {
        font-size: 0.98rem;
        color: #94a3b8;
        line-height: 1.55;
        margin-bottom: 1.4rem;
        max-width: 580px;
    }
    .hero-pills {
        display: flex;
        flex-wrap: wrap;
        gap: 0.5rem;
    }
    .hero-pill {
        display: inline-flex;
        align-items: center;
        gap: 0.4rem;
        padding: 0.35rem 0.75rem;
        background: rgba(255, 255, 255, 0.04);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 8px;
        font-size: 0.78rem;
        color: #cbd5e1;
        font-weight: 500;
    }

    /* Conceptual Flow Illustration (Pure CSS, No Arrows!) */
    .flow-rail-box {
        background: rgba(7, 12, 23, 0.6);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 1.6rem 1.4rem;
    }
    .rail-title {
        font-size: 0.75rem;
        text-transform: uppercase;
        letter-spacing: 0.12em;
        color: #64748b;
        font-weight: 700;
        margin-bottom: 1.2rem;
        text-align: center;
    }
    .visual-flow {
        display: flex;
        align-items: center;
        justify-content: space-between;
        position: relative;
    }
    .visual-step {
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 0.5rem;
        z-index: 2;
    }
    .step-circle {
        width: 42px;
        height: 42px;
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 700;
        font-size: 0.8rem;
        color: #ffffff;
        background: #1e293b;
        border: 1px solid rgba(255, 255, 255, 0.15);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.4);
    }
    .step-label {
        font-size: 0.75rem;
        font-weight: 600;
        color: #cbd5e1;
    }
    .flow-connector-line {
        flex: 1;
        height: 2px;
        background: linear-gradient(90deg, rgba(99, 102, 241, 0.4), rgba(168, 85, 247, 0.4));
        margin: 0 8px;
        margin-bottom: 1.4rem;
        z-index: 1;
    }

    /* Compact Available Nodes Styling */
    .node-lib-item-compact {
        display: flex;
        align-items: center;
        gap: 0.55rem;
        padding: 0.22rem 0;
    }
    .node-lib-icon-compact {
        width: 26px;
        height: 26px;
        border-radius: 6px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 0.68rem;
        font-weight: 800;
        letter-spacing: 0.04em;
        flex-shrink: 0;
    }
    .node-lib-meta-compact {
        overflow: hidden;
        line-height: 1.25;
    }
    .node-lib-name-compact {
        font-size: 0.82rem;
        font-weight: 700;
        color: #f1f5f9;
        white-space: nowrap;
    }
    .node-lib-tag-compact {
        font-size: 0.68rem;
        color: #94a3b8;
        white-space: nowrap;
    }

    /* Compact Canvas Grid Cards (3 per row) */
    .compact-canvas-card {
        background: rgba(11, 19, 38, 0.75);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 12px;
        padding: 0.7rem 0.85rem;
        margin-bottom: 0.35rem;
        min-height: 58px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.25);
        transition: border-color 0.2s ease, transform 0.15s ease;
    }
    .compact-canvas-card:hover {
        border-color: rgba(129, 140, 248, 0.45);
    }
    .compact-card-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
    }
    .compact-node-icon {
        width: 26px;
        height: 26px;
        border-radius: 6px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 0.68rem;
        font-weight: 800;
        flex-shrink: 0;
    }
    .compact-node-title {
        font-size: 0.85rem;
        font-weight: 700;
        color: #ffffff;
        line-height: 1.2;
    }
    .compact-node-tagline {
        font-size: 0.68rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.04em;
        line-height: 1.2;
    }
    .compact-step-pill {
        font-size: 0.68rem;
        font-weight: 800;
        color: #64748b;
        background: rgba(255, 255, 255, 0.05);
        padding: 0.15rem 0.4rem;
        border-radius: 5px;
    }

    /* Low-Profile API Settings Bar */
    .api-settings-panel {
        margin-top: -0.2rem;
        margin-bottom: 1.2rem;
    }

    /* Execution Result Cards */
    .result-node-card {
        background: rgba(11, 19, 38, 0.7);
        border: 1px solid rgba(255, 255, 255, 0.07);
        border-radius: 14px;
        padding: 1.1rem 1.4rem;
        margin-bottom: 0.85rem;
    }
    .result-node-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 0.5rem;
    }
    .result-status-title {
        font-size: 0.92rem;
        font-weight: 700;
        color: #f8fafc;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    .result-time-pill {
        font-size: 0.72rem;
        font-weight: 600;
        color: #94a3b8;
        padding: 0.2rem 0.55rem;
        border-radius: 6px;
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.08);
    }

    /* Large Deliverable Box */
    .deliverable-box {
        background: rgba(7, 12, 23, 0.75);
        border: 1px solid rgba(99, 102, 241, 0.25);
        border-radius: 16px;
        padding: 1.8rem;
        color: #f1f5f9;
        font-size: 0.95rem;
        line-height: 1.65;
        white-space: pre-wrap;
        box-shadow: 0 10px 30px -10px rgba(0, 0, 0, 0.6);
    }

    /* Final CTA Card */
    .cta-card {
        background: linear-gradient(135deg, rgba(30, 27, 75, 0.75) 0%, rgba(17, 24, 39, 0.85) 100%);
        border: 1px solid rgba(99, 102, 241, 0.3);
        border-radius: 20px;
        padding: 2.2rem;
        text-align: center;
        margin-top: 1rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 16px 36px -12px rgba(99, 102, 241, 0.2);
    }
    .cta-card h3 {
        font-size: 1.6rem;
        font-weight: 800;
        margin: 0 0 0.4rem 0;
        color: #ffffff;
    }
    .cta-card p {
        font-size: 0.95rem;
        color: #94a3b8;
        margin: 0 0 1.2rem 0;
    }

    /* Override Streamlit Widget Styles for Premium Look */
    .stTextArea textarea {
        background: rgba(8, 14, 28, 0.75) !important;
        border: 1px solid rgba(255, 255, 255, 0.12) !important;
        border-radius: 12px !important;
        color: #f8fafc !important;
        font-size: 0.93rem !important;
        padding: 0.85rem 1rem !important;
    }
    .stTextArea textarea:focus {
        border-color: #818cf8 !important;
        box-shadow: 0 0 0 1px #818cf8 !important;
    }

    .stTextInput input {
        background: rgba(8, 14, 28, 0.75) !important;
        border: 1px solid rgba(255, 255, 255, 0.12) !important;
        border-radius: 12px !important;
        color: #f8fafc !important;
        font-size: 0.9rem !important;
        padding: 0.6rem 0.9rem !important;
    }
    .stTextInput input:focus {
        border-color: #818cf8 !important;
        box-shadow: 0 0 0 1px #818cf8 !important;
    }

    .stSelectbox div[data-baseweb="select"] > div {
        background: rgba(8, 14, 28, 0.75) !important;
        border: 1px solid rgba(255, 255, 255, 0.12) !important;
        border-radius: 12px !important;
        color: #f8fafc !important;
    }

    /* Streamlit Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0.5rem;
        background: transparent;
        border-bottom: 1px solid rgba(255, 255, 255, 0.08);
        padding-bottom: 0.3rem;
    }
    .stTabs [data-baseweb="tab"] {
        background: transparent !important;
        border: none !important;
        color: #94a3b8 !important;
        font-weight: 600 !important;
        font-size: 0.9rem !important;
        padding: 0.5rem 1.1rem !important;
        border-radius: 8px !important;
    }
    .stTabs [aria-selected="true"] {
        background: rgba(99, 102, 241, 0.15) !important;
        color: #ffffff !important;
    }

    /* Expanders */
    .streamlit-expanderHeader {
        background: rgba(15, 23, 42, 0.6) !important;
        border: 1px solid rgba(255, 255, 255, 0.06) !important;
        border-radius: 10px !important;
        color: #cbd5e1 !important;
        font-weight: 600 !important;
    }
    .streamlit-expanderContent {
        background: rgba(8, 14, 28, 0.4) !important;
        border-left: 1px solid rgba(255, 255, 255, 0.06) !important;
        border-right: 1px solid rgba(255, 255, 255, 0.06) !important;
        border-bottom: 1px solid rgba(255, 255, 255, 0.06) !important;
        border-radius: 0 0 10px 10px !important;
    }

    /* Primary Gradient Button Styling */
    div.stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 50%, #9333ea 100%) !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 0.7rem 1.6rem !important;
        font-weight: 700 !important;
        font-size: 0.95rem !important;
        letter-spacing: 0.01em !important;
        box-shadow: 0 6px 20px -4px rgba(124, 58, 237, 0.5) !important;
        transition: all 0.2s ease !important;
    }
    div.stButton > button[kind="primary"]:hover {
        transform: translateY(-1px) !important;
        box-shadow: 0 8px 24px -3px rgba(124, 58, 237, 0.65) !important;
    }

    /* Secondary Action Button Styling */
    div.stButton > button[kind="secondary"] {
        background: rgba(255, 255, 255, 0.04) !important;
        border: 1px solid rgba(255, 255, 255, 0.12) !important;
        color: #cbd5e1 !important;
        border-radius: 10px !important;
        font-weight: 600 !important;
        font-size: 0.84rem !important;
        transition: all 0.2s ease !important;
    }
    div.stButton > button[kind="secondary"]:hover {
        background: rgba(255, 255, 255, 0.08) !important;
        border-color: rgba(255, 255, 255, 0.22) !important;
        color: #ffffff !important;
    }
</style>
""",
    unsafe_allow_html=True,
)

# -----------------------------------------------------------------------------
# Session State Initialization
# -----------------------------------------------------------------------------
if "workflow" not in st.session_state:
    st.session_state.workflow = DEFAULT_WORKFLOW.copy()

if "last_result" not in st.session_state:
    st.session_state.last_result = None

if "brief" not in st.session_state:
    st.session_state.brief = "Write a comprehensive analysis explaining why composable multi-agent AI workflows outperform single prompt-and-chat approaches for content operations."

if "audience" not in st.session_state:
    st.session_state.audience = "Tech Leaders, Founders, and Engineering Managers"

if "tone" not in st.session_state:
    st.session_state.tone = "Engaging & Bold"

if "custom_api_key" not in st.session_state:
    st.session_state.custom_api_key = ""

if "selected_template_name" not in st.session_state:
    st.session_state.selected_template_name = "LinkedIn Post"

# -----------------------------------------------------------------------------
# Active API & Mode Detection
# -----------------------------------------------------------------------------
active_key = get_api_key(st.session_state.custom_api_key)
is_live = bool(active_key)

# -----------------------------------------------------------------------------
# 1. TOP NAVIGATION / HEADER
# -----------------------------------------------------------------------------
status_pill_html = (
    '<span class="status-badge status-badge-live"><span class="status-dot dot-green"></span> Live Gemini Active</span>'
    if is_live
    else '<span class="status-badge status-badge-demo"><span class="status-dot dot-cyan"></span> Demo Mode Active</span>'
)

st.markdown(
    f"""
    <div class="top-nav">
        <div>
            <div class="nav-brand-title">AI Content <span class="gradient-text">Workflow Studio</span></div>
            <div class="nav-brand-sub">Design • Execute • Refine • Create with AI Agents</div>
        </div>
        <div class="nav-status-group">
            {status_pill_html}
            <a href="https://github.com" target="_blank" class="nav-link-btn">
                GitHub Repository
            </a>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# Compact Optional API Key & Model Settings (Accordion)
with st.expander("API Configuration & Model Settings", expanded=False):
    c_k1, c_k2 = st.columns([1.5, 1])
    with c_k1:
        user_key_input = st.text_input(
            "Gemini API Key (Optional)",
            value=st.session_state.custom_api_key,
            type="password",
            placeholder="Enter API key or leave blank for free Demo Mode",
            help="Your key is held in memory for this session and never saved to disk or repository.",
        )
        if user_key_input != st.session_state.custom_api_key:
            st.session_state.custom_api_key = user_key_input
            st.rerun()
    with c_k2:
        model_choice = st.selectbox(
            "Target Model",
            ["gemini-2.5-flash", "gemini-1.5-flash", "gemini-1.5-pro"],
            index=0,
            help="Model invoked when API key is active.",
        )

# -----------------------------------------------------------------------------
# 2. HERO SECTION
# -----------------------------------------------------------------------------
st.markdown(
    """
    <div class="hero-card">
        <div>
            <div class="eyebrow">FROM IDEA TO IMPACT</div>
            <div class="hero-headline">Create Better Content<br><span class="gradient-text">with AI Workflows</span></div>
            <div class="hero-copy">
                Combine multiple AI agents in a single workflow to research, generate, critique and refine your content.
            </div>
            <div class="hero-pills">
                <span class="hero-pill">Modular AI Agents</span>
                <span class="hero-pill">Custom Workflows</span>
                <span class="hero-pill">Multiple Templates</span>
                <span class="hero-pill">Export & Share</span>
            </div>
        </div>
        <div>
            <div class="flow-rail-box">
                <div class="rail-title">AGENTIC WORKFLOW PIPELINE</div>
                <div class="visual-flow">
                    <div class="visual-step">
                        <div class="step-circle" style="border-color:#38bdf8;">IDE</div>
                        <span class="step-label">Ideate</span>
                    </div>
                    <div class="flow-connector-line"></div>
                    <div class="visual-step">
                        <div class="step-circle" style="border-color:#a78bfa;">GEN</div>
                        <span class="step-label">Generate</span>
                    </div>
                    <div class="flow-connector-line"></div>
                    <div class="visual-step">
                        <div class="step-circle" style="border-color:#fb923c;">REF</div>
                        <span class="step-label">Refine</span>
                    </div>
                    <div class="flow-connector-line"></div>
                    <div class="visual-step">
                        <div class="step-circle" style="border-color:#22d3ee;">PUB</div>
                        <span class="step-label">Publish</span>
                    </div>
                </div>
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# -----------------------------------------------------------------------------
# 3. SECTION 1: DEFINE YOUR CONTENT
# -----------------------------------------------------------------------------
st.markdown(
    """
    <div class="saas-card">
        <div class="saas-card-header">
            <h2>1. Define Your Content</h2>
            <p>Tell us what you want to create and set your preferences.</p>
        </div>
    """,
    unsafe_allow_html=True,
)

c_brief_left, c_brief_right = st.columns([1.55, 1.0], gap="large")

with c_brief_left:
    st.markdown("**What do you want to create?**")
    user_brief = st.text_area(
        label="Content Brief",
        value=st.session_state.brief,
        height=180,
        placeholder="e.g. Write a LinkedIn post about the future of AI in education...",
        label_visibility="collapsed",
    )
    if user_brief != st.session_state.brief:
        st.session_state.brief = user_brief

with c_brief_right:
    # Template Selector
    tmpl_keys = list(TEMPLATES.keys())
    tmpl_idx = tmpl_keys.index(st.session_state.selected_template_name) if st.session_state.selected_template_name in tmpl_keys else 0
    selected_tmpl = st.selectbox(
        "Workflow Template",
        tmpl_keys,
        index=tmpl_idx,
        help="Quickly pre-fill verified pipeline steps and parameters.",
    )
    if selected_tmpl != st.session_state.selected_template_name:
        st.session_state.selected_template_name = selected_tmpl
        tmpl_data = TEMPLATES[selected_tmpl]
        st.session_state.workflow = tmpl_data["nodes"].copy()
        st.session_state.brief = tmpl_data["sample_brief"]
        st.session_state.audience = tmpl_data["sample_audience"]
        st.session_state.tone = tmpl_data["sample_tone"]
        st.session_state.last_result = None
        st.rerun()

    # Target Audience
    aud_input = st.text_input(
        "Target Audience",
        value=st.session_state.audience,
        placeholder="e.g. Early-stage Founders, Software Engineers",
    )
    if aud_input != st.session_state.audience:
        st.session_state.audience = aud_input

    # Tone & Voice
    tone_options = ["Engaging & Bold", "Professional", "Educational", "Concise & Direct", "Empathetic"]
    tone_idx = tone_options.index(st.session_state.tone) if st.session_state.tone in tone_options else 0
    tone_input = st.selectbox("Tone & Voice", tone_options, index=tone_idx)
    if tone_input != st.session_state.tone:
        st.session_state.tone = tone_input

    st.markdown("<div style='margin-top: 0.9rem;'></div>", unsafe_allow_html=True)
    run_btn = st.button("Generate / Run Workflow", type="primary", use_container_width=True)

st.markdown("</div>", unsafe_allow_html=True)  # Close Section 1 Card

# Handle Execution Trigger
if run_btn:
    if not st.session_state.brief.strip():
        st.error("Please enter a content brief before executing.")
    elif not st.session_state.workflow:
        st.error("Your workflow canvas is empty. Please add at least one node in Section 2.")
    else:
        with st.spinner("Executing agentic workflow sequence..."):
            exec_result = run_workflow(
                workflow=st.session_state.workflow,
                brief=st.session_state.brief,
                audience=st.session_state.audience,
                tone=st.session_state.tone,
                api_key=st.session_state.custom_api_key,
                model_name=model_choice if 'model_choice' in locals() else "gemini-2.5-flash",
            )
            st.session_state.last_result = exec_result
            st.rerun()

# -----------------------------------------------------------------------------
# Node UI Styling Maps & Safe Resolvers
# -----------------------------------------------------------------------------
NODE_UI_ACCENTS = {
    "input": "#38bdf8",
    "analyze": "#c084fc",
    "outline": "#f472b6",
    "generate": "#a78bfa",
    "critique": "#fb923c",
    "rewrite": "#34d399",
    "output": "#22d3ee",
}

NODE_UI_TAGLINES = {
    "input": "Content Brief",
    "analyze": "Key Insights",
    "outline": "Structure & Flow",
    "generate": "Initial Draft",
    "critique": "Review & Feedback",
    "rewrite": "Improved Version",
    "output": "Final Content",
}

DEFAULT_NODE_ACCENT = "#818cf8"
DEFAULT_NODE_TAGLINE = "Workflow Step"


def get_node_accent(node_key: str, node_info=None) -> str:
    """Safely resolve node accent color without assuming key exists."""
    if node_info and isinstance(node_info, dict) and node_info.get("accent"):
        return str(node_info["accent"])
    return NODE_UI_ACCENTS.get(node_key, DEFAULT_NODE_ACCENT)


def get_node_tagline(node_key: str, node_info=None) -> str:
    """Safely resolve node role tagline without assuming key exists."""
    if node_info and isinstance(node_info, dict) and node_info.get("tagline"):
        return str(node_info["tagline"])
    return NODE_UI_TAGLINES.get(node_key, DEFAULT_NODE_TAGLINE)


# -----------------------------------------------------------------------------
# 4. SECTION 2: BUILD YOUR WORKFLOW
# -----------------------------------------------------------------------------
st.markdown(
    """
    <div class="saas-card">
        <div class="saas-card-header">
            <h2>2. Build Your Workflow</h2>
            <p>Add and arrange nodes to create your content workflow.</p>
        </div>
    """,
    unsafe_allow_html=True,
)

c_lib_col, c_canvas_col = st.columns([1.0, 2.3], gap="large")

# Left Column: Available Nodes Panel (Compact)
with c_lib_col:
    st.markdown("##### Available Nodes")
    st.caption("Click + Add to insert into canvas:")

    for key, info in NODE_LIBRARY.items():
        node_accent = get_node_accent(key, info)
        node_tagline = get_node_tagline(key, info)
        node_label = info.get("label", key.capitalize()) if isinstance(info, dict) else key.capitalize()
        node_icon = (info.get("icon") or key[:2].upper()) if isinstance(info, dict) else key[:2].upper()

        with st.container():
            n_row_info, n_row_btn = st.columns([3.4, 1.2])
            with n_row_info:
                st.markdown(
                    f"""
                    <div class="node-lib-item-compact">
                        <div class="node-lib-icon-compact" style="background:{node_accent}18; border:1px solid {node_accent}45; color:{node_accent};">
                            {node_icon}
                        </div>
                        <div class="node-lib-meta-compact">
                            <div class="node-lib-name-compact">{node_label}</div>
                            <div class="node-lib-tag-compact">{node_tagline}</div>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
            with n_row_btn:
                st.markdown("<div style='margin-top: 3px;'></div>", unsafe_allow_html=True)
                if st.button("+ Add", key=f"add_node_btn_{key}", use_container_width=True):
                    st.session_state.workflow.append(key)
                    st.session_state.selected_template_name = "Custom Workflow"
                    st.rerun()

# Right Column: Workflow Canvas (Compact 3-Column Grid)
with c_canvas_col:
    st.markdown("##### Your Workflow Canvas")
    st.caption(f"Sequential Execution Chain ({len(st.session_state.workflow)} nodes configured):")

    if not st.session_state.workflow:
        st.markdown(
            """
            <div style="border: 2px dashed rgba(255,255,255,0.1); border-radius:14px; padding:3rem; text-align:center; color:#64748b;">
                Canvas is empty. Add nodes from the Available Nodes panel on the left.
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        # Render workflow nodes in compact grid of 3 columns per row
        cols_per_row = 3
        workflow_list = st.session_state.workflow
        total_nodes = len(workflow_list)

        for row_start in range(0, total_nodes, cols_per_row):
            row_items = workflow_list[row_start : row_start + cols_per_row]
            row_cols = st.columns(cols_per_row)
            
            for col_idx, key in enumerate(row_items):
                idx = row_start + col_idx
                info = NODE_LIBRARY.get(key, {})
                node_accent = get_node_accent(key, info)
                node_tagline = get_node_tagline(key, info)
                node_label = info.get("label", key.capitalize()) if isinstance(info, dict) else key.capitalize()
                node_icon = (info.get("icon") or key[:2].upper()) if isinstance(info, dict) else key[:2].upper()
                
                with row_cols[col_idx]:
                    # Compact Canvas Card
                    st.markdown(
                        f"""
                        <div class="compact-canvas-card" style="border-top: 3px solid {node_accent};">
                            <div class="compact-card-header">
                                <div style="display:flex; align-items:center; gap:0.45rem;">
                                    <div class="compact-node-icon" style="background:{node_accent}20; border:1px solid {node_accent}60; color:{node_accent};">
                                        {node_icon}
                                    </div>
                                    <div>
                                        <div class="compact-node-title">{node_label}</div>
                                        <div class="compact-node-tagline" style="color:{node_accent};">{node_tagline}</div>
                                    </div>
                                </div>
                                <div class="compact-step-pill">#{idx+1}</div>
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
                    # Mini-toolbar for Reorder & Remove
                    t_up, t_down, t_del = st.columns(3)
                    with t_up:
                        if st.button("▲", key=f"up_{idx}", help="Move left/up", disabled=(idx == 0), use_container_width=True):
                            st.session_state.workflow[idx - 1], st.session_state.workflow[idx] = (
                                st.session_state.workflow[idx],
                                st.session_state.workflow[idx - 1],
                            )
                            st.session_state.selected_template_name = "Custom Workflow"
                            st.rerun()
                    with t_down:
                        if st.button("▼", key=f"down_{idx}", help="Move right/down", disabled=(idx == total_nodes - 1), use_container_width=True):
                            st.session_state.workflow[idx + 1], st.session_state.workflow[idx] = (
                                st.session_state.workflow[idx],
                                st.session_state.workflow[idx + 1],
                            )
                            st.session_state.selected_template_name = "Custom Workflow"
                            st.rerun()
                    with t_del:
                        if st.button("✕", key=f"rem_{idx}", help="Remove step", use_container_width=True):
                            st.session_state.workflow.pop(idx)
                            st.session_state.selected_template_name = "Custom Workflow"
                            st.rerun()
                    st.markdown("<div style='margin-bottom: 0.5rem;'></div>", unsafe_allow_html=True)

    # Canvas Bottom Controls
    st.markdown("<div style='margin-top: 1rem;'></div>", unsafe_allow_html=True)
    st.divider()
    c_btn1, c_btn2, c_metric = st.columns([1, 1, 2])
    with c_btn1:
        if st.button("Reset Default", use_container_width=True):
            st.session_state.workflow = DEFAULT_WORKFLOW.copy()
            st.session_state.selected_template_name = "Default Pipeline"
            st.session_state.last_result = None
            st.rerun()
    with c_btn2:
        if st.button("Clear Workflow", use_container_width=True):
            st.session_state.workflow = []
            st.session_state.selected_template_name = "Empty Canvas"
            st.session_state.last_result = None
            st.rerun()
    with c_metric:
        st.markdown(
            f"""
            <div style="text-align:right; font-size:0.85rem; color:#94a3b8; padding-top:0.4rem;">
                Configured: <b>{len(st.session_state.workflow)}</b> steps &nbsp;|&nbsp;
                Estimated Time: <b>~{max(1, len(st.session_state.workflow) * 2)}s</b>
            </div>
            """,
            unsafe_allow_html=True,
        )

st.markdown("</div>", unsafe_allow_html=True)  # Close Section 2 Card

# -----------------------------------------------------------------------------
# 5. SECTION 3: EXECUTION & RESULTS
# -----------------------------------------------------------------------------
st.markdown(
    """
    <div class="saas-card">
        <div class="saas-card-header">
            <h2>3. Execution & Results</h2>
            <p>Run your workflow and view the output from each step.</p>
        </div>
    """,
    unsafe_allow_html=True,
)

res = st.session_state.last_result

if not res:
    st.markdown(
        """
        <div style="border: 1px dashed rgba(255,255,255,0.1); border-radius:14px; padding:3.5rem 2rem; text-align:center; color:#64748b;">
            <div style="font-size:1.1rem; font-weight:700; color:#cbd5e1; margin-bottom:0.4rem;">No Execution Recorded</div>
            <div>Define your content above and click <b>Generate / Run Workflow</b> to trigger the pipeline and inspect results.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
else:
    # Execution Status Summary Banner
    st.markdown(
        f"""
        <div style="display:flex; justify-content:space-between; align-items:center; background:rgba(15,23,42,0.8); border:1px solid rgba(255,255,255,0.08); border-radius:12px; padding:0.9rem 1.4rem; margin-bottom:1.5rem; flex-wrap:wrap; gap:0.5rem;">
            <div>
                <span style="font-size:0.75rem; color:#64748b; text-transform:uppercase; font-weight:700;">Status</span>
                <div style="font-size:0.95rem; font-weight:700; color:#f8fafc;">Completed ({res['step_count']} nodes executed in {res['total_duration']}s)</div>
            </div>
            <div style="font-size:0.85rem; color:#818cf8; font-weight:600;">
                Mode: {res['mode']}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Segmented Tabs for Steps and Deliverable
    tab_steps, tab_final = st.tabs(["Workflow Steps", "Final Output"])

    with tab_steps:
        st.markdown("<div style='margin-top:0.8rem;'></div>", unsafe_allow_html=True)
        for step in res["steps"]:
            step_key = step.get("node_key", "")
            accent_color = step.get("accent") or get_node_accent(step_key)
            step_tagline = step.get("tagline") or get_node_tagline(step_key)
            step_label = step.get("label", step_key.capitalize())
            step_duration = step.get("duration", 0.0)
            step_index = step.get("index", 1)
            step_source = step.get("source_mode", "demo")
            status_dot = "dot-green" if step_source == "gemini" else "dot-cyan"
            
            with st.expander(f"✓ {step_label} — {step_tagline} ({step_duration}s)", expanded=(step_index == len(res["steps"]))):
                st.markdown(
                    f"""
                    <div style="display:flex; align-items:center; justify-content:space-between; font-size:0.75rem; color:#94a3b8; margin-bottom:0.8rem; border-bottom:1px solid rgba(255,255,255,0.05); padding-bottom:0.4rem;">
                        <span>Stage #{step_index}: {step_label}</span>
                        <span>Source: <span class="status-dot {status_dot}"></span> {step_source.upper()}</span>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
                st.markdown(step.get("output", ""))

    with tab_final:
        st.markdown("<div style='margin-top:0.8rem;'></div>", unsafe_allow_html=True)
        st.markdown(
            f"""
            <div class="deliverable-box">
{res['final']}
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown("<div style='margin-top:1.2rem;'></div>", unsafe_allow_html=True)
        c_exp1, c_exp2 = st.columns(2)

        txt_payload = (
            f"AI CONTENT WORKFLOW STUDIO - DELIVERABLE\n"
            f"Execution Mode: {res['mode']}\n"
            f"Audience: {st.session_state.audience}\n"
            f"Tone: {st.session_state.tone}\n\n"
            f"--- DELIVERABLE CONTENT ---\n\n"
            f"{res['final']}\n"
        )
        with c_exp1:
            st.download_button(
                "Export as Plain Text (.TXT)",
                data=txt_payload,
                file_name="workflow_content.txt",
                mime="text/plain",
                use_container_width=True,
            )

        md_payload = (
            f"# AI Content Workflow Studio Deliverable\n\n"
            f"- **Execution Mode:** {res['mode']}\n"
            f"- **Total Runtime:** {res['total_duration']}s\n"
            f"- **Target Audience:** {st.session_state.audience}\n"
            f"- **Tone:** {st.session_state.tone}\n\n"
            f"## Final Content\n\n{res['final']}\n\n"
            f"---\n\n## Audit Trail\n\n"
        )
        for s in res["steps"]:
            md_payload += f"### Stage {s['index']}: {s['label']} ({s['duration']}s)\n\n{s['output']}\n\n"

        with c_exp2:
            st.download_button(
                "Export as Markdown (.MD)",
                data=md_payload,
                file_name="workflow_content.md",
                mime="text/markdown",
                use_container_width=True,
            )

st.markdown("</div>", unsafe_allow_html=True)  # Close Section 3 Card

# -----------------------------------------------------------------------------
# 6. FINAL BOTTOM CTA
# -----------------------------------------------------------------------------
st.markdown(
    """
    <div class="cta-card">
        <h3>Ready to create something amazing?</h3>
        <p>Use a template or build your own workflow. It's that simple.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

c_cta_space1, c_cta_btn, c_cta_space2 = st.columns([1.5, 1.2, 1.5])
with c_cta_btn:
    if st.button("Start Creating", type="primary", use_container_width=True):
        st.session_state.workflow = DEFAULT_WORKFLOW.copy()
        st.toast("Ready! Configure your brief above and click Generate.", icon=None)
        st.rerun()
