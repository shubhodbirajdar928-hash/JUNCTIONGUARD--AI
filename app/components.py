"""
UI Components and Design System for JunctionGuard AI.
Implements the Modern CareerVerse AI-Inspired Quantum Glassmorphism Interface:
  - Deep obsidian #070a13 canvas with ambient radial indigo glow
  - Electric Indigo (#6366f1) and Radiant Cyan (#38bdf8) cyber accents
  - Plus Jakarta Sans + Inter + JetBrains Mono typography
  - Floating frosted glass navigation bar with live operational pills
  - Hero eyebrow tags with subtle pulsing indicators
  - Visual KPI cards with window dots (● ● ●), live telemetry badges, and gradient glow
  - Color-coded risk badges & animated radar halos
  - Explainable contributing factor progress bars
"""

import streamlit as st
from datetime import datetime
from typing import Optional, List, Dict, Any
import streamlit.components.v1 as st_components

def scroll_to_top():
    """Scrolls the browser viewport smoothly to the absolute top of the application."""
    scroll_js = """
    <script>
    function forceScrollToTop() {
        try {
            // 1. Scroll anchor into view if found in parent or current document
            var topAnchor = (window.parent && window.parent.document.getElementById('jg-top-anchor')) ||
                            window.document.getElementById('jg-top-anchor');
            if (topAnchor) {
                topAnchor.scrollIntoView({ behavior: 'smooth', block: 'start', inline: 'nearest' });
            }

            // 2. Scroll all potential parent containers to absolute 0
            if (window.parent) {
                var doc = window.parent.document;
                var containers = [
                    doc.querySelector('[data-testid="stAppViewContainer"]'),
                    doc.querySelector('.main'),
                    doc.querySelector('section.main'),
                    doc.documentElement,
                    doc.body
                ];
                containers.forEach(function(el) {
                    if (el) {
                        el.scrollTop = 0;
                        if (typeof el.scrollTo === 'function') {
                            el.scrollTo({ top: 0, left: 0, behavior: 'smooth' });
                        }
                    }
                });
                window.parent.scrollTo({ top: 0, left: 0, behavior: 'smooth' });
            }
            window.scrollTo({ top: 0, left: 0, behavior: 'smooth' });
        } catch(e) {
            console.error('Scroll error:', e);
        }
    }

    // Execute immediately and at staggered intervals as Streamlit mounts DOM nodes
    forceScrollToTop();
    setTimeout(forceScrollToTop, 50);
    setTimeout(forceScrollToTop, 150);
    setTimeout(forceScrollToTop, 300);
    setTimeout(forceScrollToTop, 600);
    setTimeout(forceScrollToTop, 1000);
    </script>
    """
    st_components.html(scroll_js, height=0, width=0)

def scroll_to_map_section():
    """Scrolls smoothly and precisely to the Radar Map & Telemetry centerpiece."""
    scroll_js = """
    <script>
    function forceScrollToMap() {
        try {
            var target = (window.parent && window.parent.document.getElementById('jg-radar-map-section')) ||
                         window.document.getElementById('jg-radar-map-section');
            if (target) {
                target.scrollIntoView({ behavior: 'smooth', block: 'start', inline: 'nearest' });
            }
        } catch(e) {
            console.error('Scroll map error:', e);
        }
    }

    forceScrollToMap();
    setTimeout(forceScrollToMap, 60);
    setTimeout(forceScrollToMap, 180);
    setTimeout(forceScrollToMap, 350);
    setTimeout(forceScrollToMap, 650);
    setTimeout(forceScrollToMap, 1100);
    </script>
    """
    st_components.html(scroll_js, height=0, width=0)

def get_risk_badge_html(risk_level: Optional[str]) -> str:
    """Returns the HTML string for a colored risk badge."""
    if risk_level is None:
        return '<span class="badge badge-gray"><span class="badge-dot"></span>AWAITING DATA</span>'
    
    lvl = risk_level.upper()
    if lvl == "LOW":
        return '<span class="badge badge-green"><span class="badge-dot"></span>LOW RISK</span>'
    elif lvl == "MEDIUM":
        return '<span class="badge badge-amber"><span class="badge-dot"></span>MEDIUM RISK</span>'
    elif lvl == "HIGH":
        return '<span class="badge badge-red"><span class="badge-dot"></span>HIGH RISK</span>'
    else:
        return f'<span class="badge badge-amber"><span class="badge-dot"></span>{lvl}</span>'

def render_risk_badge(risk_level: Optional[str]):
    """Renders the risk badge inline in Streamlit."""
    st.markdown(get_risk_badge_html(risk_level), unsafe_allow_html=True)

def render_3d_circular_risk_gauge(risk_score: float = 69.7, risk_level: str = "MEDIUM", trend_str: str = "ELEVATED CONFLICTS"):
    """
    Renders an animated 3D circular SVG progress gauge with glowing gradient arcs,
    numerical score, and risk classification badge.
    """
    score = max(0.0, min(100.0, float(risk_score or 0.0)))
    level = (risk_level or "LOW").upper()
    
    # SVG circle calculation (Radius = 75, Circumference = 2 * PI * 75 = 471.24)
    circumference = 471.24
    dashoffset = circumference - (score / 100.0) * circumference
    
    if level == "HIGH":
        stroke_color = "url(#gauge-grad-red)"
        badge_style = "background:rgba(244,63,94,0.18); color:#fb7185; border:1px solid rgba(244,63,94,0.4);"
        badge_dot = "#fb7185"
        trend_icon = "▲"
        trend_color = "#fb7185"
    elif level == "MEDIUM":
        stroke_color = "url(#gauge-grad-amber)"
        badge_style = "background:rgba(245,158,11,0.18); color:#fbbf24; border:1px solid rgba(245,158,11,0.4);"
        badge_dot = "#fbbf24"
        trend_icon = "▲"
        trend_color = "#fbbf24"
    else:
        stroke_color = "url(#gauge-grad-green)"
        badge_style = "background:rgba(16,185,129,0.18); color:#34d399; border:1px solid rgba(16,185,129,0.4);"
        badge_dot = "#34d399"
        trend_icon = "▼"
        trend_color = "#34d399"

    gauge_html = f"""
    <div style="background: #0c101e; border: 1px solid rgba(255,255,255,0.09); border-radius: 18px; padding: 22px; display: flex; flex-direction: column; align-items: center; justify-content: center; position: relative; overflow: hidden; box-shadow: 0 12px 36px rgba(0,0,0,0.55);">
        <div style="font-size: 0.76rem; font-weight: 700; color: #94a3b8; letter-spacing: 0.08em; text-transform: uppercase; font-family: 'JetBrains Mono', monospace; margin-bottom: 8px;">
            AI COMPOSITE RISK GAUGE
        </div>
        <div style="position: relative; width: 190px; height: 190px; display: flex; align-items: center; justify-content: center;">
            <svg width="190" height="190" viewBox="0 0 200 200" style="transform: rotate(-90deg); filter: drop-shadow(0 0 12px rgba(99,102,241,0.25));">
                <defs>
                    <linearGradient id="gauge-grad-green" x1="0%" y1="0%" x2="100%" y2="100%">
                        <stop offset="0%" stop-color="#38bdf8" />
                        <stop offset="100%" stop-color="#10b981" />
                    </linearGradient>
                    <linearGradient id="gauge-grad-amber" x1="0%" y1="0%" x2="100%" y2="100%">
                        <stop offset="0%" stop-color="#f59e0b" />
                        <stop offset="100%" stop-color="#d97706" />
                    </linearGradient>
                    <linearGradient id="gauge-grad-red" x1="0%" y1="0%" x2="100%" y2="100%">
                        <stop offset="0%" stop-color="#fb7185" />
                        <stop offset="100%" stop-color="#e11d48" />
                    </linearGradient>
                </defs>
                <!-- Track background -->
                <circle cx="100" cy="100" r="75" fill="none" stroke="rgba(255,255,255,0.06)" stroke-width="14" />
                <!-- Active Progress Arc -->
                <circle cx="100" cy="100" r="75" fill="none" stroke="{stroke_color}" stroke-width="14"
                        stroke-dasharray="{circumference}" stroke-dashoffset="{dashoffset}"
                        stroke-linecap="round" style="transition: stroke-dashoffset 0.8s ease;" />
            </svg>
            <div style="position: absolute; display: flex; flex-direction: column; align-items: center; text-align: center;">
                <div style="font-size: 2.6rem; font-weight: 900; color: #ffffff; line-height: 1; font-family: 'Plus Jakarta Sans', sans-serif;">
                    {score:.1f}
                </div>
                <div style="font-size: 0.78rem; color: #64748b; font-weight: 600; font-family: 'JetBrains Mono', monospace; margin-top: 2px;">
                    / 100
                </div>
            </div>
        </div>
        <div style="display: flex; flex-direction: column; align-items: center; gap: 6px; margin-top: 10px;">
            <span style="font-size: 0.78rem; font-weight: 800; font-family: 'JetBrains Mono', monospace; padding: 4px 14px; border-radius: 9999px; {badge_style}">
                <span style="width: 7px; height: 7px; border-radius: 50%; background: {badge_dot}; display: inline-block; box-shadow: 0 0 8px {badge_dot}; margin-right: 6px;"></span>
                {level} RISK LEVEL
            </span>
            <div style="font-size: 0.70rem; color: {trend_color}; font-family: 'JetBrains Mono', monospace; font-weight: 700; display: flex; align-items: center; gap: 4px;">
                <span>{trend_icon}</span> <span>{trend_str}</span>
            </div>
        </div>
    </div>
    """
    st.markdown(gauge_html, unsafe_allow_html=True)

