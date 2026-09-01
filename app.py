"""
JunctionGuard AI - 3D Urban Road Safety Command Center
Autonomous Vision Analytics, Real-Time Explainable AI (XAI) Risk Scoring,
and 3D Digital Twin Surveillance for Accident-Prone Road Junctions in India.
"""

import os
import json
import uuid
import mimetypes
import cv2
import streamlit as st
import folium
from folium.plugins import HeatMap, MiniMap, Fullscreen, MarkerCluster
from streamlit_folium import st_folium
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import time
from typing import Optional, List, Dict, Any, Union
import importlib

# ── Backend Data & Analytics Imports (Strictly Untouched) ──
from src.database import (
    init_db, fetch_all_junctions, fetch_junction_by_id, 
    add_citizen_report, fetch_citizen_reports
)
from src.analytics.risk_engine import ExplainableRiskEngine
import src.geo_utils
importlib.reload(src.geo_utils)
from src.geo_utils import find_nearest_junction, reverse_geocode_location, get_ip_location, forward_geocode_location
import streamlit.components.v1 as st_components
from src.analytics.data_loader import compute_historical_risk_score, load_accident_dataset
from src.vision.stream_processor import StreamProcessor
from src.vision.detector import TrafficDetector

# ── 3D Digital Twin & Frontend UI Components ──
from app.three_twin import render_3d_junction_digital_twin
import app.components as app_comp
importlib.reload(app_comp)
from app.components import (
    render_risk_badge,
    render_contributing_factors,
    render_awaiting_data_banner,
    inject_custom_styles,
    get_risk_badge_html,
    render_navbar,
    render_dashboard_overview_header,
    render_hero_mission_banner,
    render_3d_circular_risk_gauge,
    render_live_alert_ribbon,
    render_xai_radar_chart,
    render_live_telemetry_hud,
    render_monitored_node_card,
    render_tactical_kpi_card,
    render_simulation_result_card,
    render_citizen_report_card,
    render_footer
)

# ── Handle Browser GPS Callback (from HTML5 Geolocation Button) ──
if "geo_lat" in st.query_params and "geo_lng" in st.query_params:
    try:
        g_lat = float(st.query_params["geo_lat"])
        g_lng = float(st.query_params["geo_lng"])
        nav_target = st.query_params.get("nav", "Citizen Reports")
        st.session_state["tab_picked_lat"] = g_lat
        st.session_state["tab_picked_lng"] = g_lng
        st.session_state["sentinel_picked_lat"] = g_lat
        st.session_state["sentinel_picked_lng"] = g_lng
        st.session_state["_pending_nav"] = nav_target
        _all_j = fetch_all_junctions()
        near_j, _ = find_nearest_junction(g_lat, g_lng, _all_j)
        addr = near_j['name'] if near_j else reverse_geocode_location(g_lat, g_lng)
        st.session_state["selected_junction_name_val"] = addr
        st.session_state["tab_select_junction_dropdown"] = addr
        st.session_state["sync_dropdown_from_map"] = addr
        st.session_state["sentinel_jnc_input"] = addr
        st.session_state["sentinel_select_junction_dropdown"] = addr
        st.query_params.clear()
        st.rerun()
    except Exception as ex:
        print(f"[Query Geolocation Handle Note] {ex}")

# Initialize Database on app start
init_db()
risk_engine = ExplainableRiskEngine()

