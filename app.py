import streamlit as st
import json
from mapping import AdaptiveTaxonomyMapper

st.set_page_config(
    page_title="Taxonomy Mapper",
    page_icon="📚",
    layout="centered"
)

st.title("Adaptive Taxonomy Mapper")
st.caption("Using rag to map stoies to an internal taxonomy ")
st.caption("By Lokesh D")

@st.cache_resource
def load_mapper():
    return AdaptiveTaxonomyMapper()

mapper = load_mapper()

st.subheader("Input Story Details")

tags_input = st.text_input(
    "User Tags (comma-separated)",
    placeholder="Love, Action, Scary"
)

story_input = st.text_area(
    "Story / Description",
    height=180,
    placeholder="Enter the story snippet here..."
)

if st.button("Map to Taxonomy"):
    if not story_input.strip():
        st.warning("Please enter a story description.")
    else:
        tags = [t.strip() for t in tags_input.split(",") if t.strip()]

        with st.spinner("Analyzing story context..."):
            result = mapper.map_story(tags, story_input)

        st.subheader(" Mapping Result")

        col1, col2 = st.columns(2)
        col1.metric("Genre", result["genre"])
        col2.metric("Subgenre", result["subgenre"])

        st.markdown("### Reasoning")
        st.write(result["reasoning"])

        with st.expander("View raw JSON output"):
            st.json(result)

st.markdown("---")

