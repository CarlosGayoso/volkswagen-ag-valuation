import pandas as pd
import streamlit as st

from utils.styles import (
    load_css,
    metric_card,
)

from utils.data import china_df

from utils.charts import china_chart


# =====================================================
# GLOBAL STYLES
# =====================================================

load_css()


# =====================================================
# DATA VALIDATION
# =====================================================

required_columns = {
    "Year",
    "Net Income",
    "P/E",
    "Value",
}

missing_columns = (
    required_columns
    - set(china_df.columns)
)

if missing_columns:

    st.error(
        "The China JV dataset is missing the following "
        f"columns: {', '.join(sorted(missing_columns))}"
    )

    st.stop()


# =====================================================
# DATA PREPARATION
# =====================================================

valuation_df = (
    china_df
    .copy()
    .sort_values("Year")
    .reset_index(drop=True)
)

numeric_columns = [
    "Year",
    "Net Income",
    "P/E",
    "Value",
]

for column in numeric_columns:

    valuation_df[column] = pd.to_numeric(
        valuation_df[column],
        errors="coerce",
    )

if valuation_df[numeric_columns].isna().any().any():

    st.error(
        "The China JV dataset contains invalid or "
        "empty numeric values."
    )

    st.stop()


# =====================================================
# FORECAST PERIOD
# =====================================================

first_year = int(
    valuation_df["Year"].iloc[0]
)

last_year = int(
    valuation_df["Year"].iloc[-1]
)

net_income_start = float(
    valuation_df["Net Income"].iloc[0]
)

net_income_end = float(
    valuation_df["Net Income"].iloc[-1]
)

value_start = float(
    valuation_df["Value"].iloc[0]
)

value_end = float(
    valuation_df["Value"].iloc[-1]
)

pe_start = float(
    valuation_df["P/E"].iloc[0]
)

pe_end = float(
    valuation_df["P/E"].iloc[-1]
)

number_of_periods = (
    len(valuation_df) - 1
)


# =====================================================
# CALCULATION HELPERS
# =====================================================

def calculate_cagr(
    initial_value,
    final_value,
    periods,
):

    if (
        periods <= 0
        or initial_value <= 0
        or final_value <= 0
    ):
        return 0.0

    return (
        (
            final_value
            / initial_value
        )
        ** (
            1 / periods
        )
        - 1
    ) * 100


net_income_cagr = calculate_cagr(
    net_income_start,
    net_income_end,
    number_of_periods,
)

value_cagr = calculate_cagr(
    value_start,
    value_end,
    number_of_periods,
)

net_income_growth = (
    (
        net_income_end
        / net_income_start
    )
    - 1
) * 100

value_growth = (
    (
        value_end
        / value_start
    )
    - 1
) * 100

pe_change = (
    pe_end
    - pe_start
)


# =====================================================
# IMPLIED VALUE CONSISTENCY
# =====================================================

valuation_df["Calculated Value"] = (
    valuation_df["Net Income"]
    * valuation_df["P/E"]
)

valuation_df["Calculation Difference"] = (
    valuation_df["Value"]
    - valuation_df["Calculated Value"]
)

