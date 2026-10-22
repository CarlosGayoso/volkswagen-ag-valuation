import streamlit as st

from utils.styles import (
    load_css,
    metric_card,
)

from utils.data import (
    CURRENT_PRICE,
    DCF_BASE,
    DCF_CONSERVATIVE,
    UPSIDE,
    CONSERVATIVE_UPSIDE,
    SOTP_VALUE,
)

from utils.charts import upside_gauge


load_css()


# =====================================================
# SIDEBAR SNAPSHOT
# =====================================================

with st.sidebar:
    st.divider()
    st.markdown("### Valuation Engine")
    st.success("Investment Rating: BUY")
    st.caption(f"Base fair value: €{DCF_BASE:.2f}")
    st.caption(f"Potential upside: {UPSIDE:.1f}%")


# =====================================================
# HERO
# =====================================================

st.html(
    """
    <div class="hero">
        <div class="hero-title">
            VOLKSWAGEN AG
        </div>

        <div class="hero-subtitle">
            Equity Research Platform
        </div>

        <div class="hero-description">
            Automotive • China JV • Financial Services • DCF
        </div>
    </div>
    """
)


# =====================================================
# KPI CARDS
# =====================================================

market_col, fair_col, conservative_col, sotp_col = st.columns(
    4,
    gap="medium",
)

with market_col:
    metric_card(
        title="Market Price",
        value=f"€{CURRENT_PRICE:,.0f}",
        delta="Reference share price",
        color="#FFFFFF",
    )

with fair_col:
    metric_card(
        title="DCF Fair Value",
        value=f"€{DCF_BASE:,.0f}",
        delta=f"+{UPSIDE:.1f}% upside",
        color="#22C55E",
    )

with conservative_col:
    metric_card(
        title="Conservative Value",
        value=f"€{DCF_CONSERVATIVE:,.0f}",
        delta=f"+{CONSERVATIVE_UPSIDE:.1f}% upside",
        color="#38BDF8",
    )

with sotp_col:
    metric_card(
        title="SOTP Equity Value",
        value=f"€{SOTP_VALUE:,.1f}bn",
        delta="2026 valuation",
        color="#F59E0B",
    )


# =====================================================
# EXECUTIVE SUMMARY
# =====================================================

st.write("")

summary_col, gauge_col = st.columns(
    [1.65, 1],
    gap="large",
)

with summary_col:
    st.html(
        """
        <div class="glass-card">
            <div class="section-header">
                Executive Summary
            </div>

            <h3>
                Investment Recommendation:
                <span style="color:#22C55E;">BUY</span>
            </h3>

            <p>
                Volkswagen appears significantly undervalued
                relative to estimated intrinsic value.
            </p>

            <p>The valuation is supported by:</p>

            <ul>
                <li>Automotive margin recovery</li>
                <li>China joint venture stabilisation</li>
                <li>Financial Services franchise value</li>
                <li>Sum-of-the-parts upside</li>
            </ul>

            <p>
                The market price appears to discount a materially
                weaker long-term scenario than the base case.
            </p>
        </div>
        """
    )

with gauge_col:
    gauge_figure = upside_gauge(UPSIDE)

    gauge_figure.update_layout(
        height=430,
        margin=dict(
            l=30,
            r=30,
            t=80,
            b=25,
        ),
    )

    st.plotly_chart(
        gauge_figure,
        width="stretch",
        config={
            "displayModeBar": False,
            "responsive": True,
        },
    )


# =====================================================
# FOOTER
# =====================================================

st.write("")
st.divider()

st.caption(
    """
Volkswagen AG Valuation

Prepared by Carlos Gayoso

For educational and investment research purposes only.
    """
)