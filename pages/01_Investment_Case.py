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


# =====================================================
# GLOBAL STYLES
# =====================================================

load_css()


# =====================================================
# VALUATION CALCULATIONS
# =====================================================

base_value_spread = (
    DCF_BASE
    - CURRENT_PRICE
)

conservative_value_spread = (
    DCF_CONSERVATIVE
    - CURRENT_PRICE
)

if UPSIDE >= 30:
    investment_rating = "BUY"
    rating_colour = "#22C55E"

elif UPSIDE >= 10:
    investment_rating = "HOLD"
    rating_colour = "#F59E0B"

else:
    investment_rating = "REDUCE"
    rating_colour = "#EF4444"


# =====================================================
# PAGE HEADER
# =====================================================

st.html(
    f"""
    <div style="
        padding:32px 38px;
        margin-bottom:24px;
        border-radius:24px;
        background:
            radial-gradient(
                circle at 88% 10%,
                rgba(34,197,94,0.24),
                transparent 32%
            ),
            linear-gradient(
                135deg,
                #001E50 0%,
                #004B93 55%,
                #0877D1 100%
            );
        border:1px solid rgba(255,255,255,0.12);
        box-shadow:0 20px 50px rgba(0,0,0,0.28);
    ">
        <div style="
            display:flex;
            justify-content:space-between;
            align-items:flex-start;
            gap:24px;
        ">
            <div>
                <div style="
                    color:#FFFFFF;
                    font-size:40px;
                    line-height:1.1;
                    font-weight:850;
                    letter-spacing:-1px;
                ">
                    Investment Case
                </div>

                <div style="
                    margin-top:10px;
                    color:#DCEBFF;
                    font-size:17px;
                ">
                    Volkswagen AG equity research thesis
                </div>

                <div style="
                    margin-top:16px;
                    color:rgba(255,255,255,0.82);
                    font-size:14px;
                ">
                    Valuation, catalysts, risks and investor positioning
                </div>
            </div>

            <div style="
                min-width:130px;
                padding:12px 18px;
                border-radius:14px;
                text-align:center;
                background:rgba(7,17,31,0.28);
                border:1px solid rgba(255,255,255,0.18);
            ">
                <div style="
                    color:#DCEBFF;
                    font-size:11px;
                    font-weight:700;
                    letter-spacing:1px;
                    text-transform:uppercase;
                ">
                    Rating
                </div>

                <div style="
                    margin-top:5px;
                    color:{rating_colour};
                    font-size:25px;
                    font-weight:850;
                ">
                    {investment_rating}
                </div>
            </div>
        </div>
    </div>
    """
)


# =====================================================
# KPI CARDS
# =====================================================

market_column, base_column, conservative_column, sotp_column = (
    st.columns(
        4,
        gap="medium",
    )
)

with market_column:

    metric_card(
        title="Market Price",
        value=f"€{CURRENT_PRICE:,.1f}",
        delta="Reference share price",
        color="#FFFFFF",
    )

with base_column:

    metric_card(
        title="DCF Fair Value",
        value=f"€{DCF_BASE:,.1f}",
        delta=f"{UPSIDE:+.1f}% upside",
        color="#22C55E",
    )

with conservative_column:

    metric_card(
        title="Conservative Value",
        value=f"€{DCF_CONSERVATIVE:,.1f}",
        delta=(
            f"{CONSERVATIVE_UPSIDE:+.1f}% upside"
        ),
        color="#38BDF8",
    )

with sotp_column:

    metric_card(
        title="SOTP Equity Value",
        value=f"€{SOTP_VALUE:,.1f}bn",
        delta="2026 business valuation",
        color="#F59E0B",
    )


# =====================================================
# INVESTMENT THESIS AND GAUGE
# =====================================================

st.write("")

thesis_column, gauge_column = st.columns(
    [1.55, 1],
    gap="large",
)