maximum_calculation_difference = float(
    valuation_df[
        "Calculation Difference"
    ]
    .abs()
    .max()
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
                rgba(245,158,11,0.25),
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
            China Joint Ventures
        </div>

        <div style="
            margin-top:10px;
            color:#DCEBFF;
            font-size:17px;
        ">
            Net income contribution and P/E valuation
        </div>

        <div style="
            margin-top:16px;
            color:rgba(255,255,255,0.82);
            font-size:14px;
        ">
            Standalone valuation outside the
            Automotive business
        </div>
    </div>
    """
)


# =====================================================
# KPI CARDS
# =====================================================

income_column, growth_column, multiple_column, value_column = (
    st.columns(
        4,
        gap="medium",
    )
)

with income_column:

    metric_card(
        title=f"{last_year} Net Income",
        value=f"€{net_income_end:,.2f}bn",
        delta=(
            f"{net_income_growth:+.1f}% "
            f"vs. {first_year}"
        ),
        color="#F59E0B",
    )

with growth_column:

    metric_card(
        title="Net Income CAGR",
        value=f"{net_income_cagr:.1f}%",
        delta=(
            f"{first_year} to {last_year}"
        ),
        color="#FFFFFF",
    )

with multiple_column:

    metric_card(
        title="P/E Multiple",
        value=f"{pe_end:.1f}x",
        delta=(
            f"{pe_change:+.1f}x "
            f"vs. {first_year}"
        ),
        color="#38BDF8",
    )

with value_column:

    metric_card(
        title=f"{last_year} Equity Value",
        value=f"€{value_end:,.2f}bn",
        delta=(
            f"{value_growth:+.1f}% "
            f"vs. {first_year}"
        ),
        color="#22C55E",
    )


# =====================================================
# MAIN CHART
# =====================================================

st.write("")

china_figure = china_chart(
    valuation_df
)

st.plotly_chart(
    china_figure,
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

interpretation_column, methodology_column = (
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
                China Joint Ventures net income changes
                from
                <strong style="color:#F59E0B;">
                    €{net_income_start:,.2f}bn
                </strong>
                in {first_year} to
                <strong style="color:#F59E0B;">
                    €{net_income_end:,.2f}bn
                </strong>
                in {last_year}.
            </p>

            <p>
                This represents cumulative growth of
                <strong style="color:#F8FAFC;">
                    {net_income_growth:+.1f}%
                </strong>
                and an annualised growth rate of
                <strong style="color:#F8FAFC;">
                    {net_income_cagr:.1f}%
                </strong>.
            </p>

            <p>
                Applying a
                <strong style="color:#38BDF8;">
                    {pe_end:.1f}x P/E multiple
                </strong>
                produces an implied equity value of
                <strong style="color:#22C55E;">
                    €{value_end:,.2f}bn
                </strong>
                in {last_year}.
            </p>

            <p>
                The implied value changes by
                <strong style="color:#22C55E;">
                    {value_growth:+.1f}%
                </strong>
                over the complete forecast period.
            </p>

            <p style="
                margin-bottom:0;
                color:#CBD5E1;
            ">
                When the valuation multiple remains stable,
                equity value is primarily determined by
                projected net income.
            </p>
        </div>
        """
    )

with methodology_column:

    st.html(
        """
        <div class="glass-card">
            <div class="section-header">
                P/E Valuation Framework
            </div>

            <div style="
                margin-bottom:16px;
                padding:15px;
                border-radius:14px;
                background:rgba(245,158,11,0.09);
                border:1px solid rgba(245,158,11,0.18);
            ">
                <div style="
                    color:#F59E0B;
                    font-size:13px;
                    font-weight:750;
                    letter-spacing:0.8px;
                    text-transform:uppercase;
                ">
                    Net Income
                </div>

                <div style="
                    margin-top:6px;
                    color:#E2E8F0;
                    line-height:1.5;
                ">
                    Earnings attributable to Volkswagen
                    from the China joint ventures.
                </div>
            </div>

            <div style="
                margin-bottom:16px;
                padding:15px;
                border-radius:14px;
                background:rgba(56,189,248,0.09);
                border:1px solid rgba(56,189,248,0.18);
            ">
                <div style="
                    color:#38BDF8;
                    font-size:13px;
                    font-weight:750;
                    letter-spacing:0.8px;
                    text-transform:uppercase;
                ">
                    P/E Multiple
                </div>

                <div style="
                    margin-top:6px;
                    color:#E2E8F0;
                    line-height:1.5;
                ">
                    The multiple reflects growth,
                    competitive and geopolitical risks.
                </div>
            </div>

            <div style="
                padding:15px;
                border-radius:14px;
                background:rgba(34,197,94,0.09);
                border:1px solid rgba(34,197,94,0.18);
            ">
                <div style="
                    color:#22C55E;
                    font-size:13px;
                    font-weight:750;
                    letter-spacing:0.8px;
                    text-transform:uppercase;
                ">
                    Equity Value
                </div>

                <div style="
                    margin-top:6px;
                    color:#E2E8F0;
                    line-height:1.5;
                ">
                    Calculated by multiplying projected
                    net income by the selected P/E multiple.
                </div>
            </div>
        </div>
        """
    )


