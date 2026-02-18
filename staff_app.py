import streamlit as st
import json
import os
from datetime import datetime

# --- CONFIGURATION ---
DATA_FILE = "knowledge_base.json"

# SECURE PASSWORD HANDLING
# Checks Streamlit Secrets first (Cloud), falls back to local (Testing)
if "STAFF_PASSWORD" in st.secrets:
    STAFF_PASSWORD = st.secrets["STAFF_PASSWORD"]
else:
    STAFF_PASSWORD = "Splash2026"  # Default for local testing only

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

            /* --- INPUT FIELDS --- */
            .stTextInput input, .stTextArea textarea, .stSelectbox div[data-baseweb="select"] {
                background-color: rgba(19, 42, 74, 0.6) !important;
                border: 1px solid rgba(255,255,255,0.2) !important;
                color: white !important;
                border-radius: 6px !important;
            }
            
            /* Focus State */
            .stTextInput input:focus, .stTextArea textarea:focus {
                border-color: var(--brand-orange) !important;
                box-shadow: 0 0 10px rgba(245, 128, 37, 0.2) !important;
            }

            /* --- BUTTONS --- */
            div.stButton > button {
                background-color: var(--brand-orange);
                color: white;
                border: none;
                border-radius: 50px;
                padding: 0.6rem 2rem;
                font-weight: 600;
                transition: all 0.3s ease;
                box-shadow: 0 4px 10px rgba(245, 128, 37, 0.2);
                width: 100%;
            }
            div.stButton > button:hover {
                background-color: #d16b1e;
                transform: translateY(-2px);
                box-shadow: 0 6px 20px rgba(245, 128, 37, 0.4);
                color: white;
            }

            /* --- EXPANDERS --- */
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
            .stWarning {
                background-color: rgba(245, 128, 37, 0.1);
                border: 1px solid var(--brand-orange);
                color: var(--brand-orange);
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
    if not query: return cases[-10:] # Return last 10 default
    query = query.lower()
    # Search across all relevant fields (The "Brain")
    results = [c for c in cases if (
        query in str(c.get('customer_verbatim', '')).lower() or
        query in str(c.get('specific_diagnosis', '')).lower() or
        query in str(c.get('fix_action', '')).lower() or
        query in str(c.get('tech_category', '')).lower()
    )]
    return reversed(results)

# --- 3. LOGIN SCREEN ---
def check_password():
    if "password_correct" not in st.session_state:
        st.session_state.password_correct = False

    if not st.session_state.password_correct:
        c1, c2, c3 = st.columns([1,2,1])
        with c2:
            st.markdown("<br><br>", unsafe_allow_html=True)
            st.markdown("""
            <div style="text-align: center; background: #132a4a; padding: 40px; border-radius: 12px; border: 1px solid #9b59b6; box-shadow: 0 20px 50px rgba(0,0,0,0.5);">
                <h2 style="color: white; margin-bottom: 5px;">PARK WIZARD</h2>
                <p style="color: #9b59b6; font-size: 0.9rem; letter-spacing: 2px; text-transform: uppercase;">Staff Access Only</p>
            </div>
            """, unsafe_allow_html=True)
            
            pwd = st.text_input("Enter Access Code", type="password", label_visibility="collapsed", placeholder="ACCESS CODE")
            
            if st.button("LOGIN"):
                if pwd == STAFF_PASSWORD:
                    st.session_state.password_correct = True
                    st.rerun()
                else:
                    st.error("⛔ Access Denied")
        return False
    return True

# --- 4. MAIN DASHBOARD ---
def main():
    st.set_page_config(page_title="Park Wizard Hive", page_icon="🧠", layout="wide")
    load_css()

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

    # --- LEFT COL: THE LOGGER (New Diagnostic Schema) ---
    with col_log:
        st.markdown("### 📝 Log a Diagnostic Fix")
        with st.container():
            st.markdown('<div style="background: rgba(19,42,74,0.4); padding: 20px; border-radius: 12px; border: 1px solid rgba(255,255,255,0.05);">', unsafe_allow_html=True)
            
            with st.form("logger"):
                st.caption("1. THE CUSTOMER'S VOICE (Crucial for AI)")
                customer_verbatim = st.text_input("What did the customer say/see?", 
                    placeholder="e.g. 'The button feels mushy and nothing happens'")

                st.caption("2. THE CONTEXT")
                c1, c2, c3 = st.columns(3)
                with c1:
                    lifecycle = st.selectbox("Lifecycle", ["Spring Startup", "Daily Operation", "Winterizing", "New Install"])
                with c2:
                    age = st.selectbox("Park Age", ["Unknown", "< 1 Year", "1-5 Years", "5-10 Years", "10+ Years"])
                with c3:
                    tech_category = st.selectbox("Component", ["Activator (Button)", "Solenoid Valve", "Controller", "Pump", "Structure/Fiberglass"])

                st.caption("3. THE TECHNICAL FIX")
                # This field replaces the vague "Failure Mode" from your CRM
                root_cause_type = st.selectbox("Root Cause", 
                    ["Wear & Tear", "Debris / Blockage", "Installation Error", "Manufacturing Defect", "Environmental (Freeze/Lightning)", "User Error"])
                
                specific_diagnosis = st.text_input("Specific Diagnosis", 
                    placeholder="e.g. Polara Switch failed (Internal spring collapsed)")

                fix_action = st.text_area("Resolution / Action Taken", 
                    placeholder="e.g. Replaced switch with new Black Polara unit. Verified click.")
                
                submitted = st.form_submit_button("💾 Save to Hive Mind")
                
                if submitted:
                    if customer_verbatim and fix_action:
                        new_case = {
                            "id": datetime.now().strftime("%Y%m%d-%H%M%S"),
                            "date": datetime.now().strftime("%Y-%m-%d"),
                            "customer_verbatim": customer_verbatim,
                            "lifecycle": lifecycle,
                            "age": age,
                            "tech_category": tech_category,
                            "root_cause_type": root_cause_type,
                            "specific_diagnosis": specific_diagnosis,
                            "fix_action": fix_action
                        }
                        save_case(new_case)
                        st.success("✅ Logged! This is high-quality training data.")
                    else:
                        st.warning("⚠️ Please fill in 'Customer Voice' and 'Resolution'.")
            
            st.markdown('</div>', unsafe_allow_html=True)

    # --- RIGHT COL: THE SEARCH ENGINE ---
    with col_search:
        st.markdown("### 🔍 Search Knowledge Base")
        query = st.text_input("Search symptoms...", placeholder="Type to search...", label_visibility="collapsed")
        
        all_cases = load_data()
        results = list(search_cases(query, all_cases))
        
        st.markdown(f"<div style='color: #8898aa; font-size: 0.8rem; margin-bottom: 10px;'>Found {len(results)} records</div>", unsafe_allow_html=True)
        
        if not results and not query:
            st.info("Start logging cases to build the brain!")
        
        for case in results:
            # Dynamic Icon
            icon = "🔧"
            if "Activator" in case['tech_category']: icon = "🔴"
            if "Valve" in case['tech_category']: icon = "💧"
            if "Controller" in case['tech_category']: icon = "⚡"
            
            with st.expander(f"{icon} {case.get('specific_diagnosis', 'Unknown Issue')}"):
                st.markdown(f"**Customer Said:** *\"{case.get('customer_verbatim', 'N/A')}\"*")
                st.markdown(f"**The Fix:** {case.get('fix_action', 'N/A')}")
                st.markdown(f"<small style='color:#f58025'>Cause: {case.get('root_cause_type')} | Context: {case.get('lifecycle')}</small>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
