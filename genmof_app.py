import streamlit as st
from typing import List, Dict

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="GenMOF – AI-Driven MOF Design",
    page_icon="⚗️",
    layout="wide",
)

# -----------------------------
# STYLES
# -----------------------------
st.markdown(
    """
    <style>
    .stApp {
        background: radial-gradient(circle at top, #1f2937 0, #020617 45%, #000 100%);
        color: #e2e8f0;
        font-family: system-ui, -apple-system, BlinkMacSystemFont, "SF Pro Text", "Segoe UI", sans-serif;
    }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    .gen-card {
        background: radial-gradient(circle at top left, rgba(56, 189, 248, 0.16), transparent 55%),
                    radial-gradient(circle at bottom right, rgba(56, 178, 172, 0.18), transparent 55%),
                    linear-gradient(135deg, rgba(15, 23, 42, 0.96), rgba(15, 23, 42, 0.98));
        border-radius: 20px;
        padding: 1.1rem 1.3rem;
        border: 1px solid rgba(148, 163, 184, 0.60);
        box-shadow: 0 18px 50px rgba(15, 23, 42, 0.90);
    }
    .gen-subtle {
        color: #94a3b8;
        font-size: 0.85rem;
    }
    .gen-chip {
        display: inline-flex;
        align-items: center;
        padding: 0.22rem 0.6rem;
        border-radius: 999px;
        border: 1px solid rgba(148, 163, 184, 0.7);
        background: rgba(15, 23, 42, 0.95);
        color: #94a3b8;
        margin: 0.12rem;
        font-size: 0.75rem;
    }
    .gen-chip b { color: #38b2ac; }

    .gen-metric-pill {
        display: inline-flex;
        align-items: center;
        padding: 0.24rem 0.65rem;
        border-radius: 999px;
        border: 1px solid rgba(148, 163, 184, 0.65);
        font-size: 0.75rem;
        background: rgba(15, 23, 42, 0.95);
        color: #94a3b8;
        margin-right: 0.35rem;
        margin-bottom: 0.25rem;
    }
    .gen-metric-pill strong { color: #e5e7eb; }

    .gen-gradient-text {
        background: linear-gradient(135deg, #22d3ee, #a855f7, #eab308);
        -webkit-background-clip: text;
        color: transparent;
    }

    .gen-mof-card {
        border-radius: 14px;
        border: 1px solid rgba(148, 163, 184, 0.70);
        padding: 0.55rem 0.70rem;
        margin-bottom: 0.40rem;
        background: linear-gradient(145deg, rgba(15, 23, 42, 0.96), rgba(15, 23, 42, 0.99));
        position: relative;
        overflow: hidden;
        font-size: 0.80rem;
    }
    .gen-mof-card::before {
        content: "";
        position: absolute;
        inset: 0;
        background: radial-gradient(circle at top left, rgba(56, 189, 248, 0.20), transparent 65%);
        opacity: 0.9;
        pointer-events: none;
    }
    .gen-mof-inner { position: relative; z-index: 1; }

    .gen-mof-title {
        display: flex;
        justify-content: space-between;
        align-items: center;
        gap: 0.40rem;
        font-weight: 600;
        font-size: 0.82rem;
    }
    .gen-mof-meta {
        display: flex;
        flex-wrap: wrap;
        gap: 0.30rem;
        margin-top: 0.25rem;
        font-size: 0.75rem;
    }
    .gen-mof-meta span {
        padding: 0.10rem 0.40rem;
        border-radius: 999px;
        border: 1px solid rgba(148, 163, 184, 0.60);
        background: rgba(15, 23, 42, 0.98);
        color: #94a3b8;
    }
    .gen-mof-meta b { color: #22d3ee; }

    /* Small cards for uploaded articles */
    .gen-article-card {
        border-radius: 12px;
        border: 1px solid rgba(148, 163, 184, 0.55);
        padding: 0.55rem 0.70rem;
        margin-bottom: 0.35rem;
        background: rgba(15, 23, 42, 0.90);
        font-size: 0.80rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# -----------------------------
# DEMO BACKEND (replace with real GenMOF later)
# -----------------------------
def generate_demo_candidates(
    prompt: str,
    metal: str,
    topology: str,
    pore_size: float,
    n: int = 3,
) -> List[Dict]:
    """Mock generator – replace with real GenMOF model later."""
    if not metal or metal == "Auto":
        metals = ["Zn", "Cu", "Zr"]
    else:
        metals = [metal] * 3

    topo = topology if topology != "Auto" else "pcu"
    base = float(pore_size) if pore_size else 12.0

    taglines = [
        "Adsorption-oriented candidate inspired by classical carboxylate MOFs.",
        "Pillared-layer framework balancing surface area and water tolerance.",
        "High-stability node with tunable functional groups for selectivity.",
    ]
    linkers = ["terephthalate", "bipyridyl + dicarboxylate", "UiO-type dicarboxylate"]

    candidates = []
    for i in range(n):
        candidates.append(
            {
                "name": f"{metals[i % len(metals)]}-GenMOF-{i+1}",
                "metal": metals[i % len(metals)],
                "topology": topo,
                "pore_size": round(base + (i - 1) * 2, 1),
                "linker": linkers[i % len(linkers)],
                "tagline": taglines[i % len(taglines)],
            }
        )
    return candidates

# -----------------------------
# SIDEBAR – project info + ARTICLE UPLOADER
# -----------------------------
with st.sidebar:
    st.markdown("### ⚗️ GenMOF Studio")
    st.markdown(
        """
        <span class="gen-subtle">
        Front-end for your Metal–Organic Framework generative project.
        Use this panel to attach relevant literature to the current session.
        </span>
        """,
        unsafe_allow_html=True,
    )

    uploaded_files = st.file_uploader(
        "📚 Upload related articles (PDF or TXT)",
        type=["pdf", "txt"],
        accept_multiple_files=True,
    )

    if "articles" not in st.session_state:
        st.session_state["articles"] = []

    # Store basic info about uploaded files in session
    if uploaded_files:
        for f in uploaded_files:
            # Avoid duplicates by name and size
            info = (f.name, f.size)
            if info not in [(a["name"], a["size"]) for a in st.session_state["articles"]]:
                st.session_state["articles"].append(
                    {"name": f.name, "size": f.size, "type": f.type}
                )

    st.markdown("---")
    st.caption(
        "Tip: later you can parse these PDFs in Python (PyPDF2, pdfplumber, etc.) "
        "to extract abstracts or key properties for GenMOF prompts."
    )

# -----------------------------
# MAIN LAYOUT
# -----------------------------
left, right = st.columns([1.3, 1.0])

with left:
    st.markdown(
        """
        <div class="gen-card">
          <span style="font-size:0.78rem; opacity:0.8;">GenMOF · AI-assisted MOF design</span>
          <h1 style="margin:0.5rem 0 0.4rem 0;">
            Turn <span class="gen-gradient-text">chemical intuition</span><br/>
            into candidate MOFs in seconds.
          </h1>
          <p class="gen-subtle" style="max-width:38rem;">
            Describe your target application (CO₂ capture, H₂ storage, drug delivery),
            choose an optional metal center and topology hint, and let
            <b>GenMOF</b> suggest chemically plausible frameworks and descriptors
            that you can export back to your notebook.
          </p>
          <div style="margin-top:0.6rem;">
            <span class="gen-metric-pill"><strong>10,000+</strong> training MOFs</span>
            <span class="gen-metric-pill"><strong>Topology-aware</strong> prompting</span>
            <span class="gen-metric-pill"><strong>LLM-guided</strong> naming</span>
          </div>
          <div style="margin-top:0.6rem;">
            <span class="gen-chip">Metal centers: <b>Zn, Cu, Zr, Co, Ni</b></span>
            <span class="gen-chip">Topologies: <b>pcu, fcu, sql, dia...</b></span>
            <span class="gen-chip">Export: <b>.csv / .json</b> from Python</span>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # 📚 show uploaded articles summary under hero
    st.write("#### 📚 Uploaded articles (session)")
    if not st.session_state["articles"]:
        st.caption("No articles uploaded yet. Use the sidebar to add PDFs or text files.")
    else:
        for art in st.session_state["articles"]:
            kb = round(art["size"] / 1024, 1)
            st.markdown(
                f"""
                <div class="gen-article-card">
                  <b>{art['name']}</b><br/>
                  <span class="gen-subtle">Type: {art['type']} · Size: {kb} kB</span>
                </div>
                """,
                unsafe_allow_html=True,
            )

with right:
    st.write("#### 🧪 GenMOF Playground")

    with st.form("genmof_form"):
        prompt = st.text_area(
            "Design brief",
            "CO₂ capture from flue gas at ~40 °C and 1 bar; high CO₂ selectivity over N₂; water-tolerant framework.",
            height=130,
        )

        c1, c2 = st.columns(2)
        with c1:
            metal = st.selectbox(
                "Preferred metal center (optional)",
                ["Auto", "Zn", "Cu", "Zr", "Co", "Ni", "Mixed metal"],
                index=0,
            )
        with c2:
            topology = st.selectbox(
                "Topology hint (optional)",
                ["Auto", "pcu", "fcu", "sql", "dia", "sql-pillared"],
                index=0,
            )

        pore_size = st.slider(
            "Target pore size window (Å)",
            min_value=3.0,
            max_value=30.0,
            value=12.0,
            step=0.5,
        )

        n_candidates = st.slider(
            "Number of candidate MOFs",
            min_value=1,
            max_value=5,
            value=3,
        )

        submitted = st.form_submit_button("Generate candidates ⚗️")

    candidates: List[Dict] = []
    if submitted:
        if not prompt.strip():
            st.warning("Please provide a design brief before generating candidates.")
        else:
            candidates = generate_demo_candidates(
                prompt=prompt,
                metal=metal,
                topology=topology,
                pore_size=pore_size,
                n=n_candidates,
            )

st.write("### Candidate MOFs")

if not candidates:
    st.caption(
        "Submit a design brief to see demo candidates. "
        "Later you can plug in your real GenMOF model instead of `generate_demo_candidates`."
    )
else:
    for c in candidates:
        st.markdown(
            f"""
            <div class="gen-mof-card">
              <div class="gen-mof-inner">
                <div class="gen-mof-title">
                  <span>{c['name']}</span>
                  <span class="gen-chip">Node: <b>{c['metal']}</b></span>
                </div>
                <div class="gen-subtle" style="margin-top:0.25rem;">{c['tagline']}</div>
                <div class="gen-mof-meta">
                  <span>Topology: <b>{c['topology']}</b></span>
                  <span>Pore window: <b>{c['pore_size']}</b> Å</span>
                  <span>Linker: <b>{c['linker']}</b></span>
                </div>
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

st.write("---")
st.caption("GenMOF Streamlit front-end · upload articles, design MOFs, and later connect your real model.")
