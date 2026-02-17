import streamlit as st
import json
import os
from datetime import datetime

# --- CONFIGURATION ---
DATA_FILE = "knowledge_base.json"

# SECURE PASSWORD HANDLING
# Try to load from Streamlit Secrets (Cloud), otherwise default to local dev password
if "STAFF_PASSWORD" in st.secrets:
    STAFF_PASSWORD = st.secrets["STAFF_PASSWORD"]
else:
    # Fallback for when you run it locally on your laptop
    STAFF_PASSWORD = "LocalDevPassword123" 

# --- 1. THEME & CSS INJECTION ---
def load_css():
    st.markdown("""
        <style>
            /* --- IMPORTING WATERPLAY THEME --- */
            :root {
                --bg-color: #0b1e3b;
                --card-bg: #132a4a;
                --text-main: #ffffff;
                --brand-orange: #f58025;
                --brand-purple: #9b59b6;
                --brand-green: #8cc63f;
            }

            /* Main Background */
            .stApp {
                background-color: var(--bg-color);
                background-image: radial-gradient(circle at 50% 0%, #163666 0%, #0b1e3b 100%);
                font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
                color: white;
            }

            /* Hide Streamlit Branding */
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}

            /* --- CUSTOM HEADER --- */
            .custom-header {
                background: rgba(11, 30, 59, 0.95);
                padding: 1.5rem;
                border-bottom: 2px solid var(--brand-purple);
                display: flex;
                align-items: center;
                justify-content: space-between;
                margin-bottom: 20px;
                border-radius: 0 0 12px 12px;
                box-shadow: 0 4px 20px rgba(0,0,0,0.4);
            }
            
            .header-title {
                font-size: 1.4rem; font-weight: 700; letter-spacing: 1px; color: white;
            }
            .header-subtitle {
                font-size: 0.8rem; color: var(--brand-orange); text-transform: uppercase; margin-left: 10px;
            }

            /* --- INPUT FIELDS (Matching style.css) --- */
            .stTextInput input, .stTextArea textarea, .stSelectbox div[data-baseweb="select"] {
                background-color: rgba(19, 42, 74, 0.6) !important;
                border: 1px solid rgba(255,255,255,0.2) !important;
                color: white !important;
                border-radius: 6px !important;
            }
            
            /* Focus State */
            .stTextInput input:focus {
                border-color: var(--brand-orange) !important;
                box-shadow: 0 0 10px rgba(245, 128, 37, 0.2) !important;
            }

            /* --- BUTTONS --- */
            div.stButton > button {
                background-color: var(--brand-orange);
                color: white;
                border: none;
                border-radius: 50px;
                padding: 0.5rem 2rem;
                font-weight: 600;
                transition: all 0.3s ease;
                box-shadow: 0 4px 10px rgba(245, 128, 37, 0.2);
            }
            div.stButton > button:hover {
                background-color: #d16b1e;
                transform: translateY(-2px);
                box-shadow: 0 6px 20px rgba(245, 128, 37, 0.4);
                color: white;
            }

            /* --- CARDS / EXPANDERS --- */
            .streamlit-expanderHeader {
                background-color: var(--card-bg);
                border: 1px solid rgba(255,255,255,0.1);
                color: white !important;
                border-radius: 8px;
            }
            
            /* --- SUCCESS/ERROR MESSAGES --- */
            .stSuccess {
                background-color: rgba(140, 198, 63, 0.1);
                border: 1px solid var(--brand-green);
                color: var(--brand-green);
            }
        </style>
    """, unsafe_allow_html=True)

# --- 2. DATA HANDLING ---
def load_data():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def save_case(case_data):
    data = load_data()
    data.append(case_data)
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

def search_cases(query, cases):
    if not query: return cases[-10:]
    query = query.lower()
    results = [c for c in cases if query in str(c).lower()]
    return reversed(results)

