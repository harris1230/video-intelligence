import streamlit as st
from video_processor import process_video
import tempfile

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="VisionIQ · Video Intelligence",
    page_icon="🎬",
    layout="wide",
)

# ── Global CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;900&family=JetBrains+Mono:wght@300;400;500&display=swap');

:root {
  --bg:         #07090E;
  --surface:    #0E1118;
  --surface2:   #141720;
  --border:     rgba(255,255,255,0.07);
  --border2:    rgba(255,255,255,0.12);
  --accent:     #F97316;
  --accent2:    #FB923C;
  --blue:       #38BDF8;
  --green:      #34D399;
  --text:       #F0F2F8;
  --muted:      rgba(200,210,230,0.45);
  --mono:       'JetBrains Mono', monospace;
  --sans:       'Outfit', sans-serif;
}

*, *::before, *::after { box-sizing: border-box; }

html, body,
[data-testid="stAppViewContainer"],
[data-testid="stApp"] {
    background: var(--bg) !important;
    color: var(--text) !important;
    font-family: var(--sans) !important;
}

[data-testid="stAppViewContainer"] {
    background:
        radial-gradient(ellipse 90% 45% at 50% -5%, rgba(249,115,22,0.10) 0%, transparent 65%),
        radial-gradient(ellipse 50% 35% at 85% 75%, rgba(56,189,248,0.07) 0%, transparent 60%),
        var(--bg) !important;
}

[data-testid="stHeader"], [data-testid="stToolbar"], footer { display: none !important; }

::-webkit-scrollbar { width: 3px; }
::-webkit-scrollbar-thumb { background: rgba(249,115,22,0.4); border-radius: 2px; }

/* ── Wrapper ── */
.viq-wrap {
    max-width: 1140px;
    margin: 0 auto;
    padding: 2.5rem 1.5rem 4rem;
}