with thesis_column:

    st.html(
        f"""
        <div class="glass-card">
            <div class="section-header">
                Investment Thesis
            </div>

            <h3 style="
                margin-top:0;
                color:#F8FAFC;
            ">
                Volkswagen is trading at a significant
                discount to estimated intrinsic value
            </h3>

            <p>
                The base DCF indicates a fair value of
                <strong style="color:#22C55E;">
                    €{DCF_BASE:,.1f}
                </strong>,
                compared with a reference market price of
                <strong style="color:#F8FAFC;">
                    €{CURRENT_PRICE:,.1f}
                </strong>.
            </p>

            <p>
                This represents a potential value gap of
                <strong style="color:#22C55E;">
                    €{base_value_spread:,.1f} per share
                </strong>
                and implied upside of
                <strong style="color:#22C55E;">
                    {UPSIDE:.1f}%
                </strong>.
            </p>

            <p>
                Even the more conservative valuation of
                <strong style="color:#38BDF8;">
                    €{DCF_CONSERVATIVE:,.1f}
                </strong>
                remains above the reference market price.
            </p>

            <p style="
                margin-bottom:0;
                color:#CBD5E1;
            ">
                The investment case depends primarily on
                Automotive margin recovery, stabilisation
                of China earnings and recognition of the
                Financial Services franchise value.
            </p>
        </div>
        """
    )

with gauge_column:

    gauge_figure = upside_gauge(
        UPSIDE
    )

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
# MARKET CONCERNS
# =====================================================

st.write("")
st.write("")

st.markdown("### What the Market Is Discounting")

china_column, ev_column, margin_column, capital_column = (
    st.columns(
        4,
        gap="medium",
    )
)

with china_column:

    st.html(
        """
        <div class="glass-card">
            <div style="
                color:#F59E0B;
                font-size:13px;
                font-weight:750;
                letter-spacing:0.8px;
                text-transform:uppercase;
            ">
                China Deceleration
            </div>

            <p style="
                margin-top:10px;
                margin-bottom:0;
                color:#E2E8F0;
                line-height:1.5;
            ">
                Competitive pressure and weaker joint venture
                earnings are reflected in a discounted
                China valuation.
            </p>
        </div>
        """
    )

with ev_column:

    st.html(
        """
        <div class="glass-card">
            <div style="
                color:#38BDF8;
                font-size:13px;
                font-weight:750;
                letter-spacing:0.8px;
                text-transform:uppercase;
            ">
                EV Transition
            </div>

            <p style="
                margin-top:10px;
                margin-bottom:0;
                color:#E2E8F0;
                line-height:1.5;
            ">
                Product investment, software execution and
                pricing competition create uncertainty around
                returns.
            </p>
        </div>
        """
    )

with margin_column:

    st.html(
        """
        <div class="glass-card">
            <div style="
                color:#F87171;
                font-size:13px;
                font-weight:750;
                letter-spacing:0.8px;
                text-transform:uppercase;
            ">
                Margin Pressure
            </div>

            <p style="
                margin-top:10px;
                margin-bottom:0;
                color:#E2E8F0;
                line-height:1.5;
            ">
                The market questions whether Automotive can
                achieve the EBIT margin recovery embedded
                in the model.
            </p>
        </div>
        """
    )

with capital_column:

    st.html(
        """
        <div class="glass-card">
            <div style="
                color:#A78BFA;
                font-size:13px;
                font-weight:750;
                letter-spacing:0.8px;
                text-transform:uppercase;
            ">
                Capital Intensity
            </div>

            <p style="
                margin-top:10px;
                margin-bottom:0;
                color:#E2E8F0;
                line-height:1.5;
            ">
                High capital expenditure and development
                costs limit free cash flow conversion.
            </p>
        </div>
        """
    )


# =====================================================
# CATALYSTS AND RISKS
# =====================================================

st.write("")
st.write("")

catalysts_column, risks_column = st.columns(
    2,
    gap="large",
)

