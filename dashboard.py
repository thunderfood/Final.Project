# dashboard_v2.py - Enhanced Dashboard with Tabs and History

import streamlit as st
from openai import OpenAI
import sys
sys.path.append('src')

from tools.system_monitor import get_system_report
from tools.storage import Storage
from config import Config

# Page config
st.set_page_config(
    page_title="AI PC Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        margin-bottom: 1rem;
    }
    .stButton>button {
        width: 100%;
    }
</style>
""", unsafe_allow_html=True)

# Initialize AI client
@st.cache_resource
def get_ai():
    return OpenAI(
        base_url=Config.LLM_BASE_URL,
        api_key="not-needed"
    )

client = get_ai()

# Initialize storage
@st.cache_resource
def get_storage():
    return Storage()

storage = get_storage()

# Sidebar
with st.sidebar:
    st.header("⚙️ Settings")
    
    st.subheader("🖥️ System")
    st.metric("LLM Status", "🟢 Connected")
    st.caption(f"URL: {Config.LLM_BASE_URL}")
    
    st.markdown("---")
    
    st.subheader("📧 Email")
    email_configured = Config.is_email_configured()
    
    if email_configured:
        st.success("✅ Configured")
        st.caption(f"📬 {Config.EMAIL_ADDRESS}")
    else:
        st.warning("⚠️ Not configured")
        with st.expander("How to configure"):
            st.markdown("""
            1. Create `.env` file in project root
            2. Add your email credentials:
```
            EMAIL_ADDRESS=your@email.com
            EMAIL_PASSWORD=your-app-password
```
            3. Restart dashboard
            """)
    
    st.markdown("---")
    
    st.subheader("📊 Statistics")
    history = storage.load_history()
    st.metric("Total Checks", len(history))
    
    if st.button("🗑️ Clear All History"):
        storage.clear_history()
        st.success("✅ History cleared!")
        st.rerun()
    
    st.markdown("---")
    st.caption("🤖 AI PC Assistant v2.0")
    st.caption("Built with LM Studio + Mistral")

# Main header
st.markdown('<p class="main-header">🤖 AI PC Health Assistant</p>', unsafe_allow_html=True)
st.markdown("Monitor your PC health and get AI-powered recommendations")
st.markdown("---")

# Create tabs
tab1, tab2, tab3 = st.tabs(["💻 System Health", "📊 History", "ℹ️ About"])

# ============================================================
# TAB 1: SYSTEM HEALTH
# ============================================================
with tab1:
    col1, col2 = st.columns([1, 1])
    
    # LEFT COLUMN: System Status
    with col1:
        st.subheader("📊 Current Status")
        
        if st.button("🔄 Check System Now", key="check_btn"):
            with st.spinner("Checking system health..."):
                report = get_system_report()
                st.session_state['current_report'] = report
                st.success("✅ System check complete!")
        
        # Display report if available
        if 'current_report' in st.session_state:
            st.code(st.session_state['current_report'], language=None)
        else:
            st.info("👆 Click 'Check System Now' to see your PC health")
    
    # RIGHT COLUMN: AI Analysis
    with col2:
        st.subheader("🧠 AI Analysis")
        
        if st.button("🔍 Get AI Recommendation", key="analyze_btn"):
            if 'current_report' not in st.session_state:
                st.warning("⚠️ Please check system first!")
            else:
                with st.spinner("AI is analyzing your system..."):
                    prompt = f"""Analyze this PC health report and provide recommendations:

{st.session_state['current_report']}

Please provide:
1. **Status**: Good/Warning/Critical (one word)
2. **Issues**: List any problems found (or "None")
3. **Recommendation**: One specific action to take

