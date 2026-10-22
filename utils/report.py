from datetime import date, datetime
from pathlib import Path

import pandas as pd
from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Inches, Pt, RGBColor

PROJECT_ROOT = Path(__file__).resolve().parent.parent
REPORT_DIR = PROJECT_ROOT / "generated_reports"
REPORT_DIR.mkdir(parents=True, exist_ok=True)
LOGO_FILE = PROJECT_ROOT / "assets" / "vw_logo.png"

VW_DARK = "001E50"
VW_BLUE = "0057B8"
GREEN = "15803D"
ORANGE = "D97706"
RED = "B91C1C"
WHITE = "FFFFFF"
DARK = "334155"
GREY = "64748B"
LIGHT = "E2E8F0"
PALE = "F8FAFC"


def _rating(upside):
    if upside >= 40:
        return "STRONG BUY"
    if upside >= 20:
        return "BUY"
    if upside >= 0:
        return "HOLD"
    return "SELL"


def _normalise_date(value):
    if isinstance(value, datetime):
        return value.date()
    if isinstance(value, date):
        return value
    return date.today()


def _cagr(start, end, periods):
    if periods <= 0 or start <= 0 or end <= 0:
        return 0.0
    return ((end / start) ** (1 / periods) - 1) * 100


def _upside(value, market_price):
    if market_price == 0:
        return 0.0
    return ((value - market_price) / market_price) * 100


def _shade(cell, colour):
    tc_pr = cell._tc.get_or_add_tcPr()
    shd = tc_pr.find(qn("w:shd"))
    if shd is None:
        shd = OxmlElement("w:shd")
        tc_pr.append(shd)
    shd.set(qn("w:fill"), colour)


def _run_style(run, size=10, bold=False, colour=DARK, font="Aptos"):
    run.font.name = font
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.color.rgb = RGBColor.from_string(colour)
    run._element.get_or_add_rPr()
    run._element.rPr.rFonts.set(qn("w:ascii"), font)
    run._element.rPr.rFonts.set(qn("w:hAnsi"), font)


def _configure_document(doc):
    section = doc.sections[0]
    section.top_margin = Inches(0.65)
    section.bottom_margin = Inches(0.65)
    section.left_margin = Inches(0.72)
    section.right_margin = Inches(0.72)

    normal = doc.styles["Normal"]
    normal.font.name = "Aptos"
    normal.font.size = Pt(10)
    normal.font.color.rgb = RGBColor.from_string(DARK)
    normal.paragraph_format.space_after = Pt(6)

    for name, size, colour in [
        ("Title", 30, VW_DARK),
        ("Heading 1", 19, VW_DARK),
        ("Heading 2", 14, VW_BLUE),
    ]:
        style = doc.styles[name]
        style.font.name = "Aptos Display"
        style.font.size = Pt(size)
        style.font.bold = True
        style.font.color.rgb = RGBColor.from_string(colour)


def _heading(doc, text, level=1):
    paragraph = doc.add_heading(text, level=level)
    paragraph.paragraph_format.space_before = Pt(10)
    paragraph.paragraph_format.space_after = Pt(6)
    return paragraph


def _paragraph(doc, text):
    paragraph = doc.add_paragraph()
    run = paragraph.add_run(text)
    _run_style(run)
    return paragraph


def _bullet(doc, text):
    paragraph = doc.add_paragraph(style="List Bullet")
    run = paragraph.add_run(text)
    _run_style(run)
    return paragraph


def _kpis(doc, items):
    table = doc.add_table(rows=1, cols=len(items))
    table.autofit = True

    for index, item in enumerate(items):
        cell = table.rows[0].cells[index]
        _shade(cell, item.get("background", PALE))

        label = cell.paragraphs[0]
        label.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = label.add_run(item["label"].upper())
        _run_style(run, size=8, bold=True, colour=GREY)

        value = cell.add_paragraph()
        value.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = value.add_run(item["value"])
        _run_style(
            run,
            size=17,
            bold=True,
            colour=item.get("colour", VW_DARK),
            font="Aptos Display",
        )

        detail = item.get("detail")
        if detail:
            detail_paragraph = cell.add_paragraph()
            detail_paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
            run = detail_paragraph.add_run(detail)
            _run_style(run, size=8, colour=GREY)

    doc.add_paragraph()