/* ── Wordmark ── */
.wordmark {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    margin-bottom: 2.8rem;
    animation: fadeRight 0.6s ease both;
}
.wordmark-icon {
    width: 36px; height: 36px;
    background: linear-gradient(135deg, var(--accent), #C2410C);
    border-radius: 10px;
    display: flex; align-items: center; justify-content: center;
    font-size: 1rem;
    box-shadow: 0 8px 24px rgba(249,115,22,0.3);
}
.wordmark-text {
    font-family: var(--sans);
    font-weight: 900;
    font-size: 1.15rem;
    letter-spacing: -0.01em;
    color: var(--text);
}
.wordmark-text span { color: var(--accent); }
.wordmark-badge {
    margin-left: auto;
    font-family: var(--mono);
    font-size: 0.62rem;
    letter-spacing: 0.18em;
    color: var(--muted);
    padding: 0.25rem 0.7rem;
    border: 1px solid var(--border2);
    border-radius: 100px;
    text-transform: uppercase;
}

/* ── Upload zone ── */
.upload-zone {
    background: var(--surface);
    border: 1.5px dashed rgba(249,115,22,0.35);
    border-radius: 18px;
    padding: 2rem 1.5rem 1.5rem;
    margin-bottom: 1.5rem;
    transition: border-color 0.3s, background 0.3s;
    animation: fadeUp 0.55s 0.1s ease both;
}
.upload-zone:hover {
    border-color: rgba(249,115,22,0.65);
    background: rgba(249,115,22,0.03);
}
.upload-label {
    font-family: var(--mono);
    font-size: 0.68rem;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: var(--accent);
    margin-bottom: 0.8rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}
.upload-label::before {
    content: '';
    width: 18px; height: 1px;
    background: var(--accent);
    opacity: 0.5;
}

/* ── Video panel ── */
.video-panel {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 16px;
    overflow: hidden;
    box-shadow: 0 20px 50px rgba(0,0,0,0.5);
    margin-bottom: 1.2rem;
}

/* ── Meta pills ── */
.meta-strip {
    display: flex;
    gap: 0.5rem;
    flex-wrap: wrap;
    margin-bottom: 1.5rem;
}
.meta-pill {
    font-family: var(--mono);
    font-size: 0.68rem;
    padding: 0.28rem 0.75rem;
    border-radius: 100px;
    background: var(--surface2);
    border: 1px solid var(--border);
    color: var(--muted);
    letter-spacing: 0.05em;
}
.meta-pill strong { color: var(--text); font-weight: 500; }

/* ── Button ── */
div[data-testid="stButton"] > button {
    width: 100% !important;
    padding: 0.9rem 1.5rem !important;
    background: linear-gradient(135deg, var(--accent) 0%, #C2410C 100%) !important;
    color: #fff !important;
    font-family: var(--sans) !important;
    font-size: 0.9rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.1em !important;
    text-transform: uppercase !important;
    border: none !important;
    border-radius: 12px !important;
    box-shadow: 0 6px 28px rgba(249,115,22,0.35) !important;
    transition: transform 0.2s, box-shadow 0.2s !important;
    margin-bottom: 1.5rem !important;
    cursor: pointer !important;
}
div[data-testid="stButton"] > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 10px 40px rgba(249,115,22,0.5) !important;
}

/* ── Processing bar ── */
.proc-bar {
    display: flex;
    align-items: center;
    gap: 0.9rem;
    padding: 1rem 1.3rem;
    background: rgba(249,115,22,0.07);
    border: 1px solid rgba(249,115,22,0.2);
    border-radius: 12px;
    margin-bottom: 1.2rem;
    font-family: var(--mono);
    font-size: 0.72rem;
    color: var(--accent2);
    letter-spacing: 0.08em;
    animation: blink 1.6s infinite;
}
.spin {
    width: 16px; height: 16px;
    border: 2px solid rgba(249,115,22,0.25);
    border-top-color: var(--accent);
    border-radius: 50%;
    animation: spin 0.7s linear infinite;
    flex-shrink: 0;
}

/* ── Success ── */
.ok-bar {
    display: flex;
    align-items: center;
    gap: 0.8rem;
    padding: 0.9rem 1.3rem;
    background: rgba(52,211,153,0.07);
    border: 1px solid rgba(52,211,153,0.2);
    border-radius: 12px;
    margin-bottom: 1.8rem;
    font-family: var(--mono);
    font-size: 0.72rem;
    color: var(--green);
    letter-spacing: 0.06em;
    animation: fadeUp 0.4s ease both;
}

/* ── Stats row ── */
.stats-row {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 1px;
    background: var(--border);
    border-radius: 14px;
    overflow: hidden;
    margin-bottom: 2rem;
    border: 1px solid var(--border);
    animation: fadeUp 0.45s ease both;
}
.stat-box {
    background: var(--surface);
    padding: 1.1rem 1rem;
    text-align: center;
}
.stat-n {
    font-family: var(--sans);
    font-size: 1.7rem;
    font-weight: 900;
    color: var(--accent);
    line-height: 1;
    display: block;
}
.stat-l {
    font-family: var(--mono);
    font-size: 0.58rem;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: var(--muted);
    display: block;
    margin-top: 0.35rem;
}

/* ── Section label ── */
.section-label {
    font-family: var(--mono);
    font-size: 0.65rem;
    letter-spacing: 0.22em;
    text-transform: uppercase;
    color: var(--accent);
    margin-bottom: 0.8rem;
    display: flex;
    align-items: center;
    gap: 0.6rem;
}
.section-label::after {
    content: '';
    flex: 1;
    height: 1px;
    background: var(--border2);
}

/* ── Summary card ── */
.summary-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-left: 3px solid var(--accent);
    border-radius: 14px;
    padding: 1.5rem 1.6rem;
    margin-bottom: 2rem;
    font-size: 0.88rem;
    line-height: 1.75;
    color: rgba(220,228,245,0.85);
    animation: fadeUp 0.5s ease both;
    position: relative;
    overflow: hidden;
}
.summary-card::before {
    content: '"';
    position: absolute;
    top: 0.4rem;
    right: 1.2rem;
    font-size: 4rem;
    color: rgba(249,115,22,0.06);
    font-family: Georgia, serif;
    line-height: 1;
}

/* ── Frame rows ── */
.frames-grid { display: flex; flex-direction: column; gap: 0.5rem; margin-bottom: 1.5rem; }

