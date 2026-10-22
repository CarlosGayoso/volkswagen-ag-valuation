import streamlit as st

from utils.styles import (
    load_css,
    metric_card,
)

from utils.data import automotive_df

from utils.charts import automotive_chart


# =====================================================
# GLOBAL STYLES
# =====================================================

load_css()


# =====================================================
# DATA CALCULATIONS
# =====================================================

revenue_start = float(
    automotive_df["Revenue"].iloc[0]
)

revenue_end = float(
    automotive_df["Revenue"].iloc[-1]
)

ebit_start = float(
    automotive_df["EBIT"].iloc[0]
)

ebit_end = float(
    automotive_df["EBIT"].iloc[-1]
)

number_of_periods = (
    len(automotive_df) - 1
)

revenue_cagr = (
    (
        revenue_end
        / revenue_start
    )
    ** (
        1
        / number_of_periods
    )
    - 1
) * 100

ebit_cagr = (
    (
        ebit_end
        / ebit_start
    )
    ** (
        1
        / number_of_periods
    )
    - 1
) * 100

ebit_margin_start = (
    ebit_start
    / revenue_start
) * 100

ebit_margin_end = (
    ebit_end
    / revenue_end
) * 100

margin_expansion = (
    ebit_margin_end
    - ebit_margin_start
)

revenue_growth = (
    (
        revenue_end
        / revenue_start
    )
    - 1
) * 100

