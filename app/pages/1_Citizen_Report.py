import streamlit as st
import os
import sys
import json
import uuid
import mimetypes
from datetime import datetime

# Add the 'app' directory to python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data_loader import load_junctions
from components import inject_custom_styles, render_navbar, render_footer, get_svg_icon

import folium
import importlib
import src.geo_utils
importlib.reload(src.geo_utils)
from src.geo_utils import find_nearest_junction, reverse_geocode_location, get_ip_location, forward_geocode_location
import streamlit.components.v1 as components
from streamlit_folium import st_folium

# ── Handle Browser GPS Callback (from HTML5 Geolocation Button) ──
if "geo_lat" in st.query_params and "geo_lng" in st.query_params:
    try:
        g_lat = float(st.query_params["geo_lat"])
        g_lng = float(st.query_params["geo_lng"])
        st.session_state["sentinel_picked_lat"] = g_lat
        st.session_state["sentinel_picked_lng"] = g_lng
        _jnc_list = load_junctions()
        near_j, _ = find_nearest_junction(g_lat, g_lng, _jnc_list)
        addr = near_j.name if near_j else reverse_geocode_location(g_lat, g_lng)
        st.session_state["sentinel_jnc_input"] = addr
        st.session_state["sentinel_select_junction_dropdown"] = addr
        st.query_params.clear()
        st.rerun()
    except Exception as ex:
        print(f"[Query Geolocation Handle Note] {ex}")

def get_safety_recommendation(issue_type: str) -> str:
    """Derives actionable safety recommendations based on reported hazard type."""
    issue_lower = (issue_type or "").lower()
    if "pothole" in issue_lower or "damaged" in issue_lower:
        return "Action: Priority Road Surface Patching & High-Vis Warning Signals"
    elif "signal" in issue_lower or "light" in issue_lower:
        return "Action: Emergency Signal Calibration & Traffic Officer Deployment"
    elif "blind spot" in issue_lower or "obstructed" in issue_lower:
        return "Action: Install Convex Mirror & Sightline Pruning"
    elif "speeding" in issue_lower or "u-turn" in issue_lower:
        return "Action: Speed Calming Installation & Automated CCTV Enforcement"
    elif "pedestrian" in issue_lower or "crossing" in issue_lower:
        return "Action: Raised Refuge Island & High-Contrast Crossing Markings"
    else:
        return "Action: Civic Safety Patrol & Rapid Site Inspection"