def _table(doc, dataframe, formats=None):
    formats = formats or {}
    table = doc.add_table(rows=1, cols=len(dataframe.columns))
    table.style = "Table Grid"

    for index, column in enumerate(dataframe.columns):
        cell = table.rows[0].cells[index]
        _shade(cell, VW_DARK)
        paragraph = cell.paragraphs[0]
        paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = paragraph.add_run(str(column))
        _run_style(run, size=8, bold=True, colour=WHITE)

    for row_index, (_, row) in enumerate(dataframe.iterrows()):
        cells = table.add_row().cells
        for column_index, column in enumerate(dataframe.columns):
            cell = cells[column_index]
            if row_index % 2:
                _shade(cell, PALE)
            value = row[column]
            formatter = formats.get(column)
            text = formatter(value) if formatter else str(value)
            paragraph = cell.paragraphs[0]
            paragraph.alignment = (
                WD_ALIGN_PARAGRAPH.LEFT
                if column_index == 0
                else WD_ALIGN_PARAGRAPH.RIGHT
            )
            run = paragraph.add_run(text)
            _run_style(run, size=8)

    doc.add_paragraph()
    return table


def _cover(
    doc,
    report_title,
    report_date,
    analyst_name,
    rating,
    current_price,
    dcf_base,
    dcf_conservative,
    upside,
):
    if LOGO_FILE.exists():
        logo = doc.add_paragraph()
        logo.alignment = WD_ALIGN_PARAGRAPH.CENTER
        logo.add_run().add_picture(str(LOGO_FILE), width=Inches(1.2))

    title = doc.add_paragraph()
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    title.paragraph_format.space_before = Pt(22)
    run = title.add_run("VOLKSWAGEN AG")
    _run_style(run, size=31, bold=True, colour=VW_DARK, font="Aptos Display")

    subtitle = doc.add_paragraph()
    subtitle.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = subtitle.add_run(report_title)
    _run_style(run, size=17, bold=True, colour=VW_BLUE, font="Aptos Display")

    metadata = doc.add_paragraph()
    metadata.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = metadata.add_run(
        f"{report_date.strftime('%d %B %Y')} | {analyst_name}"
    )
    _run_style(run, size=10, colour=GREY)

    doc.add_paragraph()
    _kpis(
        doc,
        [
            {
                "label": "Rating",
                "value": rating,
                "detail": "Investment view",
                "colour": GREEN if upside >= 0 else RED,
            },
            {
                "label": "Market Price",
                "value": f"€{current_price:.2f}",
                "detail": "Reference price",
            },
            {
                "label": "Base Fair Value",
                "value": f"€{dcf_base:.2f}",
                "detail": f"{upside:+.1f}% upside",
                "colour": GREEN,
            },
            {
                "label": "Conservative",
                "value": f"€{dcf_conservative:.2f}",
                "detail": "DCF by business",
                "colour": VW_BLUE,
            },
        ],
    )

    _heading(doc, "Investment Snapshot")
    _bullet(doc, "The base DCF remains above the reference market price.")
    _bullet(doc, "Automotive margin recovery is the central value driver.")
    _bullet(doc, "China JV and Financial Services provide standalone value.")
    _bullet(doc, "Execution, capital intensity and competition are key risks.")
    doc.add_page_break()


def _add_footer(doc):
    for section in doc.sections:
        footer = section.footer
        paragraph = footer.paragraphs[0]
        paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = paragraph.add_run(
            "Volkswagen AG Equity Research | Educational and research purposes only"
        )
        _run_style(run, size=8, colour=GREY)


