import numpy as np
import plotly.graph_objects as go

from plotly.subplots import make_subplots


# =====================================================
# COLOUR PALETTE
# =====================================================

VW_NAVY = "#001E50"
VW_BLUE = "#0057B8"
VW_LIGHT_BLUE = "#38BDF8"

GREEN = "#22C55E"
GREEN_LIGHT = "#86EFAC"

ORANGE = "#F59E0B"
RED = "#EF4444"

TEXT_PRIMARY = "#F8FAFC"
TEXT_SECONDARY = "#94A3B8"

GRID_COLOR = "rgba(148, 163, 184, 0.13)"
AXIS_COLOR = "rgba(148, 163, 184, 0.28)"
TRANSPARENT = "rgba(0, 0, 0, 0)"


# =====================================================
# COMMON CHART DESIGN
# =====================================================

def apply_chart_style(
    fig,
    title=None,
    subtitle=None,
    height=560,
):
    """Apply a shared premium design to a Plotly figure."""

    if title and subtitle:
        title_text = (
            f"<b>{title}</b><br>"
            f"<span style='font-size:13px;color:{TEXT_SECONDARY};'>"
            f"{subtitle}</span>"
        )

    elif title:
        title_text = f"<b>{title}</b>"

    else:
        title_text = None

    fig.update_layout(
        title=dict(
            text=title_text,
            x=0.02,
            xanchor="left",
            y=0.97,
            yanchor="top",
            font=dict(
                color=TEXT_PRIMARY,
                size=20,
            ),
        ),
        height=height,
        margin=dict(
            l=70,
            r=70,
            t=105 if title else 45,
            b=65,
        ),
        paper_bgcolor=TRANSPARENT,
        plot_bgcolor=TRANSPARENT,
        font=dict(
            family="Arial, sans-serif",
            color=TEXT_PRIMARY,
        ),
        hoverlabel=dict(
            bgcolor="#111827",
            bordercolor="#334155",
            font=dict(
                color=TEXT_PRIMARY,
                size=13,
            ),
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=0.98,
            bgcolor=TRANSPARENT,
            font=dict(
                color="#CBD5E1",
                size=12,
            ),
        ),
    )

    fig.update_xaxes(
        showgrid=False,
        zeroline=False,
        showline=True,
        linecolor=AXIS_COLOR,
        tickfont=dict(
            color="#CBD5E1",
            size=11,
        ),
        title_font=dict(
            color=TEXT_SECONDARY,
            size=12,
        ),
        ticks="outside",
        tickcolor=AXIS_COLOR,
    )

    fig.update_yaxes(
        gridcolor=GRID_COLOR,
        zeroline=False,
        showline=False,
        tickfont=dict(
            color="#CBD5E1",
            size=11,
        ),
        title_font=dict(
            color=TEXT_SECONDARY,
            size=12,
        ),
    )

    return fig


# =====================================================
# UPSIDE GAUGE
# =====================================================

