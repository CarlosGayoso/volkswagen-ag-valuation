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
    dcf_df,
)

from utils.charts import dcf_chart


# =====================================================
# GLOBAL STYLES
# =====================================================

load_css()


# =====================================================
# DATA VALIDATION
# =====================================================

required_columns = {
    "Year",
    "Bear",
    "Base",
    "Conservative",
}

missing_columns = (
    required_columns
    - set(dcf_df.columns)
)

if missing_columns:

    st.error(
        "The DCF dataset is missing the following "
        f"columns: {', '.join(sorted(missing_columns))}"
    )

    st.stop()


# =====================================================
# DATA PREPARATION
# =====================================================

valuation_df = (
    dcf_df
    .copy()
    .sort_values("Year")
    .reset_index(drop=True)
)

numeric_columns = [
    "Year",
    "Bear",
    "Base",
    "Conservative",
]

for column in numeric_columns:

    valuation_df[column] = pd.to_numeric(
        valuation_df[column],
        errors="coerce",
    )

if valuation_df[numeric_columns].isna().any().any():

    st.error(
        "The DCF dataset contains invalid or empty "
        "numeric values."
    )

    st.stop()


# =====================================================
# CURRENT-YEAR VALUES
# =====================================================

first_year = int(
    valuation_df["Year"].iloc[0]
)

last_year = int(
    valuation_df["Year"].iloc[-1]
)

current_row = (
    valuation_df
    .iloc[0]
)

bear_value = float(
    current_row["Bear"]
)

base_value = float(
    current_row["Base"]
)

conservative_value = float(
    current_row["Conservative"]
)


# =====================================================
# UPSIDE CALCULATIONS
# =====================================================

def calculate_upside(
    valuation,
    market_price,
):

    if market_price == 0:
        return 0.0

    return (
        (
            valuation
            - market_price
        )
        / market_price
    ) * 100


bear_upside = calculate_upside(
    bear_value,
    CURRENT_PRICE,
)

base_upside = calculate_upside(
    base_value,
    CURRENT_PRICE,
)

conservative_upside = calculate_upside(
    conservative_value,
    CURRENT_PRICE,
)


# =====================================================
# VALUE RANGE
# =====================================================

scenario_values = [
    bear_value,
    base_value,
    conservative_value,
]

minimum_value = min(
    scenario_values
)

maximum_value = max(
    scenario_values
)

