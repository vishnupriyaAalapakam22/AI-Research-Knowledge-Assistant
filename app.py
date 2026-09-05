import streamlit as st
import tempfile
import os

from src.document_processor import extract_text_from_pdf
from src.research_assistant import (
    research_search,
    research_answer,
    summarize_document,
    compare_documents_for_research,
    synthesize_research
)
from src.document_ingestion import ingest_document
from src.vector_store import get_document_names


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="AI Research & Knowledge Assistant",
    page_icon="🔬",
    layout="wide"
)


# --------------------------------------------------
# TITLE
# --------------------------------------------------

st.title("🔬 AI Research & Knowledge Assistant")

st.write(
    "Upload research papers, search across documents, "
    "summarize papers, compare studies, and generate "
    "literature insights."
)


# --------------------------------------------------
# SIDEBAR — DOCUMENT UPLOAD
# --------------------------------------------------

st.sidebar.header("📚 Research Workspace")

uploaded_files = st.sidebar.file_uploader(
    "Upload research papers",
    type=["pdf"],
    accept_multiple_files=True
)


if uploaded_files:

    st.sidebar.success(
        f"{len(uploaded_files)} document(s) uploaded"
    )

    for uploaded_file in uploaded_files:

        temp_path = os.path.join(
            tempfile.gettempdir(),
            uploaded_file.name
        )

        with open(temp_path, "wb") as file:
            file.write(uploaded_file.getbuffer())

        try:

            number_of_chunks = ingest_document(
                temp_path,
                uploaded_file.name
            )

            st.sidebar.write(
                f"✅ {uploaded_file.name}"
            )

        except Exception as e:

            st.sidebar.error(
                f"Error processing {uploaded_file.name}: {e}"
            )
# --------------------------------------------------
# DOCUMENT SELECTION
# --------------------------------------------------

st.sidebar.subheader("📑 Documents in Workspace")

available_documents = get_document_names()

if available_documents:

    selected_documents = st.sidebar.multiselect(
        "Select documents to search",
        available_documents,
        default=available_documents
    )

else:

    selected_documents = []

    st.sidebar.info(
        "Upload research papers to create your workspace."
    )
# --------------------------------------------------
# RESEARCH WORKSPACE DASHBOARD
# --------------------------------------------------

st.sidebar.subheader("📊 Workspace Overview")

st.sidebar.metric(
    "📄 Documents",
    len(available_documents)
)    

# --------------------------------------------------
# MAIN TABS
# --------------------------------------------------

tab1, tab2, tab3, tab4, tab5 = st.tabs(
    [
        "🔎 Research Search",
        "📄 Summarize",
        "⚖️ Compare",
        "📚 Literature Synthesis",
        "💬 Research Chat"
    ]
)


# ==================================================
# TAB 1 — RESEARCH SEARCH
# ==================================================

with tab1:

    st.header("🔎 Semantic Research Search")

    st.write(
        "Search your research documents using meaning rather "
        "than exact keyword matching."
    )

    query = st.text_input(
        "Enter your research query",
        placeholder="Example: What is retrieval augmented generation?"
    )

    top_k = st.slider(
        "Number of sources",
        min_value=1,
        max_value=10,
        value=5
    )

    if st.button("Search Documents"):

        if not query:

            st.warning("Please enter a search query.")

        else:

            results = research_search(
                query,
                top_k,
                selected_documents
            )

            st.subheader("Research Sources")

            for i, result in enumerate(results, 1):

                with st.expander(
                    f"Source {i}: {result['document']} — Page {result['page']}"
                ):

                    st.write(result["text"])

                    st.caption(
                        f"Document: {result['document']} | "
                        f"Page: {result['page']} | "
                        f"Distance: {result['distance']:.4f}"
                    )


# ==================================================
# TAB 2 — SUMMARIZE
# ==================================================

