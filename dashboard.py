# dashboard.py - Simple Streamlit Dashboard (FIXED)

import streamlit as st
from openai import OpenAI
import sys
sys.path.append('src')
from tools.system_monitor import get_system_report

# Page config
st.set_page_config(page_title="AI PC Assistant", page_icon="🤖", layout="wide")

# Title
st.title("🤖 AI PC Health Assistant")
st.markdown("---")

# Initialize AI
@st.cache_resource
def get_ai():
    return OpenAI(
        base_url="http://localhost:1234/v1",
        api_key="not-needed"
    )

client = get_ai()

# Two columns
col1, col2 = st.columns(2)

with col1:
    st.header("💻 System Status")
    
    if st.button("🔄 Refresh", use_container_width=True):
        with st.spinner("Checking system..."):
            report = get_system_report()
            st.session_state['report'] = report
            st.success("✅ Report generated!")
    
    # Show report if available
    if 'report' in st.session_state:
        st.code(st.session_state['report'], language=None)

with col2:
    st.header("🧠 AI Analysis")
    
    if st.button("🔍 Analyze with AI", use_container_width=True):
        if 'report' not in st.session_state:
            st.warning("⚠️ Please refresh system status first!")
        else:
            with st.spinner("AI is thinking..."):
                # Combine instruction into user prompt
                prompt = f"""You are a PC health expert. Analyze this report briefly:

{st.session_state['report']}

Provide:
1. Status (Good/Warning/Critical)
2. Issues (if any)
3. One recommendation

Be concise."""

                response = client.chat.completions.create(
                    model="local-model",
                    messages=[
                        {"role": "user", "content": prompt}  # All in user message
                    ],
                    temperature=0.7,
                    max_tokens=200
                )
                
                analysis = response.choices[0].message.content
                st.info(analysis)

# Footer
st.markdown("---")
st.caption("🔌 Powered by LM Studio + Mistral 7B")