.frame-row {
    display: flex;
    align-items: center;
    gap: 1rem;
    padding: 0.85rem 1.1rem;
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 11px;
    transition: background 0.2s, border-color 0.2s, transform 0.15s;
    animation: fadeUp 0.3s ease both;
}
.frame-row:hover {
    background: var(--surface2);
    border-color: rgba(249,115,22,0.22);
    transform: translateX(3px);
}
.f-num {
    font-family: var(--mono);
    font-size: 0.65rem;
    color: var(--muted);
    min-width: 64px;
    flex-shrink: 0;
}
.f-num em {
    display: block;
    font-style: normal;
    font-size: 0.55rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: rgba(200,210,230,0.28);
    margin-bottom: 1px;
}
.f-dot {
    width: 6px; height: 6px;
    border-radius: 50%;
    background: var(--accent);
    opacity: 0.4;
    flex-shrink: 0;
}
.tags { display: flex; flex-wrap: wrap; gap: 0.35rem; flex: 1; }
.tag {
    font-family: var(--mono);
    font-size: 0.68rem;
    padding: 0.18rem 0.6rem;
    border-radius: 6px;
    background: rgba(56,189,248,0.08);
    border: 1px solid rgba(56,189,248,0.18);
    color: #7DD3FC;
    letter-spacing: 0.03em;
}
.tag.primary {
    background: rgba(249,115,22,0.1);
    border-color: rgba(249,115,22,0.22);
    color: var(--accent2);
}
.tag.empty {
    background: transparent;
    border-color: var(--border);
    color: var(--muted);
    font-style: italic;
}
.f-count {
    font-family: var(--mono);
    font-size: 0.6rem;
    color: var(--muted);
    flex-shrink: 0;
}

.more-note {
    text-align: center;
    font-family: var(--mono);
    font-size: 0.65rem;
    color: var(--muted);
    letter-spacing: 0.1em;
    padding: 0.8rem;
    border-top: 1px solid var(--border);
}

/* ── Animations ── */
@keyframes fadeUp    { from { opacity:0; transform:translateY(12px); } to { opacity:1; transform:none; } }
@keyframes fadeRight { from { opacity:0; transform:translateX(-12px); } to { opacity:1; transform:none; } }
@keyframes spin      { to { transform:rotate(360deg); } }
@keyframes blink     { 0%,100% { opacity:1; } 50% { opacity:0.6; } }