def render_live_alert_ribbon(alerts: List[Dict[str, str]]):
    """
    Renders an enterprise live alerts ribbon.
    """
    if not alerts:
        return
    
    alert_items_html = ""
    for a in alerts[:3]:
        color = "#fb7185" if a.get("level") == "HIGH" else "#fbbf24"
        bg = "rgba(244,63,94,0.1)" if a.get("level") == "HIGH" else "rgba(245,158,11,0.1)"
        border = "rgba(244,63,94,0.3)" if a.get("level") == "HIGH" else "rgba(245,158,11,0.3)"
        alert_items_html += f"""
        <div style="background: {bg}; border: 1px solid {border}; border-radius: 10px; padding: 8px 14px; display: flex; align-items: center; gap: 10px; font-size: 0.78rem;">
            <span style="width: 8px; height: 8px; border-radius: 50%; background: {color}; box-shadow: 0 0 8px {color};"></span>
            <span style="color: #ffffff; font-weight: 700;">{a.get('title', 'Alert')}:</span>
            <span style="color: #cbd5e1;">{a.get('msg', '')}</span>
        </div>
        """
        
    ribbon_html = f"""
    <div style="background: rgba(12, 16, 30, 0.85); border: 1px solid rgba(255,255,255,0.08); border-radius: 14px; padding: 12px 18px; margin-bottom: 18px; display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 12px;">
        <div style="display: flex; align-items: center; gap: 8px; color: #fb7185; font-weight: 800; font-size: 0.82rem; font-family: 'JetBrains Mono', monospace;">
            <span class="live-dot-red"></span> <span>TACTICAL ALERTS:</span>
        </div>
        <div style="display: flex; gap: 10px; flex-wrap: wrap; flex: 1; justify-content: flex-end;">
            {alert_items_html}
        </div>
    </div>
    """
    st.markdown(ribbon_html, unsafe_allow_html=True)