with catalysts_column:

    st.html(
        """
        <div class="glass-card">
            <div class="section-header">
                Key Catalysts
            </div>

            <div style="
                margin-bottom:15px;
                padding:15px;
                border-radius:14px;
                background:rgba(34,197,94,0.09);
                border:1px solid rgba(34,197,94,0.18);
            ">
                <strong style="color:#22C55E;">
                    Automotive margin normalisation
                </strong>

                <div style="
                    margin-top:6px;
                    color:#E2E8F0;
                    line-height:1.5;
                ">
                    Cost reduction and operating leverage
                    could improve EBIT and cash generation.
                </div>
            </div>

            <div style="
                margin-bottom:15px;
                padding:15px;
                border-radius:14px;
                background:rgba(34,197,94,0.09);
                border:1px solid rgba(34,197,94,0.18);
            ">
                <strong style="color:#22C55E;">
                    China JV earnings stabilisation
                </strong>

                <div style="
                    margin-top:6px;
                    color:#E2E8F0;
                    line-height:1.5;
                ">
                    Stable earnings would reduce uncertainty
                    around the China valuation contribution.
                </div>
            </div>

            <div style="
                margin-bottom:15px;
                padding:15px;
                border-radius:14px;
                background:rgba(34,197,94,0.09);
                border:1px solid rgba(34,197,94,0.18);
            ">
                <strong style="color:#22C55E;">
                    Financial Services value recognition
                </strong>

                <div style="
                    margin-top:6px;
                    color:#E2E8F0;
                    line-height:1.5;
                ">
                    Better visibility on book value and returns
                    could support a higher implied value.
                </div>
            </div>

            <div style="
                padding:15px;
                border-radius:14px;
                background:rgba(34,197,94,0.09);
                border:1px solid rgba(34,197,94,0.18);
            ">
                <strong style="color:#22C55E;">
                    Portfolio simplification
                </strong>

                <div style="
                    margin-top:6px;
                    color:#E2E8F0;
                    line-height:1.5;
                ">
                    Improved capital allocation and greater
                    segment transparency could support rerating.
                </div>
            </div>
        </div>
        """
    )

with risks_column:

    st.html(
        """
        <div class="glass-card">
            <div class="section-header">
                Key Risks
            </div>

            <div style="
                margin-bottom:15px;
                padding:15px;
                border-radius:14px;
                background:rgba(239,68,68,0.09);
                border:1px solid rgba(239,68,68,0.18);
            ">
                <strong style="color:#F87171;">
                    China market deterioration
                </strong>

                <div style="
                    margin-top:6px;
                    color:#E2E8F0;
                    line-height:1.5;
                ">
                    Lower earnings and market share would reduce
                    the value of the joint ventures.
                </div>
            </div>

            <div style="
                margin-bottom:15px;
                padding:15px;
                border-radius:14px;
                background:rgba(239,68,68,0.09);
                border:1px solid rgba(239,68,68,0.18);
            ">
                <strong style="color:#F87171;">
                    EV competition
                </strong>

                <div style="
                    margin-top:6px;
                    color:#E2E8F0;
                    line-height:1.5;
                ">
                    Pricing pressure and product execution
                    could weaken Automotive profitability.
                </div>
            </div>

            <div style="
                margin-bottom:15px;
                padding:15px;
                border-radius:14px;
                background:rgba(239,68,68,0.09);
                border:1px solid rgba(239,68,68,0.18);
            ">
                <strong style="color:#F87171;">
                    Regulatory pressure
                </strong>

                <div style="
                    margin-top:6px;
                    color:#E2E8F0;
                    line-height:1.5;
                ">
                    Emissions requirements and trade measures
                    could increase costs.
                </div>
            </div>

            <div style="
                padding:15px;
                border-radius:14px;
                background:rgba(239,68,68,0.09);
                border:1px solid rgba(239,68,68,0.18);
            ">
                <strong style="color:#F87171;">
                    Lower free cash flow
                </strong>

                <div style="
                    margin-top:6px;
                    color:#E2E8F0;
                    line-height:1.5;
                ">
                    Higher capital expenditure or weaker cash
                    conversion would reduce DCF value.
                </div>
            </div>
        </div>
        """
    )


# =====================================================
# INVESTMENT SCORECARD
# =====================================================

st.write("")
st.write("")

st.markdown("### Investment Scorecard")

scorecard_data = {
    "Valuation": {
        "score": 9,
        "colour": "#22C55E",
    },
    "Earnings Visibility": {
        "score": 5,
        "colour": "#F59E0B",
    },
    "Balance Sheet": {
        "score": 6,
        "colour": "#38BDF8",
    },
    "Growth": {
        "score": 5,
        "colour": "#F59E0B",
    },
    "Catalysts": {
        "score": 7,
        "colour": "#22C55E",
    },
}

scorecard_columns = st.columns(
    len(scorecard_data),
    gap="medium",
)

