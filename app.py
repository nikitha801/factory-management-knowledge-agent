import os
import ssl
import certifi

# Fix macOS Python SSL certificate verification
os.environ["SSL_CERT_FILE"] = certifi.where()
os.environ["REQUESTS_CA_BUNDLE"] = certifi.where()
_orig_create_default_context = ssl.create_default_context
def _custom_create_default_context(*args, **kwargs):
    if "cafile" not in kwargs or kwargs["cafile"] is None:
        kwargs["cafile"] = certifi.where()
    return _orig_create_default_context(*args, **kwargs)
ssl.create_default_context = _custom_create_default_context

import streamlit as st
from dotenv import load_dotenv
import importlib
import agent as agent_module
importlib.reload(agent_module)
from agent import FactoryMaintenanceAgent
from seed_memory import seed_factory_memory, HISTORICAL_INCIDENTS

load_dotenv()

st.set_page_config(
    page_title="Factory Maintenance Knowledge Agent",
    page_icon="⚙️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling for modern Industrial look
st.markdown("""
<style>
    .metric-card {
        background-color: #1e293b;
        border-radius: 8px;
        padding: 16px;
        border-left: 4px solid #3b82f6;
        margin-bottom: 12px;
        color: #f8fafc;
    }
    .memory-badge {
        background-color: #10b981;
        color: white;
        padding: 3px 8px;
        border-radius: 12px;
        font-size: 0.8rem;
        font-weight: bold;
    }
    .oem-badge {
        background-color: #64748b;
        color: white;
        padding: 3px 8px;
        border-radius: 12px;
        font-size: 0.8rem;
        font-weight: bold;
    }
    .highlight-box {
        background-color: #0f172a;
        border: 1px solid #334155;
        border-radius: 8px;
        padding: 14px;
        margin-top: 8px;
    }
</style>
""", unsafe_allow_html=True)

# ----------------- SIDEBAR -----------------
with st.sidebar:
    st.image("https://img.icons8.com/isometric/100/factory.png", width=64)
    st.title("Plant Config")

    st.subheader("🔑 API Credentials")
    env_hindsight = os.getenv("HINDSIGHT_API_KEY", "")
    default_hindsight = "" if env_hindsight == "your_hindsight_api_key_here" else env_hindsight
    hindsight_key = st.text_input(
        "Hindsight API Key",
        value=default_hindsight,
        type="password",
        placeholder="Paste your Hindsight API key here",
        help="Get from ui.hindsight.vectorize.io (Use promo code MEMHACK99 for $50 credit)"
    )

    env_groq = os.getenv("GROQ_API_KEY", "")
    default_groq = "" if env_groq == "your_groq_api_key_here" else env_groq
    groq_key = st.text_input(
        "Groq API Key",
        value=default_groq,
        type="password",
        placeholder="gsk_...",
        help="Free key from console.groq.com"
    )

    if not hindsight_key:
        st.warning("⚠️ Hindsight API key needed for memory.")
    if not groq_key:
        st.warning("⚠️ Groq API key needed for AI diagnosis.")

    bank_id = st.text_input(
        "Hindsight Bank ID",
        value=os.getenv("HINDSIGHT_BANK_ID", "factory-plant-alpha")
    )

    model_choice = st.selectbox(
        "Groq Model",
        options=["llama-3.3-70b-versatile", "llama-3.1-8b-instant", "mixtral-8x7b-32768", "deepseek-r1-distill-llama-70b", "openai/gpt-oss-120b"],
        index=0,
        help="llama-3.3-70b-versatile is the recommended high-performance Groq model"
    )

    if st.button("💾 Save Keys to .env", use_container_width=True):
        env_file_path = os.path.join(os.path.dirname(__file__), ".env")
        with open(env_file_path, "w") as f:
            f.write(f"# Vectorize Hindsight API Key & Bank ID\n")
            f.write(f"HINDSIGHT_API_KEY={hindsight_key}\n")
            f.write(f"HINDSIGHT_BASE_URL=https://api.hindsight.vectorize.io\n")
            f.write(f"HINDSIGHT_BANK_ID={bank_id}\n\n")
            f.write(f"# Groq API Key\n")
            f.write(f"GROQ_API_KEY={groq_key}\n")
        st.success("✅ Keys permanently saved to .env!")

    st.divider()

    # One-click Memory Seeder
    st.subheader("🧠 Plant Memory Seeder")
    st.caption("Pre-load factory history & technician tribal knowledge into Hindsight:")
    if st.button("🚀 Seed Factory History", use_container_width=True):
        with st.spinner("Injecting historical machine logs into Hindsight memory bank..."):
            try:
                result = seed_factory_memory(api_key=hindsight_key if hindsight_key else "demo-local-key", bank_id=bank_id)
                st.success(f"✅ Factory memory successfully seeded! ({result.get('total_seeded', 0)} incidents loaded)")
                with st.expander("📋 View Recalled Historical Incidents", expanded=True):
                    for inc in result.get("incidents", []):
                        st.markdown(f"**🏭 {inc['machine_id']} (`{inc['error_code']}`)** — *{inc['technician']}*")
                        st.write(inc["text"])
                        st.caption(f"Tags: {', '.join(inc['tags'])}")
                        st.divider()
            except Exception as e:
                st.error(f"Seeding failed: {e}")

    st.divider()
    st.caption("💡 **Tip for Hackathon Demo**: Show Tab 1 side-by-side comparison to demonstrate how Hindsight transforms generic manual answers into expert shop-floor fixes!")

# Initialize Agent
agent = FactoryMaintenanceAgent(
    hindsight_api_key=hindsight_key,
    hindsight_bank_id=bank_id,
    groq_api_key=groq_key,
    llm_model=model_choice
)

# ----------------- MAIN INTERFACE -----------------
st.title("⚙️ Factory Maintenance Knowledge Agent")
st.markdown("**Long-Term Shop-Floor Memory powered by Vectorize Hindsight** — *Bridging OEM Manuals and Technician Tribal Knowledge*")

tab1, tab2, tab3, tab4 = st.tabs([
    "🔍 Diagnostic Assistant",
    "✍️ Log Field Fix (Retain)",
    "📋 Shift Handover (Reflect)",
    "🏭 Fleet & Memory Overview"
])

# ================= TAB 1: DIAGNOSTIC ASSISTANT =================
with tab1:
    st.subheader("Smart Equipment Troubleshooting")

    col_sel1, col_sel2 = st.columns(2)
    with col_sel1:
        machine_options = {m["id"]: f"{m['name']} ({m['id']})" for m in agent.get_machine_list()}
        selected_machine_id = st.selectbox("Select Equipment:", options=list(machine_options.keys()), format_func=lambda x: machine_options[x])

    machine_obj = agent.get_machine(selected_machine_id)
    error_choices = list(machine_obj.get("oem_manual", {}).keys()) if machine_obj else []

    with col_sel2:
        selected_code = st.selectbox("Reported Error Code:", options=error_choices)

    symptom_input = st.text_input(
        "Observed Symptoms / Operator Notes:",
        value="Machine stopped suddenly during heavy cycle. Loud whining sound and pressure gauge dropping below target." if selected_code == "E-402" else ""
    )

    compare_mode = st.toggle("🔥 Compare Side-by-Side: Without Memory vs With Hindsight Memory", value=True)

    if st.button("⚡ Run Intelligent Diagnostic", type="primary", use_container_width=True):
        if not groq_key:
            st.warning("⚠️ Please provide a Groq API key in the sidebar for AI generation.")

        with st.spinner("Querying OEM technical manuals and recalling Hindsight plant memory..."):
            if compare_mode:
                col_left, col_right = st.columns(2)

                with col_left:
                    st.markdown("### ❌ Baseline AI (No Memory)")
                    st.caption("Relies strictly on static OEM technical manual")
                    baseline_result = agent.diagnose_baseline_only(selected_machine_id, selected_code, symptom_input)
                    st.markdown(f'<div class="highlight-box">{baseline_result}</div>', unsafe_allow_html=True)

                with col_right:
                    st.markdown("### ✅ Hindsight Agent (With Memory)")
                    st.caption("Synthesizes OEM specs with accumulated shop-floor tribal fixes")
                    hindsight_result = agent.diagnose_with_hindsight(selected_machine_id, selected_code, symptom_input)
                    st.markdown(f'<div class="highlight-box">{hindsight_result["diagnosis"]}</div>', unsafe_allow_html=True)

                    if hindsight_result["memories"]:
                        with st.expander(f"🧠 Recalled {len(hindsight_result['memories'])} Hindsight Memory Items"):
                            for mem in hindsight_result["memories"]:
                                st.markdown(f"**Context:** {mem.get('context', 'Field Note')}")
                                st.write(mem.get("text", ""))
                                st.caption(f"Tags: {mem.get('tags', [])}")
                                st.divider()
            else:
                hindsight_result = agent.diagnose_with_hindsight(selected_machine_id, selected_code, symptom_input)
                st.markdown(f'<div class="highlight-box">{hindsight_result["diagnosis"]}</div>', unsafe_allow_html=True)
                if hindsight_result["memories"]:
                    with st.expander(f"🧠 View Recalled Memories ({len(hindsight_result['memories'])})"):
                        for mem in hindsight_result["memories"]:
                            st.markdown(f"**Context:** {mem.get('context', 'Field Note')}")
                            st.write(mem.get("text", ""))
                            st.divider()

# ================= TAB 2: LOG FIELD FIX (RETAIN) =================
with tab2:
    st.subheader("Capture Tribal Knowledge (Hindsight Retain)")
    st.markdown("When you resolve an issue, log what *actually worked*. The agent immediately commits this to **Hindsight memory**, making the entire plant smarter.")

    with st.form("log_fix_form"):
        col_f1, col_f2 = st.columns(2)
        with col_f1:
            log_machine = st.selectbox("Machine Repaired:", options=list(machine_options.keys()), format_func=lambda x: machine_options[x], key="log_mach")
            tech_name = st.text_input("Technician Name & Role:", value="Alex Rivera (Lead Millwright)")
            error_fixed = st.text_input("Error Code / Root Problem:", value="E-402")
        with col_f2:
            downtime = st.number_input("Total Downtime (Minutes):", min_value=5, max_value=2880, value=30)
            fix_description = st.text_area(
                "Actual Field Fix (What worked, what quirks did you find?):",
                placeholder="e.g. Instead of replacing pump, found solenoid valve connector was loose and cold oil clogged the filter mesh. Cleaned filter and tightened connector."
            )

        submit_fix = st.form_submit_button("💾 Commit Resolution to Hindsight Memory", type="primary")

    if submit_fix:
        if not fix_description:
            st.error("Please provide a description of the resolution.")
        elif not hindsight_key:
            st.error("Please enter a valid Hindsight API Key in the sidebar.")
        else:
            with st.spinner("Retaining experience into Hindsight memory bank..."):
                try:
                    res = agent.retain_plant_memory(
                        machine_id=log_machine,
                        error_code=error_fixed,
                        resolution=fix_description,
                        technician_name=tech_name,
                        downtime_mins=downtime
                    )
                    st.success("🎉 Resolution successfully committed to Hindsight!")
                    st.balloons()
                    st.info(f"**Memory Retained:** The agent now remembers Alex's fix for {log_machine}. Any technician asking about {error_fixed} in the future will receive this field-tested tip first!")
                except Exception as e:
                    st.error(f"Failed to retain memory: {e}")

# ================= TAB 3: SHIFT HANDOVER (REFLECT) =================
with tab3:
    st.subheader("Shift Handover & Chronic Issues (Hindsight Reflect)")
    st.markdown("Uses Hindsight's **`reflect()`** capability to analyze accumulated machine memories across the plant and synthesize actionable briefings for oncoming shifts.")

    col_h1, col_h2 = st.columns([1, 2])
    with col_h1:
        shift_select = st.selectbox("Select Shift:", ["Day Shift Handover", "Night Shift Handover", "Weekend Maintenance Review"])
        generate_handover = st.button("📊 Synthesize Handover Briefing", type="primary", use_container_width=True)

    with col_h2:
        if generate_handover:
            if not hindsight_key:
                st.error("Hindsight API key is required.")
            else:
                with st.spinner(f"Reflecting across plant memory for {shift_select}..."):
                    summary = agent.reflect_shift_handover(shift_name=shift_select)
                    st.markdown("### 📋 Executive Shift Briefing")
                    st.markdown(f'<div class="highlight-box">{summary}</div>', unsafe_allow_html=True)
        else:
            st.info("Click 'Synthesize Handover Briefing' to trigger Hindsight agentic reflection over past work orders and identify chronic issues.")

# ================= TAB 4: FLEET OVERVIEW =================
with tab4:
    st.subheader("Plant Machine Registry & OEM Manuals")
    for m in agent.get_machine_list():
        with st.expander(f"🏭 {m['name']} ({m['id']}) - {m['location']}"):
            st.write(f"**Model:** {m['model']} | **Installed:** {m['installation_year']} | **Status:** {m['status']}")
            st.markdown("#### OEM Error Specifications:")
            for code, oem in m.get("oem_manual", {}).items():
                st.markdown(f"- **`{code}` - {oem['title']}** (Criticality: `{oem['criticality']}`)")
                st.caption(f"OEM Diagnosis: {oem['oem_diagnosis']} | Procedure: {oem['oem_procedure']}")