ebit_growth = (
    (
        ebit_end
        / ebit_start
    )
    - 1
) * 100


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
            Automotive
        </div>

        <div style="
            margin-top:10px;
            color:#DCEBFF;
            font-size:17px;
        ">
            Revenue, EBIT and operating margin analysis
        </div>
    </div>
    """
)


# =====================================================
# KPI CARDS
# =====================================================

revenue_column, cagr_column, ebit_column, margin_column = (
    st.columns(
        4,
        gap="medium",
    )
)

with revenue_column:

    metric_card(
        title="2030 Revenue",
        value=f"€{revenue_end:,.1f}bn",
        delta=(
            f"+{revenue_growth:.1f}% "
            "vs. 2025"
        ),
        color="#38BDF8",
    )

with cagr_column:

    metric_card(
        title="Revenue CAGR",
        value=f"{revenue_cagr:.1f}%",
        delta="2025–2030",
        color="#FFFFFF",
    )

with ebit_column:

    metric_card(
        title="2030 EBIT",
        value=f"€{ebit_end:,.1f}bn",
        delta=(
            f"+{ebit_growth:.1f}% "
            "vs. 2025"
        ),
        color="#22C55E",
    )

with margin_column:

    metric_card(
        title="2030 EBIT Margin",
        value=f"{ebit_margin_end:.1f}%",
        delta=(
            f"{margin_expansion:+.1f} pp "
            "vs. 2025"
        ),
        color="#86EFAC",
    )


# =====================================================
# MAIN CHART
# =====================================================

st.write("")

automotive_figure = automotive_chart(
    automotive_df
)

st.plotly_chart(
    automotive_figure,
    width="stretch",
    config={
        "displayModeBar": False,
        "responsive": True,
    },
)


# =====================================================
# ANALYTICAL SUMMARY
# =====================================================

st.write("")

summary_column, drivers_column = st.columns(
    [1.35, 1],
    gap="large",
)

with summary_column:

    st.html(
        f"""
        <div class="glass-card">
            <div class="section-header">
                Operating Outlook
            </div>

            <p>
                Automotive revenue increases from
                <strong style="color:#38BDF8;">
                    €{revenue_start:,.1f}bn
                </strong>
                in 2025 to
                <strong style="color:#38BDF8;">
                    €{revenue_end:,.1f}bn
                </strong>
                in 2030.
            </p>

            <p>
                The model therefore assumes relatively
                moderate revenue growth, equivalent to a
                compound annual growth rate of
                <strong style="color:#F8FAFC;">
                    {revenue_cagr:.1f}%
                </strong>.
            </p>

            <p>
                The principal valuation driver is the
                improvement in profitability. EBIT grows
                from
                <strong style="color:#22C55E;">
                    €{ebit_start:,.1f}bn
                </strong>
                to
                <strong style="color:#22C55E;">
                    €{ebit_end:,.1f}bn
                </strong>.
            </p>

            <p>
                EBIT margin expands from
                <strong style="color:#86EFAC;">
                    {ebit_margin_start:.1f}%
                </strong>
                to
                <strong style="color:#86EFAC;">
                    {ebit_margin_end:.1f}%
                </strong>,
                representing an improvement of
                <strong style="color:#86EFAC;">
                    {margin_expansion:.1f} percentage points
                </strong>.
            </p>
        </div>
        """
    )

with drivers_column:

    st.html(
        """
        <div class="glass-card">
            <div class="section-header">
                Key Value Drivers
            </div>

            <div style="
                margin-bottom:18px;
                padding:15px;
                border-radius:14px;
                background:rgba(56,189,248,0.09);
                border:1px solid rgba(56,189,248,0.18);
            ">
                <div style="
                    color:#38BDF8;
                    font-size:13px;
                    font-weight:750;
                    text-transform:uppercase;
                    letter-spacing:0.8px;
                ">
                    Revenue resilience
                </div>

                <div style="
                    margin-top:6px;
                    color:#E2E8F0;
                    line-height:1.5;
                ">
                    Stable group revenue provides the base
                    for operating leverage.
                </div>
            </div>

            <div style="
                margin-bottom:18px;
                padding:15px;
                border-radius:14px;
                background:rgba(34,197,94,0.09);
                border:1px solid rgba(34,197,94,0.18);
            ">
                <div style="
                    color:#22C55E;
                    font-size:13px;
                    font-weight:750;
                    text-transform:uppercase;
                    letter-spacing:0.8px;
                ">
                    Margin recovery
                </div>

                <div style="
                    margin-top:6px;
                    color:#E2E8F0;
                    line-height:1.5;
                ">
                    EBIT expansion is the primary source
                    of value creation in the forecast.
                </div>
            </div>

            <div style="
                padding:15px;
                border-radius:14px;
                background:rgba(245,158,11,0.09);
                border:1px solid rgba(245,158,11,0.18);
            ">
                <div style="
                    color:#F59E0B;
                    font-size:13px;
                    font-weight:750;
                    text-transform:uppercase;
                    letter-spacing:0.8px;
                ">
                    Execution sensitivity
                </div>

                <div style="
                    margin-top:6px;
                    color:#E2E8F0;
                    line-height:1.5;
                ">
                    The valuation depends more heavily on
                    margin execution than on high revenue
                    growth.
                </div>
            </div>
        </div>
        """
    )


# =====================================================
# FORECAST TABLE
# =====================================================

st.write("")
st.write("")

st.markdown("### Automotive Forecast")

forecast_table = automotive_df.copy()

forecast_table["EBIT Margin"] = (
    forecast_table["EBIT"]
    / forecast_table["Revenue"]
    * 100
)

if "FCF" in forecast_table.columns:

    forecast_table = forecast_table[
        [
            "Year",
            "Revenue",
            "EBIT",
            "EBIT Margin",
            "FCF",
        ]
    ]

else:

    forecast_table = forecast_table[
        [
            "Year",
            "Revenue",
            "EBIT",
            "EBIT Margin",
        ]
    ]


formatting = {
    "Year": st.column_config.NumberColumn(
        "Year",
        format="%d",
    ),
    "Revenue": st.column_config.NumberColumn(
        "Revenue (€bn)",
        format="€%.1f",
    ),
    "EBIT": st.column_config.NumberColumn(
        "EBIT (€bn)",
        format="€%.1f",
    ),
    "EBIT Margin": st.column_config.NumberColumn(
        "EBIT Margin",
        format="%.1f%%",
    ),
}

if "FCF" in forecast_table.columns:

    formatting["FCF"] = (
        st.column_config.NumberColumn(
            "FCF (€bn)",
            format="€%.1f",
        )
    )

st.dataframe(
    forecast_table,
    width="stretch",
    hide_index=True,
    column_config=formatting,
)


# =====================================================
# FOOTER NOTE
# =====================================================

st.write("")

st.caption(
    """
Automotive forecasts are sourced from the Volkswagen
valuation model. Revenue, EBIT and free cash flow figures
are expressed in billions of euros.
    """
)