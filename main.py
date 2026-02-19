import streamlit as st
import pandas as pd
from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from vector import retriever 

# --- 1. UI CONFIGURATION ---
st.set_page_config(
    page_title="Ex-Rate WALL-E | USD-INR Analyst", 
    page_icon="💹", 
    layout="wide"
)

# --- 2. SESSION STATE INITIALIZATION ---
if "messages" not in st.session_state:
    st.session_state.messages = []
if "auto_submit" not in st.session_state:
    st.session_state.auto_submit = None

# --- 3. CUSTOM CSS & TICKER ---
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; }
    section[data-testid="stSidebar"] { background-color: #161b22; border-right: 1px solid #30363d; }
    [data-testid="stMetricValue"] { font-family: 'Courier New', monospace; color: #58a6ff; }
    @keyframes ticker { 0% { transform: translateX(100%); } 100% { transform: translateX(-100%); } }
    .ticker-wrap { width: 100%; overflow: hidden; background: #1f2937; color: #10b981; padding: 8px 0; font-family: monospace; border-bottom: 1px solid #30363d; }
    .ticker-move { display: inline-block; white-space: nowrap; animation: ticker 30s linear infinite; }
    
    /* Style for the suggestion chips */
    .suggestion-header { color: #8b949e; font-size: 14px; margin-bottom: 10px; }
    </style>
    <div class="ticker-wrap"><div class="ticker-move">
        USD/INR: 91.0364 (+0.4154) • Market Status: OPEN • Historical Archive: 2016 - 2026
    </div></div>
    """, unsafe_allow_html=True)

# --- 4. LLM SETUP ---
@st.cache_resource
def get_chain():
    model = OllamaLLM(model="gemma3:latest", temperature=0.1)
    template = """
    ### 📊 FX Analysis Report
    {records}
    
    *Analyst Note:* [Provide a professional economic explanation for {question}]

    ---
    **What would you like to explore next?**
    """
    return ChatPromptTemplate.from_template(template) | model

chain = get_chain()

# --- 5. SIDEBAR ---
suggestions = ["2016", "2017", "2018", "2019", "2020", "2021", "2022", "2023", "2024", "2025", "2026"]

with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2489/2489756.png", width=80)
    st.title("FX Control Panel")
    
    st.markdown("### 🔍 Quick Autofill")
    # Callback to handle selectbox selection
    def side_callback():
        if st.session_state.side_val:
            st.session_state.auto_submit = st.session_state.side_val
            
    st.selectbox("Select a year:", options=[None] + suggestions, 
                 key="side_val", on_change=side_callback)
    
    st.markdown("---")
    st.metric(label="Base", value="USD")
    st.metric(label="Quote", value="INR")
    if st.button("Clear Conversation"):
        st.session_state.messages = []
        st.session_state.auto_submit = None
        st.rerun()

# --- 6. MAIN HEADER ---
col1, col2 = st.columns([1, 5])
with col1:
    st.image("https://cdn-icons-png.flaticon.com/512/2108/2108625.png", width=70)
with col2:
    st.title("Ex-Rate WALL-E")
    st.caption("AI-Powered Foreign Exchange Historical Analyst")

st.markdown("---")

# --- 7. CENTRAL ANALYSIS FUNCTION ---
def execute_analysis(query):
    # Add User Message
    st.session_state.messages.append({"role": "user", "content": query})
    with st.chat_message("user"):
        st.markdown(query)

    # Generate Assistant Response
    with st.chat_message("assistant"):
        with st.status("🔍 Scanning Ledger...", expanded=True) as status:
            records = retriever.invoke(query)
            
            # Prep Chart Data
            chart_data = []
            for doc in records:
                chart_data.append({
                    "Date": pd.to_datetime(doc.metadata.get("date"), dayfirst=True),
                    "Rate": float(doc.metadata.get("rate", 0))
                })
            df_plot = pd.DataFrame(chart_data).sort_values("Date").set_index("Date")
            
            # Get AI Response
            response = chain.invoke({"records": [d.page_content for d in records], "question": query})
            status.update(label="Analysis Complete", state="complete", expanded=False)
            
        st.markdown(response)
        if not df_plot.empty:
            with st.expander("📈 View Trend Chart", expanded=True):
                st.line_chart(df_plot, y="Rate", color="#58a6ff")

    # Save to history
    st.session_state.messages.append({"role": "assistant", "content": response})

# --- 8. RENDER CONVERSATION ---
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 9. DYNAMIC SUGGESTIONS (The "Next Prompt" Feature) ---
# We show these only if the last message was from the assistant
if st.session_state.messages and st.session_state.messages[-1]["role"] == "assistant":
    st.markdown('<p class="suggestion-header">💡 Suggested next prompts:</p>', unsafe_allow_html=True)
    
    # Create 3 clickable suggestion buttons
    c1, c2, c3 = st.columns(3)
    
    if c1.button("📉 Analyze 2020 Volatility"):
        st.session_state.auto_submit = "Tell me about the volatility in 2020"
        st.rerun()
        
    if c2.button("🚀 Compare with 2026"):
        st.session_state.auto_submit = "Compare current trends with 2026 data"
        st.rerun()
        
    if c3.button("💎 Show Peak Exchange Rate"):
        st.session_state.auto_submit = "What was the highest INR rate in the ledger?"
        st.rerun()

# --- 10. INPUT HANDLERS (Pinned to bottom) ---
if st.session_state.auto_submit:
    target = st.session_state.auto_submit
    st.session_state.auto_submit = None # Reset
    execute_analysis(target)

prompt = st.chat_input("Ask a follow-up or type your own question...")
if prompt:
    execute_analysis(prompt)