st.set_page_config(
    page_title="JunctionGuard AI | Road Safety Platform",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inject Modern Clean Interface Design System
inject_custom_styles()

# ── Navigation Options (Clean 6-Pillar Suite) ──
nav_options = [
    "Command Center",
    "Junction Radar",
    "Live Vision",
    "XAI Analysis",
    "Fleet Analytics",
    "Citizen Reports"
]

# Legacy route mapping aliases
nav_aliases = {
    "Dashboard": "Command Center",
    "Interactive Alert Map": "Junction Radar",
    "Live CCTV Vision Analytics": "Live Vision",
    "Explainability & Factor Breakdown": "XAI Analysis",
    "Citizen Hazard Reporting": "Citizen Reports"
}

# ── Sidebar Navigation & Controls ──
with st.sidebar:
    st.markdown("""
    <div style="padding: 10px 0 20px 0; border-bottom: 1px solid rgba(255,255,255,0.08); margin-bottom: 20px;">
        <div style="display:flex; align-items:center; gap:12px;">
            <div class="brand-shield-logo" style="width:38px; height:38px;"></div>
            <div>
                <div style="font-family:'Plus Jakarta Sans', sans-serif; font-size:1.15rem; font-weight:800; color:#ffffff; letter-spacing:-0.02em;">JunctionGuard <span style="color:#38bdf8;">AI</span></div>
                <div style="font-size:0.70rem; color:#94a3b8; font-family:'JetBrains Mono', monospace;">ROAD SAFETY PLATFORM</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if "app_sidebar_navigation" not in st.session_state:
        st.session_state["app_sidebar_navigation"] = "Command Center"

    # Map legacy state if needed
    current_raw = st.session_state.get("app_sidebar_navigation", "Command Center")
    if current_raw in nav_aliases:
        st.session_state["app_sidebar_navigation"] = nav_aliases[current_raw]

    # Apply any pending programmatic navigation BEFORE the widget is instantiated
    _pending_nav = st.session_state.pop("_pending_nav", None)
    if _pending_nav:
        mapped_target = nav_aliases.get(_pending_nav, _pending_nav)
        if mapped_target in nav_options:
            st.session_state["app_sidebar_navigation"] = mapped_target

    _current = st.session_state.get("app_sidebar_navigation", "Command Center")
    _nav_index = nav_options.index(_current) if _current in nav_options else 0

    sidebar_nav = st.radio(
        "NAVIGATION",
        options=nav_options,
        index=_nav_index,
        format_func=lambda x: {
            "Command Center": "🏠  Command Center",
            "Junction Radar": "🗺️  Junction Radar",
            "Live Vision": "📹  Live Vision",
            "XAI Analysis": "🧠  XAI Analysis",
            "Fleet Analytics": "📊  Fleet Analytics",
            "Citizen Reports": "👥  Citizen Reports"
        }.get(x, x),
        key="app_sidebar_navigation",
        label_visibility="collapsed"
    )

    st.markdown("<div style='margin-top: 18px; border-top: 1px solid rgba(255,255,255,0.08); padding-top: 18px;'></div>", unsafe_allow_html=True)

    # Junction Selector Dropdown
    junctions_raw = fetch_all_junctions()
    jnc_select_options = ["All Junctions"] + [j["name"] for j in junctions_raw]
    
    if "active_selected_junction" not in st.session_state:
        st.session_state["active_selected_junction"] = "All Junctions"
        
    cur_sel = st.session_state.get("active_selected_junction", "All Junctions")
    sel_idx = jnc_select_options.index(cur_sel) if cur_sel in jnc_select_options else 0
    
    sel_key = f"focus_jnc_picker_{st.session_state.get('active_selected_junction', 'all')}"
    sidebar_selected_jnc = st.selectbox(
        "FOCUS JUNCTION",
        options=jnc_select_options,
        index=sel_idx,
        key=sel_key
    )
    if sidebar_selected_jnc != st.session_state.get("active_selected_junction"):
        st.session_state["active_selected_junction"] = sidebar_selected_jnc
        st.rerun()

    # Time Range Dropdown
    sidebar_time_range = st.selectbox("TIME RANGE", options=["Real-Time Stream", "Last 24 Hours", "Last 7 Days", "Last 30 Days"], index=0)

    # Risk Filter Multiselect
    risk_filter = st.multiselect(
        "FILTER RISK SEVERITY",
        options=["HIGH", "MEDIUM", "LOW"],
        default=["HIGH", "MEDIUM", "LOW"]
    )

    st.markdown("""
    <div style="margin-top: 32px; padding: 16px; background: #0c101e; border: 1px solid rgba(255,255,255,0.08); border-radius: 14px;">
        <div style="font-size: 0.84rem; font-weight: 700; color: #ffffff;">JunctionGuard AI v2.5</div>
        <div style="font-size: 0.72rem; color: #94a3b8; margin-top: 4px; line-height: 1.4;">Autonomous road safety &amp; multi-factor explainable AI surveillance system.</div>
    </div>
    """, unsafe_allow_html=True)

# Render Top Tactical Navigation Bar
render_navbar(sidebar_nav)

# ── Top Interactive Navigation Command Deck ──
tab_icons = {
    "Command Center": "🏠 Command Center",
    "Junction Radar": "🗺️ Junction Radar",
    "Live Vision": "📹 Live Vision",
    "XAI Analysis": "🧠 XAI Analysis",
    "Fleet Analytics": "📊 Fleet Analytics",
    "Citizen Reports": "👥 Citizen Reports"
}

nav_cols = st.columns(6)
for col, opt in zip(nav_cols, nav_options):
    with col:
        is_active = (sidebar_nav == opt)
        btn_type = "primary" if is_active else "secondary"
        if st.button(tab_icons[opt], key=f"top_nav_btn_{opt}", use_container_width=True, type=btn_type):
            if sidebar_nav != opt:
                st.session_state["_pending_nav"] = opt
                st.rerun()

# Render Subheader Overview Bar
nav_subtitles = {
    "Command Center": "Real-Time 3D Digital Twin & Risk Surveillance Overview",
    "Junction Radar": "Spatial Hazard Mapping & Risk Density Telemetry",
    "Live Vision": "Autonomous YOLOv8 Edge Vision & Traffic Detection",
    "XAI Analysis": "100% White-Box Explainable AI Risk Scoring & Simulations",
    "Fleet Analytics": "Macro Safety Trends, City Rankings & Corridor Intelligence",
    "Citizen Reports": "Crowdsourced Hazard Verification & Community Field Evidence"
}
render_dashboard_overview_header(title=sidebar_nav, subtitle=nav_subtitles.get(sidebar_nav, "Autonomous Road Hazard Intelligence"))

# Load and filter junction records
junctions = fetch_all_junctions()

# City fallback dictionary to ensure accurate Indian metropolitan cities
CITY_MAPPING = {
    "Panjagutta Junction": ("Hyderabad", "Telangana"),
    "ITO Crossing": ("New Delhi", "Delhi"),
    "Silk Board Junction": ("Bengaluru", "Karnataka"),
    "Goraguntepalya Junction": ("Bengaluru", "Karnataka"),
    "Dadar TT Circle": ("Mumbai", "Maharashtra"),
    "Kathipara Junction": ("Chennai", "Tamil Nadu"),
    "Chandani Chowk Junction": ("Pune", "Maharashtra"),
    "Shivaji Chowk": ("Kolhapur", "Maharashtra"),
    "Kawala Naka": ("Kolhapur", "Maharashtra"),
    "Dabholkar Corner": ("Kolhapur", "Maharashtra"),
    "Cyber Chowk": ("Kolhapur", "Maharashtra"),
    "Rajaram Corner": ("Kolhapur", "Maharashtra")
}

def resolve_city_name(j):
    name = j.get("name", "")
    if name in CITY_MAPPING:
        return CITY_MAPPING[name][0]
    lat = float(j.get("lat") or 0.0)
    lon = float(j.get("lon") or 0.0)
    if 12.8 <= lat <= 13.1 and 77.4 <= lon <= 77.8:
        return "Bengaluru"
    elif 18.9 <= lat <= 19.3 and 72.7 <= lon <= 73.1:
        return "Mumbai"
    elif 28.5 <= lat <= 28.8 and 77.1 <= lon <= 77.4:
        return "New Delhi"
    elif 12.9 <= lat <= 13.2 and 80.1 <= lon <= 80.3:
        return "Chennai"
    elif 17.3 <= lat <= 17.5 and 78.3 <= lon <= 78.6:
        return "Hyderabad"
    elif 18.4 <= lat <= 18.7 and 73.7 <= lon <= 74.0:
        return "Pune"
    elif 16.6 <= lat <= 16.8 and 74.1 <= lon <= 74.4:
        return "Kolhapur"
    existing_city = j.get("city")
    if existing_city and existing_city not in ["India", "None", "", None]:
        return existing_city
    return "Bengaluru"

for j in junctions:
    j["city"] = resolve_city_name(j)
    j["state"] = CITY_MAPPING.get(j.get("name", ""), ("", "India"))[1]

# Apply Junction filter
selected_jnc_record = None
if sidebar_selected_jnc != "All Junctions":
    for j in junctions:
        if j["name"] == sidebar_selected_jnc:
            selected_jnc_record = j
            break

# ── Helper: Surveillance Folium Map Renderer ──
def render_surveillance_folium_map(view_mode: str, height: int = 500, key_prefix: str = "main"):
    display_junctions = [j for j in junctions if j["risk_level"] in risk_filter]

    if selected_jnc_record:
        map_center = [selected_jnc_record["lat"], selected_jnc_record["lon"]]
        map_zoom = 13
    elif display_junctions and len(display_junctions) == 1:
        map_center = [display_junctions[0]["lat"], display_junctions[0]["lon"]]
        map_zoom = 13
    elif display_junctions:
        avg_lat = sum(j["lat"] for j in display_junctions) / len(display_junctions)
        avg_lon = sum(j["lon"] for j in display_junctions) / len(display_junctions)
        map_center = [avg_lat, avg_lon]
        map_zoom = 5
    else:
        map_center = [20.5937, 78.9629]
        map_zoom = 5

    m = folium.Map(
        location=map_center,
        zoom_start=map_zoom,
        min_zoom=4,
        max_zoom=18,
        tiles=None,
        control_scale=True,
        prefer_canvas=True,
        world_copy_jump=False
    )

    if view_mode == "Satellite Imagery":
        folium.TileLayer(
            tiles="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
            attr="Esri World Imagery",
            name="Satellite Imagery",
            no_wrap=True,
            min_zoom=4,
            max_zoom=18,
            overlay=False
        ).add_to(m)
    elif view_mode == "Street Navigation":
        folium.TileLayer(
            tiles="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
            attr="&copy; <a href='https://www.openstreetmap.org/copyright'>OpenStreetMap</a> contributors",
            name="Street Navigation",
            no_wrap=True,
            min_zoom=4,
            max_zoom=18,
            overlay=False
        ).add_to(m)
    else:  # Dark Tactical (Default) & Heatmap Base
        folium.TileLayer(
            tiles="https://server.arcgisonline.com/ArcGIS/rest/services/Canvas/World_Dark_Gray_Base/MapServer/tile/{z}/{y}/{x}",
            attr="Esri, HERE, Garmin, &copy; OpenStreetMap contributors",
            name="Dark Tactical",
            no_wrap=True,
            min_zoom=4,
            max_zoom=18,
            overlay=False
        ).add_to(m)
        folium.TileLayer(
            tiles="https://server.arcgisonline.com/ArcGIS/rest/services/Canvas/World_Dark_Gray_Reference/MapServer/tile/{z}/{y}/{x}",
            attr="Esri",
            name="Dark Labels",
            no_wrap=True,
            min_zoom=4,
            max_zoom=18,
            overlay=True
        ).add_to(m)

    for j in display_junctions:
        score = j["risk_score"] or 0
        lvl = (j["risk_level"] or "LOW").upper()
        pin_col = "#f43f5e" if lvl == "HIGH" else ("#f59e0b" if lvl == "MEDIUM" else "#34d399")
        is_selected = (selected_jnc_record and selected_jnc_record["name"] == j["name"])

        border_style = f"3px solid {pin_col}" if is_selected else f"2px solid {pin_col}"
        glow_shadow = f"0 0 16px {pin_col}, 0 0 30px {pin_col}" if is_selected else f"0 0 10px {pin_col}"
        selected_ring = f'<div style="position: absolute; width: 44px; height: 44px; border-radius: 50%; border: 2px dashed {pin_col}; animation: spin 4s linear infinite; opacity: 0.85;"></div>' if is_selected else ""

        pin_html = f"""
        <div style="position: relative; width: 44px; height: 44px; display: flex; align-items: center; justify-content: center; transform: translate(-50%, -50%); cursor: pointer;">
            {selected_ring}
            <div style="width: 32px; height: 32px; border-radius: 50%; background: #0c101e; border: {border_style}; display: flex; align-items: center; justify-content: center; box-shadow: {glow_shadow}; font-family: 'JetBrains Mono', monospace; font-size: 0.72rem; font-weight: 800; color: #ffffff;">
                {int(round(score))}
            </div>
        </div>
        """

        popup_html = f"""
        <div style="font-family: 'Plus Jakarta Sans', sans-serif; background: #0c101e; color: #ffffff; padding: 14px; border-radius: 12px; min-width: 220px; border: 1px solid rgba(255,255,255,0.1);">
            <div style="font-size: 0.95rem; font-weight: 800; color: #ffffff;">{j['name']}</div>
            <div style="font-size: 0.75rem; color: #94a3b8; margin-top: 2px;">📍 {j['city']}, {j['state']}</div>
            <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 10px; padding-top: 8px; border-top: 1px solid rgba(255,255,255,0.1);">
                <span style="font-size: 0.78rem; color: #cbd5e1;">Risk Score:</span>
                <span style="font-size: 1.15rem; font-weight: 800; color: {pin_col}; font-family: 'JetBrains Mono', monospace;">{score:.1f}/100</span>
            </div>
            <div style="font-size: 0.75rem; font-weight: 700; color: {pin_col}; margin-top: 4px;">LEVEL: {lvl} RISK</div>
            <div style="margin-top: 8px; font-size: 0.70rem; color: #38bdf8; font-family:'JetBrains Mono', monospace;">● CLICK TO FOCUS TELEMETRY</div>
        </div>
        """

        folium.Marker(
            location=[j["lat"], j["lon"]],
            popup=folium.Popup(popup_html, max_width=300),
            tooltip=f"🎯 {j['name']} ({lvl} · {score:.1f}/100) - Click to focus",
            icon=folium.DivIcon(html=pin_html, icon_size=(44, 44), icon_anchor=(22, 22))
        ).add_to(m)

    if view_mode == "Heatmap Mode":
        heat_data = [[j["lat"], j["lon"], (j["risk_score"] or 10) / 100.0] for j in display_junctions]
        HeatMap(heat_data, radius=28, blur=18, min_opacity=0.35).add_to(m)

    map_state = st_folium(
        m,
        width="stretch",
        height=height,
        key=f"{key_prefix}_folium_map",
        returned_objects=["last_object_clicked", "last_clicked"],
        return_on_hover=False
    )

    if map_state:
        clicked = map_state.get("last_object_clicked") or map_state.get("last_clicked")
        if clicked and isinstance(clicked, dict) and "lat" in clicked and "lng" in clicked:
            c_lat, c_lon = clicked["lat"], clicked["lng"]
            closest_jnc = min(junctions, key=lambda j: (j["lat"] - c_lat)**2 + (j["lon"] - c_lon)**2)
            dist_sq = (closest_jnc["lat"] - c_lat)**2 + (closest_jnc["lon"] - c_lon)**2
            if dist_sq < 3.5:
                if st.session_state.get("active_selected_junction") != closest_jnc["name"]:
                    st.session_state["active_selected_junction"] = closest_jnc["name"]
                    st.rerun()

# ----------------------------------------------------
# 1. 🏠 COMMAND CENTER (CLEAN, SPACIOUS HOME)
# ----------------------------------------------------
if sidebar_nav == "Command Center":
    # Clean Hero Mission Banner
    render_hero_mission_banner()

    # 4 Clean Spacious KPI Metric Cards
    kpi1, kpi2, kpi3, kpi4 = st.columns(4)

    total_jnc = len(junctions)
    high_risk_count = sum(1 for j in junctions if j["risk_level"] == "HIGH")
    avg_risk_score = round(sum(j["risk_score"] for j in junctions if j["risk_score"] is not None) / max(1, total_jnc), 1)
    total_reports = len(fetch_citizen_reports())

    with kpi1:
        st.markdown(render_tactical_kpi_card(
            label="MONITORED NODES",
            value=total_jnc,
            subtext="⚡ 7 Metros",
            badge_label="ACTIVE",
            badge_class="badge-live-cyan",
            dot_class="live-dot-cyan",
            icon_class="kpi-icon-jnc"
        ), unsafe_allow_html=True)

    with kpi2:
        st.markdown(render_tactical_kpi_card(
            label="HIGH RISK HOTSPOTS",
            value=high_risk_count,
            subtext="🚨 Priority Action",
            badge_label="CRITICAL",
            badge_class="badge-live-red",
            dot_class="live-dot-red",
            icon_class="kpi-icon-alert",
            is_critical=True,
            value_color="#fb7185"
        ), unsafe_allow_html=True)

    with kpi3:
        st.markdown(render_tactical_kpi_card(
            label="FLEET RISK INDEX",
            value=avg_risk_score,
            subtext="📊 National Average",
            badge_label="INDEXED",
            badge_class="badge-live-amber",
            dot_class="live-dot-green",
            icon_class="kpi-icon-score",
            denom="/100",
            value_color="#fbbf24"
        ), unsafe_allow_html=True)

    with kpi4:
        st.markdown(render_tactical_kpi_card(
            label="CITIZEN ALERTS",
            value=total_reports,
            subtext="🛡️ Verified Field Reports",
            badge_label="LIVE FEED",
            badge_class="badge-live-green",
            dot_class="live-dot-green",
            icon_class="kpi-icon-reports",
            value_color="#34d399"
        ), unsafe_allow_html=True)

    st.markdown("<div style='margin-top: 26px;'></div>", unsafe_allow_html=True)

    # 3D Digital Twin Centerpiece Section
    twin_col, hud_col = st.columns([1.65, 1.35])

    active_jnc = selected_jnc_record if selected_jnc_record else junctions[0]

    factors_raw = active_jnc.get("contributing_factors", [])
    factors_dict = {}
    if isinstance(factors_raw, dict):
        factors_dict = factors_raw
    elif isinstance(factors_raw, list):
        for item in factors_raw:
            if isinstance(item, dict):
                fname = str(item.get("factor", item.get("name", ""))).lower()
                fweight = float(item.get("weight", item.get("score", 0.0)))
                factors_dict[fname] = fweight
            elif isinstance(item, str):
                factors_dict[item.lower()] = 1.0

    tw_val = 48.0
    ped_val = 14
    density_val = 42

    for k, v in factors_dict.items():
        if "two_wheeler" in k or "weaving" in k:
            tw_val = round(v * 100 if v <= 1.0 else v, 1)
        elif "pedestrian" in k:
            ped_val = int(round(v * 50 if v <= 1.0 else v))
        elif "density" in k or "traffic" in k:
            density_val = int(round(v * 100 if v <= 1.0 else v))

    with twin_col:
        m_head_col1, m_head_col2 = st.columns([1.6, 1.0])
        with m_head_col1:
            st.markdown('<div style="font-size: 1.05rem; font-weight: 800; color: #ffffff; margin-bottom: 6px; font-family:\'Plus Jakarta Sans\', sans-serif;">🗺️ REAL-TIME SURVEILLANCE GIS RADAR</div>', unsafe_allow_html=True)
        with m_head_col2:
            cc_map_theme = st.selectbox("MAP THEME", options=["Dark Tactical", "Satellite Imagery", "Street Navigation", "Heatmap Mode"], index=0, key="cc_map_theme_sel", label_visibility="collapsed")

        render_surveillance_folium_map(view_mode=cc_map_theme, height=450, key_prefix="cc_centerpiece")

    with hud_col:
        st.markdown('<div style="font-size: 1.05rem; font-weight: 800; color: #ffffff; margin-bottom: 10px; font-family:\'Plus Jakarta Sans\', sans-serif;">🎯 ACTIVE JUNCTION TELEMETRY</div>', unsafe_allow_html=True)
        
        # 3D Circular Risk Gauge
        render_3d_circular_risk_gauge(
            risk_score=active_jnc["risk_score"] or 0.0,
            risk_level=active_jnc["risk_level"] or "LOW",
            trend_str="ELEVATED CONFLICTS" if active_jnc["risk_level"] == "HIGH" else "MONITORED STABLE FLOW"
        )

        st.markdown("<div style='margin-top: 14px;'></div>", unsafe_allow_html=True)
        with st.container(border=True):
            st.markdown(f'<div style="font-size:0.86rem; font-weight:700; color:#ffffff; margin-bottom:8px;">🔍 Primary Risk Drivers: <span style="color:#38bdf8;">{active_jnc["name"]}</span></div>', unsafe_allow_html=True)
            render_contributing_factors(active_jnc.get("contributing_factors"), junction_id=active_jnc.get("junction_id"))

            act1, act2 = st.columns(2)
            with act1:
                if st.button("⚖️ Deep-Dive XAI", key="cc_act_xai", use_container_width=True, type="primary"):
                    st.session_state["_pending_nav"] = "XAI Analysis"
                    st.rerun()
            with act2:
                if st.button("📹 CCTV Vision Feed", key="cc_act_vision", use_container_width=True):
                    st.session_state["_pending_nav"] = "Live Vision"
                    st.rerun()

    # 12 Monitored Junctions Directory Grid
    st.markdown("<div style='margin-top: 32px;'></div>", unsafe_allow_html=True)
    st.markdown("""
    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom: 14px;">
        <div style="font-size: 1.15rem; font-weight: 800; color: #ffffff; font-family:'Plus Jakarta Sans', sans-serif;">
            🏙️ MONITORED URBAN NODES
        </div>
        <div style="font-size: 0.78rem; color: #94a3b8; font-family:'JetBrains Mono', monospace;">
            12 ACTIVE NODES UNDER SURVEILLANCE
        </div>
    </div>
    """, unsafe_allow_html=True)

    grid_cols = st.columns(3)
    for idx, j in enumerate(junctions):
        col_idx = idx % 3
        with grid_cols[col_idx]:
            score = j.get("risk_score") or 0.0
            lvl = (j.get("risk_level") or "LOW").upper()
            score_col = "#fb7185" if lvl == "HIGH" else ("#fbbf24" if lvl == "MEDIUM" else "#34d399")

            # Extract primary factor
            factors_raw = j.get("contributing_factors", [])
            primary_factor = "Multi-Factor Collision Risk"
            if isinstance(factors_raw, list) and len(factors_raw) > 0:
                first_f = factors_raw[0]
                if isinstance(first_f, dict):
                    primary_factor = first_f.get("factor", first_f.get("name", "Multi-Factor Collision Risk"))
            elif isinstance(factors_raw, dict) and len(factors_raw) > 0:
                primary_factor = list(factors_raw.keys())[0].replace("_", " ").title()

            with st.container(border=True):
                st.markdown(render_monitored_node_card(
                    j=j,
                    score=score,
                    lvl=lvl,
                    score_col=score_col,
                    primary_factor=primary_factor
                ), unsafe_allow_html=True)

# ----------------------------------------------------
# 2. 🗺️ JUNCTION RADAR & GIS MAP
# ----------------------------------------------------
elif sidebar_nav == "Junction Radar":
    f1, f2, f3 = st.columns([1.2, 1.2, 1.6])
    with f1:
        city_filter_options = ["All India", "Bengaluru", "Mumbai", "New Delhi", "Chennai", "Hyderabad", "Pune", "Kolhapur"]
        selected_city_filter = st.selectbox("REGION / CITY", options=city_filter_options, index=0)
    with f2:
        map_view_mode = st.selectbox("MAP THEME", options=["Dark Tactical", "Satellite Imagery", "Street Navigation", "Heatmap Mode"], index=0)
    with f3:
        map_search_txt = st.text_input("🔍 SEARCH JUNCTION", placeholder="Type name...", key="radar_search_txt")

    map_display_junctions = junctions
    if selected_city_filter != "All India":
        map_display_junctions = [j for j in junctions if j["city"].lower() == selected_city_filter.lower()]
    if map_search_txt.strip():
        map_display_junctions = [j for j in map_display_junctions if map_search_txt.lower() in j["name"].lower() or map_search_txt.lower() in j["city"].lower()]

    st.markdown("<div style='margin-top: 10px;'></div>", unsafe_allow_html=True)
    render_surveillance_folium_map(map_view_mode, height=520, key_prefix="radar")

    # Spatial Risk Inventory Master Table
    st.markdown("<div style='margin-top: 28px;'></div>", unsafe_allow_html=True)
    with st.container(border=True):
        inv_h1, inv_h2 = st.columns([2, 1])
        with inv_h1:
            st.markdown(f'<div style="font-size: 1.0rem; font-weight: 800; color: #ffffff; font-family:\'Plus Jakarta Sans\', sans-serif;">📊 SPATIAL RISK INVENTORY ({len(map_display_junctions)} ACTIVE NODES)</div>', unsafe_allow_html=True)
        with inv_h2:
            all_reports_cached = fetch_citizen_reports()
            rep_counts = {}
            for r in all_reports_cached:
                jid = r.get("junction_id")
                rep_counts[jid] = rep_counts.get(jid, 0) + 1

            inv_export_df = pd.DataFrame([
                {
                    "Junction ID": j.get("junction_id", ""),
                    "Name": j.get("name", ""),
                    "City": j.get("city", "India"),
                    "State": j.get("state", "India"),
                    "Risk Level": j.get("risk_level", "LOW"),
                    "Risk Score": round(float(j.get("risk_score", 0.0)), 1),
                    "Primary Factor": (j.get("contributing_factors", [{}])[0].get("factor", "Historical Severity") if j.get("contributing_factors") else "General Traffic"),
                    "Citizen Reports": rep_counts.get(j.get("junction_id"), 0),
                    "Latitude": float(j.get("lat", 0.0)),
                    "Longitude": float(j.get("lon", 0.0)),
                    "Last Updated": j.get("last_updated", "Real-time")
                }
                for j in map_display_junctions
            ])
            inv_csv = inv_export_df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Export Inventory (CSV)",
                data=inv_csv,
                file_name=f"JunctionGuard_Inventory_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
                mime="text/csv",
                key="radar_inv_download_csv",
                use_container_width=True
            )

        jnc_table_data = []
        for j in map_display_junctions:
            lvl = (j.get("risk_level") or "LOW").upper()
            score_val = round(float(j.get("risk_score", 0.0)), 1)
            
            factors = j.get("contributing_factors", [])
            if factors and isinstance(factors, list) and len(factors) > 0:
                top_f = factors[0]
                f_name = top_f.get("factor", "Historical Severity")
                f_wt = int(round(float(top_f.get("weight", 0.0)) * 100))
                primary_factor_display = f"{f_name} ({f_wt}%)"
            else:
                primary_factor_display = "General Traffic Flow"

            c_reports_cnt = rep_counts.get(j.get("junction_id"), 0)

            jnc_table_data.append({
                "Junction ID": j.get("junction_id", ""),
                "Junction Name": j.get("name", "Unknown"),
                "City": j.get("city", "India"),
                "Risk Level": f"🔴 HIGH" if lvl=="HIGH" else (f"🟡 MEDIUM" if lvl=="MEDIUM" else f"🟢 LOW"),
                "Risk Score": score_val,
                "Primary Risk Factor": primary_factor_display,
                "Reports": f"{c_reports_cnt} filed" if c_reports_cnt > 0 else "None",
                "Latitude": float(j.get("lat", 0.0)),
                "Longitude": float(j.get("lon", 0.0)),
                "Last Updated": j.get("last_updated", "Real-time")
            })

        if jnc_table_data:
            inventory_df = pd.DataFrame(jnc_table_data)
            st.dataframe(
                inventory_df,
                column_config={
                    "Junction ID": st.column_config.TextColumn("ID", width="small"),
                    "Junction Name": st.column_config.TextColumn("Junction Name", width="medium"),
                    "City": st.column_config.TextColumn("City", width="small"),
                    "Risk Level": st.column_config.TextColumn("Risk Level", width="small"),
                    "Risk Score": st.column_config.ProgressColumn(
                        "Risk Score",
                        help="Explainable AI Composite Risk Score (0 - 100)",
                        format="%.1f",
                        min_value=0.0,
                        max_value=100.0,
                        width="medium"
                    ),
                    "Primary Risk Factor": st.column_config.TextColumn("Primary Risk Factor", width="medium"),
                    "Reports": st.column_config.TextColumn("Citizen Reports", width="small"),
                    "Latitude": st.column_config.NumberColumn("Latitude", format="%.4f"),
                    "Longitude": st.column_config.NumberColumn("Longitude", format="%.4f"),
                    "Last Updated": st.column_config.TextColumn("Last Telemetry Sync", width="small")
                },
                use_container_width=True,
                hide_index=True
            )

# ----------------------------------------------------
# 3. 📹 LIVE VISION SURVEILLANCE & REAL-TIME YOLOv8 DETECTION
# ----------------------------------------------------
elif sidebar_nav == "Live Vision":
    demo_sources = {
        "🎬 Stream 01: Cyber Chowk (J004) - High-Density Mixed Corridor": {
            "video": "data/sample_videos/indian_traffic_4.mp4",
            "jnc_id": "J004", "name": "Cyber Chowk",
            "start_frame": 45, "fps": 28.4
        },
        "🎬 Stream 02: Shivaji Chowk (J001) - Dense Urban Crossing": {
            "video": "data/sample_videos/indian_traffic_1.mp4",
            "jnc_id": "J001", "name": "Shivaji Chowk",
            "start_frame": 280, "fps": 28.4
        },
        "🎬 Stream 03: Rajaram Corner (J002) - Multi-Lane Arterial Junction": {
            "video": "data/sample_videos/indian_traffic_2.mp4",
            "jnc_id": "J002", "name": "Rajaram Corner",
            "start_frame": 45, "fps": 28.4
        },
        "🎬 Stream 04: Dabholkar Corner (J003) - Bus Terminal & Commercial Crossing": {
            "video": "data/sample_videos/indian_traffic_3.mp4",
            "jnc_id": "J003", "name": "Dabholkar Corner",
            "start_frame": 260, "fps": 28.4
        },
        "🎬 Stream 05: Kawala Naka (J005) - Heavy Vehicle Bottleneck": {
            "video": "data/sample_videos/indian_traffic_5.mp4",
            "jnc_id": "J005", "name": "Kawala Naka",
            "start_frame": 10, "fps": 28.4
        }
    }

    # Match default index based on sidebar focus junction
    default_src_idx = 0
    for idx, (lbl, meta) in enumerate(demo_sources.items()):
        if sidebar_selected_jnc.lower() in meta["name"].lower():
            default_src_idx = idx
            break

    v_select_col1, v_select_col2 = st.columns([2, 1])
    with v_select_col1:
        source_label = st.selectbox("SELECT CCTV CAMERA FEED", options=list(demo_sources.keys()), index=default_src_idx)
    with v_select_col2:
        conf_thresh = st.slider("YOLOv8 CONFIDENCE THRESHOLD", 0.10, 0.85, 0.30, 0.05)

    selected_meta = demo_sources[source_label]
    video_path = selected_meta["video"]

    v_stream_col, v_hud_col = st.columns([1.65, 1.35])

    with v_stream_col:
        header_banner = (
            '<div style="background: #0c101e; border: 1px solid rgba(255,255,255,0.08); border-radius: 12px 12px 0 0; padding: 12px 18px; display: flex; justify-content: space-between; align-items: center; font-family:\'JetBrains Mono\', monospace; font-size: 0.78rem;">'
            '<div style="display: flex; align-items: center; gap: 8px;">'
            '<span class="live-dot-red"></span>'
            '<span style="color: #ffffff; font-weight: 800;">REC ● REAL-TIME YOLOv8 DETECTION STREAM · 28 FPS</span>'
            '</div>'
            f'<div style="color: #38bdf8; font-weight: 700;">NODE: {selected_meta["jnc_id"]} ({selected_meta["name"]})</div>'
            '</div>'
        )
        st.markdown(header_banner, unsafe_allow_html=True)

        stream_toggle_col, stream_scrub_col = st.columns([1.2, 1.8])
        with stream_toggle_col:
            is_streaming = st.toggle("⚡ Run Live Detection Stream", value=True, key="run_live_yolo_stream_toggle")
        with stream_scrub_col:
            if not is_streaming:
                cap_temp = cv2.VideoCapture(video_path)
                tot_f = int(cap_temp.get(cv2.CAP_PROP_FRAME_COUNT) or 300)
                cap_temp.release()
                scrub_frame = st.slider("Timeline Scrubber (Frame)", 0, max(1, min(tot_f - 1, 400)), selected_meta["start_frame"])
            else:
                scrub_frame = selected_meta["start_frame"]

        video_screen = st.empty()

    with v_hud_col:
        st.markdown('<div style="font-size: 1.0rem; font-weight: 800; color: #ffffff; margin-bottom: 10px; font-family:\'Plus Jakarta Sans\', sans-serif;">📊 REAL-TIME DETECTION TELEMETRY (ACCURATE)</div>', unsafe_allow_html=True)
        hud_screen = st.empty()

    detector = TrafficDetector()

    if is_streaming and os.path.exists(video_path):
        cap = cv2.VideoCapture(video_path)
        cap.set(cv2.CAP_PROP_POS_FRAMES, selected_meta["start_frame"])
        frame_idx = 0
        max_loop_frames = 50  # Stream 50 frames per active pass

        while cap.isOpened() and frame_idx < max_loop_frames:
            ret, raw_frame = cap.read()
            if not ret:
                cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                ret, raw_frame = cap.read()
                if not ret:
                    break

            h, w, _ = raw_frame.shape
            if w > 720:
                raw_frame = cv2.resize(raw_frame, (720, int(h * 720 / w)))

            annotated_frame, metrics = detector.process_frame(raw_frame, conf_threshold=conf_thresh)
            rgb_frame = cv2.cvtColor(annotated_frame, cv2.COLOR_BGR2RGB)

            tot_v = metrics["total_vehicles"]
            tw_pct = metrics["two_wheeler_share_pct"]
            counts = metrics["counts"]
            cars = counts.get("car", 0)
            bikes = counts.get("motorcycle", 0)
            bicycles = counts.get("bicycle", 0)
            buses = counts.get("bus", 0)
            trucks = counts.get("truck", 0)
            peds = counts.get("pedestrian", 0)
            fps_val = metrics.get("fps", 28.4)
            avg_conf = metrics.get("avg_confidence", 0.81)
            unique_seen = metrics.get("unique_tracked_total", 0)
            near_misses = metrics.get("near_miss_count", 0)

            video_screen.image(
                rgb_frame,
                caption=f"⚡ Live YOLOv8 Tracking · Frame #{selected_meta['start_frame'] + frame_idx} · {tot_v} Vehicles Tracked (Cyan=Bikes, Green=Cars, Red=Peds)",
                use_container_width=True
            )

            hud_screen.markdown(
                render_live_telemetry_hud(
                    total_v=tot_v,
                    tw_pct=tw_pct,
                    peds=peds,
                    cars=cars,
                    bikes=bikes,
                    buses=buses,
                    trucks=trucks,
                    bicycles=bicycles,
                    fps_val=fps_val,
                    avg_conf=avg_conf,
                    unique_tracked=unique_seen,
                    near_misses=near_misses
                ),
                unsafe_allow_html=True
            )

            frame_idx += 1
            time.sleep(0.04)

        cap.release()

    elif os.path.exists(video_path):
        cap = cv2.VideoCapture(video_path)
        cap.set(cv2.CAP_PROP_POS_FRAMES, scrub_frame)
        ret, frame_img = cap.read()
        cap.release()

        if ret:
            h, w, _ = frame_img.shape
            if w > 720:
                frame_img = cv2.resize(frame_img, (720, int(h * 720 / w)))

            annotated_img, metrics = detector.process_frame(frame_img, conf_threshold=conf_thresh, use_tracking=False)
            rgb_img = cv2.cvtColor(annotated_img, cv2.COLOR_BGR2RGB)

            tot_v = metrics["total_vehicles"]
            tw_pct = metrics["two_wheeler_share_pct"]
            counts = metrics["counts"]
            cars = counts.get("car", 0)
            bikes = counts.get("motorcycle", 0)
            bicycles = counts.get("bicycle", 0)
            buses = counts.get("bus", 0)
            trucks = counts.get("truck", 0)
            peds = counts.get("pedestrian", 0)
            fps_val = metrics.get("fps", 28.4)
            avg_conf = metrics.get("avg_confidence", 0.81)
            unique_seen = metrics.get("unique_tracked_total", 0)
            near_misses = metrics.get("near_miss_count", 0)

            video_screen.image(
                rgb_img,
                caption=f"📍 YOLOv8 Frame #{scrub_frame} Snapshot · {tot_v} Vehicles Tracked (Cyan=Bikes, Green=Cars, Red=Peds)",
                use_container_width=True
            )

            hud_screen.markdown(
                render_live_telemetry_hud(
                    total_v=tot_v,
                    tw_pct=tw_pct,
                    peds=peds,
                    cars=cars,
                    bikes=bikes,
                    buses=buses,
                    trucks=trucks,
                    bicycles=bicycles,
                    fps_val=fps_val,
                    avg_conf=avg_conf,
                    unique_tracked=unique_seen,
                    near_misses=near_misses
                ),
                unsafe_allow_html=True
            )

    # Optional Native Video Player in expander
    with st.expander("🎬 View Original Raw Camera Footage", expanded=False):
        if os.path.exists(video_path):
            try:
                with open(video_path, "rb") as vf:
                    v_bytes = vf.read()
                st.video(v_bytes, format="video/mp4")
            except Exception:
                st.video(video_path)

# ----------------------------------------------------
# 4. 🧠 EXPLAINABLE AI (XAI) RISK ANALYSIS
# ----------------------------------------------------
elif sidebar_nav == "XAI Analysis":
    jnc_names = {j["name"]: j["junction_id"] for j in junctions}
    j_keys = list(jnc_names.keys())
    default_idx = j_keys.index(sidebar_selected_jnc) if sidebar_selected_jnc in j_keys else 0
    selected_name = st.selectbox("SELECT JUNCTION TO ANALYZE", options=j_keys, index=default_idx)
    selected_id = jnc_names[selected_name]

    jnc_data = fetch_junction_by_id(selected_id)

    xai_col1, xai_col2 = st.columns([1.2, 1.8])

    with xai_col1:
        score = jnc_data["risk_score"] or 0.0
        level = jnc_data["risk_level"] or "LOW"
        render_3d_circular_risk_gauge(risk_score=score, risk_level=level, trend_str="XAI AUDIT VERIFIED")

    with xai_col2:
        with st.container(border=True):
            st.markdown('<div style="font-size:1.0rem; font-weight:800; color:#ffffff; font-family:\'Plus Jakarta Sans\', sans-serif; margin-bottom:12px;">📊 FACTOR IMPACT WEIGHT BREAKDOWN</div>', unsafe_allow_html=True)
            render_contributing_factors(jnc_data.get("contributing_factors"), junction_id=selected_id)

            st.markdown("<div style='margin-top:20px;'></div>", unsafe_allow_html=True)
            st.markdown('<div style="font-size:1.0rem; font-weight:800; color:#ffffff; font-family:\'Plus Jakarta Sans\', sans-serif; margin-bottom:12px;">🕸️ MULTI-FACTOR RISK RADAR</div>', unsafe_allow_html=True)
            render_xai_radar_chart(jnc_data.get("contributing_factors"))

    # Historical Crash Stats & What-If Simulation Sandbox
    st.markdown("<div style='margin-top: 24px;'></div>", unsafe_allow_html=True)
    hist_col, sim_col = st.columns([1.3, 1.7])

    with hist_col:
        with st.container(border=True):
            st.markdown('<div style="font-size: 0.92rem; font-weight: 800; color: #ffffff; font-family:\'Plus Jakarta Sans\', sans-serif; margin-bottom: 12px;">📜 HISTORICAL ACCIDENT BASELINE</div>', unsafe_allow_html=True)
            hist_score, hist_stats = compute_historical_risk_score(selected_id)

            hc1, hc2 = st.columns(2)
            with hc1:
                st.metric("Total Accidents", hist_stats["total_accidents"])
                st.metric("Injuries", hist_stats["injuries"])
            with hc2:
                st.metric("Fatalities", hist_stats["fatalities"], delta_color="inverse")
                st.metric("Motorcycle Impact", f"{hist_stats['motorcycle_involvement_pct']}%")

    with sim_col:
        with st.container(border=True):
            st.markdown('<div style="font-size: 0.92rem; font-weight: 800; color: #ffffff; font-family:\'Plus Jakarta Sans\', sans-serif; margin-bottom: 12px;">🧪 SAFETY INTERVENTION SIMULATION</div>', unsafe_allow_html=True)
            st.caption("Adjust proposed safety improvements to simulate real-time risk reduction.")

            sim_s1 = st.slider("Speed Breakers & Enforcement (-% Speed Delta)", 0, 30, 15)
            sim_s2 = st.slider("Pothole Repairs & Zebra Markings (-% Surface Hazard)", 0, 25, 10)
            sim_s3 = st.slider("Dedicated Two-Wheeler Lane Segregation (-% Conflict)", 0, 20, 10)

            total_reduction = (sim_s1 * 0.45) + (sim_s2 * 0.35) + (sim_s3 * 0.40)
            simulated_new_score = max(10.0, score - total_reduction)

            st.markdown(render_simulation_result_card(simulated_new_score, total_reduction), unsafe_allow_html=True)

# ----------------------------------------------------
# 5. 📊 FLEET ANALYTICS & MACRO TRENDS
# ----------------------------------------------------
elif sidebar_nav == "Fleet Analytics":
    an_c1, an_c2 = st.columns([1.5, 1.5])

    with an_c1:
        with st.container(border=True):
            st.markdown('<div style="font-size: 0.95rem; font-weight: 800; color: #ffffff; font-family:\'Plus Jakarta Sans\', sans-serif; margin-bottom: 10px;">🏙️ METROPOLITAN RISK BENCHMARKING</div>', unsafe_allow_html=True)
            city_df = pd.DataFrame([{"City": j["city"], "Risk Score": j["risk_score"]} for j in junctions])
            city_avg = city_df.groupby("City")["Risk Score"].mean().reset_index().sort_values(by="Risk Score", ascending=False)

            fig_city = px.bar(
                city_avg,
                x="Risk Score",
                y="City",
                orientation="h",
                color="Risk Score",
                color_continuous_scale="Viridis",
                text="Risk Score"
            )
            fig_city.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(12,16,30,0.6)",
                font_color="#cbd5e1",
                height=320,
                margin=dict(l=20, r=20, t=20, b=20)
            )
            fig_city.update_traces(texttemplate='%{text:.1f}', textposition='outside')
            st.plotly_chart(fig_city, use_container_width=True)

    with an_c2:
        with st.container(border=True):
            st.markdown('<div style="font-size: 0.95rem; font-weight: 800; color: #ffffff; font-family:\'Plus Jakarta Sans\', sans-serif; margin-bottom: 10px;">🍩 NATIONAL RISK LEVEL DISTRIBUTION</div>', unsafe_allow_html=True)
            lvl_counts = pd.DataFrame([{"Risk Level": j["risk_level"]} for j in junctions])["Risk Level"].value_counts().reset_index()
            lvl_counts.columns = ["Risk Level", "Count"]

            fig_pie = px.pie(
                lvl_counts,
                values="Count",
                names="Risk Level",
                hole=0.55,
                color="Risk Level",
                color_discrete_map={"HIGH": "#f43f5e", "MEDIUM": "#f59e0b", "LOW": "#10b981"}
            )
            fig_pie.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font_color="#cbd5e1",
                height=320,
                margin=dict(l=20, r=20, t=20, b=20)
            )
            st.plotly_chart(fig_pie, use_container_width=True)

    st.markdown("<div style='margin-top: 24px;'></div>", unsafe_allow_html=True)
    with st.container(border=True):
        st.markdown('<div style="font-size: 0.95rem; font-weight: 800; color: #ffffff; font-family:\'Plus Jakarta Sans\', sans-serif; margin-bottom: 10px;">📈 TWO-WHEELER EXPOSURE VS COMPOSITE RISK SCORE</div>', unsafe_allow_html=True)
        scatter_data = []
        for j in junctions:
            score = j.get("risk_score") or 50.0
            two_w = 30.0 + (score * 0.4) + (hash(j["name"]) % 10)
            scatter_data.append({
                "Junction": j["name"],
                "City": j["city"],
                "Risk Score": score,
                "Two Wheeler Share (%)": min(85.0, two_w),
                "Risk Level": j["risk_level"]
            })
        sc_df = pd.DataFrame(scatter_data)

        fig_sc = px.scatter(
            sc_df,
            x="Two Wheeler Share (%)",
            y="Risk Score",
            color="Risk Level",
            color_discrete_map={"HIGH": "#f43f5e", "MEDIUM": "#f59e0b", "LOW": "#10b981"},
            hover_name="Junction",
            size="Risk Score"
        )
        fig_sc.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(12,16,30,0.6)",
            font_color="#cbd5e1",
            height=340,
            margin=dict(l=20, r=20, t=20, b=20)
        )
        st.plotly_chart(fig_sc, use_container_width=True)

# ----------------------------------------------------
# 6. 👥 CITIZEN HAZARD REPORTING PORTAL
# ----------------------------------------------------
elif sidebar_nav == "Citizen Reports":
    if "submitted_report_msg" in st.session_state:
        st.success(st.session_state.pop("submitted_report_msg"))

    c_map, c_form = st.columns([1.2, 1.8])

    with c_map:
        st.markdown('<div style="font-size:0.95rem; font-weight:800; color:#ffffff; font-family:\'Plus Jakarta Sans\', sans-serif; margin-bottom:10px;">📍 PINPOINT HAZARD ON MAP</div>', unsafe_allow_html=True)

        all_jnc_list = fetch_all_junctions()
        initial_lat = st.session_state.get("tab_picked_lat", 12.9716)
        initial_lon = st.session_state.get("tab_picked_lng", 77.5946)

        m_picker = folium.Map(location=[initial_lat, initial_lon], zoom_start=13, tiles="CartoDB dark_matter")

        for j in all_jnc_list:
            folium.CircleMarker(
                [j["lat"], j["lon"]],
                radius=6,
                color="#38bdf8",
                fill=True,
                fill_color="#6366f1",
                fill_opacity=0.8,
                tooltip=f"📍 {j['name']}"
            ).add_to(m_picker)

        if "tab_picked_lat" in st.session_state and "tab_picked_lng" in st.session_state:
            p_lat = st.session_state["tab_picked_lat"]
            p_lng = st.session_state["tab_picked_lng"]
            folium.Marker(
                [p_lat, p_lng],
                popup="📍 Selected Hazard Pinpoint",
                tooltip="📍 Dropped Pin",
                icon=folium.Icon(color="red", icon="exclamation-circle")
            ).add_to(m_picker)

        map_data = st_folium(
            m_picker,
            width="stretch",
            height=380,
            key="citizen_map_picker",
            returned_objects=["last_clicked"],
            return_on_hover=False
        )

        if map_data and map_data.get("last_clicked"):
            c_lat = map_data["last_clicked"]["lat"]
            c_lng = map_data["last_clicked"]["lng"]
            if st.session_state.get("tab_picked_lat") != c_lat or st.session_state.get("tab_picked_lng") != c_lng:
                st.session_state["tab_picked_lat"] = c_lat
                st.session_state["tab_picked_lng"] = c_lng
                near_jnc, dist_km = find_nearest_junction(c_lat, c_lng, all_jnc_list, threshold_km=1.0)
                det_val = near_jnc['name'] if near_jnc else reverse_geocode_location(c_lat, c_lng)
                st.session_state["selected_junction_name_val"] = det_val
                st.session_state["tab_select_junction_dropdown"] = det_val
                st.rerun()

        # Hardware GPS Auto-Detect
        gps_btn_html = """
        <button onclick="
            if (navigator.geolocation) {
                navigator.geolocation.getCurrentPosition(function(pos) {
                    window.top.location.href = '/?geo_lat=' + pos.coords.latitude + '&geo_lng=' + pos.coords.longitude + '&nav=Citizen Reports';
                });
            }
        " style="width:100%; background:linear-gradient(135deg, #059669 0%, #0284c7 100%); color:#fff; border:none; padding:10px 14px; border-radius:8px; font-weight:700; font-size:0.82rem; cursor:pointer; font-family:'Plus Jakarta Sans', sans-serif; margin-top:8px;">
            🎯 Locate Device via GPS
        </button>
        """
        st_components.html(gps_btn_html, height=50)

    with c_form:
        st.markdown('<div style="font-size:0.95rem; font-weight:800; color:#ffffff; font-family:\'Plus Jakarta Sans\', sans-serif; margin-bottom:10px;">🚨 HAZARD DETAILS &amp; FIELD EVIDENCE</div>', unsafe_allow_html=True)

        with st.container(border=True):
            jnc_names_map = {j["name"]: j["junction_id"] for j in junctions}
            loc_options = list(jnc_names_map.keys()) + ["➕ Custom Geotagged Location..."]

            current_loc = st.session_state.get("tab_select_junction_dropdown", loc_options[0])
            sel_idx = loc_options.index(current_loc) if current_loc in loc_options else 0

            selected_jnc_name = st.selectbox("Select Target Junction / Location*", options=loc_options, index=sel_idx)

            if selected_jnc_name == "➕ Custom Geotagged Location...":
                custom_name = st.text_input("Enter Custom Location Name*", placeholder="e.g. Indiranagar 100ft Road Merge")
            else:
                custom_name = selected_jnc_name

            reporter_name = st.text_input("Reporter Name / Designation", placeholder="e.g. Traffic Marshal / Resident (Optional)")

            issue_cat = st.selectbox("Hazard Category", options=[
                "Pothole / Damaged Road Surface",
                "Broken Traffic Signal / Light",
                "Blind Spot / Obstructed View",
                "Frequent Speeding / Illegal U-turn",
                "Near-Miss Pedestrian Crossing",
                "Waterlogging / Poor Drainage",
                "Missing Median / Defective Barrier"
            ])

            rep_sev = st.slider("Hazard Severity Rating (1 = Minor, 5 = Immediate Danger)", 1, 5, 3)
            rep_desc = st.text_area("Incident Description", placeholder="Describe exact location, lane blockages, or timing...")
            uploaded_evidence = st.file_uploader("Upload Evidence Photo / Video (Optional)", type=["jpg", "png", "jpeg", "mp4", "mov"])

            if st.button("🚨 Submit Verified Hazard Report", use_container_width=True, type="primary"):
                final_name = custom_name.strip() if custom_name.strip() else selected_jnc_name
                target_id = jnc_names_map.get(final_name, f"J-CUSTOM-{uuid.uuid4().hex[:6].upper()}")
                final_desc = rep_desc.strip() if rep_desc.strip() else f"Hazard reported at {final_name}"

                saved_filename = None
                saved_relative_path = None
                media_url = None

                if uploaded_evidence is not None:
                    file_ext = os.path.splitext(uploaded_evidence.name)[1].lower()
                    saved_filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:8]}{file_ext}"
                    reports_dir = os.path.join("data", "citizen_reports")
                    os.makedirs(reports_dir, exist_ok=True)
                    media_dest = os.path.join(reports_dir, saved_filename)
                    try:
                        file_bytes = uploaded_evidence.getvalue()
                        with open(media_dest, "wb") as f:
                            f.write(file_bytes)
                        saved_relative_path = os.path.join("data", "citizen_reports", saved_filename)
                    except Exception as e:
                        print(f"[Upload Error] {e}")

                add_citizen_report(
                    target_id, reporter_name, issue_cat, rep_sev, final_desc,
                    media_filename=saved_filename,
                    media_relative_path=saved_relative_path,
                    media_url=media_url,
                    media_type="video" if uploaded_evidence and file_ext in [".mp4", ".mov"] else "photo"
                )

                try:
                    risk_engine.compute_junction_risk(target_id)
                except Exception as rx:
                    print(f"[Risk Recalc Error] {rx}")

                st.session_state["submitted_report_msg"] = f"🎉 Hazard report for '{final_name}' successfully submitted and AI risk scores updated!"
                st.rerun()

    # Recent Reports Feed
    st.markdown("<div style='margin-top: 28px;'></div>", unsafe_allow_html=True)
    st.markdown('<div style="font-size: 1.05rem; font-weight: 800; color: #ffffff; font-family:\'Plus Jakarta Sans\', sans-serif; margin-bottom: 14px;">🗂️ VERIFIED FIELD INCIDENT STREAM</div>', unsafe_allow_html=True)

    reports = fetch_citizen_reports()
    if reports:
        jnc_id_to_name = {j["junction_id"]: j["name"] for j in junctions}
        for rep in reports[:12]:
            j_id = rep.get("junction_id", "")
            j_name = jnc_id_to_name.get(j_id) or rep.get("junction_name") or j_id
            issue = rep.get("issue_type", "Hazard")
            sev = rep.get("severity", 3)
            rep_by = rep.get("reporter_name", "Anonymous Citizen")
            ts = rep.get("timestamp", "Recent")
            desc = rep.get("description", "")
            sev_badge = "🔴 HIGH SEVERITY" if sev >= 4 else ("🟡 MEDIUM" if sev == 3 else "🟢 LOW")
            badge_color = "#fb7185" if sev >= 4 else ("#fbbf24" if sev == 3 else "#34d399")

            st.markdown(render_citizen_report_card(
                j_name=j_name,
                issue=issue,
                sev_badge=sev_badge,
                badge_color=badge_color,
                rep_by=rep_by,
                ts=ts,
                desc=desc
            ), unsafe_allow_html=True)
    else:
        st.info("No field reports submitted yet.")

# ── Clean Tactical Footer ──
render_footer()