for column, (category, details) in zip(
    scorecard_columns,
    scorecard_data.items(),
):

    with column:

        score = details["score"]
        colour = details["colour"]
        bar_width = score * 10

        st.html(
            f"""
            <div class="glass-card">
                <div style="
                    color:#94A3B8;
                    font-size:12px;
                    font-weight:700;
                    text-transform:uppercase;
                    letter-spacing:0.8px;
                ">
                    {category}
                </div>

                <div style="
                    margin-top:8px;
                    color:{colour};
                    font-size:30px;
                    font-weight:850;
                ">
                    {score}/10
                </div>

                <div style="
                    margin-top:12px;
                    width:100%;
                    height:6px;
                    border-radius:6px;
                    background:rgba(148,163,184,0.18);
                    overflow:hidden;
                ">
                    <div style="
                        width:{bar_width}%;
                        height:100%;
                        border-radius:6px;
                        background:{colour};
                    ">
                    </div>
                </div>
            </div>
            """
        )


# =====================================================
# VALUATION SNAPSHOT
# =====================================================

st.write("")
st.write("")

st.markdown("### Valuation Snapshot")

snapshot_column, conclusion_column = st.columns(
    [1, 1.4],
    gap="large",
)

with snapshot_column:

    st.html(
        f"""
        <div class="glass-card">
            <div class="section-header">
                Quantitative Summary
            </div>

            <div style="
                display:flex;
                justify-content:space-between;
                margin-bottom:14px;
            ">
                <span style="color:#94A3B8;">
                    Market price
                </span>

                <strong style="color:#F8FAFC;">
                    €{CURRENT_PRICE:,.2f}
                </strong>
            </div>

            <div style="
                display:flex;
                justify-content:space-between;
                margin-bottom:14px;
            ">
                <span style="color:#94A3B8;">
                    Base fair value
                </span>

                <strong style="color:#22C55E;">
                    €{DCF_BASE:,.2f}
                </strong>
            </div>

            <div style="
                display:flex;
                justify-content:space-between;
                margin-bottom:14px;
            ">
                <span style="color:#94A3B8;">
                    Conservative value
                </span>

                <strong style="color:#38BDF8;">
                    €{DCF_CONSERVATIVE:,.2f}
                </strong>
            </div>

            <div style="
                display:flex;
                justify-content:space-between;
                margin-bottom:14px;
            ">
                <span style="color:#94A3B8;">
                    Base value gap
                </span>

                <strong style="color:#22C55E;">
                    €{base_value_spread:,.2f}
                </strong>
            </div>

            <div style="
                display:flex;
                justify-content:space-between;
                margin-bottom:14px;
            ">
                <span style="color:#94A3B8;">
                    Conservative value gap
                </span>

                <strong style="color:#38BDF8;">
                    €{conservative_value_spread:,.2f}
                </strong>
            </div>

            <div style="
                display:flex;
                justify-content:space-between;
            ">
                <span style="color:#94A3B8;">
                    Investment rating
                </span>

                <strong style="color:{rating_colour};">
                    {investment_rating}
                </strong>
            </div>
        </div>
        """
    )

with conclusion_column:

    st.html(
        f"""
        <div class="glass-card">
            <div class="section-header">
                Investment Conclusion
            </div>

            <p>
                The valuation framework indicates that
                Volkswagen offers a material discount to
                estimated intrinsic value.
            </p>

            <p>
                The base case implies
                <strong style="color:#22C55E;">
                    {UPSIDE:.1f}% upside
                </strong>,
                while the conservative case implies
                <strong style="color:#38BDF8;">
                    {CONSERVATIVE_UPSIDE:.1f}% upside
                </strong>.
            </p>

            <p>
                The principal source of value is not a
                high-growth revenue scenario. The investment
                case depends on better Automotive margins,
                stable China earnings and recognition of the
                Financial Services business.
            </p>

            <p style="
                margin-bottom:0;
                color:#CBD5E1;
            ">
                The risk-reward profile is therefore attractive
                for investors prepared to accept execution,
                competitive and cyclical uncertainty.
            </p>
        </div>
        """
    )


# =====================================================
# FOOTER
# =====================================================

st.write("")

st.caption(
    """
The investment case is based on the valuation assumptions
contained in Finance_Evaluation_VW_v2.xlsx. The scorecard
represents an analytical assessment and is not imported
from the Excel model.
    """
)