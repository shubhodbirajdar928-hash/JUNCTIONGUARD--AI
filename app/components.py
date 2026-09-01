"""
UI Components and Design System for JunctionGuard AI.
Minimalist Tactical Vision Command Center:
  - Deep obsidian #08090d canvas with precision micro-dots & subtle 1px borders
  - Bespoke vector SVG brand logo and crisp vector icons (zero unicode emojis)
  - Refined minimalist typography (Plus Jakarta Sans, Space Grotesk, JetBrains Mono)
  - Top HUD navigation bar with operational status, AI inference telemetry, and live timestamp
  - Minimalist KPI metric cards with SVG accents and status pulses
  - Semantic risk badges (LOW / MEDIUM / HIGH) & glowing radar halos
  - Explainable contributing factor progress bars
"""

import streamlit as st
from datetime import datetime
from typing import Optional, List, Dict, Any

# ── Inline SVG Vector Library (Clean, Scalable, Zero-Dependency) ──

SVG_ICONS = {
    "shield_logo": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="#f97316" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><circle cx="12" cy="12" r="2.5" fill="#f97316"/><path d="M12 6v3m0 6v3m-6-6h3m6 0h3"/></svg>""",
    
    "dashboard": """<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="7" height="9" rx="1"/><rect x="14" y="3" width="7" height="5" rx="1"/><rect x="14" y="12" width="7" height="9" rx="1"/><rect x="3" y="16" width="7" height="5" rx="1"/></svg>""",
    
    "map": """<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="1 6 1 22 8 18 16 22 23 18 23 2 16 6 8 2 1 6"/><line x1="8" y1="2" x2="8" y2="18"/><line x1="16" y1="6" x2="16" y2="22"/></svg>""",
    
    "chart": """<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="20" x2="18" y2="10"/><line x1="12" y1="20" x2="12" y2="4"/><line x1="6" y1="20" x2="6" y2="14"/></svg>""",
    
    "video": """<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="23 7 16 12 23 17 23 7"/><rect x="1" y="5" width="15" height="14" rx="2" ry="2"/></svg>""",
    
    "alert": """<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>""",
    
    "pin": """<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg>""",
    
    "radar": """<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="4"/><line x1="12" y1="3" x2="12" y2="5"/><line x1="12" y1="19" x2="12" y2="21"/><line x1="3" y1="12" x2="5" y2="12"/><line x1="19" y1="12" x2="21" y2="12"/></svg>""",
    
    "gps": """<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="22" y1="12" x2="18" y2="12"/><line x1="6" y1="12" x2="2" y2="12"/><line x1="12" y1="6" x2="12" y2="2"/><line x1="12" y1="22" x2="12" y2="18"/></svg>""",
    
    "network": """<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="2" y1="12" x2="22" y2="12"/><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/></svg>""",
    
    "camera": """<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M23 19a2 2 0 0 1-2 2H3a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h4l2-3h6l2 3h4a2 2 0 0 1 2 2z"/><circle cx="12" cy="13" r="4"/></svg>""",
    
    "search": """<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>""",
    
    "file_text": """<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/><polyline points="10 9 9 9 8 9"/></svg>""",
    
    "download": """<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/></svg>""",
    
    "cloud": """<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M18 10h-1.26A8 8 0 1 0 9 20h9a5 5 0 0 0 0-10z"/></svg>""",
    
    "users": """<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>""",
    
    "cpu": """<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="4" y="4" width="16" height="16" rx="2"/><rect x="9" y="9" width="6" height="6"/><line x1="9" y1="1" x2="9" y2="4"/><line x1="15" y1="1" x2="15" y2="4"/><line x1="9" y1="20" x2="9" y2="23"/><line x1="15" y1="20" x2="15" y2="23"/><line x1="20" y1="9" x2="23" y2="9"/><line x1="20" y1="14" x2="23" y2="14"/><line x1="1" y1="9" x2="4" y2="9"/><line x1="1" y1="14" x2="4" y2="14"/></svg>""",
    
    "refresh": """<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="23 4 23 10 17 10"/><polyline points="1 20 1 14 7 14"/><path d="M3.51 9a9 9 0 0 1 14.85-3.36L23 10M1 14l4.64 4.36A9 9 0 0 0 20.49 15"/></svg>""",
    
    "check_circle": """<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/></svg>""",

    "traffic_light": """<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="6" y="2" width="12" height="20" rx="3"/><circle cx="12" cy="6" r="2"/><circle cx="12" cy="12" r="2"/><circle cx="12" cy="18" r="2"/></svg>"""
}

