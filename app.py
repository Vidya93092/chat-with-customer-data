import streamlit as st
from data_handler import load_excel
from ai_engine import ask_gemini

st.set_page_config(
    page_title="Pune Leads Chat", 
    page_icon="🏠", 
    layout="wide"
)

st.title("🏠 Chat with Pune Real Estate Leads")
st.caption("Ask anything about your customer data in plain English")

#sidebar
with st.sidebar:
    st.header("📁 Data File")
    uploaded_file = st.file_uploader(
        "Upload Excel file", 
        type=["xlsx", "xls"]
    )
    
    st.markdown("---")
    st.markdown("### 💡 Try these questions:")
    
    examples = [
        "How many customers have budget above 90 lakhs?",
        "List all customers in Kharadi",
        "Show all 2BHK customers",
        "What is the average budget?",
        "Which customers have Call Back status?",
        "List customers expecting to buy in 2026",
        "How many 3BHK leads do we have?",
        "Show customers in Aundh or Baner",
    ]
    
    for q in examples:
        if st.button(q, use_container_width=True):
            st.session_state.quick_q = q

#Load data
if uploaded_file:
    df = load_excel(uploaded_file)
    st.success(f"✅ Loaded {len(df)} customers")
else:
    try:
        df = load_excel("pune_real_estate_leads_updated.xlsx")
        st.info("📊 Using default data file")
    except:
        st.warning("Please upload your Excel file")
        st.stop()

# Data preview
with st.expander("📊 View Raw Data"):
    st.dataframe(df, use_container_width=True)
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Leads", len(df))
    col2.metric("Locations", df['Location'].nunique())
    budget_col = [c for c in df.columns if 'Budget' in c or 'budget' in c][0]
    col3.metric("Avg Budget", f"₹{int(df[budget_col].mean()):,}")

# Chat
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Handle sidebar button clicks
if "quick_q" in st.session_state:
    question = st.session_state.pop("quick_q")
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.markdown(question)
    with st.chat_message("assistant"):
        with st.spinner("Analyzing your data..."):
            answer = ask_gemini(question, df)
        st.markdown(answer)
    st.session_state.messages.append({"role": "assistant", "content": answer})
    st.rerun()

# Chat input
if question := st.chat_input("Ask about your Pune leads..."):
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.markdown(question)
    with st.chat_message("assistant"):
        with st.spinner("Analyzing your data..."):
            answer = ask_gemini(question, df)
        st.markdown(answer)
    st.session_state.messages.append({"role": "assistant", "content": answer})
    st.rerun()