import os
import time
from typing import List, Dict, Any, Optional

NODE_LIBRARY: Dict[str, Dict[str, str]] = {
    "input": {
        "label": "Input",
        "icon": "IN",
        "category": "Source",
        "tagline": "Content Brief",
        "accent": "#38bdf8",
        "description": "Accept and structure the user's content brief, audience persona, and tone guidelines.",
    },
    "analyze": {
        "label": "Analyze",
        "icon": "AN",
        "category": "Strategy",
        "tagline": "Key Insights",
        "accent": "#c084fc",
        "description": "Deconstruct requirements, strategic goals, target audience triggers, and core constraints.",
    },
    "outline": {
        "label": "Outline",
        "icon": "OT",
        "category": "Planning",
        "tagline": "Structure & Flow",
        "accent": "#f472b6",
        "description": "Structure the narrative into logical sections, headings, key points, and narrative arcs.",
    },
    "generate": {
        "label": "Generate",
        "icon": "GN",
        "category": "Creation",
        "tagline": "Initial Draft",
        "accent": "#a78bfa",
        "description": "Synthesize a comprehensive first draft following the outline and strategic guidelines.",
    },
    "critique": {
        "label": "Critique",
        "icon": "CR",
        "category": "Evaluation",
        "tagline": "Review & Feedback",
        "accent": "#fb923c",
        "description": "Perform an editorial review assessing clarity, punchiness, tone match, and weak spots.",
    },
    "rewrite": {
        "label": "Rewrite",
        "icon": "RW",
        "category": "Refinement",
        "tagline": "Improved Version",
        "accent": "#34d399",
        "description": "Revise the draft by incorporating actionable critique feedback for maximum impact.",
    },
    "output": {
        "label": "Output",
        "icon": "OP",
        "category": "Delivery",
        "tagline": "Final Content",
        "accent": "#22d3ee",
        "description": "Format and polish the final deliverable into a production-ready asset.",
    },
}

DEFAULT_WORKFLOW: List[str] = ["input", "analyze", "generate", "critique", "rewrite", "output"]

TEMPLATES: Dict[str, Dict[str, Any]] = {
    "LinkedIn Post": {
        "nodes": ["input", "generate", "critique", "rewrite", "output"],
        "description": "Creates an engaging, insight-driven LinkedIn post with strong hook, concise takeaway, and discussion CTA.",
        "sample_brief": "Explain why multi-agent AI workflows outperform single prompt-and-chat approaches for content operations.",
        "sample_audience": "Tech leaders, Product Managers, and AI Builders",
        "sample_tone": "Engaging & Bold",
    },
    "Blog Article": {
        "nodes": ["input", "outline", "generate", "critique", "rewrite", "output"],
        "description": "Builds a long-form, well-structured educational article with clear headings and actionable takeaways.",
        "sample_brief": "A comprehensive beginner-friendly guide to understanding and deploying agentic workflows in modern SaaS.",
        "sample_audience": "Software developers and engineering managers",
        "sample_tone": "Educational",
    },
    "Marketing Copy": {
        "nodes": ["input", "generate", "critique", "rewrite", "output"],
        "description": "Generates high-converting marketing copy with problem agitation, value propositions, and a crisp call-to-action.",
        "sample_brief": "Launch announcement for Workflow Studio: A visual canvas to chain AI steps and eliminate content rework.",
        "sample_audience": "Growth marketers and bootstrapped startup founders",
        "sample_tone": "Engaging & Bold",
    },
    "Resume Improvement": {
        "nodes": ["input", "analyze", "rewrite", "output"],
        "description": "Analyzes raw resume experience bullets and rewrites them into quantifiable, high-impact achievement statements.",
        "sample_brief": "Managed engineering sprint cycles, wrote backend Python APIs, and helped improve onboarding for new hires.",
        "sample_audience": "Technical Recruiters and Hiring Managers at top tech firms",
        "sample_tone": "Professional",
    },
}