# Page Config
st.set_page_config(
    page_title="Citizen Safety Reporting | JunctionGuard AI",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inject Minimalist Dark Design System
inject_custom_styles()

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
REPORTS_DIR = os.path.join(PROJECT_ROOT, "data", "citizen_reports")
INDEX_FILE = os.path.join(REPORTS_DIR, "index.json")
os.makedirs(REPORTS_DIR, exist_ok=True)

ISSUE_OPTIONS = [
    "Pothole / Damaged Road Surface",
    "Broken Traffic Signal / Light",
    "Blind Spot / Obstructed Sightline",
    "Frequent Speeding / Illegal U-turn",
    "Near-Miss Pedestrian Crossing",
    "Other (Specify below)"
]

def load_reports():
    """Fetches reports from unified SQLite/Supabase database with local json fallback."""
    try:
        from src.database import fetch_citizen_reports
        from data_loader import load_junctions as _lj
        db_reports = fetch_citizen_reports()
        if db_reports:
            _jmap = {j.junction_id: j.name for j in _lj()}
            for r in db_reports:
                if not r.get("junction_name"):
                    r["junction_name"] = _jmap.get(r.get("junction_id"), r.get("junction_id", "Custom Location"))
            return db_reports
    except Exception as e:
        print(f"[Load Reports DB Note] {e}")

    if not os.path.exists(INDEX_FILE):
        return []
    try:
        with open(INDEX_FILE, "r") as f:
            return json.load(f)
    except Exception:
        return []

def save_report(report_data):
    reports = []
    if os.path.exists(INDEX_FILE):
        try:
            with open(INDEX_FILE, "r") as f:
                reports = json.load(f)
        except Exception:
            reports = []
    reports.append(report_data)
    try:
        with open(INDEX_FILE, "w") as f:
            json.dump(reports, f, indent=4)
        return True
    except Exception as e:
        st.error(f"Failed to save report: {e}")
        return False

# Top HUD Navigation Bar
render_navbar("Reports")

junctions = load_junctions()
junction_names = [j.name for j in junctions]

st.markdown("### File a Citizen Safety Report")

if "sentinel_submitted_msg" in st.session_state:
    st.success(st.session_state.pop("sentinel_submitted_msg"))

col_map, col_form = st.columns([1, 1])

@st.fragment
def render_map_picker():
    search_c1, search_c2 = st.columns([3, 1])
    with search_c1:
        search_query = st.text_input(
            "Search location",
            placeholder="Search area, road, or city (e.g. Kolhapur, Koge, MG Road...)",
            label_visibility="collapsed",
            key="sentinel_map_search_txt"
        )
    with search_c2:
        if st.button("Search", key="sentinel_map_search_btn", use_container_width=True):
            if search_query and search_query.strip():
                with st.spinner("Searching..."):
                    found = forward_geocode_location(search_query.strip())
                if found:
                    f_lat, f_lon, f_name = found
                    st.session_state["sentinel_picked_lat"] = f_lat
                    st.session_state["sentinel_picked_lng"] = f_lon
                    st.session_state["sentinel_jnc_input"] = f_name
                    st.session_state["sentinel_select_junction_dropdown"] = f_name
                    st.rerun(scope="app")
                else:
                    st.warning("Location not found. Try a nearby landmark or city.")

    default_lat = junctions[0].lat if junctions else 12.9716
    default_lon = junctions[0].lon if junctions else 77.5946

    m_picker = folium.Map(
        location=[default_lat, default_lon],
        zoom_start=13,
        tiles="OpenStreetMap",
        attr="OpenStreetMap"
    )

    map_inner_css = """
    <style>
    .leaflet-container, .leaflet-grab, .leaflet-interactive, .leaflet-drag-target {
        cursor: crosshair !important;
        background-color: #08090d !important;
    }
    .leaflet-tile, .leaflet-pane, .leaflet-tile-pane, .leaflet-tile-container img {
        filter: none !important;
        -webkit-filter: none !important;
        transition: none !important;
        opacity: 1 !important;
    }
    .leaflet-tile:hover {
        filter: none !important;
        -webkit-filter: none !important;
        opacity: 1 !important;
    }
    .leaflet-marker-icon {
        background: transparent !important;
        border: none !important;
    }
    </style>
    """
    m_picker.get_root().html.add_child(folium.Element(map_inner_css))

    for jnc in junctions:
        level = (getattr(jnc, 'risk_level', None) or "LOW").upper()
        m_col = "#ef4444" if level == "HIGH" else ("#f59e0b" if level == "MEDIUM" else "#10b981")
        m_html = f'<div style="width:14px; height:14px; border-radius:50%; background:{m_col}; box-shadow:0 0 8px {m_col}; border:2px solid #ffffff;"></div>'
        folium.Marker(
            [jnc.lat, jnc.lon],
            popup=jnc.name,
            tooltip=f"Junction: {jnc.name}",
            icon=folium.DivIcon(html=m_html, icon_size=(14, 14), icon_anchor=(7, 7))
        ).add_to(m_picker)

    if "sentinel_picked_lat" in st.session_state and "sentinel_picked_lng" in st.session_state:
        p_lat = st.session_state["sentinel_picked_lat"]
        p_lng = st.session_state["sentinel_picked_lng"]
        pin_html = '<div style="width:22px; height:22px; border-radius:50%; background:#ef4444; box-shadow:0 0 14px #ef4444; border:2px solid #ffffff; display:flex; align-items:center; justify-content:center;"><div style="width:6px; height:6px; background:#fff; border-radius:50%;"></div></div>'
        folium.Marker(
            [p_lat, p_lng],
            popup=folium.Popup(f"<b>Selected Hazard Location</b><br>({p_lat:.5f}, {p_lng:.5f})", max_width=250),
            tooltip="Selected Hazard Pinpoint",
            icon=folium.DivIcon(html=pin_html, icon_size=(22, 22), icon_anchor=(11, 11))
        ).add_to(m_picker)

    map_data = st_folium(
        m_picker,
        use_container_width=True,
        height=380,
        key="citizen_sentinel_map_picker",
        returned_objects=["last_clicked"],
        return_on_hover=False
    )

    if map_data and map_data.get("last_clicked"):
        c_lat = map_data["last_clicked"]["lat"]
        c_lng = map_data["last_clicked"]["lng"]
        if st.session_state.get("sentinel_picked_lat") != c_lat or st.session_state.get("sentinel_picked_lng") != c_lng:
            st.session_state["sentinel_picked_lat"] = c_lat
            st.session_state["sentinel_picked_lng"] = c_lng

            near_jnc, dist_km = find_nearest_junction(c_lat, c_lng, junctions, threshold_km=1.0)
            if near_jnc:
                det_val = near_jnc.name
            else:
                det_val = reverse_geocode_location(c_lat, c_lng)

            st.session_state["sentinel_jnc_input"] = det_val
            st.session_state["sentinel_select_junction_dropdown"] = det_val
            st.rerun(scope="app")

    if "sentinel_picked_lat" in st.session_state and "sentinel_picked_lng" in st.session_state:
        click_lat = st.session_state["sentinel_picked_lat"]
        click_lng = st.session_state["sentinel_picked_lng"]
        near_jnc, dist_km = find_nearest_junction(click_lat, click_lng, junctions, threshold_km=1.0)
        if near_jnc:
            st.success(f"**Junction Detected**: {near_jnc.name} ({round(dist_km*1000)}m away)")
        else:
            addr = reverse_geocode_location(click_lat, click_lng)
            st.success(f"**Pinpoint Location**: {addr}")

        st.markdown(
            f'<div style="margin-top:4px; font-size:0.74rem; color:#94a3b8; font-family:monospace;">'
            f'Coordinates: <code style="color:#38bdf8">{click_lat:.6f}, {click_lng:.6f}</code></div>',
            unsafe_allow_html=True
        )

        st.markdown("<div style='margin-top: 10px;'></div>", unsafe_allow_html=True)
        loc_c1, loc_c2 = st.columns([1, 1])
        with loc_c1:
            if st.button("Auto-Detect My Location", key="sentinel_btn_ip_autodetect", use_container_width=True, type="secondary"):
                with st.spinner("Detecting network location..."):
                    loc = get_ip_location()
                    if loc:
                        ip_lat, ip_lon, ip_name = loc
                        st.session_state["sentinel_picked_lat"] = ip_lat
                        st.session_state["sentinel_picked_lng"] = ip_lon
                        near_j, dist_km = find_nearest_junction(ip_lat, ip_lon, junctions, threshold_km=1.0)
                        det_name = near_j.name if near_j else (reverse_geocode_location(ip_lat, ip_lon) or ip_name)
                        st.session_state["sentinel_jnc_input"] = det_name
                        st.session_state["sentinel_select_junction_dropdown"] = det_name
                        st.rerun()
                    else:
                        st.error("Could not detect location. Please use the search bar or city buttons.")
        with loc_c2:
            if st.button("Reset Location Pin", key="sentinel_reset_loc_btn", use_container_width=True):
                for k in ["sentinel_picked_lat", "sentinel_picked_lng", "sentinel_jnc_input", "sentinel_select_junction_dropdown"]:
                    st.session_state.pop(k, None)
                st.rerun()

    st.markdown("<div style='font-size:0.76rem; font-weight:600; color:#94a3b8; margin-top:6px; margin-bottom:6px;'>Quick Jump to City / Area:</div>", unsafe_allow_html=True)
    q_col1, q_col2, q_col3, q_col4, q_col5 = st.columns(5)
    with q_col1:
        if st.button("Ichalkaranji", key="sentinel_quick_ich", use_container_width=True):
            st.session_state["sentinel_picked_lat"] = 16.7013
            st.session_state["sentinel_picked_lng"] = 74.4951
            st.session_state["sentinel_jnc_input"] = "Sangli Naka, Ichalkaranji"
            st.session_state["sentinel_select_junction_dropdown"] = "Sangli Naka, Ichalkaranji"
            st.rerun()
    with q_col2:
        if st.button("Kolhapur", key="sentinel_quick_kolhapur", use_container_width=True):
            st.session_state["sentinel_picked_lat"] = 16.7050
            st.session_state["sentinel_picked_lng"] = 74.2433
            st.session_state["sentinel_jnc_input"] = "Kolhapur, Maharashtra"
            st.session_state["sentinel_select_junction_dropdown"] = "Kolhapur, Maharashtra"
            st.rerun()
    with q_col3:
        if st.button("Bangalore", key="sentinel_quick_blr", use_container_width=True):
            st.session_state["sentinel_picked_lat"] = 12.9716
            st.session_state["sentinel_picked_lng"] = 77.5946
            st.session_state["sentinel_jnc_input"] = "Bangalore, Karnataka"
            st.session_state["sentinel_select_junction_dropdown"] = "Bangalore, Karnataka"
            st.rerun()
    with q_col4:
        if st.button("Pune", key="sentinel_quick_pune", use_container_width=True):
            st.session_state["sentinel_picked_lat"] = 18.5204
            st.session_state["sentinel_picked_lng"] = 73.8567
            st.session_state["sentinel_jnc_input"] = "Pune, Maharashtra"
            st.session_state["sentinel_select_junction_dropdown"] = "Pune, Maharashtra"
            st.rerun()
    with q_col5:
        if st.button("Mumbai", key="sentinel_quick_mum", use_container_width=True):
            st.session_state["sentinel_picked_lat"] = 19.0760
            st.session_state["sentinel_picked_lng"] = 72.8777
            st.session_state["sentinel_jnc_input"] = "Mumbai, Maharashtra"
            st.session_state["sentinel_select_junction_dropdown"] = "Mumbai, Maharashtra"
            st.rerun()

with col_map:
    st.markdown("##### Pinpoint Location on Map")
    st.caption("Search area, click map, or use GPS to select exact coordinates.")
    render_map_picker()

with col_form:
    st.markdown("##### Hazard Details & Evidence")

    def _reset_full_form():
        for k in [
            "sentinel_picked_lat", "sentinel_picked_lng",
            "sentinel_jnc_input", "sentinel_select_junction_dropdown",
            "sentinel_reporter_name", "sentinel_description",
            "sentinel_severity", "sentinel_custom_loc_input",
            "sentinel_custom_issue", "sentinel_issue_select",
            "_form_junction_name",
        ]:
            st.session_state.pop(k, None)

    current_loc = st.session_state.get("sentinel_jnc_input", "")
    loc_options = []
    if current_loc and current_loc not in junction_names:
        loc_options.append(current_loc)
    for jname in junction_names:
        if jname not in loc_options:
            loc_options.append(jname)
    loc_options.append("Type Custom Location Manually...")

    stored_sel = st.session_state.get("sentinel_select_junction_dropdown", "")
    if current_loc and current_loc in loc_options:
        st.session_state["sentinel_select_junction_dropdown"] = current_loc
        idx = loc_options.index(current_loc)
    elif stored_sel and stored_sel in loc_options:
        idx = loc_options.index(stored_sel)
    else:
        idx = 0

    selected_option = st.selectbox(
        "Select Junction / Location*",
        options=loc_options,
        index=idx,
        key="sentinel_select_junction_dropdown"
    )

    if selected_option == "Type Custom Location Manually...":
        typed_loc = st.text_input(
            "Enter Custom Location*",
            placeholder="e.g. MG Road & Brigade Junction, Bangalore",
            key="sentinel_custom_loc_input"
        )
        st.session_state["_form_junction_name"] = typed_loc
    else:
        st.session_state["_form_junction_name"] = selected_option
        st.session_state["sentinel_jnc_input"] = selected_option

    st.text_input(
        "Your Name (Optional)",
        placeholder="e.g. Anonymous / Traffic Marshal",
        key="sentinel_reporter_name"
    )

    st.selectbox("Issue Category", options=ISSUE_OPTIONS, key="sentinel_issue_select")

    if st.session_state.get("sentinel_issue_select") == "Other (Specify below)":
        st.text_input(
            "Specify Custom Issue Category*",
            placeholder="e.g. Waterlogging, Broken Street Lamp, Construction Debris...",
            key="sentinel_custom_issue"
        )

    st.slider(
        "Hazard Severity Level (1 = Low, 5 = High Danger)",
        min_value=1, max_value=5,
        value=st.session_state.get("sentinel_severity", 3),
        key="sentinel_severity"
    )

    st.text_area(
        "Detailed Description (Optional)",
        placeholder="Describe exact hazard location, traffic disruption, or vehicle conflicts...",
        key="sentinel_description"
    )

    st.file_uploader(
        "Upload Photo or Video Evidence (Optional)",
        type=["jpg", "png", "jpeg", "mp4", "mov", "avi", "webm"],
        key="sentinel_uploaded_file"
    )

    btn_col1, btn_col2 = st.columns([3, 1])
    with btn_col1:
        if st.button("Submit Safety Report", use_container_width=True, type="primary", key="sentinel_submit_btn"):
            st.session_state["_form_submit_requested"] = True
            st.rerun()
    with btn_col2:
        st.button("Reset", use_container_width=True, on_click=_reset_full_form, key="sentinel_reset_form_btn")

if st.session_state.pop("_form_submit_requested", False):
    selected_junction_name = st.session_state.get("_form_junction_name", "")
    selected_issue         = st.session_state.get("sentinel_issue_select", ISSUE_OPTIONS[0])
    custom_issue_type      = st.session_state.get("sentinel_custom_issue", "").strip()
    rep_severity           = st.session_state.get("sentinel_severity", 3)
    description            = st.session_state.get("sentinel_description", "").strip()
    reporter_name          = st.session_state.get("sentinel_reporter_name", "").strip()
    uploaded_file          = st.session_state.get("sentinel_uploaded_file", None)

    if not selected_junction_name.strip():
        st.error("Please select or enter a junction location before submitting.")
    elif selected_issue == "Other (Specify below)" and not custom_issue_type:
        st.error("Please specify the custom issue category.")
    else:
        final_jnc_name = selected_junction_name.strip()
        final_desc     = description if description else f"Safety hazard reported at {final_jnc_name}."
        selected_j     = next((j for j in junctions if j.name == final_jnc_name), None)

        from src.database import upsert_custom_junction
        p_lat = float(st.session_state.get("sentinel_picked_lat") or (selected_j.lat if selected_j else 18.5204))
        p_lng = float(st.session_state.get("sentinel_picked_lng") or (selected_j.lon if selected_j else 73.8567))

        if selected_j:
            final_jnc_id = selected_j.junction_id
        else:
            name_clean = final_jnc_name.strip().lower()
            name_hash = abs(hash(name_clean)) % 100000
            final_jnc_id = f"JNC-CUST-{name_hash:05d}"
            city_val = "Pune" if "pune" in name_clean else ("Bengaluru" if "bangalore" in name_clean or "bengaluru" in name_clean else ("Kolhapur" if "kolhapur" in name_clean else "India"))
            upsert_custom_junction(final_jnc_id, final_jnc_name, p_lat, p_lng, city=city_val)

        final_issue    = custom_issue_type if selected_issue == "Other (Specify below)" else selected_issue

        saved_filename = None
        saved_relative_path = None
        media_url = None

        if uploaded_file is not None:
            file_ext = os.path.splitext(uploaded_file.name)[1].lower()
            saved_filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:8]}{file_ext}"
            media_dest = os.path.join(REPORTS_DIR, saved_filename)
            try:
                file_bytes = uploaded_file.getvalue()
                with open(media_dest, "wb") as f:
                    f.write(file_bytes)
                saved_relative_path = os.path.join("data", "citizen_reports", saved_filename)
                guessed_mime = mimetypes.guess_type(uploaded_file.name)[0]
                if not guessed_mime:
                    guessed_mime = "video/mp4" if file_ext in [".mp4", ".mov", ".avi", ".webm"] else "image/jpeg"
                from src.supabase_client import upload_citizen_media_supabase
                media_url = upload_citizen_media_supabase(file_bytes, saved_filename, content_type=guessed_mime)
            except Exception as e:
                st.error(f"Failed to process media file: {e}")

        new_report = {
            "report_id": uuid.uuid4().hex,
            "junction_id": final_jnc_id,
            "junction_name": final_jnc_name,
            "reporter_name": reporter_name if reporter_name else "Anonymous",
            "issue_type": final_issue,
            "severity": rep_severity,
            "description": final_desc,
            "media_filename": saved_filename,
            "media_relative_path": saved_relative_path,
            "media_url": media_url,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        media_type_val = None
        if uploaded_file is not None:
            file_ext = os.path.splitext(uploaded_file.name)[1].lower()
            media_type_val = "video" if file_ext in [".mp4", ".mov", ".avi", ".webm"] else "photo"

        try:
            from src.database import add_citizen_report
            add_citizen_report(
                junction_id=final_jnc_id,
                reporter=new_report["reporter_name"],
                issue=final_issue,
                severity=rep_severity,
                description=final_desc,
                media_filename=saved_filename,
                media_relative_path=saved_relative_path,
                media_url=media_url,
                media_type=media_type_val
            )
        except Exception as ex:
            print(f"[Database Sync Note] {ex}")

        try:
            from src.analytics.risk_engine import ExplainableRiskEngine
            risk_engine = ExplainableRiskEngine()
            if final_jnc_id:
                risk_engine.compute_junction_risk(final_jnc_id)
        except Exception as rx:
            print(f"[Risk Engine Compute Note] {rx}")

        if save_report(new_report):
            for k in [
                "sentinel_picked_lat", "sentinel_picked_lng",
                "sentinel_jnc_input", "sentinel_select_junction_dropdown",
                "sentinel_reporter_name", "sentinel_description",
                "sentinel_severity", "sentinel_custom_loc_input",
                "sentinel_custom_issue", "sentinel_issue_select",
                "sentinel_uploaded_file", "_form_junction_name", "_form_junction_is_custom",
            ]:
                st.session_state.pop(k, None)
            st.session_state["sentinel_submitted_msg"] = f"Report for '{final_jnc_name}' successfully submitted."
            st.rerun()

st.markdown("---")
st.markdown("### Recent Citizen Reports & Safety Intelligence Feed")

all_reports = load_reports()

if not all_reports:
    st.info("No citizen reports have been filed yet.")
else:
    f_col1, f_col2, f_col3 = st.columns([1, 1, 1])
    with f_col1:
        feed_filter = st.selectbox("Filter by Junction", options=["All Junctions"] + junction_names)
    with f_col2:
        cat_filter = st.selectbox("Filter by Category", options=["All Categories"] + ISSUE_OPTIONS)
    with f_col3:
        sev_filter = st.selectbox("Filter by Risk Level", options=["All Levels", "High Risk", "Medium Risk", "Low Risk"])
    
    filtered_reports = all_reports
    if feed_filter != "All Junctions":
        filtered_reports = [r for r in filtered_reports if r.get("junction_name") == feed_filter]
    if cat_filter != "All Categories":
        filtered_reports = [r for r in filtered_reports if r.get("issue_type") == cat_filter]
    if sev_filter != "All Levels":
        if "High" in sev_filter:
            filtered_reports = [r for r in filtered_reports if r.get("severity", 3) >= 4]
        elif "Medium" in sev_filter:
            filtered_reports = [r for r in filtered_reports if r.get("severity", 3) == 3]
        elif "Low" in sev_filter:
            filtered_reports = [r for r in filtered_reports if r.get("severity", 3) <= 2]
        
    if not filtered_reports:
        st.info("No reports found matching the active filter criteria.")
    else:
        for report in reversed(filtered_reports):
            issue_name = report.get("issue_type", "Hazard")
            rec_action = get_safety_recommendation(issue_name)
            m_url = report.get("media_url")
            m_rel = report.get("media_relative_path")
            sev_val = report.get("severity", 3)
            
            if sev_val >= 4:
                sev_tag = '<span class="badge badge-red"><span class="badge-dot"></span>HIGH SEVERITY</span>'
            elif sev_val == 3:
                sev_tag = '<span class="badge badge-amber"><span class="badge-dot"></span>MEDIUM SEVERITY</span>'
            else:
                sev_tag = '<span class="badge badge-green"><span class="badge-dot"></span>LOW SEVERITY</span>'

            cloud_badge = '<span style="font-size:0.70rem; background:rgba(56,189,248,0.1); color:#38bdf8; border:1px solid rgba(56,189,248,0.25); padding:2px 8px; border-radius:9999px; font-weight:600; font-family:\'JetBrains Mono\', monospace;">Cloud Storage Synced</span>' if m_url else '<span style="font-size:0.70rem; background:rgba(148,163,184,0.1); color:#94a3b8; border:1px solid rgba(148,163,184,0.2); padding:2px 8px; border-radius:9999px; font-weight:600; font-family:\'JetBrains Mono\', monospace;">Local Storage</span>'

            st.markdown(f"""
            <div style="background:#0f131a; border:1px solid rgba(255,255,255,0.06); border-radius:10px; padding:16px; margin-bottom:12px;">
                <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:8px;">
                    <div>
                        <span style="font-weight:700; color:#ffffff; font-size:0.95rem; font-family:'Space Grotesk', sans-serif;">{report.get('junction_name')}</span>
                        <span style="color:#64748b; font-size:0.75rem; font-family:'JetBrains Mono', monospace;"> (ID: {report.get('junction_id')})</span> {cloud_badge}
                    </div>
                    <div style="font-size:0.74rem; color:#94a3b8; font-family:'JetBrains Mono', monospace;">{report.get('timestamp')}</div>
                </div>
                <div style="margin-top:6px; font-size:0.80rem; color:#cbd5e1;">
                    <span style="color:#94a3b8;">Reporter:</span> <b>{report.get('reporter_name')}</b> | <span style="color:#f59e0b;">Category: {issue_name}</span> | {sev_tag}
                </div>
                <div style="margin-top: 8px; font-size:0.86rem; color:#e2e8f0; line-height:1.4;">
                    {report.get('description')}
                </div>
                <div style="margin-top: 10px; padding: 8px 12px; background: rgba(56, 189, 248, 0.08); border-left: 3px solid #38bdf8; border-radius: 4px; font-size: 0.80rem; color: #bae6fd; font-weight: 500;">
                    {rec_action}
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            if m_url:
                ext = os.path.splitext(m_url.split('?')[0])[1].lower()
                if ext in [".mp4", ".mov", ".avi", ".webm", ".mkv"]:
                    st.caption("Video Evidence (Cloud Storage)")
                    st.video(m_url)
                else:
                    st.image(m_url, caption=f"Photo Evidence (Cloud): {report.get('media_filename', '')}", use_container_width=True)
            elif m_rel:
                full_media_path = os.path.join(PROJECT_ROOT, m_rel)
                if os.path.exists(full_media_path):
                    ext = os.path.splitext(m_rel)[1].lower()
                    if ext in [".mp4", ".mov", ".avi", ".webm", ".mkv"]:
                        st.caption("Video Evidence (Local Storage)")
                        st.video(full_media_path)
                    else:
                        st.image(full_media_path, caption=f"Photo Evidence (Local): {report.get('media_filename')}", use_container_width=True)
                    
            st.markdown("<div style='margin-bottom: 0.5rem;'></div>", unsafe_allow_html=True)

render_footer()
