import streamlit as st
from research_critic import executor

st.set_page_config(page_title="Scientific Critic AI", layout="wide")

st.title("🔬 Multi-Agent Scientific Research Critic")
st.markdown("Identify methodological flaws and missing baselines using CoT agents.")

uploaded_file = st.file_uploader("Upload a Research Paper (PDF)", type="pdf")

if uploaded_file:
    with st.status("Agents are analyzing...", expanded=True) as status:
        st.write("🤖 Agent A: Extracting Claims & LaTeX...")
        # Save file and run graph
        results = executor.invoke({"pdf_text": "Sample content..."})
        
        st.write("📚 Agent B: Searching 2024/2025 Baselines...")
        st.write("⚖️ Agent C: Evaluating Statistical Significance...")
        status.update(label="Analysis Complete!", state="complete")

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Extracted Equations")
        for eq in results['equations']:
            st.latex(eq) # Native Streamlit LaTeX support
            
    with col2:
        st.subheader("Scholar Findings")
        st.write(results['baselines'])

    st.divider()
    st.subheader("Final Methodological Critique")
    st.info(results['critique'])