def get_api_key(explicit_key: Optional[str] = None) -> Optional[str]:
    """Retrieve Gemini API key from explicit param, Streamlit secrets, or environment."""
    if explicit_key and explicit_key.strip():
        return explicit_key.strip()

    # Try streamlit secrets safely
    try:
        import streamlit as st
        if hasattr(st, "secrets") and "GEMINI_API_KEY" in st.secrets:
            key = st.secrets["GEMINI_API_KEY"]
            if key and str(key).strip():
                return str(key).strip()
    except Exception:
        pass

    env_key = os.getenv("GEMINI_API_KEY")
    if env_key and env_key.strip():
        return env_key.strip()

    return None


def get_gemini_client(api_key: Optional[str] = None):
    """Instantiate a Gemini client if API key is provided and library is available."""
    key = get_api_key(api_key)
    if not key:
        return None, None

    # Modern google-genai library
    try:
        from google import genai
        client = genai.Client(api_key=key)
        return client, "google-genai"
    except Exception:
        pass

    # Legacy google.generativeai fallback
    try:
        import google.generativeai as legacy_genai
        legacy_genai.configure(api_key=key)
        return legacy_genai, "google-generativeai"
    except Exception:
        pass

    return None, None


def _call_gemini(client, client_type: str, prompt: str, model_name: str = "gemini-2.5-flash") -> Optional[str]:
    """Execute Gemini prompt using whichever client is active, with robust error catching."""
    try:
        if client_type == "google-genai":
            response = client.models.generate_content(
                model=model_name,
                contents=prompt,
            )
            if response and hasattr(response, "text") and response.text:
                return response.text.strip()
        elif client_type == "google-generativeai":
            compat_model = model_name
            if "2.5" in compat_model:
                compat_model = "gemini-1.5-flash"
            model = client.GenerativeModel(compat_model)
            response = model.generate_content(prompt)
            if response and hasattr(response, "text") and response.text:
                return response.text.strip()
    except Exception as exc:
        print(f"[WorkflowEngine] Gemini API call error: {exc}")
        return None

    return None


