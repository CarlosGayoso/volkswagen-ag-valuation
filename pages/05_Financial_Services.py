import pandas as pd
import streamlit as st

from utils.styles import (
    load_css,
    metric_card,
)

from utils.data import finance_df

from utils.charts import finance_chart


# =====================================================
# GLOBAL STYLES
# =====================================================

load_css()


# =====================================================
# DATA VALIDATION
# =====================================================

required_columns = {
    "Year",
    "Book Value",
    "P/B",
    "Value",
}

missing_columns = (
    required_columns
    - set(finance_df.columns)
)

if missing_columns:

    st.error(
        "The Financial Services dataset is missing "
        "the following columns: "
        f"{', '.join(sorted(missing_columns))}"
    )

    st.stop()


# =====================================================
# DATA PREPARATION
# =====================================================

valuation_df = (
    finance_df
    .copy()
    .sort_values("Year")
    .reset_index(drop=True)
)

numeric_columns = [
    "Year",
    "Book Value",
    "P/B",
    "Value",
]

for column in numeric_columns:

    valuation_df[column] = pd.to_numeric(
        valuation_df[column],
        errors="coerce",
    )

if valuation_df[numeric_columns].isna().any().any():

    st.error(
        "The Financial Services dataset contains "
        "invalid or empty numeric values."
    )

    st.stop()


# =====================================================
# CURRENT AND FORECAST VALUES
# =====================================================

first_year = int(
    valuation_df["Year"].iloc[0]
)

last_year = int(
    valuation_df["Year"].iloc[-1]
)

book_value_start = float(
    valuation_df["Book Value"].iloc[0]
)

book_value_end = float(
    valuation_df["Book Value"].iloc[-1]
)

equity_value_start = float(
    valuation_df["Value"].iloc[0]
)

equity_value_end = float(
    valuation_df["Value"].iloc[-1]
)

pb_start = float(
    valuation_df["P/B"].iloc[0]
)

pb_end = float(
    valuation_df["P/B"].iloc[-1]
)

number_of_periods = (
    len(valuation_df) - 1
)


# =====================================================
# GROWTH CALCULATIONS
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


book_value_cagr = calculate_cagr(
    book_value_start,
    book_value_end,
    number_of_periods,
)

equity_value_cagr = calculate_cagr(
    equity_value_start,
    equity_value_end,
    number_of_periods,
)

book_value_growth = (
    (
        book_value_end
        / book_value_start
    )
    - 1
) * 100

equity_value_growth = (
    (
        equity_value_end
        / equity_value_start
    )
    - 1
) * 100

pb_change = (
    pb_end
    - pb_start
)


# =====================================================
# IMPLIED VALUE CHECK
# =====================================================

valuation_df["Calculated Value"] = (
    valuation_df["Book Value"]
    * valuation_df["P/B"]
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
            Financial Services
        </div>

        <div style="
            margin-top:10px;
            color:#DCEBFF;
            font-size:17px;
        ">
            Book value development and P/B valuation
        </div>

        <div style="
            margin-top:16px;
            color:rgba(255,255,255,0.82);
            font-size:14px;
        ">
            Financial Services equity value forecast
        </div>
    </div>
    """
)


# =====================================================
# KPI CARDS
# =====================================================

book_value_column, growth_column, multiple_column, value_column = (
    st.columns(
        4,
        gap="medium",
    )
)

with book_value_column:

    metric_card(
        title=f"{last_year} Book Value",
        value=f"€{book_value_end:,.1f}bn",
        delta=(
            f"+{book_value_growth:.1f}% "
            f"vs. {first_year}"
        ),
        color="#38BDF8",
    )

with growth_column:

    metric_card(
        title="Book Value CAGR",
        value=f"{book_value_cagr:.1f}%",
        delta=(
            f"{first_year}–{last_year}"
        ),
        color="#FFFFFF",
    )

with multiple_column:

    metric_card(
        title="P/B Multiple",
        value=f"{pb_end:.2f}x",
        delta=(
            f"{pb_change:+.2f}x "
            f"vs. {first_year}"
        ),
        color="#F59E0B",
    )

with value_column:

    metric_card(
        title=f"{last_year} Equity Value",
        value=f"€{equity_value_end:,.1f}bn",
        delta=(
            f"+{equity_value_growth:.1f}% "
            f"vs. {first_year}"
        ),
        color="#22C55E",
    )


# =====================================================
# MAIN CHART
# =====================================================

st.write("")

financial_services_figure = finance_chart(
    valuation_df
)

st.plotly_chart(
    financial_services_figure,
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
                Financial Services book value increases
                from
                <strong style="color:#38BDF8;">
                    €{book_value_start:,.1f}bn
                </strong>
                in {first_year} to
                <strong style="color:#38BDF8;">
                    €{book_value_end:,.1f}bn
                </strong>
                in {last_year}.
            </p>

            <p>
                This represents cumulative growth of
                <strong style="color:#F8FAFC;">
                    {book_value_growth:.1f}%
                </strong>
                and a compound annual growth rate of
                <strong style="color:#F8FAFC;">
                    {book_value_cagr:.1f}%
                </strong>.
            </p>

            <p>
                Applying a
                <strong style="color:#F59E0B;">
                    {pb_end:.2f}x P/B multiple
                </strong>
                results in an implied equity value of
                <strong style="color:#22C55E;">
                    €{equity_value_end:,.1f}bn
                </strong>
                in {last_year}.
            </p>

            <p>
                Equity value grows at an annualised rate
                of
                <strong style="color:#22C55E;">
                    {equity_value_cagr:.1f}%
                </strong>
                over the forecast period.
            </p>

            <p style="
                margin-bottom:0;
                color:#CBD5E1;
            ">
                With a constant valuation multiple, growth
                in implied equity value is primarily driven
                by the expansion of book value.
            </p>
        </div>
        """
    )

