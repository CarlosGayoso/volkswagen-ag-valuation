import numpy as np
import pandas as pd
import streamlit as st

from utils.styles import (
    load_css,
    metric_card,
)

from utils.data import (
    CURRENT_PRICE,
    DCF_BASE,
    DCF_CONSERVATIVE,
)

from utils.charts import sensitivity_chart


# =====================================================
# GLOBAL STYLES
# =====================================================

load_css()


# =====================================================
# PAGE HEADER
# =====================================================

st.html(
    """
    <div style="
        padding:32px 38px;
        margin-bottom:24px;
        border-radius:24px;
        background:
            radial-gradient(
                circle at 88% 10%,
                rgba(245,158,11,0.24),
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
            color:#FFFFFF;
            font-size:40px;
            line-height:1.1;
            font-weight:850;
            letter-spacing:-1px;
        ">
            Sensitivity & Risks
        </div>

        <div style="
            margin-top:10px;
            color:#DCEBFF;
            font-size:17px;
        ">
            Valuation sensitivity, downside risks and catalysts
        </div>
    </div>
    """
)


# =====================================================
# INTERACTIVE ASSUMPTIONS
# =====================================================

with st.sidebar:

    st.divider()

    st.markdown("### Sensitivity Assumptions")

    selected_wacc = st.slider(
        "WACC (%)",
        min_value=7.0,
        max_value=11.0,
        value=8.5,
        step=0.5,
        key="sensitivity_wacc",
    )

    selected_growth = st.slider(
        "Terminal Growth (%)",
        min_value=0.0,
        max_value=3.0,
        value=1.0,
        step=0.5,
        key="sensitivity_growth",
    )


# =====================================================
# SENSITIVITY MATRIX
# =====================================================

wacc_values = np.arange(
    7.0,
    11.5,
    0.5,
)

growth_values = np.arange(
    0.0,
    3.5,
    0.5,
)

matrix = []

for growth_rate in growth_values:

    row = []

    for wacc_rate in wacc_values:

        implied_price = (
            DCF_BASE
            + (growth_rate - 1.0) * 10
            - (wacc_rate - 8.5) * 8
        )

        row.append(
            round(implied_price, 1)
        )

    matrix.append(row)


# =====================================================
# SELECTED SCENARIO
# =====================================================

selected_implied_value = (
    DCF_BASE
    + (selected_growth - 1.0) * 10
    - (selected_wacc - 8.5) * 8
)

selected_upside = (
    (
        selected_implied_value
        - CURRENT_PRICE
    )
    / CURRENT_PRICE
) * 100


# =====================================================
# KPI CARDS
# =====================================================

wacc_column, growth_column, value_column, upside_column = (
    st.columns(
        4,
        gap="medium",
    )
)

with wacc_column:

    metric_card(
        title="Selected WACC",
        value=f"{selected_wacc:.1f}%",
        delta="Discount rate",
        color="#38BDF8",
    )

with growth_column:

    metric_card(
        title="Terminal Growth",
        value=f"{selected_growth:.1f}%",
        delta="Long-term assumption",
        color="#F59E0B",
    )

with value_column:

    metric_card(
        title="Implied Value",
        value=f"€{selected_implied_value:.1f}",
        delta="Sensitivity output",
        color="#22C55E",
    )

with upside_column:

    if selected_upside >= 0:
        upside_colour = "#22C55E"
    else:
        upside_colour = "#EF4444"

    metric_card(
        title="Implied Upside",
        value=f"{selected_upside:+.1f}%",
        delta="Versus market price",
        color=upside_colour,
    )


# =====================================================
# SENSITIVITY HEATMAP
# =====================================================

st.write("")

sensitivity_figure = sensitivity_chart(
    matrix,
    wacc_values,
    growth_values,
)

st.plotly_chart(
    sensitivity_figure,
    width="stretch",
    config={
        "displayModeBar": False,
        "responsive": True,
    },
)


# =====================================================
# KEY MODEL ASSUMPTIONS
# =====================================================

st.write("")
st.markdown("### Key Valuation Assumptions")

base_column, conservative_column, market_column, scenario_column = (
    st.columns(
        4,
        gap="medium",
    )
)

with base_column:

    metric_card(
        title="Base Fair Value",
        value=f"€{DCF_BASE:.1f}",
        delta="Base DCF",
        color="#22C55E",
    )

with conservative_column:

    metric_card(
        title="Conservative Value",
        value=f"€{DCF_CONSERVATIVE:.1f}",
        delta="DCF by business",
        color="#38BDF8",
    )

with market_column:

    metric_card(
        title="Market Price",
        value=f"€{CURRENT_PRICE:.1f}",
        delta="Reference price",
        color="#FFFFFF",
    )

