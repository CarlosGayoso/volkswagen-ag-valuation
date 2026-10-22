import streamlit as st

from utils.styles import (
    load_css,
    metric_card,
)

from utils.data import (
    sotp_df,
    SOTP_VALUE,
)

from utils.charts import (
    sotp_waterfall,
    business_mix,
)


# =====================================================
# GLOBAL STYLES
# =====================================================

load_css()


# =====================================================
# DATA PREPARATION
# =====================================================

required_columns = {
    "Business",
    "Value",
}

missing_columns = (
    required_columns
    - set(sotp_df.columns)
)

if missing_columns:
    st.error(
        "The SOTP dataset is missing the following "
        f"columns: {', '.join(sorted(missing_columns))}"
    )
    st.stop()


valuation_df = sotp_df.copy()

valuation_df["Value"] = (
    valuation_df["Value"]
    .astype(float)
)

calculated_sotp_value = float(
    valuation_df["Value"].sum()
)

valuation_df["Weight"] = (
    valuation_df["Value"]
    / calculated_sotp_value
    * 100
)


# =====================================================
# BUSINESS VALUE HELPER
# =====================================================

def get_business_value(
    business_name,
):
    matching_rows = valuation_df.loc[
        valuation_df["Business"]
        == business_name,
        "Value",
    ]

    if matching_rows.empty:
        return 0.0

    return float(
        matching_rows.iloc[0]
    )


automotive_value = get_business_value(
    "Automotive"
)

china_value = get_business_value(
    "China JV"
)

finance_value = get_business_value(
    "Financial Services"
)


def calculate_weight(value):
    if calculated_sotp_value == 0:
        return 0.0

    return (
        value
        / calculated_sotp_value
        * 100
    )


automotive_weight = calculate_weight(
    automotive_value
)

china_weight = calculate_weight(
    china_value
)

finance_weight = calculate_weight(
    finance_value
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
                rgba(56,189,248,0.26),
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
            Sum-of-the-Parts Valuation
        </div>

        <div style="
            margin-top:10px;
            color:#DCEBFF;
            font-size:17px;
        ">
            Automotive, China JV and Financial Services
        </div>

        <div style="
            margin-top:16px;
            color:rgba(255,255,255,0.82);
            font-size:14px;
        ">
            2026 equity value by business segment
        </div>
    </div>
    """
)


# =====================================================
# KPI CARDS
# =====================================================

total_column, automotive_column, china_column, finance_column = (
    st.columns(
        4,
        gap="medium",
    )
)

with total_column:
    metric_card(
        title="Total SOTP Value",
        value=(
            f"€{calculated_sotp_value:,.1f}bn"
        ),
        delta="2026 equity value",
        color="#F8FAFC",
    )

with automotive_column:
    metric_card(
        title="Automotive",
        value=(
            f"€{automotive_value:,.1f}bn"
        ),
        delta=(
            f"{automotive_weight:.1f}% "
            "of total value"
        ),
        color="#38BDF8",
    )

with china_column:
    metric_card(
        title="China JV",
        value=(
            f"€{china_value:,.1f}bn"
        ),
        delta=(
            f"{china_weight:.1f}% "
            "of total value"
        ),
        color="#F59E0B",
    )

with finance_column:
    metric_card(
        title="Financial Services",
        value=(
            f"€{finance_value:,.1f}bn"
        ),
        delta=(
            f"{finance_weight:.1f}% "
            "of total value"
        ),
        color="#22C55E",
    )


# =====================================================
# VALUATION CHARTS
# =====================================================

st.write("")

waterfall_column, mix_column = st.columns(
    [1.55, 1],
    gap="large",
)

plotly_config = {
    "displayModeBar": False,
    "responsive": True,
}

with waterfall_column:
    waterfall_figure = sotp_waterfall(
        valuation_df
    )

    st.plotly_chart(
        waterfall_figure,
        width="stretch",
        config=plotly_config,
    )

with mix_column:
    mix_figure = business_mix(
        valuation_df
    )

    st.plotly_chart(
        mix_figure,
        width="stretch",
        config=plotly_config,
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
                The sum-of-the-parts analysis produces
                a total equity value of
                <strong style="color:#F8FAFC;">
                    €{calculated_sotp_value:,.1f}bn
                </strong>.
            </p>

            <p>
                Automotive contributes
                <strong style="color:#38BDF8;">
                    €{automotive_value:,.1f}bn
                </strong>,
                representing
                <strong style="color:#38BDF8;">
                    {automotive_weight:.1f}%
                </strong>
                of total SOTP value.
            </p>

            <p>
                Financial Services contributes
                <strong style="color:#22C55E;">
                    €{finance_value:,.1f}bn
                </strong>,
                equivalent to
                <strong style="color:#22C55E;">
                    {finance_weight:.1f}%
                </strong>
                of the total.
            </p>

            <p>
                China Joint Ventures contribute
                <strong style="color:#F59E0B;">
                    €{china_value:,.1f}bn
                </strong>,
                representing
                <strong style="color:#F59E0B;">
                    {china_weight:.1f}%
                </strong>
                of the group valuation.
            </p>

            <p style="
                margin-bottom:0;
                color:#CBD5E1;
            ">
                The valuation therefore depends primarily
                on Automotive execution and recognition of
                the Financial Services franchise value.
            </p>
        </div>
        """
    )

with methodology_column:
    st.html(
        """
        <div class="glass-card">
            <div class="section-header">
                Valuation Methods
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
                    Automotive
                </div>

                <div style="
                    margin-top:6px;
                    color:#E2E8F0;
                    line-height:1.5;
                ">
                    Free cash flow and operating
                    performance valuation.
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
                    China JV
                </div>

                <div style="
                    margin-top:6px;
                    color:#E2E8F0;
                    line-height:1.5;
                ">
                    P/E multiple applied to projected
                    net income.
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
                    Financial Services
                </div>

                <div style="
                    margin-top:6px;
                    color:#E2E8F0;
                    line-height:1.5;
                ">
                    P/B multiple applied to projected
                    book value.
                </div>
            </div>
        </div>
        """
    )


# =====================================================
# VALUATION TABLE
# =====================================================

st.write("")
st.write("")

st.markdown(
    "### Business Valuation Detail"
)

display_df = valuation_df.copy()

display_df["Value per €100 of SOTP"] = (
    display_df["Weight"]
)

st.dataframe(
    display_df,
    width="stretch",
    hide_index=True,
    column_order=[
        "Business",
        "Value",
        "Weight",
    ],
    column_config={
        "Business": (
            st.column_config.TextColumn(
                "Business",
                width="medium",
            )
        ),
        "Value": (
            st.column_config.NumberColumn(
                "Equity Value (€bn)",
                format="€%.2f",
            )
        ),
        "Weight": (
            st.column_config.ProgressColumn(
                "SOTP Weight",
                format="%.1f%%",
                min_value=0,
                max_value=100,
            )
        ),
    },
)


# =====================================================
# CONSISTENCY NOTE
# =====================================================

difference = (
    calculated_sotp_value
    - float(SOTP_VALUE)
)

if abs(difference) > 0.01:
    st.warning(
        "The sum of the business values differs from "
        f"the imported SOTP total by €{difference:.2f}bn."
    )


# =====================================================
# FOOTER
# =====================================================

st.write("")

st.caption(
    """
The SOTP valuation is sourced automatically from
Finance_Evaluation_VW_v2.xlsx. All values are expressed
in billions of euros.
    """
)