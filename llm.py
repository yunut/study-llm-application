from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_pinecone import PineconeVectorStore
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain.chains import create_history_aware_retriever
from langchain_core.prompts import MessagesPlaceholder
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain

from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

store = {}

def get_session_history(session_id: str) -> BaseChatMessageHistory:
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]

def get_retriever():
    embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
    index_name = "tax-markdown-index"
    database = PineconeVectorStore.from_existing_index(
        index_name=index_name,
        embedding=embeddings
    )
    retriever = database.as_retriever(search_kwargs={"k": 4})
    return retriever

def get_llm(model = "gpt-4o"):
    llm = ChatOpenAI(model=model)
    return llm

def get_rag_chain():
    llm = get_llm()
    retriever = get_retriever()
    contextualize_q_system_prompt = (
        "Given a chat history and the latest user question "
        "which might reference context in the chat history, "
        "formulate a standalone question which can be understood "
        "without the chat history. Do NOT answer the question, "
        "just reformulate it if needed and otherwise return it as is."
    )

    contextualize_q_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", contextualize_q_system_prompt),
            MessagesPlaceholder("chat_history"),
            ("human", "{input}"),
        ]
    )
    
    history_aware_retriever = create_history_aware_retriever(
        llm, retriever, contextualize_q_prompt
    )

    system_prompt = (
        "You are an assistant for question-answering tasks. "
        "Use the following pieces of retrieved context to answer "
        "the question. If you don't know the answer, say that you "
        "don't know. Use three sentences maximum and keep the "
        "answer concise."
        "\n\n"
        "{context}"
    )
    qa_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            MessagesPlaceholder("chat_history"),
            ("human", "{input}"),
        ]
    )
    question_answer_chain = create_stuff_documents_chain(llm, qa_prompt)

    rag_chain = create_retrieval_chain(history_aware_retriever, question_answer_chain)

    conversational_rag_chain = RunnableWithMessageHistory(
        rag_chain,
        get_session_history,
        input_messages_key="input",
        history_messages_key="chat_history",
        output_messages_key="answer"
    ).pick("answer")

    return conversational_rag_chain


def get_dictionary_chain():
    llm = get_llm()
    dictionary = ["사람을 나타내는 표현 -> 거주자"]

    prompt = ChatPromptTemplate.from_template(
        f"""
        사용자의 질문을 보고, 우리의 사전을 참고해서 사용자의 질문을 변경해 주세요
        만약 변경할 필요가 없다고 판단되면, 사용자의 질문을 변경하지 않아도 됩니다.
        사전: {dictionary}
        질문: {{question}}
    """
    )

    dictionary_chain = prompt | llm | StrOutputParser()
    return dictionary_chain

def get_ai_response(user_message):
    dictionary_chain = get_dictionary_chain()
    rag_chain = get_rag_chain()
    tax_chain = {"input": dictionary_chain} | rag_chain
    return tax_chain.stream(
        {"question": user_message},
        config = {"configurable": {"session_id": "123"}}
    ) 