def create_report(
    report_title,
    report_date,
    analyst_name,
    current_price,
    dcf_base,
    dcf_conservative,
    upside,
    conservative_upside,
    sotp_value,
    sotp_df,
    automotive_df,
    china_df,
    finance_df,
    dcf_df,
    include_appendix=True,
    include_methodology=True,
):
    """Create the consolidated Volkswagen AG Word research report."""

    report_date = _normalise_date(report_date)
    rating = _rating(upside)

    sotp = sotp_df.copy()
    automotive = automotive_df.copy().sort_values("Year").reset_index(drop=True)
    china = china_df.copy().sort_values("Year").reset_index(drop=True)
    finance = finance_df.copy().sort_values("Year").reset_index(drop=True)
    dcf = dcf_df.copy().sort_values("Year").reset_index(drop=True)

    auto_start = automotive.iloc[0]
    auto_end = automotive.iloc[-1]
    revenue_start = float(auto_start["Revenue"])
    revenue_end = float(auto_end["Revenue"])
    ebit_start = float(auto_start["EBIT"])
    ebit_end = float(auto_end["EBIT"])
    margin_start = ebit_start / revenue_start * 100
    margin_end = ebit_end / revenue_end * 100
    revenue_cagr = _cagr(revenue_start, revenue_end, len(automotive) - 1)
    ebit_cagr = _cagr(ebit_start, ebit_end, len(automotive) - 1)

    china_forecast = china.loc[china["Year"] >= 2026].reset_index(drop=True)
    if china_forecast.empty:
        china_forecast = china
    china_start = china_forecast.iloc[0]
    china_end = china_forecast.iloc[-1]

    finance_start = finance.iloc[0]
    finance_end = finance.iloc[-1]

    sotp_total = float(sotp["Value"].sum())
    sotp["Weight"] = sotp["Value"] / sotp_total * 100

    doc = Document()
    _configure_document(doc)
    doc.core_properties.author = analyst_name
    doc.core_properties.title = report_title
    doc.core_properties.subject = "Volkswagen AG valuation"

    _cover(
        doc,
        report_title,
        report_date,
        analyst_name,
        rating,
        current_price,
        dcf_base,
        dcf_conservative,
        upside,
    )

    _heading(doc, "1. Executive Summary")
    _paragraph(
        doc,
        f"Volkswagen AG is rated {rating}. The base DCF fair value is "
        f"€{dcf_base:.2f} per share versus a reference market price of "
        f"€{current_price:.2f}, implying {upside:.1f}% potential upside. "
        f"The conservative valuation is €{dcf_conservative:.2f} per share, "
        f"equivalent to {conservative_upside:.1f}% upside.",
    )
    _paragraph(
        doc,
        "The investment case depends primarily on Automotive margin recovery, "
        "stabilisation of China JV earnings and recognition of Financial "
        "Services value. The principal risks are execution, capital intensity, "
        "EV competition and further weakness in China.",
    )

    _heading(doc, "2. Valuation Summary")
    _kpis(
        doc,
        [
            {"label": "Market", "value": f"€{current_price:.2f}"},
            {
                "label": "Base DCF",
                "value": f"€{dcf_base:.2f}",
                "detail": f"{upside:+.1f}%",
                "colour": GREEN,
            },
            {
                "label": "Conservative",
                "value": f"€{dcf_conservative:.2f}",
                "detail": f"{conservative_upside:+.1f}%",
                "colour": VW_BLUE,
            },
            {
                "label": "SOTP Equity",
                "value": f"€{sotp_value:.1f}bn",
                "detail": "Business value",
                "colour": ORANGE,
            },
        ],
    )

    _heading(doc, "3. Investment Thesis")
    _bullet(
        doc,
        f"Automotive revenue increases from €{revenue_start:.1f}bn to "
        f"€{revenue_end:.1f}bn, a {revenue_cagr:.1f}% CAGR.",
    )
    _bullet(
        doc,
        f"Automotive EBIT increases from €{ebit_start:.1f}bn to "
        f"€{ebit_end:.1f}bn, a {ebit_cagr:.1f}% CAGR.",
    )
    _bullet(
        doc,
        f"Automotive EBIT margin expands from {margin_start:.1f}% to "
        f"{margin_end:.1f}%.",
    )
    _bullet(doc, "Financial Services book value supports recurring equity value.")
    _bullet(doc, "China JV earnings recovery offers additional optionality.")

    _heading(doc, "4. Sum-of-the-Parts")
    _paragraph(
        doc,
        f"The SOTP analysis produces aggregate equity value of approximately "
        f"€{sotp_total:.1f}bn.",
    )
    _table(
        doc,
        sotp[["Business", "Value", "Weight"]],
        formats={
            "Value": lambda x: f"€{float(x):.2f}bn",
            "Weight": lambda x: f"{float(x):.1f}%",
        },
    )

    _heading(doc, "5. Automotive Outlook")
    _paragraph(
        doc,
        f"Between {int(auto_start['Year'])} and {int(auto_end['Year'])}, "
        f"revenue rises from €{revenue_start:.1f}bn to €{revenue_end:.1f}bn. "
        f"EBIT rises from €{ebit_start:.1f}bn to €{ebit_end:.1f}bn. The main "
        f"valuation driver is margin expansion from {margin_start:.1f}% to "
        f"{margin_end:.1f}% rather than aggressive sales growth.",
    )
    if "FCF" in automotive.columns:
        negative_years = automotive.loc[automotive["FCF"] < 0, "Year"].astype(int).tolist()
        if negative_years:
            _paragraph(
                doc,
                "Automotive free cash flow is negative in "
                + ", ".join(map(str, negative_years))
                + ", highlighting sensitivity to capital expenditure and "
                "working-capital assumptions.",
            )

    _heading(doc, "6. China Joint Ventures")
    _paragraph(
        doc,
        f"China JV net income increases from €{float(china_start['Net Income']):.3f}bn "
        f"in {int(china_start['Year'])} to €{float(china_end['Net Income']):.3f}bn "
        f"in {int(china_end['Year'])}. Applying a {float(china_end['P/E']):.1f}x "
        f"P/E multiple produces final-year equity value of "
        f"€{float(china_end['Value']):.2f}bn.",
    )

    _heading(doc, "7. Financial Services")
    _paragraph(
        doc,
        f"Book value increases from €{float(finance_start['Book Value']):.1f}bn "
        f"to €{float(finance_end['Book Value']):.1f}bn. Applying a "
        f"{float(finance_end['P/B']):.2f}x P/B multiple produces final-year "
        f"equity value of €{float(finance_end['Value']):.2f}bn.",
    )

    _heading(doc, "8. DCF Scenario Analysis")
    dcf_table = dcf[["Year", "Bear", "Base", "Conservative"]].rename(
        columns={"Bear": "Alternative"}
    )
    _table(
        doc,
        dcf_table,
        formats={
            "Year": lambda x: str(int(x)),
            "Alternative": lambda x: f"€{float(x):.2f}",
            "Base": lambda x: f"€{float(x):.2f}",
            "Conservative": lambda x: f"€{float(x):.2f}",
        },
    )

    _heading(doc, "9. Catalysts and Risks")
    _heading(doc, "Key Catalysts", level=2)
    for item in [
        "Automotive margin normalisation.",
        "Stabilisation of China JV earnings.",
        "Recognition of Financial Services value.",
        "Cost optimisation and portfolio simplification.",
        "Improved capital allocation and shareholder returns.",
    ]:
        _bullet(doc, item)

    _heading(doc, "Key Risks", level=2)
    for item in [
        "Further deterioration in the Chinese market.",
        "EV competition and sustained pricing pressure.",
        "Failure to deliver Automotive margin recovery.",
        "Higher capital expenditure and weaker free cash flow.",
        "Higher discount rates and regulatory pressure.",
    ]:
        _bullet(doc, item)

    if include_methodology:
        _heading(doc, "10. Valuation Methodology")
        _bullet(doc, "Discounted Cash Flow valuation for Automotive.")
        _bullet(doc, "P/E valuation for China Joint Ventures.")
        _bullet(doc, "P/B valuation for Financial Services.")
        _bullet(doc, "Sum-of-the-parts reconciliation at group level.")

    _heading(doc, "11. Investment Conclusion")
    _paragraph(
        doc,
        f"The valuation supports a {rating} recommendation. The base case "
        f"indicates {upside:.1f}% upside and the conservative case indicates "
        f"{conservative_upside:.1f}% upside. The risk-reward profile is "
        "attractive if Volkswagen delivers margin recovery and preserves the "
        "value of China JV and Financial Services.",
    )

    if include_appendix:
        doc.add_page_break()
        _heading(doc, "Appendix: Forecast Tables")

        _heading(doc, "Automotive Forecast", level=2)
        auto_columns = ["Year", "Revenue", "EBIT"]
        if "FCF" in automotive.columns:
            auto_columns.append("FCF")
        _table(
            doc,
            automotive[auto_columns],
            formats={
                "Year": lambda x: str(int(x)),
                "Revenue": lambda x: f"€{float(x):.2f}bn",
                "EBIT": lambda x: f"€{float(x):.2f}bn",
                "FCF": lambda x: f"€{float(x):.2f}bn",
            },
        )

        _heading(doc, "China JV Forecast", level=2)
        _table(
            doc,
            china[["Year", "Net Income", "P/E", "Value"]],
            formats={
                "Year": lambda x: str(int(x)),
                "Net Income": lambda x: f"€{float(x):.3f}bn",
                "P/E": lambda x: f"{float(x):.1f}x",
                "Value": lambda x: f"€{float(x):.3f}bn",
            },
        )

        _heading(doc, "Financial Services Forecast", level=2)
        _table(
            doc,
            finance[["Year", "Book Value", "P/B", "Value"]],
            formats={
                "Year": lambda x: str(int(x)),
                "Book Value": lambda x: f"€{float(x):.2f}bn",
                "P/B": lambda x: f"{float(x):.2f}x",
                "Value": lambda x: f"€{float(x):.2f}bn",
            },
        )

    _heading(doc, "Disclaimer")
    _paragraph(
        doc,
        "This report is generated automatically for educational and research "
        "purposes only. It is not investment advice or a recommendation to buy "
        "or sell securities. All assumptions should be independently verified.",
    )

    _add_footer(doc)

    output_file = REPORT_DIR / (
        "Volkswagen_AG_Research_Report_"
        f"{report_date.strftime('%Y%m%d')}.docx"
    )
    doc.save(output_file)
    return str(output_file)