# --- 3. LOGIN SCREEN (Matches Login Overlay) ---
def check_password():
    if "password_correct" not in st.session_state:
        st.session_state.password_correct = False

    if not st.session_state.password_correct:
        # Centered Login Box
        c1, c2, c3 = st.columns([1,2,1])
        with c2:
            st.markdown("<br><br><br>", unsafe_allow_html=True)
            with st.container():
                st.markdown("""
                <div style="text-align: center; background: #132a4a; padding: 40px; border-radius: 12px; border: 1px solid #9b59b6; box-shadow: 0 20px 50px rgba(0,0,0,0.5);">
                    <h2 style="color: white; margin-bottom: 5px;">PARK WIZARD</h2>
                    <p style="color: #9b59b6; font-size: 0.9rem; letter-spacing: 2px; text-transform: uppercase;">Staff Access Only</p>
                </div>
                """, unsafe_allow_html=True)
                
                pwd = st.text_input("Enter Access Code", type="password", label_visibility="collapsed", placeholder="ACCESS CODE")
                
                if st.button("LOGIN", use_container_width=True):
                    if pwd == STAFF_PASSWORD:
                        st.session_state.password_correct = True
                        st.rerun()
                    else:
                        st.error("⛔ Access Denied")
        return False
    return True

# --- 4. MAIN DASHBOARD ---
def main():
    st.set_page_config(page_title="Park Wizard Staff", layout="wide")
    load_css() # Inject the theme

    if not check_password():
        return

    # -- Custom Header --
    st.markdown("""
        <div class="custom-header">
            <div class="header-title">PARK WIZARD <span class="header-subtitle">HIVE MIND</span></div>
            <div style="font-size: 0.8rem; color: #aab8c2;">LOGGED IN: <strong>SUPPORT TEAM</strong></div>
        </div>
    """, unsafe_allow_html=True)

    # -- Layout --
    col_log, col_search = st.columns([1.2, 1])

    # --- LEFT COL: THE LOGGER ---
    with col_log:
        st.markdown("### 📝 Log a Fix")
        with st.container():
            st.markdown('<div style="background: rgba(19,42,74,0.4); padding: 20px; border-radius: 12px; border: 1px solid rgba(255,255,255,0.05);">', unsafe_allow_html=True)
            
            with st.form("logger"):
                c1, c2 = st.columns(2)
                with c1:
                    cat = st.selectbox("Category", ["Solenoid Valve", "Controller", "Activator", "Pump", "Plumbing"])
                with c2:
                    tags = st.multiselect("Tags", ["Spring Startup", "Freeze Damage", "New Install", "High Pressure"])
                
                symptom = st.text_input("Symptom Observed", placeholder="e.g. Valve clicking but not opening")
                root_cause = st.text_input("Root Cause", placeholder="e.g. Diaphragm stuck from winter storage")
                fix = st.text_area("Action Taken", placeholder="e.g. Disassembled and lubricated seal.")
                
                submitted = st.form_submit_button("💾 Save to Hive Mind")
                
                if submitted:
                    if symptom and fix:
                        new_case = {
                            "id": datetime.now().strftime("%Y%m%d-%H%M%S"),
                            "date": datetime.now().strftime("%Y-%m-%d"),
                            "category": cat,
                            "tags": tags,
                            "symptom": symptom,
                            "diagnosis": root_cause,
                            "fix": fix
                        }
                        save_case(new_case)
                        st.success("✅ Logged successfully!")
                    else:
                        st.warning("⚠️ Symptom and Fix are required.")
            
            st.markdown('</div>', unsafe_allow_html=True)

    # --- RIGHT COL: THE HIVE MIND ---
    with col_search:
        st.markdown("### 🔍 Search Hive")
        query = st.text_input("Search symptoms...", placeholder="Type to search...", label_visibility="collapsed")
        
        results = list(search_cases(query, load_data()))
        
        st.markdown(f"<div style='color: #8898aa; font-size: 0.8rem; margin-bottom: 10px;'>Found {len(results)} records</div>", unsafe_allow_html=True)
        
        for case in results:
            # Dynamic Icon based on category
            icon = "🔧"
            if case['category'] == "Controller": icon = "⚡"
            if case['category'] == "Solenoid Valve": icon = "💧"
            
            with st.expander(f"{icon} {case['symptom']}"):
                st.markdown(f"**Cause:** {case['diagnosis']}")
                st.markdown(f"**Fix:** {case['fix']}")
                st.markdown(f"<small style='color:#f58025'>Tags: {', '.join(case['tags'])}</small>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