with tab2:

    st.header("📄 Document Summarization")

    st.write(
        "Generate a structured research summary."
    )

    summary_file = st.file_uploader(
        "Upload a PDF to summarize",
        type=["pdf"],
        key="summary"
    )

    if summary_file:

        if st.button("Generate Summary"):

            temp_path = os.path.join(
                tempfile.gettempdir(),
                summary_file.name
            )

            with open(temp_path, "wb") as file:
                file.write(summary_file.getbuffer())

            pages = extract_text_from_pdf(
                temp_path
            )

            document_text = "\n\n".join(
                page["text"]
                for page in pages
            )

            with st.spinner("Generating summary..."):

                summary = summarize_document(
                    document_text
                )

            st.subheader("Research Summary")

            st.markdown(summary)


# ==================================================
# TAB 3 — COMPARE
# ==================================================

with tab3:

    st.header("⚖️ Research Paper Comparison")

    st.write(
        "Compare two research papers across methodology, "
        "datasets, findings, and limitations."
    )

    col1, col2 = st.columns(2)

    with col1:

        paper1 = st.file_uploader(
            "Upload Paper 1",
            type=["pdf"],
            key="paper1"
        )

    with col2:

        paper2 = st.file_uploader(
            "Upload Paper 2",
            type=["pdf"],
            key="paper2"
        )

    if paper1 and paper2:

        if st.button("Compare Papers"):

            temp1 = os.path.join(
                tempfile.gettempdir(),
                "paper1.pdf"
            )

            temp2 = os.path.join(
                tempfile.gettempdir(),
                "paper2.pdf"
            )

            with open(temp1, "wb") as file:
                file.write(paper1.getbuffer())

            with open(temp2, "wb") as file:
                file.write(paper2.getbuffer())

            pages1 = extract_text_from_pdf(temp1)

            pages2 = extract_text_from_pdf(temp2)

            document1 = "\n\n".join(
                page["text"]
                for page in pages1
            )

            document2 = "\n\n".join(
                page["text"]
                for page in pages2
            )

            with st.spinner("Comparing research papers..."):

                comparison = compare_documents_for_research(
                    document1,
                    document2
                )

            st.subheader("Research Comparison")

            st.markdown(comparison)


# ==================================================
# TAB 4 — LITERATURE SYNTHESIS
# ==================================================

with tab4:

    st.header("📚 Literature Synthesis")

    st.write(
        "Analyze multiple research papers together to "
        "identify common findings, differences, limitations, "
        "and research gaps."
    )

    synthesis_files = st.file_uploader(
        "Upload research papers",
        type=["pdf"],
        accept_multiple_files=True,
        key="synthesis"
    )

    if synthesis_files:

        st.info(
            f"{len(synthesis_files)} paper(s) selected."
        )

        if st.button("Generate Literature Synthesis"):

            documents = []

            for uploaded_file in synthesis_files:

                temp_path = os.path.join(
                    tempfile.gettempdir(),
                    uploaded_file.name
                )

                with open(temp_path, "wb") as file:
                    file.write(
                        uploaded_file.getbuffer()
                    )

                pages = extract_text_from_pdf(
                    temp_path
                )

                text = "\n\n".join(
                    page["text"]
                    for page in pages
                )

                documents.append(text)

            with st.spinner(
                "Analyzing research literature..."
            ):

                synthesis = synthesize_research(
                    documents
                )

            st.subheader("Literature Synthesis")

            st.markdown(synthesis)


# ==================================================
# TAB 5 — RESEARCH CHAT
# ==================================================

with tab5:

    st.header("💬 Research Chat")

    st.write(
        "Ask questions about the research documents "
        "in your workspace."
    )

    question = st.text_input(
        "Ask a research question",
        placeholder="Example: What methodology was used in the papers?"
    )

    if st.button("Ask Research Assistant"):

        if not question:

            st.warning(
                "Please enter a question."
            )

        else:

            with st.spinner(
                "Searching research documents..."
            ):

                answer, sources = research_answer(
                    question,
                    selected_documents=selected_documents
                )

            st.subheader("Answer")

            st.markdown(answer)

            st.subheader("📌 Sources")

            for i, source in enumerate(sources, 1):

                st.write(
                    f"[{i}]📄 {source['document']} "
                    f"— Page {source['page']}"
                )

                with st.expander("View source"):

                    st.write(
                        source["text"]
                    )