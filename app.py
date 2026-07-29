import os
import streamlit as st
from langchain_text_splitters import MarkdownHeaderTextSplitter, RecursiveCharacterTextSplitter
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_community.vectorstores import FAISS

# Set up clean page layout
st.set_page_config(page_title="Documentation RAG Assistant", page_icon="🤖")
st.title("🤖 Data Center Analytics Chatbot")
st.caption("Optimized for accuracy with Qwen 2.5 (1.5B) & Precision Markdown Splitting")

# 1. Initialize RAG Chain with Caching
@st.cache_resource
def initialize_rag_chain():
    os.chdir(r"C:\Users\jfxia\AI Projects\Chatbot")
    
    if not os.path.exists("Documentation.md"):
        st.error("Could not find Documentation.md file.")
        st.stop()
        
    with open("Documentation.md", "r", encoding="utf-8") as f:
        raw_text = f.read()

    # MATCHED TO YOUR EXACT FORMAT: Splitting logically by your main sections and item sub-headers
    headers_to_split_on = [
        ("###", "Main Section"),
        ("#####", "Sub Item")
    ]
    markdown_splitter = MarkdownHeaderTextSplitter(headers_to_split_on=headers_to_split_on)
    md_header_splits = markdown_splitter.split_text(raw_text)

    # Sub-split long blocks cleanly while preserving header metadata
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1200, chunk_overlap=150)
    splits = text_splitter.split_documents(md_header_splits)

    # Core AI and vector store linking
    # embeddings = OllamaEmbeddings(model="nomic-embed-text", base_url="http://127.0.0.1:11434")
    # db = FAISS.from_documents(splits, embeddings)
    
    # 1.5B model for high-speed technical reasoning
    # llm = OllamaLLM(model="qwen2.5:1.5b", base_url="http://127.0.0.1:11434")

    # New Cloud Version
    from langchain_groq import ChatGroq
    from langchain_community.embeddings import HuggingFaceEmbeddings

    # Free, serverless embeddings that run completely inside the cloud container
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    db = FAISS.from_documents(splits, embeddings)

    # Connects to high-speed model on Groq's servers using your hidden API Key
    api_key = st.secrets["GROQ_API_KEY"]
    llm = ChatGroq(model="qwen2.5:1.5b", groq_api_key=api_key)

    system_prompt = (
        "You are an expert technical documentation assistant.\n"
        "Analyze the provided context thoroughly to answer the user's question accurately.\n"
        "Provide direct, factual answers. Do not make assumptions or infer things outside the context.\n"
        "If the context does not contain the answer, say 'I cannot find that information in the document.'\n\n"
        "Context:\n{context}"
    )
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "{question}"),
    ])

    def format_docs(documents):
        return "\n\n".join(doc.page_content for doc in documents)

    # Compile the final chain pipeline
    chain = (
        {"context": RunnablePassthrough(), "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    return chain, db

try:
    rag_chain, vector_db = initialize_rag_chain()
except Exception as e:
    st.error(f"Failed to connect to Ollama. Make sure the app is running! Error: {e}")
    st.stop()

# 2. ULTRA-COMPACT SIDEBAR WITH PORTFOLIO SIGNATURE
with st.sidebar:
    st.markdown("<h3 style='margin: 5px 0px 5px 0px; padding: 0px;'>ℹ️ Project Info</h3>", unsafe_allow_html=True)
    
    with st.expander("🔍 Read Detailed Overview", expanded=False):
        st.markdown(
            "This interactive **Retrieval-Augmented Generation (RAG)** chatbot "
            "acts as an intelligent assistant for specialized internal project documentation.\n\n"
            "**How It Works:**\n"
            "1. **Parsing:** Reads a local raw markdown file.\n"
            "2. **Vector Search:** Converts text chunks into vectors using `nomic-embed-text`.\n"
            "3. **Inference:** Queries Meta's `Qwen 2.5 (1.5B)` model via **Ollama** completely offline."
        )
    
    st.markdown(
        "<div style='margin-top: 5px; margin-bottom: 5px; padding: 0px; font-size: 14px; line-height: 1.3;'>"
        "<strong>Tech Stack:</strong><br>"
        "• Parsing: Markdown Header Splits<br>"
        "• Vectors: <code>nomic-embed-text</code><br>"
        "• LLM: <code>Qwen 2.5 (1.5B)</code> via Ollama<br><br>"
        "<strong>💡 Sample Prompt:</strong><br>"
        "<em>'Summarize the AI involvement'</em>"
        "</div>", 
        unsafe_allow_html=True
    )
    
    st.markdown("<hr style='margin: 8px 0px 8px 0px; padding: 0px; border: none; border-top: 1px solid #ccc;'/>", unsafe_allow_html=True)
    st.markdown("<h3 style='margin: 5px 0px 5px 0px; padding: 0px;'>⚙️ Controls</h3>", unsafe_allow_html=True)
    
    num_chunks = st.slider("Search Depth (k chunks)", min_value=1, max_value=7, value=4)
    
    st.markdown("<hr style='margin: 8px 0px 8px 0px; padding: 0px; border: none; border-top: 1px solid #ccc;'/>", unsafe_allow_html=True)
    
    if st.button("🗑️ Clear Chat History", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    # ==================== PORTFOLIO BRANDING FOOTER ====================
    st.markdown("<hr style='margin: 15px 0px 8px 0px; padding: 0px; border: none; border-top: 1px solid #ccc;'/>", unsafe_allow_html=True)
    st.markdown(
        "<div style='text-align: center; font-size: 12px; color: #777; margin-top: 5px;'>\n"
        "Built by <a href='https://github.com' target='_blank' style='text-decoration: none; color: #000000; font-weight: bold;'>Jingfeng Xia</a>"
        "</div>",
        unsafe_allow_html=True
    )

# Dynamic retriever generation based on user sidebar selection
retriever = vector_db.as_retriever(search_kwargs={"k": num_chunks})

# 3. Track and display conversation history
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 4. Handle user input with text streaming
if user_query := st.chat_input("Ask your chatbot something..."):
    with st.chat_message("user"):
        st.markdown(user_query)
    st.session_state.messages.append({"role": "user", "content": user_query})

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        message_placeholder.markdown("🤖 *Thinking and reading documents...*")
        
        retrieved_docs = retriever.invoke(user_query)
        context_str = "\n\n".join(doc.page_content for doc in retrieved_docs)
        
        full_response = ""
        try:
            for chunk in rag_chain.stream({"context": context_str, "question": user_query}):
                full_response += chunk
                message_placeholder.markdown(full_response + "▌")
                
            message_placeholder.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            
        except Exception as e:
            st.error(f"An error occurred: {e}")
