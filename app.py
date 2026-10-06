import time
import streamlit as st
from openai import OpenAI

# ============================================================
# CONFIGURATION
# ============================================================

MODEL_NAME = "google/gemma-3-1b"

client = OpenAI(
    base_url="http://localhost:1234/v1",
    api_key="lm-studio",
)

# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="VocabGo — Local Language Assistant",
    page_icon="🌐",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    /* ---------- GLOBAL ---------- */

    .stApp {
        background: #0b1020;
    }

    .main {
        padding-top: 1rem;
    }

    /* ---------- SIDEBAR ---------- */

    [data-testid="stSidebar"] {
        background: #111827;
        border-right: 1px solid #273244;
    }

    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 {
        color: #f8fafc;
    }

    /* ---------- HEADER ---------- */

    .hero {
        padding: 30px 35px;
        border-radius: 20px;
        background: linear-gradient(
            135deg,
            #111827 0%,
            #172554 100%
        );
        border: 1px solid #293548;
        margin-bottom: 25px;
    }

    .hero-title {
        font-size: 42px;
        font-weight: 800;
        color: #f8fafc;
        margin-bottom: 5px;
    }

    .hero-subtitle {
        font-size: 17px;
        color: #94a3b8;
        margin-top: 5px;
    }

    .local-badge {
        display: inline-block;
        padding: 6px 12px;
        border-radius: 20px;
        background: #123524;
        color: #4ade80;
        font-size: 13px;
        font-weight: 600;
        margin-bottom: 15px;
        border: 1px solid #1f6b45;
    }

    /* ---------- CARDS ---------- */

    .feature-card {
        padding: 20px;
        border-radius: 16px;
        background: #111827;
        border: 1px solid #273244;
        min-height: 120px;
    }

    .feature-icon {
        font-size: 25px;
        margin-bottom: 8px;
    }

    .feature-title {
        color: #f8fafc;
        font-size: 17px;
        font-weight: 700;
    }

    .feature-text {
        color: #94a3b8;
        font-size: 13px;
        margin-top: 5px;
    }

    /* ---------- SECTION HEADINGS ---------- */

    .section-title {
        color: #f8fafc;
        font-size: 22px;
        font-weight: 700;
        margin-top: 25px;
        margin-bottom: 12px;
    }

    /* ---------- OUTPUT ---------- */

    .output-box {
        padding: 22px;
        border-radius: 16px;
        background: #111827;
        border: 1px solid #334155;
        margin-top: 15px;
    }

    .output-label {
        color: #60a5fa;
        font-size: 14px;
        font-weight: 700;
        margin-bottom: 10px;
    }

    /* ---------- STATUS ---------- */

    .status-card {
        padding: 14px;
        border-radius: 12px;
        background: #0f172a;
        border: 1px solid #273244;
        margin-top: 10px;
    }

    .status-online {
        color: #4ade80;
        font-weight: 700;
    }

    .status-text {
        color: #94a3b8;
        font-size: 13px;
    }

    /* ---------- FOOTER ---------- */

    .footer {
        text-align: center;
        color: #64748b;
        font-size: 12px;
        margin-top: 40px;
        padding: 20px;
    }

    </style>
    """,
    unsafe_allow_html=True,
)

# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown("## 🌐 VocabGo")

    st.caption("Private • Local • Offline")

    st.divider()

    st.markdown("### ⚙️ System")

    st.markdown(
        """
        <div class="status-card">
            <div class="status-online">● LOCAL AI ONLINE</div>
            <div class="status-text">
                LM Studio
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.write("")

    st.markdown("**Model**")
    st.code(MODEL_NAME)

    st.markdown("**Server**")
    st.code("localhost:1234")

    st.divider()

    st.markdown("### 🔒 Privacy")

    st.info(
        "Your text is processed by the AI model "
        "running locally on your computer."
    )

    st.divider()

    st.markdown("### 🧠 Model")

    st.write("Gemma 3 1B")
    st.caption("Lightweight local language model")

# ============================================================
# HERO
# ============================================================

st.success("🟢 100% LOCAL AI")

st.title("🌐 VocabGo")

st.write(
    "Your private AI language assistant — "
    "running directly on your computer."
)

st.caption(
    "🔒 Powered by Gemma 3 1B • LM Studio"
)

# ============================================================
# FEATURES
# ============================================================

