from pathlib import Path

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
    sotp_df,
    automotive_df,
    china_df,
    finance_df,
    dcf_df,
)

from utils.report import create_report


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
                rgba(167,139,250,0.24),
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
            Export Research Report
        </div>

        <div style="
            margin-top:10px;
            color:#DCEBFF;
            font-size:17px;
        ">
            Generate a consolidated Volkswagen AG
            equity research report
        </div>
    </div>
    """
)


# =====================================================
# REPORT SETTINGS
# =====================================================

st.markdown("### Report Configuration")

settings_column, preview_column = st.columns(
    [1, 1.45],
    gap="large",
)

with settings_column:

    analyst_name = st.text_input(
        "Analyst",
        value="Carlos Gayoso",
    )

    report_date = st.date_input(
        "Report date",
    )

    report_title = st.text_input(
        "Report title",
        value=(
            "Volkswagen AG Equity Research "
            "and Valuation Report"
        ),
    )

    include_appendix = st.checkbox(
        "Include forecast appendix",
        value=True,
    )

    include_methodology = st.checkbox(
        "Include valuation methodology",
        value=True,
    )

with preview_column:

    investment_rating = (
        "BUY"
        if UPSIDE >= 30
        else "HOLD"
        if UPSIDE >= 10
        else "REDUCE"
    )

    st.html(
        f"""
        <div class="glass-card">
            <div class="section-header">
                Report Preview
            </div>

            <div style="
                display:flex;
                justify-content:space-between;
                margin-bottom:14px;
            ">
                <span style="color:#94A3B8;">
                    Rating
                </span>

                <strong style="color:#22C55E;">
                    {investment_rating}
                </strong>
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
                    €{CURRENT_PRICE:.2f}
                </strong>
            </div>

            <div style="
                display:flex;
                justify-content:space-between;
                margin-bottom:14px;
            ">
                <span style="color:#94A3B8;">
                    DCF fair value
                </span>

                <strong style="color:#22C55E;">
                    €{DCF_BASE:.2f}
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
                    €{DCF_CONSERVATIVE:.2f}
                </strong>
            </div>

            <div style="
                display:flex;
                justify-content:space-between;
            ">
                <span style="color:#94A3B8;">
                    Base upside
                </span>

                <strong style="color:#22C55E;">
                    {UPSIDE:.1f}%
                </strong>
            </div>
        </div>
        """
    )


# =====================================================
# REPORT CONTENT
# =====================================================

st.write("")
st.markdown("### Included Research Sections")

sections = [
    "Executive summary",
    "Valuation snapshot",
    "Investment thesis",
    "SOTP valuation",
    "Automotive outlook",
    "China Joint Ventures",
    "Financial Services",
    "DCF scenario analysis",
    "Catalysts and risks",
    "Investment conclusion",
]

for section in sections:
    st.markdown(f"- {section}")


# =====================================================
# GENERATE REPORT
# =====================================================

st.write("")

generate_report = st.button(
    "Generate Word Report",
    type="primary",
    width="stretch",
)

if generate_report:

    with st.spinner(
        "Generating Volkswagen AG research report..."
    ):

        report_path = create_report(
            report_title=report_title,
            report_date=report_date,
            analyst_name=analyst_name,
            current_price=CURRENT_PRICE,
            dcf_base=DCF_BASE,
            dcf_conservative=DCF_CONSERVATIVE,
            upside=UPSIDE,
            conservative_upside=(
                CONSERVATIVE_UPSIDE
            ),
            sotp_value=SOTP_VALUE,
            sotp_df=sotp_df,
            automotive_df=automotive_df,
            china_df=china_df,
            finance_df=finance_df,
            dcf_df=dcf_df,
            include_appendix=include_appendix,
            include_methodology=(
                include_methodology
            ),
        )

    report_path = Path(report_path)

    if report_path.exists():

        st.success(
            "Volkswagen AG research report generated."
        )

        report_bytes = report_path.read_bytes()

        st.download_button(
            label="Download Word Report",
            data=report_bytes,
            file_name=report_path.name,
            mime=(
                "application/vnd.openxmlformats-"
                "officedocument.wordprocessingml.document"
            ),
            width="stretch",
        )

    else:

        st.error(
            "The report could not be generated."
        )