def upside_gauge(upside):
    """Create a gauge chart displaying potential upside."""

    upside_value = float(upside)

    gauge_maximum = max(
        100,
        int(
            np.ceil(
                max(upside_value, 1) / 20
            ) * 20
        ),
    )

    if upside_value >= 30:
        gauge_color = GREEN

    elif upside_value >= 10:
        gauge_color = ORANGE

    else:
        gauge_color = RED

    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=upside_value,
            number=dict(
                suffix="%",
                valueformat=".1f",
                font=dict(
                    color=TEXT_PRIMARY,
                    size=48,
                ),
            ),
            title=dict(
                text=(
                    "<b>Potential Upside</b><br>"
                    f"<span style='font-size:13px;"
                    f"color:{TEXT_SECONDARY};'>"
                    "Base fair value versus market price"
                    "</span>"
                ),
                font=dict(
                    color=TEXT_PRIMARY,
                    size=19,
                ),
            ),
            gauge=dict(
                axis=dict(
                    range=[
                        0,
                        gauge_maximum,
                    ],
                    tickwidth=0,
                    tickcolor=TRANSPARENT,
                    tickfont=dict(
                        color=TEXT_SECONDARY,
                        size=10,
                    ),
                ),
                bar=dict(
                    color=gauge_color,
                    thickness=0.25,
                ),
                bgcolor="rgba(30, 41, 59, 0.60)",
                borderwidth=0,
                steps=[
                    {
                        "range": [0, 10],
                        "color": (
                            "rgba(239, 68, 68, 0.20)"
                        ),
                    },
                    {
                        "range": [10, 30],
                        "color": (
                            "rgba(245, 158, 11, 0.20)"
                        ),
                    },
                    {
                        "range": [
                            30,
                            gauge_maximum,
                        ],
                        "color": (
                            "rgba(34, 197, 94, 0.18)"
                        ),
                    },
                ],
                threshold=dict(
                    line=dict(
                        color=TEXT_PRIMARY,
                        width=3,
                    ),
                    thickness=0.75,
                    value=upside_value,
                ),
            ),
        )
    )

    fig.update_layout(
        height=410,
        margin=dict(
            l=35,
            r=35,
            t=85,
            b=30,
        ),
        paper_bgcolor=TRANSPARENT,
        plot_bgcolor=TRANSPARENT,
        font=dict(
            family="Arial, sans-serif",
            color=TEXT_PRIMARY,
        ),
    )

    return fig


# =====================================================
# SOTP WATERFALL
# =====================================================

def sotp_waterfall(df=None):
    """
    Create the sum-of-the-parts waterfall chart.

    If no DataFrame is supplied, default model values
    are used for compatibility with existing pages.
    """

    if df is None:
        businesses = [
            "Automotive",
            "China JV",
            "Financial Services",
        ]

        values = [
            14.318,
            3.600,
            13.905,
        ]

    else:
        businesses = (
            df["Business"]
            .astype(str)
            .tolist()
        )

        values = (
            df["Value"]
            .astype(float)
            .tolist()
        )

    total_value = sum(values)

    labels = (
        businesses
        + ["Total Equity Value"]
    )

    fig = go.Figure(
        go.Waterfall(
            orientation="v",
            measure=(
                ["relative"] * len(values)
                + ["total"]
            ),
            x=labels,
            y=values + [0],
            connector=dict(
                line=dict(
                    color=(
                        "rgba(148, 163, 184, 0.35)"
                    ),
                    width=1,
                    dash="dot",
                )
            ),
            increasing=dict(
                marker=dict(
                    color=VW_BLUE,
                    line=dict(
                        color=(
                            "rgba(125, 211, 252, 0.55)"
                        ),
                        width=1,
                    ),
                )
            ),
            totals=dict(
                marker=dict(
                    color=GREEN,
                    line=dict(
                        color=GREEN_LIGHT,
                        width=1,
                    ),
                )
            ),
            text=(
                [
                    f"€{value:.1f}bn"
                    for value in values
                ]
                + [
                    f"€{total_value:.1f}bn"
                ]
            ),
            textposition="outside",
            textfont=dict(
                color=TEXT_PRIMARY,
                size=12,
            ),
            hovertemplate=(
                "<b>%{x}</b><br>"
                "Value: €%{y:.2f}bn"
                "<extra></extra>"
            ),
        )
    )

    apply_chart_style(
        fig,
        title="Sum-of-the-Parts Valuation",
        subtitle=(
            "Contribution of each business "
            "to total equity value"
        ),
        height=580,
    )

    fig.update_layout(
        showlegend=False,
        waterfallgap=0.35,
    )

    fig.update_yaxes(
        title="Equity value (€bn)",
        tickprefix="€",
        ticksuffix="bn",
        range=[
            0,
            total_value * 1.22,
        ],
    )

    return fig


