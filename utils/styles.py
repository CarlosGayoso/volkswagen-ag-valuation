import html
import streamlit as st


# =====================================================
# COLOR PALETTE
# =====================================================

VW_BLUE = "#0057B8"
VW_DARK_BLUE = "#001E50"
VW_NAVY = "#07111F"

BACKGROUND = "#07111F"
CARD_BACKGROUND = "#111827"

TEXT_PRIMARY = "#F8FAFC"
TEXT_SECONDARY = "#94A3B8"

SUCCESS = "#22C55E"
WARNING = "#F59E0B"
INFO = "#38BDF8"


# =====================================================
# GLOBAL CSS
# =====================================================

def load_css():

    st.markdown(
        """
<style>
:root {
    --vw-blue: #0057B8;
    --vw-dark-blue: #001E50;
    --background: #07111F;
    --card-background: #111827;
    --text-primary: #F8FAFC;
    --text-secondary: #94A3B8;
    --success: #22C55E;
    --warning: #F59E0B;
    --info: #38BDF8;
}

html,
body,
[data-testid="stAppViewContainer"],
.stApp {
    background:
        radial-gradient(
            circle at top right,
            rgba(0, 87, 184, 0.24) 0%,
            rgba(7, 17, 31, 0.98) 42%,
            #07111F 100%
        );
    color: var(--text-primary);
}

[data-testid="stHeader"] {
    background: rgba(7, 17, 31, 0.82);
}

[data-testid="stMainBlockContainer"] {
    max-width: 1500px;
    padding-top: 1rem;
    padding-bottom: 3rem;
}

section[data-testid="stSidebar"] {
    background:
        linear-gradient(
            180deg,
            #091525 0%,
            #07111F 100%
        );
    border-right: 1px solid rgba(148, 163, 184, 0.14);
}

section[data-testid="stSidebar"] * {
    color: #F8FAFC;
}

.hero {
    position: relative;
    overflow: hidden;
    padding: 46px 52px;
    margin-bottom: 28px;
    min-height: 180px;

    border-radius: 0 0 34px 34px;

    background:
        radial-gradient(
            circle at 88% 5%,
            rgba(56, 189, 248, 0.30),
            transparent 34%
        ),
        linear-gradient(
            135deg,
            #001E50 0%,
            #004B93 48%,
            #0877D1 100%
        );

    border: 1px solid rgba(255, 255, 255, 0.14);

    box-shadow:
        0 22px 60px rgba(0, 0, 0, 0.34);
}

.hero::after {
    content: "";
    position: absolute;
    width: 280px;
    height: 280px;
    right: -70px;
    bottom: -150px;

    border-radius: 50%;

    background:
        rgba(255, 255, 255, 0.08);
}

.hero-title {
    position: relative;
    z-index: 1;

    margin: 0 0 8px 0;

    color: #FFFFFF;
    font-size: clamp(38px, 5vw, 62px);
    line-height: 1.05;
    font-weight: 900;
    letter-spacing: -1.5px;
}

.hero-subtitle {
    position: relative;
    z-index: 1;

    color: #DCEBFF;
    font-size: 22px;
    font-weight: 500;
}

.hero-description {
    position: relative;
    z-index: 1;

    margin-top: 16px;

    color: rgba(255, 255, 255, 0.92);
    font-size: 16px;
    font-weight: 500;
}

.premium-card {
    box-sizing: border-box;
    width: 100%;
    min-height: 148px;
    padding: 22px 24px;

    border-radius: 22px;

    background:
        linear-gradient(
            145deg,
            rgba(30, 41, 59, 0.96),
            rgba(15, 23, 42, 0.98)
        );

    border: 1px solid rgba(148, 163, 184, 0.20);

    box-shadow:
        0 14px 35px rgba(0, 0, 0, 0.28),
        inset 0 1px 0 rgba(255, 255, 255, 0.05);

    transition:
        transform 160ms ease,
        border-color 160ms ease,
        box-shadow 160ms ease;
}

.premium-card:hover {
    transform: translateY(-3px);

    border-color:
        rgba(56, 189, 248, 0.42);

    box-shadow:
        0 20px 44px rgba(0, 0, 0, 0.34),
        0 0 0 1px rgba(56, 189, 248, 0.08);
}

.metric-title {
    margin-bottom: 10px;

    color: #94A3B8;
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 1.4px;
    text-transform: uppercase;
}

.metric-value {
    margin-bottom: 7px;

    color: #FFFFFF;
    font-size: clamp(29px, 3vw, 42px);
    line-height: 1.05;
    font-weight: 850;
    letter-spacing: -1px;
}

.metric-delta {
    color: #22C55E;
    font-size: 13px;
    font-weight: 650;
}

.glass-card {
    box-sizing: border-box;
    width: 100%;
    padding: 30px 32px;

    border-radius: 24px;

    background:
        linear-gradient(
            145deg,
            rgba(17, 24, 39, 0.98),
            rgba(15, 23, 42, 0.98)
        );

    border:
        1px solid rgba(148, 163, 184, 0.18);

    box-shadow:
        0 18px 48px rgba(0, 0, 0, 0.30);
}

.glass-card h1,
.glass-card h2,
.glass-card h3,
.glass-card h4,
.glass-card p,
.glass-card li {
    color: #F8FAFC;
}

.glass-card li {
    margin-bottom: 9px;
}

.section-header {
    margin-bottom: 20px;

    color: #FFFFFF;
    font-size: 29px;
    line-height: 1.2;
    font-weight: 800;
    letter-spacing: -0.5px;
}

[data-testid="stPlotlyChart"] {
    overflow: hidden;

    border-radius: 24px;

    background:
        linear-gradient(
            145deg,
            rgba(17, 24, 39, 0.98),
            rgba(15, 23, 42, 0.98)
        );

    border:
        1px solid rgba(148, 163, 184, 0.17);

    box-shadow:
        0 18px 48px rgba(0, 0, 0, 0.24);
}

[data-baseweb="tab-list"] {
    gap: 8px;
}

button[data-baseweb="tab"] {
    padding-right: 18px;
    padding-left: 18px;

    border-radius: 12px 12px 0 0;
}

[data-testid="stDataFrame"] {
    overflow: hidden;

    border-radius: 18px;

    border:
        1px solid rgba(148, 163, 184, 0.17);
}

[data-testid="stMetric"] {
    padding: 18px;

    border-radius: 18px;

    background:
        linear-gradient(
            145deg,
            rgba(30, 41, 59, 0.94),
            rgba(15, 23, 42, 0.98)
        );

    border:
        1px solid rgba(148, 163, 184, 0.18);
}

hr {
    border-color:
        rgba(148, 163, 184, 0.18);
}

footer {
    visibility: hidden;
}

#MainMenu {
    visibility: hidden;
}
</style>
        """,
        unsafe_allow_html=True,
    )


# =====================================================
# KPI CARD
# =====================================================

def metric_card(
    title,
    value,
    delta="",
    color="#FFFFFF"
):

    safe_title = html.escape(str(title))
    safe_value = html.escape(str(value))
    safe_delta = html.escape(str(delta))
    safe_color = html.escape(str(color))

    card_html = (
        '<div class="premium-card">'
        f'<div class="metric-title">{safe_title}</div>'
        f'<div class="metric-value" style="color:{safe_color};">'
        f'{safe_value}'
        '</div>'
        f'<div class="metric-delta">{safe_delta}</div>'
        '</div>'
    )

    st.html(card_html)