def render_live_telemetry_hud(
    total_v: int,
    tw_pct: float,
    peds: int,
    cars: int,
    bikes: int,
    buses: int,
    trucks: int,
    bicycles: int = 0,
    fps_val: float = 28.4,
    avg_conf: float = 0.81,
    unique_tracked: int = 0,
    near_misses: int = 0
) -> str:
    """Returns a clean, error-free HTML string for the live detection telemetry & diagnostics HUD."""
    hud_html = (
        '<div style="background: #0c101e; border: 1px solid rgba(255,255,255,0.08); border-radius: 14px; padding: 18px; box-shadow: 0 4px 20px rgba(0,0,0,0.4);">'
        
        # 4 Core KPI Tiles
        '<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin-bottom: 16px;">'
        '<div style="background: rgba(15,23,42,0.85); border: 1px solid rgba(255,255,255,0.08); border-radius: 12px; padding: 14px; text-align: center;">'
        '<div style="font-size: 0.70rem; color: #94a3b8; font-family:\'JetBrains Mono\', monospace; font-weight:700; text-transform:uppercase;">IN-FRAME VEHICLES</div>'
        f'<div style="font-size: 1.7rem; font-weight: 800; color: #38bdf8; font-family:\'Plus Jakarta Sans\', sans-serif;">{total_v}</div>'
        f'<div style="font-size: 0.68rem; color: #10b981;">● Unique Seen: {unique_tracked}</div>'
        '</div>'
        '<div style="background: rgba(15,23,42,0.85); border: 1px solid rgba(255,255,255,0.08); border-radius: 12px; padding: 14px; text-align: center;">'
        '<div style="font-size: 0.70rem; color: #94a3b8; font-family:\'JetBrains Mono\', monospace; font-weight:700; text-transform:uppercase;">2-WHEELER SHARE</div>'
        f'<div style="font-size: 1.7rem; font-weight: 800; color: #fbbf24; font-family:\'Plus Jakarta Sans\', sans-serif;">{tw_pct:.1f}%</div>'
        '<div style="font-size: 0.68rem; color: #fbbf24;">(Bikes / Total Vehicles)</div>'
        '</div>'
        '<div style="background: rgba(15,23,42,0.85); border: 1px solid rgba(255,255,255,0.08); border-radius: 12px; padding: 14px; text-align: center;">'
        '<div style="font-size: 0.70rem; color: #94a3b8; font-family:\'JetBrains Mono\', monospace; font-weight:700; text-transform:uppercase;">PEDESTRIANS</div>'
        f'<div style="font-size: 1.7rem; font-weight: 800; color: #fb7185; font-family:\'Plus Jakarta Sans\', sans-serif;">{peds}</div>'
        '<div style="font-size: 0.68rem; color: #f43f5e;">On-Foot Conflict Risk</div>'
        '</div>'
        '<div style="background: rgba(15,23,42,0.85); border: 1px solid rgba(255,255,255,0.08); border-radius: 12px; padding: 14px; text-align: center;">'
        '<div style="font-size: 0.70rem; color: #94a3b8; font-family:\'JetBrains Mono\', monospace; font-weight:700; text-transform:uppercase;">INFERENCE SPEED</div>'
        f'<div style="font-size: 1.7rem; font-weight: 800; color: #10b981; font-family:\'Plus Jakarta Sans\', sans-serif;">{fps_val} FPS</div>'
        f'<div style="font-size: 0.68rem; color: #38bdf8;">Avg Conf: {avg_conf:.2f}</div>'
        '</div>'
        '</div>'

        # Accurate Class Breakdown
        '<div style="background: #080c18; border: 1px solid rgba(255,255,255,0.06); border-radius: 10px; padding: 14px; font-family:\'JetBrains Mono\', monospace; font-size: 0.78rem; margin-bottom: 12px;">'
        '<div style="display:flex; justify-content:space-between; align-items:center; margin-bottom: 10px;">'
        '<div style="color: #38bdf8; font-weight: 700; font-size: 0.80rem;">● ACCURATE DETECTIONS (IN-FRAME):</div>'
        f'<div style="color: #fbbf24; font-size: 0.72rem;">Near-Misses: <b>{near_misses}</b></div>'
        '</div>'
        f'<div style="display:flex; justify-content:space-between; color:#cbd5e1; margin-bottom:5px; padding:3px 0; border-bottom:1px solid rgba(255,255,255,0.04);"><span>🚗 Cars (Green Box):</span> <b style="color:#ffffff;">{cars}</b></div>'
        f'<div style="display:flex; justify-content:space-between; color:#cbd5e1; margin-bottom:5px; padding:3px 0; border-bottom:1px solid rgba(255,255,255,0.04);"><span>🏍️ Motorcycles / Two-Wheelers (Cyan):</span> <b style="color:#38bdf8;">{bikes}</b></div>'
        f'<div style="display:flex; justify-content:space-between; color:#cbd5e1; margin-bottom:5px; padding:3px 0; border-bottom:1px solid rgba(255,255,255,0.04);"><span>🚲 Bicycles / Cyclists (Lime):</span> <b style="color:#a3e635;">{bicycles}</b></div>'
        f'<div style="display:flex; justify-content:space-between; color:#cbd5e1; margin-bottom:5px; padding:3px 0; border-bottom:1px solid rgba(255,255,255,0.04);"><span>🚌 Transit Buses (Amber):</span> <b style="color:#fbbf24;">{buses}</b></div>'
        f'<div style="display:flex; justify-content:space-between; color:#cbd5e1; margin-bottom:5px; padding:3px 0; border-bottom:1px solid rgba(255,255,255,0.04);"><span>🚚 Commercial Trucks (Orange):</span> <b style="color:#f97316;">{trucks}</b></div>'
        f'<div style="display:flex; justify-content:space-between; color:#cbd5e1; padding:3px 0;"><span>🚶 Pedestrians on Foot (Red Box):</span> <b style="color:#fb7185;">{peds}</b></div>'
        '</div>'

        # Transparent Architecture Note
        '<div style="background: rgba(99,102,241,0.08); border: 1px solid rgba(99,102,241,0.25); border-radius: 8px; padding: 10px 12px; font-size: 0.72rem; color: #c7d2fe; line-height: 1.4;">'
        '<b>Model Scope:</b> YOLOv8 (COCO 80-Class) with ByteTrack &amp; Rider Overlap Filter. '
        '<i>Note: Auto-rickshaws &amp; 3-wheelers classify within general vehicle taxonomy; custom IDD fine-tuning recommended for Indian 3-wheeler specialization.</i>'
        '</div>'

        '</div>'
    )
    return hud_html

def render_monitored_node_card(j: Dict[str, Any], score: float, lvl: str, score_col: str, primary_factor: str) -> str:
    """Returns a clean HTML card for a monitored junction node with zero leading markdown indentation."""
    badge_html = get_risk_badge_html(lvl)
    card_html = (
        '<div style="padding: 2px;">'
        '<div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 8px;">'
        '<div>'
        f'<div style="font-size: 1.0rem; font-weight: 800; color: #ffffff; font-family: \'Plus Jakarta Sans\', sans-serif;">{j["name"]}</div>'
        f'<div style="font-size: 0.78rem; color: #94a3b8; margin-top: 2px;">📍 {j["city"]}, {j["state"]}</div>'
        '</div>'
        '<div style="text-align: right;">'
        f'<div style="font-size: 1.5rem; font-weight: 800; color: {score_col}; font-family: \'Plus Jakarta Sans\', sans-serif; line-height: 1;">{score:.1f}</div>'
        '<div style="font-size: 0.65rem; color: #64748b; font-family: \'JetBrains Mono\', monospace;">/ 100</div>'
        '</div>'
        '</div>'
        '<div style="background: rgba(15, 23, 42, 0.75); border: 1px solid rgba(255,255,255,0.06); border-radius: 8px; padding: 8px 10px; margin: 10px 0; font-size: 0.74rem;">'
        '<span style="color: #64748b; font-weight: 700; font-family:\'JetBrains Mono\', monospace; text-transform:uppercase;">PRIMARY DRIVER:</span>'
        f'<div style="color: #cbd5e1; font-weight: 600; margin-top: 2px;">⚡ {primary_factor}</div>'
        '</div>'
        '<div style="display: flex; justify-content: space-between; align-items: center; margin-top: 8px; padding-top: 6px; border-top: 1px solid rgba(255,255,255,0.06);">'
        f'<div>{badge_html}</div>'
        f'<span style="font-size: 0.70rem; color: #64748b; font-family: \'JetBrains Mono\', monospace;">ID: {j["junction_id"]}</span>'
        '</div>'
        '</div>'
    )
    return card_html

def render_tactical_kpi_card(label: str, value: Any, subtext: str, badge_label: str = "ACTIVE", badge_class: str = "badge-live-cyan", dot_class: str = "live-dot-cyan", icon_class: str = "kpi-icon-jnc", is_critical: bool = False, denom: str = "", value_color: str = "#ffffff") -> str:
    """Returns a clean unindented HTML string for top tactical KPI metric cards."""
    card_crit = " kpi-card-critical" if is_critical else ""
    denom_html = f' <span class="kpi-denom">{denom}</span>' if denom else ""
    return (
        f'<div class="kpi-tactical-card{card_crit}">'
        '<div class="kpi-card-header">'
        '<div class="window-dots"><span class="dot"></span><span class="dot"></span><span class="dot"></span></div>'
        f'<span class="{badge_class}"><span class="{dot_class}"></span> {badge_label}</span>'
        '</div>'
        '<div class="kpi-card-body">'
        f'<div class="kpi-icon-wrap {icon_class}"></div>'
        '<div>'
        f'<div class="kpi-label">{label}</div>'
        f'<div class="kpi-num" style="color: {value_color};">{value}{denom_html}</div>'
        f'<div class="kpi-sub"><span>{subtext}</span></div>'
        '</div>'
        '</div>'
        '</div>'
    )