# =====================================================
# BUSINESS MIX
# =====================================================

def business_mix(df):
    """Create a donut chart showing the SOTP mix."""

    total_value = float(
        df["Value"].sum()
    )

    colours = [
        VW_BLUE,
        ORANGE,
        VW_LIGHT_BLUE,
        GREEN,
    ]

    fig = go.Figure(
        go.Pie(
            labels=df["Business"],
            values=df["Value"],
            hole=0.68,
            sort=False,
            direction="clockwise",
            marker=dict(
                colors=colours[:len(df)],
                line=dict(
                    color="#07111F",
                    width=4,
                ),
            ),
            textinfo="percent",
            textposition="inside",
            textfont=dict(
                color="#FFFFFF",
                size=12,
            ),
            hovertemplate=(
                "<b>%{label}</b><br>"
                "Value: €%{value:.2f}bn<br>"
                "Weight: %{percent}"
                "<extra></extra>"
            ),
        )
    )

    apply_chart_style(
        fig,
        title="Business Value Mix",
        subtitle=(
            "Weight of each division "
            "in SOTP value"
        ),
        height=580,
    )

    fig.update_layout(
        annotations=[
            dict(
                text=(
                    f"<b>€{total_value:.1f}bn</b>"
                    "<br>"
                    f"<span style='font-size:12px;"
                    f"color:{TEXT_SECONDARY};'>"
                    "Total SOTP"
                    "</span>"
                ),
                x=0.5,
                y=0.5,
                showarrow=False,
                font=dict(
                    color=TEXT_PRIMARY,
                    size=22,
                ),
            )
        ],
        legend=dict(
            orientation="v",
            yanchor="middle",
            y=0.5,
            xanchor="left",
            x=1.02,
            font=dict(
                color="#CBD5E1",
                size=11,
            ),
        ),
    )

    return fig


# =====================================================
# AUTOMOTIVE
# =====================================================