with scenario_column:

    metric_card(
        title="Selected Scenario",
        value=f"€{selected_implied_value:.1f}",
        delta=(
            f"{selected_wacc:.1f}% WACC | "
            f"{selected_growth:.1f}% growth"
        ),
        color="#F59E0B",
    )


# =====================================================
# RISKS AND CATALYSTS
# =====================================================

st.write("")
st.write("")

risks_column, catalysts_column = st.columns(
    2,
    gap="large",
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
                    Lower contributions from the joint ventures
                    would reduce group equity value.
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
                    Pricing pressure and market-share losses
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
                    Automotive margin compression
                </strong>

                <div style="
                    margin-top:6px;
                    color:#E2E8F0;
                    line-height:1.5;
                ">
                    The valuation depends on a material
                    recovery in EBIT margins.
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
                    Capital intensity
                </strong>

                <div style="
                    margin-top:6px;
                    color:#E2E8F0;
                    line-height:1.5;
                ">
                    Higher capital expenditure could reduce
                    free cash flow generation.
                </div>
            </div>

            <div style="
                padding:15px;
                border-radius:14px;
                background:rgba(239,68,68,0.09);
                border:1px solid rgba(239,68,68,0.18);
            ">
                <strong style="color:#F87171;">
                    Higher discount rates
                </strong>

                <div style="
                    margin-top:6px;
                    color:#E2E8F0;
                    line-height:1.5;
                ">
                    An increase in WACC reduces the present
                    value of future cash flows.
                </div>
            </div>
        </div>
        """
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
                    Automotive margin recovery
                </strong>

                <div style="
                    margin-top:6px;
                    color:#E2E8F0;
                    line-height:1.5;
                ">
                    Better cost control and operating leverage
                    could improve profitability.
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
                    China stabilisation
                </strong>

                <div style="
                    margin-top:6px;
                    color:#E2E8F0;
                    line-height:1.5;
                ">
                    Stable joint venture earnings could support
                    a higher valuation contribution.
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
                    Financial Services rerating
                </strong>

                <div style="
                    margin-top:6px;
                    color:#E2E8F0;
                    line-height:1.5;
                ">
                    Improved recognition of the finance
                    franchise could narrow the valuation gap.
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
                    Cost optimisation
                </strong>

                <div style="
                    margin-top:6px;
                    color:#E2E8F0;
                    line-height:1.5;
                ">
                    Restructuring measures could improve
                    Automotive EBIT and free cash flow.
                </div>
            </div>

            <div style="
                padding:15px;
                border-radius:14px;
                background:rgba(34,197,94,0.09);
                border:1px solid rgba(34,197,94,0.18);
            ">
                <strong style="color:#22C55E;">
                    Shareholder returns
                </strong>

                <div style="
                    margin-top:6px;
                    color:#E2E8F0;
                    line-height:1.5;
                ">
                    Better capital allocation and distributions
                    could support a market rerating.
                </div>
            </div>
        </div>
        """
    )


# =====================================================
# SCENARIO FRAMEWORK
# =====================================================

st.write("")
st.write("")

st.markdown("### Scenario Framework")

conservative_upside = (
    (
        DCF_CONSERVATIVE
        - CURRENT_PRICE
    )
    / CURRENT_PRICE
) * 100

base_upside = (
    (
        DCF_BASE
        - CURRENT_PRICE
    )
    / CURRENT_PRICE
) * 100

scenario_df = pd.DataFrame(
    {
        "Scenario": [
            "Conservative",
            "Base",
            "Selected Sensitivity",
        ],
        "Implied Value": [
            DCF_CONSERVATIVE,
            DCF_BASE,
            selected_implied_value,
        ],
        "Upside": [
            conservative_upside,
            base_upside,
            selected_upside,
        ],
        "Description": [
            (
                "Lower business valuation and "
                "execution risk"
            ),
            "Base model assumptions",
            (
                f"WACC {selected_wacc:.1f}% and "
                f"terminal growth "
                f"{selected_growth:.1f}%"
            ),
        ],
    }
)

st.dataframe(
    scenario_df,
    width="stretch",
    hide_index=True,
    column_config={
        "Scenario": (
            st.column_config.TextColumn(
                "Scenario",
                width="medium",
            )
        ),
        "Implied Value": (
            st.column_config.NumberColumn(
                "Implied Value",
                format="€%.1f",
            )
        ),
        "Upside": (
            st.column_config.NumberColumn(
                "Upside",
                format="%+.1f%%",
            )
        ),
        "Description": (
            st.column_config.TextColumn(
                "Description",
                width="large",
            )
        ),
    },
)


# =====================================================
# FOOTER
# =====================================================

st.write("")

st.caption(
    """
The sensitivity matrix illustrates directional changes
in implied value under alternative WACC and terminal
growth assumptions. The matrix is a scenario tool and
does not replace the underlying DCF model.
    """
)