# =====================================================
# KEY VALUE DRIVERS
# =====================================================

st.write("")
st.write("")

st.markdown("### Key Value Drivers")

earnings_column, multiple_driver_column, competition_column, risk_column = (
    st.columns(
        4,
        gap="medium",
    )
)

with earnings_column:

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
                Earnings Growth
            </div>

            <p style="
                margin-top:10px;
                margin-bottom:0;
                color:#E2E8F0;
                line-height:1.5;
            ">
                Higher joint venture earnings directly
                increase the implied equity value.
            </p>
        </div>
        """
    )

with multiple_driver_column:

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
                Valuation Multiple
            </div>

            <p style="
                margin-top:10px;
                margin-bottom:0;
                color:#E2E8F0;
                line-height:1.5;
            ">
                A higher or lower P/E assumption has an
                immediate impact on equity value.
            </p>
        </div>
        """
    )

with competition_column:

    st.html(
        """
        <div class="glass-card">
            <div style="
                color:#22C55E;
                font-size:13px;
                font-weight:750;
                letter-spacing:0.8px;
                text-transform:uppercase;
            ">
                Market Position
            </div>

            <p style="
                margin-top:10px;
                margin-bottom:0;
                color:#E2E8F0;
                line-height:1.5;
            ">
                Market share, product competitiveness
                and pricing influence earnings quality.
            </p>
        </div>
        """
    )

with risk_column:

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
                Risk Discount
            </div>

            <p style="
                margin-top:10px;
                margin-bottom:0;
                color:#E2E8F0;
                line-height:1.5;
            ">
                Competitive, regulatory and geopolitical
                risks can constrain the P/E multiple.
            </p>
        </div>
        """
    )


# =====================================================
# FORECAST TABLE
# =====================================================

st.write("")
st.write("")

st.markdown(
    f"### China JV Forecast: {first_year} to {last_year}"
)

display_df = valuation_df[
    [
        "Year",
        "Net Income",
        "P/E",
        "Value",
    ]
].copy()

display_df["Net Income Growth"] = (
    display_df["Net Income"]
    .pct_change()
    * 100
)

display_df["Equity Value Growth"] = (
    display_df["Value"]
    .pct_change()
    * 100
)

display_df["Net Income Growth"] = (
    display_df["Net Income Growth"]
    .fillna(0.0)
)

display_df["Equity Value Growth"] = (
    display_df["Equity Value Growth"]
    .fillna(0.0)
)

display_df = display_df[
    [
        "Year",
        "Net Income",
        "Net Income Growth",
        "P/E",
        "Value",
        "Equity Value Growth",
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
        "Net Income": (
            st.column_config.NumberColumn(
                "Net Income (€bn)",
                format="€%.3f",
            )
        ),
        "Net Income Growth": (
            st.column_config.NumberColumn(
                "Net Income Growth",
                format="%+.1f%%",
            )
        ),
        "P/E": (
            st.column_config.NumberColumn(
                "P/E Multiple",
                format="%.1fx",
            )
        ),
        "Value": (
            st.column_config.NumberColumn(
                "Equity Value (€bn)",
                format="€%.3f",
            )
        ),
        "Equity Value Growth": (
            st.column_config.NumberColumn(
                "Equity Value Growth",
                format="%+.1f%%",
            )
        ),
    },
)


# =====================================================
# MODEL CHECK
# =====================================================

if maximum_calculation_difference > 0.01:

    st.warning(
        "The imported equity values differ from "
        "Net Income × P/E by more than €0.01bn. "
        "Check the Excel formulas or cell mapping."
    )


# =====================================================
# FOOTER
# =====================================================

st.write("")

st.caption(
    """
China Joint Ventures forecasts are sourced automatically
from Finance_Evaluation_VW_v2.xlsx. Net income and equity
value figures are expressed in billions of euros.
    """
)