def _generate_contextual_demo(node: str, brief: str, audience: str, tone: str, previous: str) -> str:
    """Generate high-quality, deterministic demo outputs that dynamically adapt to the user's brief, audience, and tone."""
    clean_brief = brief.strip() or "Standard Content Topic"
    short_topic = clean_brief if len(clean_brief) <= 120 else clean_brief[:117] + "..."

    # Detect resume workflow context
    is_resume = any(word in clean_brief.lower() for word in ["resume", "experience", "hire", "managed", "skills", "engineer", "bullet"])

    if node == "input":
        return (
            f"### Content Brief Specification\n"
            f"- **Primary Objective:** {clean_brief}\n"
            f"- **Target Audience:** {audience}\n"
            f"- **Specified Tone:** {tone}\n"
            f"- **Workflow Status:** Initialized with parameters verified."
        )

    if node == "analyze":
        if is_resume:
            return (
                f"### Strategic Experience Analysis\n"
                f"- **Target Reader:** {audience} (Screening for ownership, scale, and tangible metrics)\n"
                f"- **Tone Goal:** {tone} & High Impact\n"
                f"- **Identified Deficiencies:** Passive voice ('helped', 'worked on'), lacking quantitative metrics, missing business outcome.\n"
                f"- **Transformation Goal:** Convert tasks into Google XYZ format ('Accomplished [X] as measured by [Y], by doing [Z]')."
            )
        return (
            f"### Strategic Intent & Audience Analysis\n"
            f"- **Core Topic:** {short_topic}\n"
            f"- **Primary Reader Persona:** {audience}\n"
            f"- **Desired Voice & Tone:** {tone}\n"
            f"- **Audience Hook:** Address the exact pain point of repetitive effort and cognitive overload.\n"
            f"- **Key Constraints:** Avoid generic buzzwords; highlight concrete architectural advantages; keep takeaways actionable."
        )

    if node == "outline":
        return (
            f"### Content Architecture Outline\n"
            f"**Working Title:** Practical Guide: {short_topic}\n\n"
            f"1. **The Hook:** The hidden cost of disjointed prompt-and-chat workflows.\n"
            f"2. **The Paradigm Shift:** Why deterministic pipelines and targeted AI nodes create compound value.\n"
            f"3. **Step-by-Step Anatomy:** Breaking monolithic prompts into Analyze, Generate, Critique, and Rewrite.\n"
            f"4. **Concrete Application:** Real-world productivity uplift for {audience}.\n"
            f"5. **Actionable Takeaway & Next Step:** Building your first reusable workflow pipeline."
        )

    if node == "generate":
        return (
            f"### First Draft (Tone: {tone})\n\n"
            f"Most teams using AI today are stuck in a single-turn prompt trap: paste context, ask a question, get a mediocre draft, and spend 20 minutes manually editing.\n\n"
            f"Here is a smarter paradigm for {audience}: composable AI workflows.\n\n"
            f"Instead of asking one generic model to research, outline, write, and proofread all at once, you chain specialized nodes together:\n"
            f"1. **Analyze:** Extract audience triggers and structural requirements.\n"
            f"2. **Generate:** Produce raw material focused purely on substance.\n"
            f"3. **Critique:** Identify fluff, passive phrasing, and logical leaps.\n"
            f"4. **Rewrite:** Polish with razor-sharp precision.\n\n"
            f"The result? Higher consistency, zero hallucination drift, and hours saved every sprint."
        )

    if node == "critique":
        return (
            f"### Editorial & Quality Critique\n\n"
            f"**Strengths:**\n"
            f"- Strong structural thesis contrasting single prompts against composable workflows.\n"
            f"- Tone resonates well with {audience}.\n\n"
            f"**Opportunities for Improvement:**\n"
            f"- **Opening Hook:** The opening sentence can be more provocative and immediate.\n"
            f"- **Specificity:** Add a concise metric or rule-of-thumb to anchor credibility.\n"
            f"- **Call to Action:** Make the closing invitation more engaging for discussion."
        )

    if node == "rewrite":
        if is_resume:
            return (
                f"### High-Impact Quantified Experience Bullets (Rewritten)\n\n"
                f"- **Spearheaded backend API development in Python**, delivering 12 microservices that reduced latency by 38% and supported 250k+ daily active users.\n"
                f"- **Orchestrated bi-weekly Agile sprint cycles** across a 9-engineer cross-functional team, increasing sprint velocity by 24% while cutting release defects in half.\n"
                f"- **Engineered a structured developer onboarding playbook**, accelerating ramp-up time for new hires from 3 weeks to 6 business days."
            )
        return (
            f"### Polished & Revised Content\n\n"
            f"If your AI strategy is still 'one giant prompt in a chat window,' you're doing 80% of the heavy lifting yourself.\n\n"
            f"Leading teams don't chat with AI - they build composable pipelines.\n\n"
            f"Here is why: monolithic prompts force a single model to strategize, draft, edit, and format simultaneously. Quality degrades at each boundary.\n\n"
            f"When you decompose the job into specialized micro-steps:\n"
            f"- **Analysis** locks in the strategic intent for {audience}.\n"
            f"- **Generation** creates raw substance without editorial inhibition.\n"
            f"- **Critique** stress-tests the draft against clarity and tone standards.\n"
            f"- **Rewrite** sharpens every phrase for maximum reader retention.\n\n"
            f"Stop treating AI like an intern you micromanage in chat. Start building reusable workflows that do the work for you."
        )

    if node == "output":
        if previous and previous.strip():
            return (
                f"===============================================================\n"
                f"         FINAL DELIVERABLE | AI WORKFLOW STUDIO\n"
                f"===============================================================\n\n"
                f"{previous.strip()}\n\n"
                f"---------------------------------------------------------------\n"
                f"Workflow completed successfully | Ready for publication"
            )
        return "Workflow completed. No content was generated in earlier stages."

    return previous or "Step completed."