def automotive_chart(df):
    """
    Create the Automotive chart.

    Revenue is displayed as bars and EBIT as a line
    on a secondary axis.
    """

    chart_df = df.copy()

    chart_df["EBIT Margin"] = (
        chart_df["EBIT"]
        / chart_df["Revenue"]
        * 100
    )

    blue_scale = [
        "#174C7E",
        "#16548D",
        "#145C9C",
        "#1265AC",
        "#0E6EBC",
        "#0877D1",
    ]

    if len(chart_df) <= len(blue_scale):
        bar_colours = blue_scale[
            :len(chart_df)
        ]
    else:
        bar_colours = [
            VW_BLUE
            for _ in range(len(chart_df))
        ]

    customdata = np.column_stack(
        [
            chart_df["EBIT"].to_numpy(),
            chart_df[
                "EBIT Margin"
            ].to_numpy(),
        ]
    )

    fig = make_subplots(
        specs=[
            [
                {
                    "secondary_y": True
                }
            ]
        ]
    )

    fig.add_trace(
        go.Bar(
            x=chart_df["Year"],
            y=chart_df["Revenue"],
            name="Revenue",
            marker=dict(
                color=bar_colours,
                line=dict(
                    color=(
                        "rgba(125, 211, 252, 0.38)"
                    ),
                    width=1,
                ),
            ),
            opacity=0.94,
            text=[
                f"€{value:.1f}bn"
                for value
                in chart_df["Revenue"]
            ],
            textposition="outside",
            cliponaxis=False,
            textfont=dict(
                color="#DCEBFF",
                size=11,
            ),
            customdata=customdata,
            hovertemplate=(
                "<b>%{x}</b><br>"
                "Revenue: €%{y:.2f}bn<br>"
                "EBIT: €%{customdata.2f}bn<br>"
                "EBIT margin: "
                "%{customdata.2f}%"
                "<extra></extra>"
            ),
        ),
        secondary_y=False,
    )

    fig.add_trace(
        go.Scatter(
            x=chart_df["Year"],
            y=chart_df["EBIT"],
            name="EBIT",
            mode="lines+markers+text",
            line=dict(
                color=GREEN,
                width=4,
                shape="spline",
                smoothing=0.65,
            ),
            marker=dict(
                size=10,
                color=GREEN,
                line=dict(
                    color="#07111F",
                    width=3,
                ),
            ),
            text=[
                f"€{value:.1f}bn"
                for value
                in chart_df["EBIT"]
            ],
            textposition="top center",
            textfont=dict(
                color=GREEN_LIGHT,
                size=11,
            ),
            hovertemplate=(
                "<b>%{x}</b><br>"
                "EBIT: €%{y:.2f}bn"
                "<extra></extra>"
            ),
        ),
        secondary_y=True,
    )

    apply_chart_style(
        fig,
        title="Automotive Revenue & EBIT",
        subtitle=(
            "Historical base year and "
            "forecast operating performance"
        ),
        height=600,
    )

    fig.update_layout(
        hovermode="x unified",
        bargap=0.28,
    )

    fig.update_xaxes(
        title=None,
        tickmode="array",
        tickvals=chart_df["Year"],
        ticktext=[
            str(year)
            for year in chart_df["Year"]
        ],
        fixedrange=True,
    )

    fig.update_yaxes(
        title=dict(
            text="Revenue (€bn)",
            font=dict(
                color="#93C5FD",
                size=13,
            ),
        ),
        range=[
            0,
            chart_df["Revenue"].max()
            * 1.17,
        ],
        tickprefix="€",
        ticksuffix="bn",
        tickformat=".0f",
        tickfont=dict(
            color="#93C5FD",
            size=11,
        ),
        gridcolor=GRID_COLOR,
        fixedrange=True,
        secondary_y=False,
    )

    fig.update_yaxes(
        title=dict(
            text="EBIT (€bn)",
            font=dict(
                color=GREEN_LIGHT,
                size=13,
            ),
        ),
        range=[
            0,
            chart_df["EBIT"].max()
            * 1.28,
        ],
        tickprefix="€",
        ticksuffix="bn",
        tickformat=".0f",
        tickfont=dict(
            color=GREEN_LIGHT,
            size=11,
        ),
        showgrid=False,
        fixedrange=True,
        secondary_y=True,
    )

    if len(chart_df) > 1:
        first_year = float(
            chart_df["Year"].iloc[0]
        )

        second_year = float(
            chart_df["Year"].iloc[1]
        )

        separator = (
            first_year + second_year
        ) / 2

        fig.add_vline(
            x=separator,
            line_width=1,
            line_dash="dot",
            line_color=(
                "rgba(148, 163, 184, 0.50)"
            ),
        )

        fig.add_annotation(
            x=separator,
            y=1.0,
            xref="x",
            yref="paper",
            text="Forecast →",
            showarrow=False,
            xanchor="left",
            yanchor="bottom",
            xshift=9,
            font=dict(
                color=TEXT_SECONDARY,
                size=11,
            ),
        )

    return fig


# =====================================================
# CHINA JOINT VENTURES
# =====================================================