valuation_range = (
    maximum_value
    - minimum_value
)


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
                rgba(34,197,94,0.24),
                transparent 32%
            ),
            linear-gradient(
                135deg,
                #001E50 0%,
                #004B93 55%,
                #0877D1 100%
            );
        border:
            1px solid rgba(255,255,255,0.12);
        box-shadow:
            0 20px 50px rgba(0,0,0,0.28);
    ">
        <div style="
            color:#FFFFFF;
            font-size:40px;
            line-height:1.1;
            font-weight:850;
            letter-spacing:-1px;
        ">
            DCF Valuation
        </div>

        <div style="
            margin-top:10px;
            color:#DCEBFF;
            font-size:17px;
        ">
            Implied share price under alternative
            valuation scenarios
        </div>

        <div style="
            margin-top:16px;
            color:rgba(255,255,255,0.82);
            font-size:14px;
        ">
            Base, conservative and alternative
            model outcomes
        </div>
    </div>
    """
)


# =====================================================
# KPI CARDS
# =====================================================

market_column, base_column, conservative_column, bear_column = (
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
        title="Base Fair Value",
        value=f"€{base_value:,.1f}",
        delta=(
            f"{base_upside:+.1f}% "
            "vs. market price"
        ),
        color="#22C55E",
    )

with conservative_column:

    metric_card(
        title="Conservative Value",
        value=f"€{conservative_value:,.1f}",
        delta=(
            f"{conservative_upside:+.1f}% "
            "vs. market price"
        ),
        color="#38BDF8",
    )

with bear_column:

    metric_card(
        title="Alternative Scenario",
        value=f"€{bear_value:,.1f}",
        delta=(
            f"{bear_upside:+.1f}% "
            "vs. market price"
        ),
        color="#F59E0B",
    )


# =====================================================
# DCF CHART
# =====================================================

st.write("")

dcf_figure = dcf_chart(
    valuation_df
)

st.plotly_chart(
    dcf_figure,
    width="stretch",
    config={
        "displayModeBar": False,
        "responsive": True,
    },
)


# =====================================================
# VALUATION INTERPRETATION
# =====================================================

st.write("")

interpretation_column, framework_column = (
    st.columns(
        [1.35, 1],
        gap="large",
    )
)

with interpretation_column:

    st.html(
        f"""
        <div class="glass-card">
            <div class="section-header">
                Valuation Interpretation
            </div>

            <p>
                The base DCF produces an implied
                share value of
                <strong style="color:#22C55E;">
                    €{base_value:,.1f}
                </strong>
                in {first_year}.
            </p>

            <p>
                Relative to the reference market price
                of
                <strong style="color:#F8FAFC;">
                    €{CURRENT_PRICE:,.1f}
                </strong>,
                the base case indicates potential upside
                of
                <strong style="color:#22C55E;">
                    {base_upside:+.1f}%
                </strong>.
            </p>

            <p>
                The conservative approach produces a value
                of
                <strong style="color:#38BDF8;">
                    €{conservative_value:,.1f}
                </strong>,
                equivalent to
                <strong style="color:#38BDF8;">
                    {conservative_upside:+.1f}%
                </strong>
                versus the market price.
            </p>

            <p>
                The full range between the lowest and
                highest {first_year} scenario values is
                <strong style="color:#F59E0B;">
                    €{valuation_range:,.1f}
                </strong>
                per share.
            </p>

            <p style="
                margin-bottom:0;
                color:#CBD5E1;
            ">
                The dispersion between scenarios illustrates
                the sensitivity of the valuation to cash flow,
                debt and terminal-value assumptions.
            </p>
        </div>
        """
    )

with framework_column:

    st.html(
        """
        <div class="glass-card">
            <div class="section-header">
                Scenario Framework
            </div>

            <div style="
                margin-bottom:16px;
                padding:15px;
                border-radius:14px;
                background:rgba(34,197,94,0.09);
                border:
                    1px solid
                    rgba(34,197,94,0.18);
            ">
                <div style="
                    color:#22C55E;
                    font-size:13px;
                    font-weight:750;
                    letter-spacing:0.8px;
                    text-transform:uppercase;
                ">
                    Base
                </div>

                <div style="
                    margin-top:6px;
                    color:#E2E8F0;
                    line-height:1.5;
                ">
                    Central assumptions for free cash flow,
                    WACC, debt and terminal value.
                </div>
            </div>

            <div style="
                margin-bottom:16px;
                padding:15px;
                border-radius:14px;
                background:rgba(56,189,248,0.09);
                border:
                    1px solid
                    rgba(56,189,248,0.18);
            ">
                <div style="
                    color:#38BDF8;
                    font-size:13px;
                    font-weight:750;
                    letter-spacing:0.8px;
                    text-transform:uppercase;
                ">
                    Conservative
                </div>

                <div style="
                    margin-top:6px;
                    color:#E2E8F0;
                    line-height:1.5;
                ">
                    Business-by-business valuation with
                    more cautious assumptions.
                </div>
            </div>

            <div style="
                padding:15px;
                border-radius:14px;
                background:rgba(245,158,11,0.09);
                border:
                    1px solid
                    rgba(245,158,11,0.18);
            ">
                <div style="
                    color:#F59E0B;
                    font-size:13px;
                    font-weight:750;
                    letter-spacing:0.8px;
                    text-transform:uppercase;
                ">
                    Alternative
                </div>

                <div style="
                    margin-top:6px;
                    color:#E2E8F0;
                    line-height:1.5;
                ">
                    Alternative cash flow and balance-sheet
                    assumptions from the scenario model.
                </div>
            </div>
        </div>
        """
    )


# =====================================================
# VALUATION SPREAD
# =====================================================

st.write("")
st.write("")

st.markdown("### Current Scenario Comparison")

comparison_df = pd.DataFrame(
    {
        "Scenario": [
            "Market Price",
            "Base",
            "Conservative",
            "Alternative",
        ],
        "Value": [
            CURRENT_PRICE,
            base_value,
            conservative_value,
            bear_value,
        ],
    }
)

comparison_df["Upside"] = (
    (
        comparison_df["Value"]
        - CURRENT_PRICE
    )
    / CURRENT_PRICE
) * 100

comparison_df["Difference vs. Market"] = (
    comparison_df["Value"]
    - CURRENT_PRICE
)


# =====================================================
# COMPARISON TABLE
# =====================================================

st.dataframe(
    comparison_df,
    width="stretch",
    hide_index=True,
    column_config={
        "Scenario": (
            st.column_config.TextColumn(
                "Scenario",
                width="medium",
            )
        ),
        "Value": (
            st.column_config.NumberColumn(
                "Implied Value",
                format="€%.2f",
            )
        ),
        "Upside": (
            st.column_config.NumberColumn(
                "Upside / Downside",
                format="%+.1f%%",
            )
        ),
        "Difference vs. Market": (
            st.column_config.NumberColumn(
                "Difference vs. Market",
                format="€%+.2f",
            )
        ),
    },
)


# =====================================================
# DCF FORECAST TABLE
# =====================================================

st.write("")
st.write("")

st.markdown(
    f"### DCF Scenario Evolution: {first_year}–{last_year}"
)

display_df = valuation_df.copy()

display_df["Base vs. Market"] = (
    (
        display_df["Base"]
        - CURRENT_PRICE
    )
    / CURRENT_PRICE
) * 100

display_df["Conservative vs. Market"] = (
    (
        display_df["Conservative"]
        - CURRENT_PRICE
    )
    / CURRENT_PRICE
) * 100

display_df["Alternative vs. Market"] = (
    (
        display_df["Bear"]
        - CURRENT_PRICE
    )
    / CURRENT_PRICE
) * 100

display_df = display_df[
    [
        "Year",
        "Base",
        "Conservative",
        "Bear",
        "Base vs. Market",
        "Conservative vs. Market",
        "Alternative vs. Market",
    ]
]

st.dataframe(
    display_df,
    width="stretch",
    hide_index=True,
    column_config={
        "Year": (
            st.column_config.NumberColumn(
                "Year",
                format="%d",
            )
        ),
        "Base": (
            st.column_config.NumberColumn(
                "Base Value",
                format="€%.2f",
            )
        ),
        "Conservative": (
            st.column_config.NumberColumn(
                "Conservative Value",
                format="€%.2f",
            )
        ),
        "Bear": (
            st.column_config.NumberColumn(
                "Alternative Value",
                format="€%.2f",
            )
        ),
        "Base vs. Market": (
            st.column_config.NumberColumn(
                "Base Upside",
                format="%+.1f%%",
            )
        ),
        "Conservative vs. Market": (
            st.column_config.NumberColumn(
                "Conservative Upside",
                format="%+.1f%%",
            )
        ),
        "Alternative vs. Market": (
            st.column_config.NumberColumn(
                "Alternative Upside",
                format="%+.1f%%",
            )
        ),
    },
)


# =====================================================
# MODEL OBSERVATIONS
# =====================================================

st.write("")
st.write("")

observations_column, limitations_column = (
    st.columns(
        2,
        gap="large",
    )
)

with observations_column:

    st.html(
        """
        <div class="glass-card">
            <div class="section-header">
                Key Observations
            </div>

            <ul>
                <li>
                    The base valuation remains above the
                    reference market price.
                </li>

                <li>
                    The conservative scenario provides a
                    lower valuation benchmark.
                </li>

                <li>
                    Scenario dispersion is driven by
                    differences in cash flow and debt.
                </li>

                <li>
                    Terminal value remains an important
                    component of enterprise value.
                </li>
            </ul>
        </div>
        """
    )

with limitations_column:

    st.html(
        """
        <div class="glass-card">
            <div class="section-header">
                Model Considerations
            </div>

            <ul>
                <li>
                    DCF outcomes are sensitive to WACC and
                    terminal-growth assumptions.
                </li>

                <li>
                    Forecast accuracy depends on operating
                    margin and cash-conversion execution.
                </li>

                <li>
                    Debt and pension adjustments materially
                    affect equity value.
                </li>

                <li>
                    Scenario labels should be interpreted
                    according to the underlying Excel model.
                </li>
            </ul>
        </div>
        """
    )


# =====================================================
# CONSISTENCY CHECK
# =====================================================

base_difference = (
    base_value
    - float(DCF_BASE)
)

conservative_difference = (
    conservative_value
    - float(DCF_CONSERVATIVE)
)

if (
    abs(base_difference) > 0.01
    or abs(conservative_difference) > 0.01
):

    st.warning(
        "The first-year values in dcf_df differ from "
        "the imported DCF summary values. Check the "
        "Excel cell mapping in utils/data.py."
    )


# =====================================================
# FOOTER
# =====================================================

st.write("")

st.caption(
    """
DCF valuations are sourced automatically from
Finance_Evaluation_VW_v2.xlsx. Values represent implied
share prices in euros. The analysis is for educational
and investment research purposes only.
    """
)