
import streamlit as st
from agent import find_opportunities

st.set_page_config(
    page_title="Upnext AI Navigator",
    page_icon="🚀",
    layout="wide",
)

st.title("🚀 Upnext")
st.subheader("AI Opportunity Navigator for Students")

st.write(
    "Discover your next step. Explore hackathons, internships, "
    "open-source contributions and scholarships."
)

st.info(
    "Prototype mode: opportunities are illustrative demo data, "
    "not verified live listings."
)

with st.form("opportunity_form"):
    interests = st.text_input(
        "Your skills and interests",
        placeholder="Example: Python, coding, hackathon, GitHub",
    )

    submitted = st.form_submit_button("Find My Opportunities")

if submitted:
    if not interests.strip():
        st.warning("Please enter at least one skill or interest.")
    else:
        with st.spinner("Finding relevant opportunities..."):
            result = find_opportunities(interests)

        st.success("Your opportunity plan is ready!")
        st.markdown("### Your personalised results")
        st.text(result)

st.divider()
st.caption(
    "Built with Python, Streamlit and LangGraph. "
    "Match scores are keyword-based, not verified eligibility scores."
)