def china_chart(df):
    """Create the China JV valuation chart."""

    chart_df = df.copy()

    customdata = np.column_stack(
        [
            chart_df[
                "Net Income"
            ].to_numpy(),
            chart_df["P/E"].to_numpy(),
        ]
    )

    fig = go.Figure(
        go.Scatter(
            x=chart_df["Year"],
            y=chart_df["Value"],
            name="China JV Value",
            mode="lines+markers",
            line=dict(
                color=ORANGE,
                width=4,
                shape="spline",
                smoothing=0.55,
            ),
            marker=dict(
                size=10,
                color=ORANGE,
                line=dict(
                    color="#07111F",
                    width=3,
                ),
            ),
            fill="tozeroy",
            fillcolor=(
                "rgba(245, 158, 11, 0.08)"
            ),
            customdata=customdata,
            hovertemplate=(
                "<b>%{x}</b><br>"
                "Equity value: €%{y:.2f}bn"
                "<br>"
                "Net income: "
                "€%{customdata.3f}bn"
                "<br>"
                "P/E: %{customdata.1f}x"
                "<extra></extra>"
            ),
        )
    )

    apply_chart_style(
        fig,
        title="China Joint Ventures",
        subtitle=(
            "Net income contribution "
            "and implied equity value"
        ),
        height=520,
    )

    fig.update_layout(
        showlegend=False,
        hovermode="x unified",
    )

    fig.update_yaxes(
        title="Equity value (€bn)",
        tickprefix="€",
        ticksuffix="bn",
        tickformat=".1f",
        rangemode="tozero",
    )

    fig.update_xaxes(
        tickmode="array",
        tickvals=chart_df["Year"],
    )

    return fig


# =====================================================
# FINANCIAL SERVICES
# =====================================================

def finance_chart(df):
    """Create the Financial Services valuation chart."""

    chart_df = df.copy()

    fig = make_subplots(
        specs=[
            [
                {
                    "secondary_y": True
                }
            ]
        ]
    )

    fig.add_trace(
        go.Bar(
            x=chart_df["Year"],
            y=chart_df["Book Value"],
            name="Book Value",
            marker=dict(
                color=(
                    "rgba(56, 189, 248, 0.70)"
                ),
                line=dict(
                    color=VW_LIGHT_BLUE,
                    width=1,
                ),
            ),
            text=[
                f"€{value:.1f}bn"
                for value
                in chart_df["Book Value"]
            ],
            textposition="outside",
            cliponaxis=False,
            textfont=dict(
                color="#BAE6FD",
                size=10,
            ),
            customdata=chart_df["P/B"],
            hovertemplate=(
                "<b>%{x}</b><br>"
                "Book value: €%{y:.2f}bn"
                "<br>"
                "P/B multiple: "
                "%{customdata:.2f}x"
                "<extra></extra>"
            ),
        ),
        secondary_y=False,
    )

    fig.add_trace(
        go.Scatter(
            x=chart_df["Year"],
            y=chart_df["Value"],
            name="Equity Value",
            mode="lines+markers",
            line=dict(
                color=GREEN,
                width=4,
                shape="spline",
                smoothing=0.55,
            ),
            marker=dict(
                color=GREEN,
                size=9,
                line=dict(
                    color="#07111F",
                    width=3,
                ),
            ),
            hovertemplate=(
                "<b>%{x}</b><br>"
                "Equity value: €%{y:.2f}bn"
                "<extra></extra>"
            ),
        ),
        secondary_y=True,
    )

    apply_chart_style(
        fig,
        title="Financial Services",
        subtitle=(
            "Book value evolution "
            "and P/B implied valuation"
        ),
        height=520,
    )

    fig.update_layout(
        hovermode="x unified",
        bargap=0.34,
    )

    fig.update_xaxes(
        tickmode="array",
        tickvals=chart_df["Year"],
    )

    fig.update_yaxes(
        title="Book value (€bn)",
        tickprefix="€",
        ticksuffix="bn",
        tickformat=".0f",
        range=[
            0,
            chart_df["Book Value"].max()
            * 1.18,
        ],
        secondary_y=False,
    )

    fig.update_yaxes(
        title=dict(
            text="Equity value (€bn)",
            font=dict(
                color=GREEN_LIGHT,
            ),
        ),
        tickprefix="€",
        ticksuffix="bn",
        tickformat=".0f",
        tickfont=dict(
            color=GREEN_LIGHT,
        ),
        showgrid=False,
        range=[
            0,
            chart_df["Value"].max()
            * 1.30,
        ],
        secondary_y=True,
    )

    return fig


# =====================================================
# DCF SCENARIOS
# =====================================================