with methodology_column:

    st.html(
        """
        <div class="glass-card">
            <div class="section-header">
                P/B Valuation Framework
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
                    Book Value
                </div>

                <div style="
                    margin-top:6px;
                    color:#E2E8F0;
                    line-height:1.5;
                ">
                    Represents the equity capital attributed
                    to the Financial Services business.
                </div>
            </div>

            <div style="
                margin-bottom:16px;
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
                    P/B Multiple
                </div>

                <div style="
                    margin-top:6px;
                    color:#E2E8F0;
                    line-height:1.5;
                ">
                    The valuation multiple reflects returns,
                    credit quality, funding and capital risk.
                </div>
            </div>

            <div style="
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
                    Equity Value
                </div>

                <div style="
                    margin-top:6px;
                    color:#E2E8F0;
                    line-height:1.5;
                ">
                    Calculated by multiplying projected
                    book value by the selected P/B multiple.
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

credit_column, return_column, capital_column, funding_column = (
    st.columns(
        4,
        gap="medium",
    )
)

with credit_column:

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
                Credit Quality
            </div>

            <p style="
                margin-top:10px;
                margin-bottom:0;
                color:#E2E8F0;
                line-height:1.5;
            ">
                Lower credit losses support profitability,
                capital generation and valuation.
            </p>
        </div>
        """
    )

with return_column:

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
                Return on Equity
            </div>

            <p style="
                margin-top:10px;
                margin-bottom:0;
                color:#E2E8F0;
                line-height:1.5;
            ">
                Stronger returns can justify a higher
                price-to-book valuation multiple.
            </p>
        </div>
        """
    )

with capital_column:

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
                Capital Adequacy
            </div>

            <p style="
                margin-top:10px;
                margin-bottom:0;
                color:#E2E8F0;
                line-height:1.5;
            ">
                Capital strength influences growth capacity,
                risk resilience and distributions.
            </p>
        </div>
        """
    )

with funding_column:

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
                Funding Costs
            </div>

            <p style="
                margin-top:10px;
                margin-bottom:0;
                color:#E2E8F0;
                line-height:1.5;
            ">
                Funding conditions affect net interest
                margins and the value of new business.
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
    f"### Financial Services Forecast: "
    f"{first_year}–{last_year}"
)

display_df = valuation_df[
    [
        "Year",
        "Book Value",
        "P/B",
        "Value",
    ]
].copy()

display_df["Book Value Growth"] = (
    display_df["Book Value"]
    .pct_change()
    * 100
)

display_df["Equity Value Growth"] = (
    display_df["Value"]
    .pct_change()
    * 100
)

display_df["Book Value Growth"] = (
    display_df["Book Value Growth"]
    .fillna(0.0)
)

display_df["Equity Value Growth"] = (
    display_df["Equity Value Growth"]
    .fillna(0.0)
)

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
        "Book Value": (
            st.column_config.NumberColumn(
                "Book Value (€bn)",
                format="€%.2f",
            )
        ),
        "Book Value Growth": (
            st.column_config.NumberColumn(
                "Book Value Growth",
                format="%+.1f%%",
            )
        ),
        "P/B": (
            st.column_config.NumberColumn(
                "P/B Multiple",
                format="%.2fx",
            )
        ),
        "Value": (
            st.column_config.NumberColumn(
                "Equity Value (€bn)",
                format="€%.2f",
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
        "Book Value × P/B by more than €0.01bn. "
        "Check the Excel cell mapping or formulas."
    )


# =====================================================
# FOOTER
# =====================================================

st.write("")

st.caption(
    """
Financial Services forecasts are sourced automatically
from Finance_Evaluation_VW_v2.xlsx. Book value and equity
value figures are expressed in billions of euros.
    """
)