/* ── Streamlit overrides ── */
[data-testid="stFileUploaderDropzone"] { background: transparent !important; border: none !important; }
div[data-testid="stFileUploaderDropzoneInstructions"] p,
div[data-testid="stFileUploaderDropzoneInstructions"] span {
    color: var(--muted) !important;
    font-family: var(--mono) !important;
    font-size: 0.75rem !important;
}
div[data-testid="stFileUploaderDropzoneInstructions"] svg { color: var(--accent) !important; }
.stProgress > div > div { background: linear-gradient(90deg, var(--accent), #FDBA74) !important; }
</style>
""", unsafe_allow_html=True)

# ── Layout ────────────────────────────────────────────────────────────────────
st.markdown('<div class="viq-wrap">', unsafe_allow_html=True)

# Wordmark header
st.markdown("""
<div class="wordmark">
  <div class="wordmark-icon">🎬</div>
  <div class="wordmark-text">Vision<span>IQ</span></div>
  <div class="wordmark-badge">Intelligence Engine · v2.0</div>
</div>
""", unsafe_allow_html=True)

# Upload zone
st.markdown('<div class="upload-zone"><div class="upload-label">Input Source</div>', unsafe_allow_html=True)
uploaded_file = st.file_uploader(
    "Drop a video file (MP4 / AVI)",
    type=["mp4", "avi"],
    label_visibility="collapsed",
)
st.markdown('</div>', unsafe_allow_html=True)

if uploaded_file is not None:
    tfile = tempfile.NamedTemporaryFile(delete=False)
    tfile.write(uploaded_file.read())

    col_v, col_s = st.columns([2, 1], gap="large")

    with col_v:
        st.markdown('<div class="video-panel">', unsafe_allow_html=True)
        st.video(uploaded_file)
        st.markdown('</div>', unsafe_allow_html=True)

        size_kb  = round(uploaded_file.size / 1024, 1)
        size_str = f"{round(size_kb/1024,2)} MB" if size_kb > 1024 else f"{size_kb} KB"
        st.markdown(f"""
        <div class="meta-strip">
          <div class="meta-pill">📄 <strong>{uploaded_file.name}</strong></div>
          <div class="meta-pill">💾 <strong>{size_str}</strong></div>
          <div class="meta-pill">🎞 <strong>{uploaded_file.type or 'video'}</strong></div>
        </div>
        """, unsafe_allow_html=True)

    with col_s:
        st.markdown("""
        <div style="padding:1.3rem;background:var(--surface);border:1px solid var(--border);
                    border-radius:14px;margin-bottom:1.2rem;font-size:0.8rem;line-height:2.1;">
          <div style="font-family:'JetBrains Mono',monospace;font-size:0.6rem;letter-spacing:0.2em;
                      text-transform:uppercase;color:var(--accent);margin-bottom:0.8rem;">
            Pipeline Steps
          </div>
          <div style="color:var(--muted);">
            <span style="color:#34D399;">✓</span>&nbsp; Frame extraction<br>
            <span style="color:#34D399;">✓</span>&nbsp; Object detection<br>
            <span style="color:#34D399;">✓</span>&nbsp; Scene classification<br>
            <span style="color:#34D399;">✓</span>&nbsp; Summary generation
          </div>
        </div>
        """, unsafe_allow_html=True)

    analyze = st.button("⚡  Run Intelligence Analysis")

    if analyze:
        st.markdown("""
        <div class="proc-bar">
          <div class="spin"></div>
          ANALYZING — EXTRACTING FRAMES &amp; RUNNING DETECTION…
        </div>
        """, unsafe_allow_html=True)

        prog = st.progress(0)
        for i in range(100):
            prog.progress(i + 1)

        results, summary = process_video(tfile.name)
        prog.empty()

        total_det = sum(len(r.get("objects", [])) for r in results)
        uniq_det  = len({obj for r in results for obj in r.get("objects", [])})
        avg_det   = round(total_det / max(len(results), 1), 1)

        # Success
        st.markdown(f"""
        <div class="ok-bar">
          ✅ &nbsp;Analysis complete — <strong>{len(results)}</strong> frames · <strong>{total_det}</strong> total detections
        </div>
        """, unsafe_allow_html=True)

        # Stats
        st.markdown(f"""
        <div class="stats-row">
          <div class="stat-box"><span class="stat-n">{len(results)}</span><span class="stat-l">Frames</span></div>
          <div class="stat-box"><span class="stat-n">{total_det}</span><span class="stat-l">Detections</span></div>
          <div class="stat-box"><span class="stat-n">{uniq_det}</span><span class="stat-l">Unique Obj</span></div>
          <div class="stat-box"><span class="stat-n">{avg_det}</span><span class="stat-l">Avg/Frame</span></div>
        </div>
        """, unsafe_allow_html=True)

        # ── Summary section ──────────────────────────────────────────────────
        st.markdown('<div class="section-label">Video Summary</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="summary-card">{summary}</div>', unsafe_allow_html=True)

        # ── Frame detections ─────────────────────────────────────────────────
        st.markdown('<div class="section-label">Frame-wise Detection · First 10 Frames</div>', unsafe_allow_html=True)
        st.markdown('<div class="frames-grid">', unsafe_allow_html=True)

        for i, res in enumerate(results[:10]):
            objects   = res.get("objects", [])
            delay     = i * 0.04
            obj_count = f"{len(objects)} obj" if objects else ""

            tags_html = ""
            for j, obj in enumerate(objects):
                cls = "primary" if j == 0 else ""
                tags_html += f'<span class="tag {cls}">{obj}</span>'
            if not tags_html:
                tags_html = '<span class="tag empty">no detections</span>'

            st.markdown(f"""
            <div class="frame-row" style="animation-delay:{delay}s">
              <div class="f-num"><em>frame</em>#{res['frame']:04d}</div>
              <div class="f-dot"></div>
              <div class="tags">{tags_html}</div>
              <div class="f-count">{obj_count}</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)  # frames-grid

        if len(results) > 10:
            st.markdown(f"""
            <div class="more-note">+ {len(results) - 10} additional frames · expand in full export</div>
            """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)  # viq-wrap