def render_simulation_result_card(simulated_new_score: float, total_reduction: float) -> str:
    """Returns clean HTML for what-if simulation result card."""
    return (
        '<div style="background: rgba(16, 185, 129, 0.12); border: 1px solid rgba(16, 185, 129, 0.35); border-radius: 12px; padding: 14px; margin-top: 10px; display: flex; justify-content: space-between; align-items: center;">'
        '<div>'
        '<div style="font-size: 0.80rem; font-weight: 700; color: #34d399; font-family:\'JetBrains Mono\', monospace;">SIMULATED RISK REDUCTION:</div>'
        '<div style="font-size: 0.76rem; color: #94a3b8;">Projected impact after civic interventions</div>'
        '</div>'
        f'<div style="font-size: 1.65rem; font-weight: 900; color: #34d399; font-family:\'Plus Jakarta Sans\', sans-serif;">{simulated_new_score:.1f} <span style="font-size: 0.88rem; color: #64748b;">(-{total_reduction:.1f})</span></div>'
        '</div>'
    )

def render_citizen_report_card(j_name: str, issue: str, sev_badge: str, badge_color: str, rep_by: str, ts: str, desc: str) -> str:
    """Returns clean HTML for a citizen field report card."""
    return (
        '<div style="background: #0c101e; border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 14px; padding: 16px 20px; margin-bottom: 14px; box-shadow: 0 4px 16px rgba(0,0,0,0.35);">'
        '<div style="display:flex; justify-content:space-between; align-items:center;">'
        f'<strong style="color:#ffffff; font-size:0.98rem; font-family:\'Plus Jakarta Sans\', sans-serif;">📍 {j_name} · <span style="color:#38bdf8;">{issue}</span></strong>'
        f'<span style="font-size: 0.74rem; font-weight:800; color:{badge_color}; font-family:\'JetBrains Mono\', monospace;">{sev_badge}</span>'
        '</div>'
        f'<div style="font-size: 0.76rem; color: #94a3b8; margin-top: 4px;">Reporter: <b style="color:#cbd5e1;">{rep_by}</b> | 📅 {ts}</div>'
        f'<div style="font-size: 0.88rem; color: #cbd5e1; margin-top: 8px; line-height:1.5;">{desc}</div>'
        '</div>'
    )

def render_xai_radar_chart(factors: List[Dict[str, Any]]):
    """
    Renders an interactive Plotly Radar / Spider chart comparing multi-factor risk vectors.
    """
    import plotly.graph_objects as go
    
    categories = []
    values = []
    
    if factors:
        for f in factors:
            categories.append(f.get("factor", "Factor"))
            values.append(round(float(f.get("weight", 0.0)) * 100, 1))
    else:
        categories = ["Crash Severity", "Traffic Density", "Near-Miss Conflicts", "Two-Wheeler Share", "Citizen Reports"]
        values = [45, 30, 25, 20, 15]

    # Close radar loop
    categories.append(categories[0])
    values.append(values[0])

    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        fillcolor='rgba(99, 102, 241, 0.25)',
        line=dict(color='#38bdf8', width=2),
        marker=dict(size=6, color='#6366f1'),
        name='Risk Contribution'
    ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, max(60, max(values) + 10)],
                color='#64748b',
                gridcolor='rgba(255, 255, 255, 0.08)',
                linecolor='rgba(255, 255, 255, 0.08)'
            ),
            angularaxis=dict(
                color='#cbd5e1',
                gridcolor='rgba(255, 255, 255, 0.08)',
                linecolor='rgba(255, 255, 255, 0.08)'
            ),
            bgcolor='rgba(12, 16, 30, 0.5)'
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=30, r=30, t=25, b=25),
        height=280,
        showlegend=False,
        font=dict(family='Plus Jakarta Sans', color='#f1f5f9', size=11)
    )
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

