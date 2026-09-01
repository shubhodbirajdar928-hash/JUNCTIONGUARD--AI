"""
JunctionGuard AI - Geographic Surveillance & Directory Portal
Provides search, filtering, and deep-dive risk diagnostics across monitored junctions.
"""

import streamlit as st
import folium
from folium.plugins import HeatMap, MiniMap, Fullscreen
from streamlit_folium import st_folium
import pandas as pd
from typing import Optional, List

from data_loader import load_junctions
from components import (
    render_risk_badge,
    render_contributing_factors,
    render_awaiting_data_banner,
    inject_custom_styles,
    get_risk_badge_html,
    render_navbar,
    render_footer,
    get_svg_icon
)

st.set_page_config(
    page_title="Junction Directory | JunctionGuard AI",
    layout="wide",
    initial_sidebar_state="expanded"
)

inject_custom_styles()

render_navbar("Junction Directory")

junctions = load_junctions()

with st.sidebar:
    st.markdown(f"""
    <div style="padding: 8px 0 16px 0; border-bottom: 1px solid rgba(255,255,255,0.06); margin-bottom: 16px; display:flex; align-items:center; gap:10px;">
        <div class="brand-shield-logo" style="width:32px; height:32px;">
            {get_svg_icon("shield_logo", size=18)}
        </div>
        <div>
            <div style="font-size: 1.02rem; font-weight: 700; color: #f8fafc; font-family:'Space Grotesk', sans-serif;">Directory Filters</div>
            <div style="font-size: 0.62rem; color: #10b981; font-family:'JetBrains Mono', monospace;">
                FLEET SURVEILLANCE ACTIVE
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    search_query = st.text_input("Search Junctions", placeholder="Enter junction name or ID...").strip()
    
    available_cities = ["All Cities"] + sorted(list(set(j.city for j in junctions if j.city)))
    city_filter = st.selectbox("Filter by City", options=available_cities)

    risk_filter = st.selectbox(
        "Filter by Risk Level",
        options=["All Levels", "HIGH", "MEDIUM", "LOW"]
    )
    
    sort_by = st.selectbox(
        "Sort Order",
        options=[
            "Risk Score (High to Low)",
            "Risk Score (Low to High)",
            "Name (A-Z)",
            "Name (Z-A)"
        ]
    )

filtered_junctions = []
for j in junctions:
    if search_query:
        query_lower = search_query.lower()
        if query_lower not in j.name.lower() and query_lower not in j.junction_id.lower():
            continue
            
    if city_filter != "All Cities" and j.city != city_filter:
        continue

    if risk_filter != "All Levels":
        actual_level = j.risk_level.upper() if j.risk_level else "AWAITING DATA"
        if actual_level != risk_filter:
            continue
            
    filtered_junctions.append(j)

def get_sort_key(junction):
    if "Name" in sort_by:
        return junction.name
    else:
        score = junction.risk_score
        if score is None:
            return -1.0 if "High to Low" in sort_by else float('inf')
        return score

reverse_sort = "Z-A" in sort_by or "High to Low" in sort_by
filtered_junctions.sort(key=get_sort_key, reverse=reverse_sort)

kpi1, kpi2, kpi3, kpi4 = st.columns(4)
total_jnc = len(junctions)
high_risk_count = sum(1 for j in junctions if j.risk_level == "HIGH")
avg_risk_score = round(sum(j.risk_score for j in junctions if j.risk_score is not None) / max(1, total_jnc), 1)
filtered_count = len(filtered_junctions)

with kpi1:
    st.markdown(f"""
    <div class="kpi-tactical-card">
        <div>
            <div class="kpi-label">MONITORED NODES</div>
            <div class="kpi-num">{total_jnc}</div>
            <div class="kpi-sub" style="color: #f97316;"><span class="live-dot-green"></span> ACTIVE FLEET</div>
        </div>
        <div class="kpi-icon-wrap" style="background: rgba(249, 115, 22, 0.1); border: 1px solid rgba(249, 115, 22, 0.25); color: #f97316;">
            {get_svg_icon("radar", color="#f97316", size=20)}
        </div>
    </div>
    """, unsafe_allow_html=True)

with kpi2:
    st.markdown(f"""
    <div class="kpi-tactical-card kpi-card-critical">
        <div>
            <div class="kpi-label">HIGH RISK NODES</div>
            <div class="kpi-num" style="color: #f87171;">{high_risk_count}</div>
            <div class="kpi-sub" style="color: #ef4444;"><span class="live-dot-red"></span> CRITICAL ATTENTION</div>
        </div>
        <div class="kpi-icon-wrap" style="background: rgba(239, 68, 68, 0.1); border: 1px solid rgba(239, 68, 68, 0.25); color: #ef4444;">
            {get_svg_icon("alert", color="#ef4444", size=20)}
        </div>
    </div>
    """, unsafe_allow_html=True)

with kpi3:
    st.markdown(f"""
    <div class="kpi-tactical-card">
        <div>
            <div class="kpi-label">FLEET AVG RISK</div>
            <div class="kpi-num" style="color: #fbbf24;">{avg_risk_score} <span class="kpi-denom">/100</span></div>
            <div class="kpi-sub" style="color: #f59e0b;"><span class="live-dot-green"></span> CALIBRATED</div>
        </div>
        <div class="kpi-icon-wrap" style="background: rgba(245, 158, 11, 0.1); border: 1px solid rgba(245, 158, 11, 0.25); color: #f59e0b;">
            {get_svg_icon("chart", color="#f59e0b", size=20)}
        </div>
    </div>
    """, unsafe_allow_html=True)

with kpi4:
    st.markdown(f"""
    <div class="kpi-tactical-card">
        <div>
            <div class="kpi-label">MATCHED NODES</div>
            <div class="kpi-num" style="color: #38bdf8;">{filtered_count}</div>
            <div class="kpi-sub" style="color: #38bdf8;"><span class="live-dot-green"></span> ACTIVE FILTER</div>
        </div>
        <div class="kpi-icon-wrap" style="background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.25); color: #38bdf8;">
            {get_svg_icon("search", color="#38bdf8", size=20)}
        </div>
    </div>
    """, unsafe_allow_html=True)

st.write("")

col_list, col_map = st.columns([2, 3])

if "selected_junction_id" not in st.session_state:
    st.session_state.selected_junction_id = junctions[0].junction_id if junctions else None

with col_list:
    st.markdown("### Monitored Junctions Roster")
    
    if not filtered_junctions:
        st.info("No junctions match the current search or filter criteria.")
    else:
        for j in filtered_junctions:
            is_selected = st.session_state.selected_junction_id == j.junction_id
            
            badge_html = get_risk_badge_html(j.risk_level)

            if j.risk_level and j.risk_level.upper() == "HIGH":
                border_accent = "border-left: 3px solid #ef4444;"
                score_badge_style = "background: rgba(239, 68, 68, 0.12); color: #f87171; border: 1px solid rgba(239, 68, 68, 0.25);"
            elif j.risk_level and j.risk_level.upper() == "MEDIUM":
                border_accent = "border-left: 3px solid #f59e0b;"
                score_badge_style = "background: rgba(245, 158, 11, 0.12); color: #fbbf24; border: 1px solid rgba(245, 158, 11, 0.25);"
            elif j.risk_level and j.risk_level.upper() == "LOW":
                border_accent = "border-left: 3px solid #10b981;"
                score_badge_style = "background: rgba(16, 185, 129, 0.12); color: #34d399; border: 1px solid rgba(16, 185, 129, 0.25);"
            else:
                border_accent = "border-left: 3px solid #6366f1;"
                score_badge_style = "background: rgba(99, 102, 241, 0.12); color: #a5b4fc; border: 1px solid rgba(99, 102, 241, 0.25);"
            
            score_disp = f"{j.risk_score:.1f}" if j.risk_score is not None else "--"

            st.markdown(f"""
            <div style="background:#0f131a; border:1px solid rgba(255,255,255,0.06); {border_accent} border-radius:8px; padding:14px; margin-bottom:8px;">
                <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                    <div>
                        <strong style="color: #f8fafc; font-size: 0.95rem; font-family:'Space Grotesk', sans-serif;">{j.name}</strong>
                        <div style="font-size: 0.74rem; color: #94a3b8; margin-top: 3px; font-family: 'JetBrains Mono', monospace;">
                            <code>{j.junction_id}</code> &bull; {j.city or 'India'} &bull; {j.lat:.4f}, {j.lon:.4f}
                        </div>
                    </div>
                    <div style="display: flex; flex-direction: column; align-items: flex-end; gap: 4px;">
                        {badge_html}
                        <span style="font-size: 0.82rem; font-weight: 700; padding: 2px 8px; border-radius: 6px; font-family: 'JetBrains Mono', monospace; {score_badge_style}">
                            {score_disp} <span style="font-size:0.68rem; font-weight:400;">/100</span>
                        </span>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            btn_col_left, btn_col_right = st.columns([3, 1])
            with btn_col_right:
                if st.button("Inspect Node", key=f"btn_{j.junction_id}", use_container_width=True):
                    st.session_state.selected_junction_id = j.junction_id
                    st.rerun()
            
            st.markdown("<div style='margin-bottom: 0.2rem;'></div>", unsafe_allow_html=True)

selected_junction = next((j for j in junctions if j.junction_id == st.session_state.selected_junction_id), None)

with col_map:
    st.markdown("### Geographic Surveillance & Radar View")
    
    if selected_junction:
        map_center = [selected_junction.lat, selected_junction.lon]
        map_zoom = 14
    elif filtered_junctions:
        avg_lat = sum(j.lat for j in filtered_junctions) / len(filtered_junctions)
        avg_lon = sum(j.lon for j in filtered_junctions) / len(filtered_junctions)
        map_center = [avg_lat, avg_lon]
        map_zoom = 12
    else:
        map_center = [20.5937, 78.9629]
        map_zoom = 5

    m = folium.Map(
        location=map_center,
        zoom_start=map_zoom,
        min_zoom=2,
        max_zoom=19,
        tiles=None,
        control_scale=True,
        world_copy_jump=False,
        max_bounds=True,
        min_lat=-85, max_lat=85, min_lon=-180, max_lon=180
    )
    
    folium.TileLayer(
        tiles="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
        attr="&copy; OpenStreetMap",
        name="Street View",
        overlay=False,
        control=True,
        no_wrap=True,
        bounds=[[-85, -180], [85, 180]]
    ).add_to(m)

    folium.TileLayer(
        tiles="https://server.arcgisonline.com/ArcGIS/rest/services/Canvas/World_Dark_Gray_Base/MapServer/tile/{z}/{y}/{x}",
        attr="Esri World Dark Gray Canvas",
        name="Dark Tactical",
        overlay=False,
        control=True,
        no_wrap=True,
        bounds=[[-85, -180], [85, 180]]
    ).add_to(m)

    folium.TileLayer(
        tiles="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
        attr="Esri World Imagery",
        name="Satellite Imagery",
        overlay=False,
        control=True,
        no_wrap=True,
        bounds=[[-85, -180], [85, 180]]
    ).add_to(m)

    markers_layer = folium.FeatureGroup(name="Junction Hotspots", overlay=True)
    for j in filtered_junctions:
        level = (j.risk_level or "LOW").upper()
        if level == "HIGH":
            circle_color = "#ef4444"
        elif level == "MEDIUM":
            circle_color = "#f59e0b"
        else:
            circle_color = "#10b981"
            
        is_current = (selected_junction and selected_junction.junction_id == j.junction_id)

        pulse_html = f"""
        <div style="position:relative; width:22px; height:22px; display:flex; align-items:center; justify-content:center;">
            <div style="width:12px; height:12px; border-radius:50%; background:{circle_color}; border:2px solid #ffffff; box-shadow:0 0 8px {circle_color};"></div>
        </div>
        """
        
        folium.Marker(
            location=[j.lat, j.lon],
            popup=folium.Popup(f"<b>{j.name}</b><br>ID: {j.junction_id}<br>Score: {j.risk_score or 0.0:.1f}/100", max_width=240),
            tooltip=f"{j.name} ({level})",
            icon=folium.DivIcon(html=pulse_html, icon_size=(22, 22), icon_anchor=(11, 11))
        ).add_to(markers_layer)
        
        if is_current or level == "HIGH":
            folium.Circle(
                location=[j.lat, j.lon],
                radius=300,
                color=circle_color,
                fill=True,
                fill_color=circle_color,
                fill_opacity=0.12,
                weight=1
            ).add_to(markers_layer)

    markers_layer.add_to(m)
    folium.LayerControl(position="topright", collapsed=True).add_to(m)
            
    st_folium(
        m,
        width="stretch",
        height=480,
        key=f"junctions_map_{st.session_state.selected_junction_id}",
        returned_objects=[],
        return_on_hover=False
    )

st.markdown("<div style='margin-top: 1.5rem;'></div>", unsafe_allow_html=True)
if selected_junction:
    st.markdown(f"### Deep-Dive Risk Diagnostics: **{selected_junction.name}** ({selected_junction.city or 'India'})")
    
    col_detail_left, col_detail_right = st.columns([1, 2])
    
    with col_detail_left:
        score_val = f"{selected_junction.risk_score:.1f}" if selected_junction.risk_score is not None else "N/A"
        level_str = (selected_junction.risk_level or "LOW").upper()
        s_col = "#f87171" if level_str == "HIGH" else ("#fbbf24" if level_str == "MEDIUM" else "#34d399")

        st.markdown(f"""
        <div style="background:#0f131a; border:1px solid rgba(255,255,255,0.06); border-radius:10px; padding: 20px;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
                <span style="font-size: 0.76rem; color: #94a3b8; font-weight: 700; text-transform: uppercase;">NODE ID</span>
                <code style="background: rgba(249,115,22,0.1); color: #f97316; padding: 2px 10px; border-radius: 9999px; font-weight:700;">
                    {selected_junction.junction_id}
                </code>
            </div>
            <div style="font-size: 0.80rem; color: #94a3b8; margin-bottom: 16px;">
                <b>Coordinates:</b> {selected_junction.lat:.4f}&deg; N, {selected_junction.lon:.4f}&deg; E
            </div>
            <div style="margin: 12px 0;">
                <div style="font-size: 0.74rem; color: #94a3b8; font-weight: 700; text-transform: uppercase;">COMPOSITE RISK INDEX</div>
                <div style="font-size: 2.5rem; font-weight: 800; color: {s_col}; font-family: 'Space Grotesk', sans-serif; line-height: 1.1;">
                    {score_val}<span style="font-size: 1.1rem; color: #64748b; font-weight: 400;"> / 100</span>
                </div>
            </div>
            <div style="margin-top: 14px; padding-top: 12px; border-top: 1px solid rgba(255,255,255,0.06); display:flex; justify-content:space-between; align-items:center;">
                <span style="font-size: 0.78rem; color: #94a3b8;">Classification:</span>
                {get_risk_badge_html(selected_junction.risk_level)}
            </div>
        </div>
        """, unsafe_allow_html=True)
        
    with col_detail_right:
        st.markdown("""
        <div style="background:#0f131a; border:1px solid rgba(255,255,255,0.06); border-radius:10px; padding: 20px;">
            <div style="font-size: 0.82rem; color: #94a3b8; font-weight: 700; text-transform: uppercase; margin-bottom: 14px;">
                Explainable Factor Weights &amp; Multi-Source Attribution (Sum = 100%)
            </div>
        """, unsafe_allow_html=True)
        render_contributing_factors(selected_junction.contributing_factors, junction_id=selected_junction.junction_id)
        st.markdown("</div>", unsafe_allow_html=True)
else:
    st.info("Select a junction above to view its detailed breakdown.")

render_footer()