Be concise and actionable."""

                    try:
                        response = client.chat.completions.create(
                            model="local-model",
                            messages=[{"role": "user", "content": prompt}],
                            temperature=0.7,
                            max_tokens=250
                        )
                        
                        analysis = response.choices[0].message.content
                        
                        # Display analysis
                        st.markdown("### 📋 Analysis Result")
                        st.info(analysis)
                        
                        # Save to history
                        storage.save_analysis(
                            "system",
                            st.session_state['current_report'],
                            analysis
                        )
                        st.success("💾 Saved to history!")
                        
                    except Exception as e:
                        st.error(f"❌ Error: {e}")
                        st.info("Make sure LM Studio server is running!")
        
        # Show placeholder if no report yet
        if 'current_report' not in st.session_state:
            st.info("👈 Check system first, then get AI analysis")

# ============================================================
# TAB 2: HISTORY
# ============================================================
with tab2:
    st.subheader("📊 Analysis History")
    
    # Load history
    history = storage.load_history()
    
    if history:
        st.info(f"📝 Total checks performed: **{len(history)}**")
        
        # Show most recent first
        for i, entry in enumerate(reversed(history)):
            timestamp = entry.get('timestamp', 'Unknown time')
            analysis_type = entry.get('type', 'system').title()
            
            with st.expander(f"🔍 {analysis_type} Check - {timestamp}", expanded=(i==0)):
                # Show report
                st.markdown("**System Report:**")
                st.code(entry.get('report', 'No report'), language=None)
                
                # Show analysis
                st.markdown("**AI Analysis:**")
                st.info(entry.get('analysis', 'No analysis'))
                
                # Add separator
                if i < len(history) - 1:
                    st.markdown("---")
    else:
        st.warning("📭 No history yet!")
        st.markdown("""
        History will appear here after you:
        1. Check your system health
        2. Get AI analysis
        3. Results are automatically saved
        """)
        
        # Show sample
        with st.expander("📖 See example"):
            st.code("""PC Health Report - 2025-01-15 16:30:00

CPU Usage: 25.0%
Memory: 8.5 GB / 16.0 GB (53.1%)
Disk: 450.0 GB / 512.0 GB (87.9%)""")
            
            st.info("""**Status**: Warning
**Issues**: High disk usage at 87.9%
**Recommendation**: Free up disk space by removing temporary files""")

# ============================================================
# TAB 3: ABOUT
# ============================================================
with tab3:
    st.subheader("ℹ️ About This Project")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### 🎯 Features
        - ✅ Real-time system monitoring
        - ✅ AI-powered health analysis
        - ✅ Local LLM (privacy-first)
        - ✅ Analysis history tracking
        - ✅ Zero cloud dependency
        
        ### 🛠️ Technology Stack
        - **LLM**: Mistral 7B (via LM Studio)
        - **Backend**: Python + psutil
        - **Frontend**: Streamlit
        - **Storage**: JSON files
        - **Privacy**: 100% local processing
        """)
    
    with col2:
        st.markdown("""
        ### 📚 How to Use
        
        **Step 1**: Check System
        - Go to "System Health" tab
        - Click "Check System Now"
        
        **Step 2**: Get AI Analysis
        - Review the system report
        - Click "Get AI Recommendation"
        - AI will analyze and suggest actions
        
        **Step 3**: View History
        - Go to "History" tab
        - See all past analyses
        - Track improvements over time
        
        ### 🔧 Configuration
        Settings can be modified in:
        - `.env` file (email, intervals)
        - `src/config.py` (defaults)
        """)
    
    st.markdown("---")
    
    st.markdown("""
    ### 👥 Team Project
    This is a B.Tech final year project demonstrating:
    - Local AI deployment
    - Privacy-preserving analysis
    - Professional PC maintenance tools
    
    ### 📞 Need Help?
    - Check that LM Studio server is running
    - Ensure model is loaded in LM Studio
    - Check sidebar for connection status
    """)

# Footer
st.markdown("---")
col1, col2, col3 = st.columns(3)
with col1:
    st.caption("🔌 Connected to LM Studio")
with col2:
    st.caption("💾 Data stored locally")
with col3:
    st.caption("🔒 100% private")