st.markdown(
    '<div class="section-title">What can you do?</div>',
    unsafe_allow_html=True,
)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(
        """
        <div class="feature-card">
            <div class="feature-icon">🌍</div>
            <div class="feature-title">Translate</div>
            <div class="feature-text">
                Translate between English, Hindi and Marathi.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col2:
    st.markdown(
        """
        <div class="feature-card">
            <div class="feature-icon">✍️</div>
            <div class="feature-title">Grammar</div>
            <div class="feature-text">
                Correct grammar, spelling and punctuation.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col3:
    st.markdown(
        """
        <div class="feature-card">
            <div class="feature-icon">✨</div>
            <div class="feature-title">Rewrite</div>
            <div class="feature-text">
                Rewrite your text in different styles.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col4:
    st.markdown(
        """
        <div class="feature-card">
            <div class="feature-icon">💡</div>
            <div class="feature-title">Simplify</div>
            <div class="feature-text">
                Make complex text easier to understand.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# ============================================================
# WORKSPACE
# ============================================================

st.markdown(
    '<div class="section-title">🛠️ Workspace</div>',
    unsafe_allow_html=True,
)

left, right = st.columns([1, 2])

# ------------------------------------------------------------
# SETTINGS
# ------------------------------------------------------------

with left:

    st.markdown("### Choose your task")

    task = st.radio(
        "Task",
        [
            "🌍 Translate",
            "✍️ Correct Grammar",
            "✨ Rewrite",
            "💡 Simplify",
        ],
        label_visibility="collapsed",
    )

    target_language = None
    rewrite_style = None

    if task == "🌍 Translate":

        target_language = st.selectbox(
            "Translate to",
            [
                "English",
                "Hindi",
                "Marathi",
            ],
        )

    elif task == "✨ Rewrite":

        rewrite_style = st.selectbox(
            "Writing style",
            [
                "Professional",
                "Simple",
                "Friendly",
            ],
        )

# ------------------------------------------------------------
# INPUT
# ------------------------------------------------------------

with right:

    st.markdown("### Enter your text")

    user_text = st.text_area(
        "Input",
        height=220,
        placeholder=(
            "Type or paste your text here...\n\n"
            "Example:\n"
            "Artificial intelligence is changing "
            "the way we learn."
        ),
        label_visibility="collapsed",
    )

# ============================================================
# PROMPT FUNCTION
# ============================================================

def create_prompt(
    task,
    text,
    language=None,
    style=None,
):

    if task == "🌍 Translate":

        return (
            f"Translate this text into {language}.\n"
            "Return only the translation.\n\n"
            f"Text:\n{text}"
        )

    if task == "✍️ Correct Grammar":

        return (
            "Correct the grammar, spelling, punctuation "
            "and sentence structure.\n"
            "Preserve the original meaning.\n"
            "Return only the corrected text.\n\n"
            f"Text:\n{text}"
        )

    if task == "✨ Rewrite":

        return (
            f"Rewrite this text in a {style.lower()} style.\n"
            "Preserve the original meaning.\n"
            "Return only the rewritten text.\n\n"
            f"Text:\n{text}"
        )

    if task == "💡 Simplify":

        return (
            "Simplify this text so it is easier "
            "to understand.\n"
            "Preserve the original meaning.\n"
            "Return only the simplified text.\n\n"
            f"Text:\n{text}"
        )

    return text


# ============================================================
# PROCESS BUTTON
# ============================================================

st.write("")

process = st.button(
    "✨  Process with Local AI",
    type="primary",
    use_container_width=True,
)

if process:

    if not user_text.strip():

        st.warning(
            "Please enter some text before processing."
        )

    else:

        prompt = create_prompt(
            task,
            user_text,
            target_language,
            rewrite_style,
        )

        try:

            start_time = time.perf_counter()

            with st.spinner(
                "🧠 Gemma 3 1B is thinking..."
            ):

                response = client.chat.completions.create(
                    model=MODEL_NAME,
                    messages=[
                        {
                            "role": "system",
                            "content": (
                                "You are a precise language "
                                "assistant. Follow the user's "
                                "requested task exactly. "
                                "Do not add unnecessary "
                                "explanations."
                            ),
                        },
                        {
                            "role": "user",
                            "content": prompt,
                        },
                    ],
                    temperature=0.3,
                )

            elapsed = round(
                time.perf_counter() - start_time,
                2,
            )

            result = (
                response
                .choices[0]
                .message
                .content
                .strip()
            )

            # =================================================
            # OUTPUT
            # =================================================

            st.markdown(
                '<div class="section-title">🎯 Result</div>',
                unsafe_allow_html=True,
            )

            st.markdown(
                '<div class="output-box">',
                unsafe_allow_html=True,
            )

            st.markdown(
                '<div class="output-label">LOCAL AI OUTPUT</div>',
                unsafe_allow_html=True,
            )

            st.write(result)

            st.markdown(
                '</div>',
                unsafe_allow_html=True,
            )

            # =================================================
            # METRICS
            # =================================================

            st.write("")

            m1, m2, m3 = st.columns(3)

            with m1:
                st.metric(
                    "⚡ Response Time",
                    f"{elapsed}s",
                )

            with m2:
                st.metric(
                    "🧠 Model",
                    "Gemma 3 1B",
                )

            with m3:
                st.metric(
                    "🔒 Runtime",
                    "Local",
                )

        except Exception as error:

            st.error(
                "❌ Could not connect to LM Studio."
            )

            st.write(
                "Make sure LM Studio is open and "
                "the local server is running."
            )

            st.code(
                "http://localhost:1234/v1"
            )

            st.error(
                f"Technical error: {error}"
            )

# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div class="footer">
        🔒 LingoAI • Gemma 3 1B • LM Studio<br>
        Your data stays on your machine.
    </div>
    """,
    unsafe_allow_html=True,
)