def dcf_chart(df):
    """Create the DCF scenario comparison chart."""

    scenario_styles = {
        "Bear": {
            "color": RED,
            "dash": "dot",
        },
        "Base": {
            "color": GREEN,
            "dash": "solid",
        },
        "Conservative": {
            "color": VW_LIGHT_BLUE,
            "dash": "dash",
        },
    }

    fig = go.Figure()

    for scenario, style in scenario_styles.items():

        if scenario not in df.columns:
            continue

        fig.add_trace(
            go.Scatter(
                x=df["Year"],
                y=df[scenario],
                name=scenario,
                mode="lines+markers",
                line=dict(
                    color=style["color"],
                    width=4,
                    dash=style["dash"],
                    shape="spline",
                    smoothing=0.45,
                ),
                marker=dict(
                    size=9,
                    color=style["color"],
                    line=dict(
                        color="#07111F",
                        width=2,
                    ),
                ),
                hovertemplate=(
                    f"<b>{scenario}</b><br>"
                    "Year: %{x}<br>"
                    "Value: €%{y:.2f}"
                    "<extra></extra>"
                ),
            )
        )

    apply_chart_style(
        fig,
        title="DCF Scenario Analysis",
        subtitle=(
            "Implied share price under "
            "alternative assumptions"
        ),
        height=610,
    )

    fig.update_layout(
        hovermode="x unified",
    )

    fig.update_xaxes(
        tickmode="array",
        tickvals=df["Year"],
        title=None,
    )

    fig.update_yaxes(
        title="Implied share price (€)",
        tickprefix="€",
        tickformat=".0f",
        rangemode="tozero",
    )

    return fig


# =====================================================
# SENSITIVITY MATRIX
# =====================================================

def sensitivity_chart(
    matrix,
    wacc_values,
    growth_values,
):
    """Create the DCF sensitivity heatmap."""

    matrix_array = np.asarray(
        matrix,
        dtype=float,
    )

    text_matrix = np.array(
        [
            [
                f"€{value:.1f}"
                for value in row
            ]
            for row in matrix_array
        ]
    )

    fig = go.Figure(
        go.Heatmap(
            z=matrix_array,
            x=wacc_values,
            y=growth_values,
            colorscale=[
                [0.00, "#7F1D1D"],
                [0.25, "#DC2626"],
                [0.45, "#F59E0B"],
                [0.60, "#FACC15"],
                [0.78, "#22C55E"],
                [1.00, "#15803D"],
            ],
            text=text_matrix,
            texttemplate="%{text}",
            textfont=dict(
                color="#FFFFFF",
                size=12,
            ),
            colorbar=dict(
                title=dict(
                    text="Share price (€)",
                    side="right",
                    font=dict(
                        color=TEXT_SECONDARY,
                    ),
                ),
                tickprefix="€",
                tickfont=dict(
                    color="#CBD5E1",
                ),
                thickness=14,
                outlinewidth=0,
            ),
            hovertemplate=(
                "<b>DCF Sensitivity</b><br>"
                "WACC: %{x:.1f}%<br>"
                "Terminal growth: %{y:.1f}%"
                "<br>"
                "Implied value: €%{z:.2f}"
                "<extra></extra>"
            ),
        )
    )

    apply_chart_style(
        fig,
        title="DCF Sensitivity Matrix",
        subtitle=(
            "Implied share price by WACC "
            "and terminal growth"
        ),
        height=590,
    )

    fig.update_xaxes(
        title="WACC (%)",
        tickmode="array",
        tickvals=wacc_values,
        ticktext=[
            f"{value:.1f}%"
            for value in wacc_values
        ],
        side="bottom",
    )

    fig.update_yaxes(
        title="Terminal growth (%)",
        tickmode="array",
        tickvals=growth_values,
        ticktext=[
            f"{value:.1f}%"
            for value in growth_values
        ],
        autorange=True,
    )

    return fig