def _build_node_prompt(node: str, brief: str, audience: str, tone: str, previous: str) -> str:
    """Construct structured, production-grade prompts for each node type."""
    system_framing = (
        f"You are an expert AI Content Workflow engine node named '{NODE_LIBRARY.get(node, {}).get('label', node)}'.\n"
        f"Original Topic/Brief: {brief}\n"
        f"Target Audience: {audience}\n"
        f"Required Tone: {tone}\n"
    )

    if node == "input":
        return (
            f"{system_framing}\n"
            f"Summarize and structure this brief into key constraints, target persona highlights, and expected outputs.\n"
            f"Brief: {brief}"
        )
    elif node == "analyze":
        return (
            f"{system_framing}\n"
            f"Perform an in-depth strategic analysis of this content brief.\n"
            f"Extract: 1) Core Value Proposition, 2) Reader Motivations & Pain Points for '{audience}', "
            f"3) Strategic Angles, 4) Critical Pitfalls to Avoid.\n"
            f"Brief Content:\n{brief}"
        )
    elif node == "outline":
        return (
            f"{system_framing}\n"
            f"Create a high-impact, structured outline for the content piece.\n"
            f"Include section titles, key arguments, and specific illustrative examples for '{audience}'.\n"
            f"Context from previous step:\n{previous or brief}"
        )
    elif node == "generate":
        return (
            f"{system_framing}\n"
            f"Synthesize a full first draft based on the provided brief and outline.\n"
            f"Maintain a {tone} tone. Write with conviction, clear structure, and zero generic fluff.\n"
            f"Context / Outline:\n{previous or brief}"
        )
    elif node == "critique":
        return (
            f"{system_framing}\n"
            f"Critique the following draft rigorously from the perspective of an executive editor and {audience}.\n"
            f"Evaluate: 1) Clarity & Hook Strength, 2) Tone Fidelity ({tone}), 3) Weak or Cliché Phrasing, "
            f"4) 3 Specific Actionable Recommendations for the rewrite.\n"
            f"Draft to critique:\n{previous}"
        )
    elif node == "rewrite":
        return (
            f"{system_framing}\n"
            f"Rewrite the draft by directly applying the critique recommendations above.\n"
            f"Enhance punchiness, eliminate filler words, and ensure tone is unmistakably {tone}.\n"
            f"Previous Draft and Critique:\n{previous}"
        )
    elif node == "output":
        return (
            f"{system_framing}\n"
            f"Format and finalize the content below into a clean, ready-to-publish asset.\n"
            f"Content:\n{previous}"
        )

    return f"{system_framing}\nProcess and enhance the following content:\n{previous}"


def run_workflow(
    workflow: List[str],
    brief: str,
    audience: str,
    tone: str,
    api_key: Optional[str] = None,
    model_name: str = "gemini-2.5-flash",
) -> Dict[str, Any]:
    """Execute the configured node sequence step-by-step with intermediate tracking and fallback support."""
    client, client_type = get_gemini_client(api_key)
    has_api_key = client is not None

    steps = []
    previous = ""
    fallback_count = 0
    total_start_time = time.time()

    for idx, node in enumerate(workflow, start=1):
        step_start_time = time.time()
        node_info = NODE_LIBRARY.get(node, {"label": node.capitalize(), "icon": "ND", "tagline": "Processing", "accent": "#6366f1"})
        output = None
        source_mode = "demo"

        if has_api_key and node != "input":
            prompt = _build_node_prompt(node, brief, audience, tone, previous)
            output = _call_gemini(client, client_type, prompt, model_name)
            if output:
                source_mode = "gemini"
            else:
                fallback_count += 1
                source_mode = "fallback_demo"
                output = _generate_contextual_demo(node, brief, audience, tone, previous)
        else:
            output = _generate_contextual_demo(node, brief, audience, tone, previous)
            source_mode = "demo"

        duration = max(0.01, round(time.time() - step_start_time, 3))
        previous = output

        steps.append({
            "index": idx,
            "node_key": node,
            "label": node_info["label"],
            "icon": node_info["icon"],
            "tagline": node_info.get("tagline", "Processing"),
            "accent": node_info.get("accent", "#6366f1"),
            "output": output,
            "duration": duration,
            "source_mode": source_mode,
        })

    total_duration = max(0.01, round(time.time() - total_start_time, 2))

    # Determine display mode
    if not has_api_key:
        mode_label = "Demo Mode (Deterministic AI Simulation)"
    elif fallback_count > 0:
        mode_label = f"Hybrid Mode (Gemini + {fallback_count} Demo Fallbacks)"
    else:
        mode_label = f"Live Gemini AI ({model_name})"

    return {
        "mode": mode_label,
        "is_live_api": has_api_key and fallback_count == 0,
        "steps": steps,
        "final": previous,
        "total_duration": total_duration,
        "step_count": len(steps),
    }