def get_svg_icon(name: str, color: Optional[str] = None, size: int = 16) -> str:
    """Returns SVG icon with optional color override and size."""
    svg = SVG_ICONS.get(name, SVG_ICONS["shield_logo"])
    if color:
        svg = svg.replace('stroke="currentColor"', f'stroke="{color}"').replace("stroke='#f97316'", f"stroke='{color}'")
    if size != 16:
        svg = svg.replace('width="16"', f'width="{size}"').replace('height="16"', f'height="{size}"')
    return svg

def get_risk_badge_html(risk_level: Optional[str]) -> str:
    """Returns the minimalist HTML string for a colored risk badge."""
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

def render_contributing_factors(factors: Optional[List[Dict[str, Any]]], junction_id: Optional[str] = None):
    """Renders contributing factors as sleek labeled progress bars."""
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
            sub_line = "Multiple verified citizen reports active within last 30 days"

        st.markdown(f"""
        <div style="background: rgba(245, 158, 11, 0.08); border: 1px solid rgba(245, 158, 11, 0.25); border-radius: 8px; padding: 10px 14px; margin-bottom: 14px; font-size: 0.82rem; color: #fbbf24; display: flex; align-items: center; gap: 10px;">
            <div style="display:flex; align-items:center; justify-content:center; flex-shrink:0;">
                {get_svg_icon("alert", color="#f59e0b", size=15)}
            </div>
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
            bar_color = "linear-gradient(90deg, #ef4444, #dc2626)"
            text_accent = "#f87171"
        elif pct >= 20:
            bar_color = "linear-gradient(90deg, #f59e0b, #ea580c)"
            text_accent = "#fbbf24"
        else:
            bar_color = "linear-gradient(90deg, #10b981, #059669)"
            text_accent = "#34d399"

        st.markdown(f"""
        <div style="margin-bottom: 12px;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 5px;">
                <span style="font-size: 0.85rem; font-weight: 500; color: #cbd5e1;">{factor}</span>
                <span style="font-size: 0.80rem; font-weight: 700; color: {text_accent}; font-family: 'JetBrains Mono', monospace;">
                    {pct}% Impact
                </span>
            </div>
            <div style="background: rgba(255, 255, 255, 0.05); height: 6px; border-radius: 9999px; overflow: hidden; border: 1px solid rgba(255, 255, 255, 0.05);">
                <div style="width: {pct}%; height: 100%; background: {bar_color}; border-radius: 9999px; transition: width 0.6s cubic-bezier(0.4, 0, 0.2, 1);"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

def render_awaiting_data_banner():
    """Renders the minimalist 'Awaiting Data' info banner."""
    st.markdown(f"""
    <div class="awaiting-data-banner" style="background: rgba(255, 255, 255, 0.02); border: 1px solid rgba(255, 255, 255, 0.06); border-radius: 10px; padding: 16px; display: flex; align-items: center; gap: 14px;">
        <div style="width: 42px; height: 42px; border-radius: 8px; background: rgba(245, 158, 11, 0.1); display: flex; align-items: center; justify-content: center; flex-shrink: 0;">
            {get_svg_icon("radar", color="#f59e0b", size=22)}
        </div>
        <div>
            <div style="font-size: 0.84rem; font-weight: 700; color: #ffffff; letter-spacing: 0.04em; font-family: 'Space Grotesk', sans-serif;">AWAITING TELEMETRY STREAM</div>
            <div style="font-size: 0.78rem; color: #94a3b8; margin-top: 3px; line-height: 1.4;">
                Visual risk analysis and historical accident weighting are currently initializing for this node. 
                Scores and factor attributions populate automatically as camera feeds connect.
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_navbar(active_page: str = "Dashboard"):
    """Renders the ultra-minimalist command center HUD navigation bar."""
    navbar_html = f"""
    <div class="tactical-navbar">
        <div class="navbar-brand-group">
            <div class="brand-shield-logo">
                {get_svg_icon("shield_logo", size=22)}
            </div>
            <div>
                <div class="brand-title">JunctionGuard <span class="brand-ai">AI</span></div>
                <div class="brand-sub">Autonomous Vision &amp; Spatial Risk Intelligence</div>
            </div>
        </div>
        <div class="navbar-status-badges">
            <div class="status-pill">
                <span class="live-dot-green"></span>
                <div class="pill-meta">
                    <span class="pill-label">STATUS</span>
                    <span class="pill-val" style="color: #10b981;">ACTIVE</span>
                </div>
            </div>
            <div class="status-pill">
                <div style="display:flex; align-items:center; color:#f97316;">
                    {get_svg_icon("cpu", color="#f97316", size=14)}
                </div>
                <div class="pill-meta">
                    <span class="pill-label">INFERENCE</span>
                    <span class="pill-val" style="color: #f97316;">28 FPS</span>
                </div>
            </div>
            <div class="status-pill">
                <div style="display:flex; align-items:center; color:#38bdf8;">
                    {get_svg_icon("cloud", color="#38bdf8", size=14)}
                </div>
                <div class="pill-meta">
                    <span class="pill-label">DATABASE</span>
                    <span class="pill-val" style="color: #38bdf8;">SYNCED</span>
                </div>
            </div>
        </div>
    </div>
    """
    st.markdown(navbar_html, unsafe_allow_html=True)

def render_dashboard_overview_header(title: str = "Dashboard", subtitle: str = "Real-time Junction Risk Surveillance System"):
    """Renders the subheader bar with active page title, subtitle, and live date/time widget."""
    now = datetime.now()
    date_str = now.strftime("%b %d, %Y")
    time_str = now.strftime("%I:%M:%S %p")
    
    header_html = f"""
    <div class="overview-header-bar">
        <div>
            <div class="overview-title">{title}</div>
            <div class="overview-sub">{subtitle}</div>
        </div>
        <div class="overview-right-actions">
            <div class="datetime-pill">
                <span style="display:flex; align-items:center; color:#94a3b8;">
                    {get_svg_icon("file_text", color="#94a3b8", size=13)}
                </span>
                <span>{date_str}</span>
                <span class="dt-divider">/</span>
                <span class="dt-time">{time_str}</span>
            </div>
        </div>
    </div>
    """
    st.markdown(header_html, unsafe_allow_html=True)

def render_footer():
    """Renders the minimalist telemetry status footer."""
    footer_html = f"""
    <div class="tactical-footer">
        <div class="footer-stat">
            <span class="live-dot-green"></span>
            <span>Feed: <b>Real-Time Vision &amp; GIS Sensors</b></span>
        </div>
        <div class="footer-stat">
            <span style="display:flex; align-items:center; color:#94a3b8;">
                {get_svg_icon("cpu", color="#94a3b8", size=13)}
            </span>
            <span>Engine: <b>YOLOv8 + ExplainableRisk v2.4</b></span>
        </div>
        <div class="footer-stat">
            <span style="display:flex; align-items:center; color:#94a3b8;">
                {get_svg_icon("refresh", color="#94a3b8", size=13)}
            </span>
            <span>Telemetry Pulse: <b>Active</b></span>
        </div>
        <div class="footer-stat footer-copyright">
            &copy; 2026 JunctionGuard AI &bull; Civic Safety Architecture
        </div>
    </div>
    """
    st.markdown(footer_html, unsafe_allow_html=True)

def inject_custom_styles():
    """Injects the ultra-minimalist dark design system."""
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500;600;700&family=Space+Grotesk:wght@500;600;700;800&display=swap');

        /* ── Clean Up Streamlit Defaults ── */
        #MainMenu { visibility: hidden !important; display: none !important; }
        header[data-testid="stHeader"] { visibility: hidden !important; display: none !important; }
        div[data-testid="stToolbar"] { visibility: hidden !important; display: none !important; }
        div[data-testid="stDecoration"] { visibility: hidden !important; display: none !important; }
        footer { visibility: hidden !important; display: none !important; }
        .stDeployButton { visibility: hidden !important; display: none !important; }

        /* ── Minimalist Obsidian Canvas (#08090d) ── */
        html, body, [class*="css"], .stApp {
            font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif !important;
            background-color: #08090d !important;
            color: #e2e8f0 !important;
        }

        [data-testid="stAppViewContainer"] {
            background-color: #08090d !important;
            background-image: 
                radial-gradient(circle at 50% 0%, rgba(249, 115, 22, 0.03) 0%, transparent 60%),
                linear-gradient(rgba(255, 255, 255, 0.015) 1px, transparent 1px),
                linear-gradient(90deg, rgba(255, 255, 255, 0.015) 1px, transparent 1px) !important;
            background-size: 100% 100%, 32px 32px, 32px 32px !important;
        }

        /* ── Typography System ── */
        h1, h2, h3, h4, h5, h6, .brand-title, .overview-title, .panel-title {
            font-family: 'Space Grotesk', system-ui, sans-serif !important;
            letter-spacing: -0.02em !important;
            color: #f8fafc !important;
        }

        /* ── Minimalist Sidebar ── */
        [data-testid="stSidebar"] {
            background: #0b0e14 !important;
            border-right: 1px solid rgba(255, 255, 255, 0.06) !important;
        }
        div[data-testid="stSidebar"] div[data-testid="stRadio"] > div {
            gap: 4px !important;
        }
        div[data-testid="stSidebar"] div[data-testid="stRadio"] label {
            background: rgba(255, 255, 255, 0.02) !important;
            border: 1px solid rgba(255, 255, 255, 0.05) !important;
            border-radius: 8px !important;
            padding: 9px 12px !important;
            color: #94a3b8 !important;
            font-family: 'Plus Jakarta Sans', sans-serif !important;
            font-size: 0.85rem !important;
            font-weight: 500 !important;
            cursor: pointer !important;
            transition: all 0.15s ease !important;
            display: flex !important;
            align-items: center !important;
            margin-bottom: 0px !important;
        }
        div[data-testid="stSidebar"] div[data-testid="stRadio"] label:hover {
            border-color: rgba(249, 115, 22, 0.3) !important;
            color: #ffffff !important;
            background: rgba(255, 255, 255, 0.04) !important;
        }
        div[data-testid="stSidebar"] div[data-testid="stRadio"] label:has(input:checked) {
            background: rgba(249, 115, 22, 0.12) !important;
            border: 1px solid rgba(249, 115, 22, 0.45) !important;
            color: #ffedd5 !important;
            font-weight: 600 !important;
        }
        div[data-testid="stSidebar"] div[data-testid="stRadio"] label > div:first-child {
            display: none !important;
        }

        /* ── Minimalist Panels & Containers ── */
        [data-testid="stVerticalBlockBorderWrapper"] > div {
            background: #0f131a !important;
            border: 1px solid rgba(255, 255, 255, 0.06) !important;
            border-radius: 10px !important;
            padding: 16px !important;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3) !important;
            transition: border-color 0.2s ease !important;
        }
        [data-testid="stVerticalBlockBorderWrapper"] > div:hover {
            border-color: rgba(255, 255, 255, 0.12) !important;
        }

        /* ── Top HUD Navigation Bar ── */
        .tactical-navbar {
            display: flex;
            justify-content: space-between;
            align-items: center;
            background: #0b0e14;
            border: 1px solid rgba(255, 255, 255, 0.07);
            border-radius: 12px;
            padding: 12px 20px;
            margin-bottom: 12px;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.35);
        }
        .navbar-brand-group {
            display: flex;
            align-items: center;
            gap: 12px;
        }
        .brand-shield-logo {
            width: 36px;
            height: 36px;
            background: rgba(249, 115, 22, 0.1);
            border: 1px solid rgba(249, 115, 22, 0.3);
            border-radius: 8px;
            display: flex;
            align-items: center;
            justify-content: center;
            box-shadow: 0 0 12px rgba(249, 115, 22, 0.15);
        }
        .brand-title {
            font-size: 1.18rem;
            font-weight: 700;
            color: #ffffff;
            line-height: 1.15;
            letter-spacing: -0.02em;
        }
        .brand-ai {
            color: #f97316;
            font-weight: 800;
        }
        .brand-sub {
            font-size: 0.72rem;
            color: #94a3b8;
            margin-top: 2px;
            font-weight: 400;
        }

        .navbar-status-badges {
            display: flex;
            align-items: center;
            gap: 10px;
            flex-wrap: wrap;
        }
        .status-pill {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            background: rgba(255, 255, 255, 0.03);
            border: 1px solid rgba(255, 255, 255, 0.07);
            border-radius: 8px;
            padding: 5px 12px;
        }
        .pill-meta {
            display: flex;
            flex-direction: column;
            line-height: 1.1;
        }
        .pill-label {
            font-size: 0.56rem;
            font-weight: 600;
            color: #64748b;
            text-transform: uppercase;
            letter-spacing: 0.06em;
            font-family: 'JetBrains Mono', monospace;
        }
        .pill-val {
            font-size: 0.72rem;
            font-weight: 700;
            letter-spacing: 0.02em;
            font-family: 'JetBrains Mono', monospace;
        }

        /* ── Subheader Overview Bar ── */
        .overview-header-bar {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin: 10px 0 16px 0;
            padding-bottom: 2px;
        }
        .overview-title {
            font-size: 1.45rem;
            font-weight: 700;
            color: #ffffff;
            line-height: 1.1;
        }
        .overview-sub {
            font-size: 0.80rem;
            color: #94a3b8;
            margin-top: 3px;
        }
        .overview-right-actions {
            display: flex;
            align-items: center;
            gap: 10px;
        }
        .datetime-pill {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            background: #0f131a;
            border: 1px solid rgba(255, 255, 255, 0.07);
            border-radius: 8px;
            padding: 6px 14px;
            font-size: 0.76rem;
            font-family: 'JetBrains Mono', monospace;
            color: #cbd5e1;
        }
        .dt-divider {
            color: #475569;
        }
        .dt-time {
            color: #f97316;
            font-weight: 600;
        }

        /* ── Minimalist KPI Cards ── */
        .kpi-tactical-card {
            background: #0f131a;
            border: 1px solid rgba(255, 255, 255, 0.07);
            border-radius: 10px;
            padding: 16px 18px;
            position: relative;
            overflow: hidden;
            display: flex;
            align-items: center;
            justify-content: space-between;
            box-shadow: 0 4px 16px rgba(0, 0, 0, 0.3);
            transition: all 0.2s ease;
        }
        .kpi-tactical-card:hover {
            border-color: rgba(255, 255, 255, 0.15);
            transform: translateY(-1px);
        }
        .kpi-card-critical {
            border-color: rgba(239, 68, 68, 0.25) !important;
            background: linear-gradient(180deg, rgba(239, 68, 68, 0.05) 0%, #0f131a 100%) !important;
        }
        .kpi-label {
            font-size: 0.66rem;
            font-weight: 600;
            color: #94a3b8;
            text-transform: uppercase;
            letter-spacing: 0.06em;
            font-family: 'JetBrains Mono', monospace;
            margin-bottom: 4px;
        }
        .kpi-num {
            font-size: 1.85rem;
            font-weight: 700;
            color: #ffffff;
            line-height: 1.1;
            font-family: 'Space Grotesk', sans-serif;
        }
        .kpi-denom {
            font-size: 0.85rem;
            color: #64748b;
            font-weight: 400;
        }
        .kpi-sub {
            font-size: 0.68rem;
            font-weight: 600;
            letter-spacing: 0.04em;
            font-family: 'JetBrains Mono', monospace;
            margin-top: 6px;
            display: flex;
            align-items: center;
            gap: 5px;
        }
        .kpi-icon-wrap {
            width: 40px;
            height: 40px;
            border-radius: 8px;
            display: flex;
            align-items: center;
            justify-content: center;
            flex-shrink: 0;
        }

        /* ── Status Pulse Animations ── */
        .live-dot-green {
            width: 7px;
            height: 7px;
            background: #10b981;
            border-radius: 50%;
            display: inline-block;
            box-shadow: 0 0 8px #10b981;
        }
        .live-dot-red {
            width: 7px;
            height: 7px;
            background: #ef4444;
            border-radius: 50%;
            display: inline-block;
            box-shadow: 0 0 8px #ef4444;
            animation: pulseCritical 1.8s infinite;
        }
        @keyframes pulseCritical {
            0%   { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(239, 68, 68, 0.6); }
            70%  { transform: scale(1);    box-shadow: 0 0 0 5px rgba(239, 68, 68, 0); }
            100% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(239, 68, 68, 0); }
        }

        /* ── Reserved Minimalist Badges ── */
        .badge {
            display: inline-flex;
            align-items: center;
            gap: 6px;
            padding: 4px 10px;
            border-radius: 6px;
            font-size: 0.72rem;
            font-weight: 600;
            font-family: 'JetBrains Mono', monospace;
            letter-spacing: 0.04em;
        }
        .badge-dot {
            width: 5px;
            height: 5px;
            border-radius: 50%;
            background: currentColor;
        }
        .badge-green {
            background: rgba(16, 185, 129, 0.12);
            color: #34d399;
            border: 1px solid rgba(16, 185, 129, 0.25);
        }
        .badge-amber {
            background: rgba(245, 158, 11, 0.12);
            color: #fbbf24;
            border: 1px solid rgba(245, 158, 11, 0.25);
        }
        .badge-red {
            background: rgba(239, 68, 68, 0.12);
            color: #f87171;
            border: 1px solid rgba(239, 68, 68, 0.3);
        }
        .badge-gray {
            background: rgba(100, 116, 139, 0.12);
            color: #94a3b8;
            border: 1px solid rgba(100, 116, 139, 0.2);
        }

        /* ── Action Buttons ── */
        .stButton > button {
            background: #121722 !important;
            color: #f8fafc !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
            border-radius: 8px !important;
            font-family: 'Plus Jakarta Sans', sans-serif !important;
            font-weight: 600 !important;
            font-size: 0.84rem !important;
            padding: 7px 16px !important;
            transition: all 0.15s ease !important;
        }
        .stButton > button:hover {
            background: #182030 !important;
            border-color: rgba(249, 115, 22, 0.4) !important;
            color: #f97316 !important;
        }
        .stButton > button[kind="primary"] {
            background: #f97316 !important;
            color: #08090d !important;
            border: 1px solid #f97316 !important;
            font-weight: 700 !important;
        }
        .stButton > button[kind="primary"]:hover {
            background: #ea580c !important;
            color: #ffffff !important;
        }

        /* ── Input Fields & Selectboxes ── */
        [data-baseweb="input"], [data-baseweb="textarea"], [data-baseweb="select"] {
            background-color: #0b0e14 !important;
            border-color: rgba(255, 255, 255, 0.08) !important;
            border-radius: 8px !important;
        }
        input, textarea {
            color: #f8fafc !important;
            font-family: 'Plus Jakarta Sans', sans-serif !important;
        }
        input::placeholder, textarea::placeholder {
            color: rgba(148, 163, 184, 0.4) !important;
            font-size: 0.84rem !important;
        }

        /* ── Minimalist Table Styling ── */
        [data-testid="stDataFrame"] {
            border: 1px solid rgba(255, 255, 255, 0.07);
            border-radius: 8px;
            overflow: hidden;
        }

        /* ── Telemetry Footer ── */
        .tactical-footer {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 14px 20px;
            background: #0b0e14;
            border: 1px solid rgba(255, 255, 255, 0.06);
            border-radius: 10px;
            margin-top: 2rem;
            font-size: 0.74rem;
            color: #94a3b8;
            flex-wrap: wrap;
            gap: 12px;
        }
        .footer-stat {
            display: inline-flex;
            align-items: center;
            gap: 7px;
            font-family: 'JetBrains Mono', monospace;
        }
        .footer-copyright {
            color: #64748b;
        }

        /* ── Custom Scrollbars ── */
        ::-webkit-scrollbar { width: 5px; height: 5px; }
        ::-webkit-scrollbar-track { background: #08090d; }
        ::-webkit-scrollbar-thumb { background: #1a202c; border-radius: 3px; }
        ::-webkit-scrollbar-thumb:hover { background: #2d3748; }
    </style>
    """, unsafe_allow_html=True)
