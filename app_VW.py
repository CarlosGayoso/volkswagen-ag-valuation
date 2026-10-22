import streamlit as st


# =====================================================
# PAGE CONFIGURATION
# =====================================================

st.set_page_config(
    page_title="Volkswagen AG Valuation",
    page_icon="🚘",
    layout="wide",
    initial_sidebar_state="expanded",
)


# =====================================================
# PAGE DEFINITIONS
# =====================================================

overview_page = st.Page(
    "pages/00_Home.py",
    title="Overview",
    icon=":material/home:",
    url_path="overview",
    default=True,
)

investment_case_page = st.Page(
    "pages/01_Investment_Case.py",
    title="Investment Case",
    icon=":material/lightbulb:",
    url_path="investment-case",
)

sotp_page = st.Page(
    "pages/02_SOTP_Valuation.py",
    title="SOTP Valuation",
    icon=":material/account_balance:",
    url_path="sotp-valuation",
)

automotive_page = st.Page(
    "pages/03_Automotive.py",
    title="Automotive",
    icon=":material/directions_car:",
    url_path="automotive",
)

china_page = st.Page(
    "pages/04_China_JV.py",
    title="China JV",
    icon=":material/public:",
    url_path="china-jv",
)

financial_services_page = st.Page(
    "pages/05_Financial_Services.py",
    title="Financial Services",
    icon=":material/payments:",
    url_path="financial-services",
)

dcf_page = st.Page(
    "pages/06_DCF.py",
    title="DCF Valuation",
    icon=":material/query_stats:",
    url_path="dcf-valuation",
)

sensitivity_page = st.Page(
    "pages/07_Sensitivity_Risks.py",
    title="Sensitivity & Risks",
    icon=":material/warning:",
    url_path="sensitivity-risks",
)

export_report_page = st.Page(
    "pages/09_Export_Report.py",
    title="Export Report",
    icon=":material/description:",
    url_path="export-report",
)

# =====================================================
# NAVIGATION
# =====================================================

pages = {
    "Volkswagen AG Valuation": [
        overview_page,
        investment_case_page,
        sotp_page,
        automotive_page,
        china_page,
        financial_services_page,
        dcf_page,
        sensitivity_page,
        export_report_page,
    ]
}

navigation = st.navigation(
    pages,
    position="sidebar",
    expanded=True,
)

navigation.run()