def render_contributing_factors(factors: Optional[List[Dict[str, Any]]], junction_id: Optional[str] = None):
    """Renders contributing factors as labeled progress bars with glowing modern styling."""
    if not factors:
        render_awaiting_data_banner()
        return
        
    st.markdown('<div class="factors-section">', unsafe_allow_html=True)

    # When "Citizen Reports" is the top contributing factor, show context sub-line
    if len(factors) > 0 and factors[0].get("factor") in ["Citizen Reports", "Citizen Hazard Reports"]:
        sub_line = None
        if junction_id:
            try:
                from src.analytics.risk_engine import get_citizen_cluster_stats
                cluster_stats = get_citizen_cluster_stats(junction_id)
                sub_line = cluster_stats.get("summary_line")
            except Exception:
                pass
        if not sub_line:
            sub_line = "Multiple reports in last 30 days driving citizen incident elevation"

        st.markdown(f"""
        <div style="background: rgba(99, 102, 241, 0.12); border: 1px solid rgba(99, 102, 241, 0.35); border-left: 4px solid #6366f1; border-radius: 8px; padding: 10px 14px; margin-bottom: 14px; font-size: 0.82rem; color: #c7d2fe; display: flex; align-items: center; gap: 10px;">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#38bdf8" stroke-width="2"><path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>
            <span><b>Citizen Alert Cluster:</b> {sub_line}</span>
        </div>
        """, unsafe_allow_html=True)

    for factor_info in factors:
        factor = factor_info.get("factor", "Unknown Factor")
        weight = factor_info.get("weight", 0.0)
        weight_clamped = max(0.0, min(1.0, float(weight)))
        pct = int(weight_clamped * 100)
        
        # Determine bar color based on impact intensity
        if pct >= 35:
            bar_color = "linear-gradient(90deg, #f43f5e, #e11d48)"
            text_accent = "#fb7185"
        elif pct >= 20:
            bar_color = "linear-gradient(90deg, #f59e0b, #d97706)"
            text_accent = "#fbbf24"
        else:
            bar_color = "linear-gradient(90deg, #6366f1, #38bdf8)"
            text_accent = "#38bdf8"

        st.markdown(f"""
        <div style="margin-bottom: 14px;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
                <span style="font-size: 0.88rem; font-weight: 600; color: #f1f5f9;">{factor}</span>
                <span style="font-size: 0.82rem; font-weight: 700; color: {text_accent}; font-family: 'JetBrains Mono', monospace;">
                    {pct}% Impact
                </span>
            </div>
            <div style="background: rgba(15, 23, 42, 0.8); height: 8px; border-radius: 9999px; overflow: hidden; border: 1px solid rgba(255, 255, 255, 0.08);">
                <div style="width: {pct}%; height: 100%; background: {bar_color}; border-radius: 9999px; transition: width 0.6s ease; box-shadow: 0 0 10px rgba(99, 102, 241, 0.3);"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

def render_awaiting_data_banner():
    """Renders the 'Awaiting Data' info banner."""
    st.markdown("""
    <div class="awaiting-data-banner">
        <div class="awaiting-icon">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#38bdf8" stroke-width="2"><circle cx="12" cy="12" r="2"/><path d="M16.24 7.76a6 6 0 0 1 0 8.49m-8.48-.01a6 6 0 0 1 0-8.49m11.31-2.82a10 10 0 0 1 0 14.14m-14.14 0a10 10 0 0 1 0-14.14"/></svg>
        </div>
        <div>
            <div class="awaiting-title">AWAITING TELEMETRY DATA</div>
            <div class="awaiting-desc">
                Visual risk analysis and historical accident weighting are currently pending for this junction. 
                Detailed contributing factor scores will be populated automatically when live streams and database 
                connectors are active.
            </div>
        </div>
        <div class="radar-sweep"></div>
    </div>
    """, unsafe_allow_html=True)

def render_navbar(active_page: str = "Dashboard"):
    """Renders the CareerVerse AI-style floating frosted navbar with status telemetry."""
    navbar_html = (
        '<div id="jg-top-anchor" style="position:relative; top:-20px; height:1px;"></div>'
        '<div class="tactical-navbar">'
        '<div class="navbar-brand-group">'
        '<div class="brand-shield-logo"></div>'
        '<div>'
        '<div class="brand-title">JunctionGuard <span class="brand-ai">AI</span></div>'
        '<div class="brand-sub">Autonomous Vision Analytics &amp; Road Hazard Intelligence</div>'
        '</div>'
        '</div>'
        '<div class="navbar-status-badges">'
        '<div class="status-pill status-pill-operational">'
        '<span class="pill-icon"></span>'
        '<div class="pill-meta">'
        '<span class="pill-label">SYSTEM STATUS</span>'
        '<span class="pill-val" style="color: #10b981;">100% OPERATIONAL</span>'
        '</div>'
        '</div>'
        '<div class="status-pill status-pill-inference">'
        '<span class="pill-icon"></span>'
        '<div class="pill-meta">'
        '<span class="pill-label">AI VISION INFERENCE</span>'
        '<span class="pill-val" style="color: #38bdf8;">28 FPS LIVE</span>'
        '</div>'
        '</div>'
        '</div>'
        '</div>'
    )
    st.markdown(navbar_html, unsafe_allow_html=True)

def render_dashboard_overview_header(title: str = "Dashboard", subtitle: str = "Real-time Junction Risk Surveillance System"):
    """Renders the subheader bar with eyebrow pill, active page title, and live date/time widget."""
    now = datetime.now()
    date_str = now.strftime("%b %d, %Y")
    time_str = now.strftime("%I:%M:%S %p")
    
    header_html = (
        '<div class="overview-header-bar">'
        '<div>'
        '<div class="hero-eyebrow"><span class="eyebrow-dot"></span> Powered by JunctionGuard Neural Engine</div>'
        f'<div class="overview-title">{title}</div>'
        f'<div class="overview-sub">{subtitle}</div>'
        '</div>'
        '<div class="overview-right-actions">'
        '<div class="datetime-pill">'
        '<span class="pill-cal-icon"></span>'
        f'<span>{date_str}</span>'
        '<span class="dt-divider">|</span>'
        f'<span class="dt-time">{time_str}</span>'
        '</div>'
        '</div>'
        '</div>'
    )
    st.markdown(header_html, unsafe_allow_html=True)

def render_hero_mission_banner():
    """Renders a clean, spacious modern website hero banner."""
    banner_html = (
        '<div style="background: linear-gradient(135deg, rgba(15, 23, 42, 0.8) 0%, rgba(10, 14, 26, 0.9) 100%); '
        'border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 16px; padding: 30px 36px; margin-bottom: 26px; '
        'box-shadow: 0 10px 30px rgba(0, 0, 0, 0.4); display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 24px;">'
        '<div style="max-width: 680px;">'
        '<div style="display: inline-flex; align-items: center; gap: 8px; background: rgba(56, 189, 248, 0.1); '
        'border: 1px solid rgba(56, 189, 248, 0.25); border-radius: 9999px; padding: 4px 14px; font-size: 0.74rem; '
        'font-weight: 700; color: #38bdf8; letter-spacing: 0.05em; text-transform: uppercase; font-family: \'JetBrains Mono\', monospace; margin-bottom: 12px;">'
        '<span style="width: 6px; height: 6px; border-radius: 50%; background: #38bdf8; display: inline-block;"></span>'
        'NATIONAL ROAD SAFETY PLATFORM'
        '</div>'
        '<div style="font-size: 2.1rem; font-weight: 800; color: #ffffff; line-height: 1.25; letter-spacing: -0.02em; font-family: \'Plus Jakarta Sans\', sans-serif;">'
        'Autonomous Road Hazard Intelligence &amp; Surveillance'
        '</div>'
        '<div style="font-size: 0.95rem; color: #94a3b8; margin-top: 8px; line-height: 1.6; font-weight: 400;">'
        'Real-time multi-factor explainable AI (XAI) risk scoring, YOLOv8 computer vision, and crowdsourced hazard verification across major Indian metropolitan corridors.'
        '</div>'
        '</div>'
        '<div style="display: flex; gap: 14px; flex-wrap: wrap;">'
        '<div style="background: rgba(15, 23, 42, 0.7); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 12px; padding: 14px 22px; min-width: 135px; text-align: center;">'
        '<div style="font-size: 0.70rem; color: #94a3b8; font-family: \'JetBrains Mono\', monospace; font-weight: 700; text-transform: uppercase;">MONITORED</div>'
        '<div style="font-size: 1.5rem; font-weight: 800; color: #38bdf8; margin-top: 2px;">7 CITIES</div>'
        '<div style="font-size: 0.68rem; color: #64748b; font-family: \'JetBrains Mono\', monospace;">12 Critical Nodes</div>'
        '</div>'
        '<div style="background: rgba(15, 23, 42, 0.7); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 12px; padding: 14px 22px; min-width: 135px; text-align: center;">'
        '<div style="font-size: 0.70rem; color: #94a3b8; font-family: \'JetBrains Mono\', monospace; font-weight: 700; text-transform: uppercase;">VISION AI</div>'
        '<div style="font-size: 1.5rem; font-weight: 800; color: #10b981; margin-top: 2px;">28 FPS</div>'
        '<div style="font-size: 0.68rem; color: #64748b; font-family: \'JetBrains Mono\', monospace;">YOLOv8 Core</div>'
        '</div>'
        '</div>'
        '</div>'
    )
    st.markdown(banner_html, unsafe_allow_html=True)

def render_footer():
    """Renders the bottom status bar with telemetry stats and copyright."""
    footer_html = (
        '<div class="tactical-footer">'
        '<div class="footer-stat">'
        '<span class="live-dot-green"></span>'
        '<span>Data Source: <b>Live Sensors + CCTV + Edge Vision</b></span>'
        '</div>'
        '<div class="footer-stat">'
        '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#38bdf8" stroke-width="2"><circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"/></svg>'
        '<span>AI Architecture: <b>JunctionGuard v2.5</b></span>'
        '</div>'
        '<div class="footer-stat footer-copyright">'
        '&copy; 2026 JunctionGuard AI. All Rights Reserved.'
        '</div>'
        '</div>'
    )
    st.markdown(footer_html, unsafe_allow_html=True)

def inject_custom_styles():
    """Injects the clean modern website design system."""
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:ital,wght@0,300;0,400;0,500;0,600;0,700;0,800;1,400&family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600;700&display=swap');

        /* ── Hide Streamlit default header/footer & Sidebar ── */
        #MainMenu { visibility: hidden !important; display: none !important; }
        header[data-testid="stHeader"] { visibility: hidden !important; display: none !important; }
        div[data-testid="stToolbar"] { visibility: hidden !important; display: none !important; }
        footer { visibility: hidden !important; display: none !important; }
        .stDeployButton { visibility: hidden !important; display: none !important; }

        /* ── Completely Hide Sidebar on All Browsers (Safari & Chrome) ── */
        section[data-testid="stSidebar"],
        div[data-testid="stSidebar"],
        button[data-testid="stSidebarCollapsedControl"],
        div[data-testid="collapsedControl"],
        [data-testid="stSidebarNav"],
        [data-testid="stSidebarUserContent"],
        [data-testid="stSidebarHeader"] {
            display: none !important;
            visibility: hidden !important;
            width: 0 !important;
            height: 0 !important;
            margin: 0 !important;
            padding: 0 !important;
            position: absolute !important;
            left: -9999px !important;
        }

        /* ── Modern Obsidian Canvas ── */
        html, body, [class*="css"], .stApp {
            font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif !important;
            background-color: #070a13 !important;
            color: #f1f5f9 !important;
            min-height: 100vh;
        }

        /* ── Clean Spacious Centered Layout (Not Congested) ── */
        .main .block-container {
            max-width: 1360px !important;
            margin: 0 auto !important;
            padding: 1.8rem 2.2rem 5rem 2.2rem !important;
        }
        @media (max-width: 900px) {
            .main .block-container {
                padding: 1rem 1rem 3rem 1rem !important;
            }
        }

        /* ── CareerVerse Hero Eyebrow Tag ── */
        .hero-eyebrow {
            display: inline-flex;
            align-items: center;
            gap: 10px;
            background: rgba(99, 102, 241, 0.14);
            border: 1px solid rgba(99, 102, 241, 0.4);
            border-radius: 9999px;
            padding: 6px 18px;
            font-size: 0.80rem;
            font-weight: 700;
            color: #818cf8;
            letter-spacing: 0.06em;
            text-transform: uppercase;
            margin-bottom: 10px;
            font-family: 'JetBrains Mono', monospace;
            box-shadow: 0 0 16px rgba(99, 102, 241, 0.2);
        }
        .eyebrow-dot {
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background: #38bdf8;
            box-shadow: 0 0 10px #38bdf8;
            animation: heat-glow-pulse 2s infinite ease-in-out;
        }

        /* ── Modern Glass Panels & Containers ── */
        .tactical-panel,
        [data-testid="stVerticalBlockBorderWrapper"] > div {
            background: #0c101e !important;
            border: 1px solid rgba(255, 255, 255, 0.09) !important;
            border-radius: 16px !important;
            padding: 22px !important;
            box-shadow: 0 10px 36px rgba(0, 0, 0, 0.5) !important;
            position: relative !important;
            overflow: hidden !important;
            transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1) !important;
        }
        .tactical-panel:hover,
        [data-testid="stVerticalBlockBorderWrapper"] > div:hover {
            border-color: rgba(99, 102, 241, 0.4) !important;
            box-shadow: 0 14px 42px rgba(0, 0, 0, 0.65), 0 0 24px rgba(99, 102, 241, 0.2) !important;
        }

        /* ── Floating Frosted Navigation Bar ── */
        .tactical-navbar {
            display: flex;
            justify-content: space-between;
            align-items: center;
            background: rgba(12, 16, 30, 0.9);
            backdrop-filter: blur(24px);
            -webkit-backdrop-filter: blur(24px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 18px;
            padding: 16px 28px;
            margin-bottom: 20px;
            box-shadow: 0 12px 36px rgba(0, 0, 0, 0.55);
        }
        .navbar-brand-group {
            display: flex;
            align-items: center;
            gap: 16px;
        }
        .brand-shield-logo {
            width: 48px;
            height: 48px;
            background: linear-gradient(135deg, #6366f1 0%, #38bdf8 100%) !important;
            background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%23ffffff' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z'/%3E%3Ccircle cx='12' cy='12' r='2' fill='%23ffffff'/%3E%3Cpath d='M12 7v3m0 4v3m-5-5h3m4 0h3'/%3E%3C/svg%3E") !important;
            background-repeat: no-repeat !important;
            background-position: center !important;
            background-size: 28px 28px !important;
            border-radius: 14px !important;
            box-shadow: 0 0 24px rgba(99, 102, 241, 0.5) !important;
            display: inline-block !important;
        }
        .brand-title {
            font-size: 1.65rem;
            font-weight: 800;
            color: #ffffff;
            line-height: 1.1;
            letter-spacing: -0.025em;
        }
        .brand-ai {
            background: linear-gradient(135deg, #38bdf8 0%, #818cf8 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-weight: 800;
        }
        .brand-sub {
            font-size: 0.82rem;
            color: #94a3b8;
            margin-top: 4px;
            font-weight: 500;
        }

        .navbar-status-badges {
            display: flex;
            align-items: center;
            gap: 14px;
            flex-wrap: wrap;
        }
        .status-pill {
            display: inline-flex;
            align-items: center;
            gap: 10px;
            background: #11172a;
            border: 1px solid rgba(255, 255, 255, 0.09);
            border-radius: 12px;
            padding: 8px 18px;
        }
        .status-pill-operational .pill-icon {
            width: 16px;
            height: 16px;
            display: inline-block;
            background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%2310b981' stroke-width='2.5'%3E%3Cpath d='M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z'/%3E%3C/svg%3E");
            background-repeat: no-repeat;
            background-position: center;
            background-size: 16px 16px;
        }
        .status-pill-inference .pill-icon {
            width: 16px;
            height: 16px;
            display: inline-block;
            background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%2338bdf8' stroke-width='2.5'%3E%3Ccircle cx='12' cy='12' r='9'/%3E%3Ccircle cx='12' cy='12' r='3'/%3E%3Cline x1='12' y1='2' x2='12' y2='5'/%3E%3Cline x1='12' y1='19' x2='12' y2='22'/%3E%3Cline x1='2' y1='12' x2='5' y2='12'/%3E%3Cline x1='19' y1='12' x2='22' y2='12'/%3E%3C/svg%3E");
            background-repeat: no-repeat;
            background-position: center;
            background-size: 16px 16px;
        }
        .pill-cal-icon {
            width: 16px;
            height: 16px;
            display: inline-block;
            background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%23818cf8' stroke-width='2'%3E%3Crect x='3' y='4' width='18' height='18' rx='2' ry='2'/%3E%3Cline x1='16' y1='2' x2='16' y2='6'/%3E%3Cline x1='8' y1='2' x2='8' y2='6'/%3E%3Cline x1='3' y1='10' x2='21' y2='10'/%3E%3C/svg%3E");
            background-repeat: no-repeat;
            background-position: center;
            background-size: 16px 16px;
        }

        /* ── Subheader Overview Bar ── */
        .overview-header-bar {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin: 14px 0 22px 0;
            padding-bottom: 6px;
        }
        .overview-title {
            font-size: 2.2rem;
            font-weight: 800;
            color: #ffffff;
            line-height: 1.15;
            letter-spacing: -0.03em;
            background: linear-gradient(135deg, #ffffff 40%, #c7d2fe 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        .overview-sub {
            font-size: 0.95rem;
            color: #94a3b8;
            margin-top: 4px;
        }
        .overview-right-actions {
            display: flex;
            align-items: center;
            gap: 14px;
        }
        .datetime-pill {
            display: inline-flex;
            align-items: center;
            gap: 10px;
            background: #0f1424;
            border: 1px solid rgba(255, 255, 255, 0.09);
            border-radius: 12px;
            padding: 9px 18px;
        .dt-divider {
            color: #475569;
        }
        .dt-time {
            color: #38bdf8;
            font-weight: 700;
        }

        /* ── CareerVerse-Style Visual Enterprise KPI Cards ── */
        .kpi-tactical-card {
            background: #0c101e;
            border: 1px solid rgba(255, 255, 255, 0.09);
            border-radius: 18px;
            padding: 22px 24px;
            position: relative;
            overflow: hidden;
            display: flex;
            flex-direction: column;
            gap: 14px;
            box-shadow: 0 10px 32px rgba(0, 0, 0, 0.5);
            transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
        }
        .kpi-tactical-card:hover {
            border-color: rgba(99, 102, 241, 0.5);
            transform: translateY(-4px);
            box-shadow: 0 16px 40px rgba(0, 0, 0, 0.65), 0 0 24px rgba(99, 102, 241, 0.25);
        }
        .kpi-card-critical {
            border-color: rgba(244, 63, 94, 0.4) !important;
            background: linear-gradient(180deg, rgba(244, 63, 94, 0.1) 0%, #0c101e 100%) !important;
        }
        .kpi-card-critical:hover {
            border-color: rgba(244, 63, 94, 0.7) !important;
            box-shadow: 0 16px 40px rgba(0, 0, 0, 0.65), 0 0 28px rgba(244, 63, 94, 0.3) !important;
        }
        .kpi-card-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .window-dots {
            display: flex;
            gap: 6px;
        }
        .window-dots .dot {
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background: rgba(255, 255, 255, 0.25);
        }
        .badge-live-cyan {
            font-size: 0.70rem;
            font-weight: 800;
            color: #38bdf8;
            background: rgba(56, 189, 248, 0.14);
            border: 1px solid rgba(56, 189, 248, 0.35);
            border-radius: 9999px;
            padding: 3px 10px;
            display: inline-flex;
            align-items: center;
            gap: 6px;
            font-family: 'JetBrains Mono', monospace;
        }
        .badge-live-red {
            font-size: 0.70rem;
            font-weight: 800;
            color: #fb7185;
            background: rgba(244, 63, 94, 0.16);
            border: 1px solid rgba(244, 63, 94, 0.45);
            border-radius: 9999px;
            padding: 3px 10px;
            display: inline-flex;
            align-items: center;
            gap: 6px;
            font-family: 'JetBrains Mono', monospace;
        }
        .badge-live-amber {
            font-size: 0.70rem;
            font-weight: 800;
            color: #fbbf24;
            background: rgba(245, 158, 11, 0.16);
            border: 1px solid rgba(245, 158, 11, 0.45);
            border-radius: 9999px;
            padding: 3px 10px;
            display: inline-flex;
            align-items: center;
            gap: 6px;
            font-family: 'JetBrains Mono', monospace;
        }
        .badge-live-green {
            font-size: 0.70rem;
            font-weight: 800;
            color: #34d399;
            background: rgba(16, 185, 129, 0.16);
            border: 1px solid rgba(16, 185, 129, 0.45);
            border-radius: 9999px;
            padding: 3px 10px;
            display: inline-flex;
            align-items: center;
            gap: 6px;
            font-family: 'JetBrains Mono', monospace;
        }
        .kpi-card-body {
            display: flex;
            align-items: center;
            gap: 16px;
        }
        .kpi-label {
            font-size: 0.76rem;
            font-weight: 700;
            color: #94a3b8;
            text-transform: uppercase;
            letter-spacing: 0.07em;
            font-family: 'JetBrains Mono', monospace;
            margin-bottom: 4px;
        }
        .kpi-num {
            font-size: 2.45rem;
            font-weight: 800;
            color: #ffffff;
            line-height: 1.1;
            font-family: 'Plus Jakarta Sans', sans-serif;
        }
        .kpi-denom {
            font-size: 0.95rem;
            color: #64748b;
            font-weight: 500;
        }
        .kpi-sub {
            font-size: 0.74rem;
            font-weight: 700;
            letter-spacing: 0.05em;
            font-family: 'JetBrains Mono', monospace;
            margin-top: 6px;
            display: flex;
            align-items: center;
            gap: 6px;
        }
        .kpi-icon-wrap {
            width: 52px;
            height: 52px;
            border-radius: 14px;
            display: flex;
            align-items: center;
            justify-content: center;
            flex-shrink: 0;
        }

        /* ── KPI Icon Backgrounds with Cyber Gradients ── */
        .kpi-icon-jnc {
            background-color: rgba(99, 102, 241, 0.15) !important;
            border: 1px solid rgba(99, 102, 241, 0.35) !important;
            background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%2338bdf8' stroke-width='2'%3E%3Ccircle cx='12' cy='12' r='3'/%3E%3Ccircle cx='19' cy='12' r='2'/%3E%3Ccircle cx='5' cy='12' r='2'/%3E%3Ccircle cx='12' cy='19' r='2'/%3E%3Ccircle cx='12' cy='5' r='2'/%3E%3Cline x1='12' y1='15' x2='12' y2='17'/%3E%3Cline x1='12' y1='7' x2='12' y2='9'/%3E%3Cline x1='15' y1='12' x2='17' y2='12'/%3E%3Cline x1='7' y1='12' x2='9' y2='12'/%3E%3C/svg%3E") !important;
            background-repeat: no-repeat !important;
            background-position: center !important;
            background-size: 22px 22px !important;
            box-shadow: 0 0 14px rgba(99, 102, 241, 0.25) !important;
        }
        .kpi-icon-alert {
            background-color: rgba(244, 63, 94, 0.15) !important;
            border: 1px solid rgba(244, 63, 94, 0.45) !important;
            background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%23fb7185' stroke-width='2'%3E%3Cpath d='M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z'/%3E%3Cline x1='12' y1='9' x2='12' y2='13'/%3E%3Cline x1='12' y1='17' x2='12.01' y2='17'/%3E%3C/svg%3E") !important;
            background-repeat: no-repeat !important;
            background-position: center !important;
            background-size: 22px 22px !important;
            box-shadow: 0 0 14px rgba(244, 63, 94, 0.25) !important;
        }
        .kpi-icon-score {
            background-color: rgba(245, 158, 11, 0.15) !important;
            border: 1px solid rgba(245, 158, 11, 0.4) !important;
            background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%23fbbf24' stroke-width='2'%3E%3Cpolyline points='22 12 18 12 15 21 9 3 6 12 2 12'/%3E%3C/svg%3E") !important;
            background-repeat: no-repeat !important;
            background-position: center !important;
            background-size: 22px 22px !important;
            box-shadow: 0 0 14px rgba(245, 158, 11, 0.25) !important;
        }
        .kpi-icon-reports {
            background-color: rgba(16, 185, 129, 0.15) !important;
            border: 1px solid rgba(16, 185, 129, 0.4) !important;
            background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%2334d399' stroke-width='2'%3E%3Cpath d='M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2'/%3E%3Ccircle cx='9' cy='7' r='4'/%3E%3Cpath d='M23 21v-2a4 4 0 0 0-3-3.87'/%3E%3Cpath d='M16 3.13a4 4 0 0 1 0 7.75'/%3E%3C/svg%3E") !important;
            background-repeat: no-repeat !important;
            background-position: center !important;
            background-size: 22px 22px !important;
            box-shadow: 0 0 14px rgba(16, 185, 129, 0.25) !important;
        }

        /* ── Pulse Indicator Dots ── */
        .live-dot-green, .live-dot-cyan {
            width: 7px;
            height: 7px;
            background: #10b981;
            border-radius: 50%;
            display: inline-block;
            box-shadow: 0 0 8px #10b981;
        }
        .live-dot-cyan {
            background: #38bdf8;
            box-shadow: 0 0 8px #38bdf8;
        }
        .live-dot-red {
            width: 7px;
            height: 7px;
            background: #f43f5e;
            border-radius: 50%;
            display: inline-block;
            box-shadow: 0 0 8px #f43f5e;
            animation: pulseCritical 1.8s infinite;
        }
        @keyframes pulseCritical {
            0%   { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(244, 63, 94, 0.7); }
            70%  { transform: scale(1);    box-shadow: 0 0 0 6px rgba(244, 63, 94, 0); }
            100% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(244, 63, 94, 0); }
        }

        /* ── Navigation Tabs Command Deck ── */
        .stTabs [data-baseweb="tab-list"] {
            gap: 8px;
            background: #0a0e1a !important;
            padding: 6px 8px;
            border-radius: 12px;
            border: 1px solid rgba(255, 255, 255, 0.08);
            box-shadow: 0 6px 20px rgba(0, 0, 0, 0.4);
            margin-bottom: 14px;
        }
        .stTabs [data-baseweb="tab"] {
            border-radius: 10px;
            padding: 9px 20px;
            font-family: 'Plus Jakarta Sans', system-ui, sans-serif;
            font-weight: 600;
            font-size: 0.88rem;
            color: #94a3b8;
            border: 1px solid transparent;
            background: transparent;
            transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
        }
        .stTabs [data-baseweb="tab"]:hover {
            color: #ffffff;
            background: rgba(255, 255, 255, 0.05);
        }
        .stTabs [aria-selected="true"] {
            background: linear-gradient(135deg, rgba(99, 102, 241, 0.2) 0%, rgba(56, 189, 248, 0.15) 100%) !important;
            color: #ffffff !important;
            border: 1px solid #6366f1 !important;
            box-shadow: 0 0 16px rgba(99, 102, 241, 0.3) !important;
        }

        /* ── Form Inputs & Selectboxes ── */
        .stTextInput input, .stTextArea textarea, [data-baseweb="select"] {
            background-color: #0d1222 !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
            border-radius: 10px !important;
            color: #f1f5f9 !important;
            font-family: 'Plus Jakarta Sans', sans-serif !important;
            font-size: 0.88rem !important;
            transition: all 0.2s ease !important;
        }
        .stTextInput input:focus, .stTextArea textarea:focus, [data-baseweb="select"]:focus-within {
            border-color: #6366f1 !important;
            box-shadow: 0 0 14px rgba(99, 102, 241, 0.3) !important;
        }

        /* ── Action Buttons ── */
        .stButton > button {
            background: #11172a !important;
            color: #ffffff !important;
            border: 1px solid rgba(255, 255, 255, 0.12) !important;
            border-radius: 10px !important;
            font-family: 'Plus Jakarta Sans', sans-serif !important;
            font-weight: 600 !important;
            font-size: 0.88rem !important;
            padding: 9px 20px !important;
            transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1) !important;
        }
        .stButton > button:hover {
            background: #182038 !important;
            border-color: #6366f1 !important;
            color: #38bdf8 !important;
            transform: translateY(-1px) !important;
            box-shadow: 0 6px 20px rgba(99, 102, 241, 0.25) !important;
        }
        .stButton > button[kind="primary"], .stButton > button[data-testid="baseButton-primary"] {
            background: linear-gradient(135deg, #4f46e5 0%, #6366f1 50%, #38bdf8 100%) !important;
            border: none !important;
            color: #ffffff !important;
            font-weight: 700 !important;
            box-shadow: 0 4px 18px rgba(99, 102, 241, 0.4) !important;
        }
        .stButton > button[kind="primary"]:hover, .stButton > button[data-testid="baseButton-primary"]:hover {
            background: linear-gradient(135deg, #4338ca 0%, #4f46e5 50%, #0ea5e9 100%) !important;
            box-shadow: 0 6px 26px rgba(99, 102, 241, 0.6) !important;
            transform: translateY(-2px) !important;
        }

        /* ── Risk Badges ── */
        .badge {
            display: inline-flex;
            align-items: center;
            gap: 6px;
            padding: 4px 12px;
            border-radius: 8px;
            font-size: 0.74rem;
            font-weight: 700;
            font-family: 'JetBrains Mono', monospace;
            letter-spacing: 0.05em;
        }
        .badge-dot {
            width: 6px;
            height: 6px;
            border-radius: 50%;
            background: currentColor;
        }
        .badge-green {
            background: rgba(16, 185, 129, 0.15);
            color: #34d399;
            border: 1px solid rgba(16, 185, 129, 0.4);
        }
        .badge-amber {
            background: rgba(245, 158, 11, 0.15);
            color: #fbbf24;
            border: 1px solid rgba(245, 158, 11, 0.4);
        }
        .badge-red {
            background: rgba(244, 63, 94, 0.18);
            color: #fb7185;
            border: 1px solid rgba(244, 63, 94, 0.5);
        }
        .badge-gray {
            background: rgba(100, 116, 139, 0.15);
            color: #94a3b8;
            border: 1px solid rgba(100, 116, 139, 0.3);
        }

        /* ── Modern Footer ── */
        .tactical-footer {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 16px 24px;
            background: rgba(12, 16, 30, 0.85);
            backdrop-filter: blur(16px);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 14px;
            margin-top: 2.5rem;
            font-size: 0.76rem;
            color: #94a3b8;
            flex-wrap: wrap;
            gap: 14px;
        }
        .footer-stat {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            font-family: 'JetBrains Mono', monospace;
        }
        .footer-copyright {
            color: #64748b;
        }

        /* ── Custom Scrollbars ── */
        ::-webkit-scrollbar { width: 6px; height: 6px; }
        ::-webkit-scrollbar-track { background: #070a13; }
        ::-webkit-scrollbar-thumb { background: #1e2640; border-radius: 4px; }
        ::-webkit-scrollbar-thumb:hover { background: #6366f1; }
    </style>
    """, unsafe_allow_html=True)
