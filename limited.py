import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage

model = ChatOpenAI(
    openai_api_base="https://api.deepseek.com/",
    openai_api_key=st.secrets["key"],
    model_name="deepseek-chat",
)

if "int1topic" not in st.session_state:
    st.session_state.int1topic = None

if "int1topic_disabled" not in st.session_state:
    st.session_state.int1topic_disabled = False

if "int1topic_confirmed" not in st.session_state:
    st.session_state.int1topic_confirmed = False

if "int1conv_count" not in st.session_state:
    st.session_state.int1conv_count = 1
if "int1messages" not in st.session_state:
    st.session_state.int1messages = []
if "int1conv_disabled" not in st.session_state:
    st.session_state.int1conv_disabled = False

if "int1conv_default" not in st.session_state:
    st.session_state.int1conv_default = True


def stream_response(response):
    for chunk in response:
        yield chunk.content


def response_decorator(func):
    def wrapper(messages):
        return stream_response(func(messages))

    return wrapper


@response_decorator
def get_response(messages):
    return model.stream(messages)


def click_int1button():
    st.session_state.int1topic_confirmed = True
    st.session_state.int1topic = int1topic
    st.session_state.int1topic_disabled = True


st.header("Limited Topics")

st.write(
    "In this page, participants are required to choose a topic they interested to talk about from our given list."
)

int1topic = st.radio(
    "Which of the following issues about GM foods are you most interested in?",
    ["Safety", "Environmental Impact", "Economic Value", "Scientific Principles"],
    captions=[
        "Are GM foods safe to me?",
        "Are GM foods harmful to environment?",
        "Will GM foods reduce my life cost?",
        "What is the principle of GM foods?",
    ],
    disabled=st.session_state.int1topic_disabled,
)

st.button("Confirm", on_click=click_int1button)


if st.session_state.int1topic_confirmed:
    st.markdown(f"The topic you concerned is **{st.session_state.int1topic}**.")

    st.write(
        "Next, you have up to 5 chances to converse with AI. Please ask AI questions related to the topic."
    )
    ## 显示聊天历史
    for message in st.session_state.int1messages:
        if message["role"] == "system":
            continue
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if st.session_state.int1conv_default:
        st.session_state.int1conv_default = False
        with st.chat_message("user"):
            init_input = f"Hello, I want know something about **Genetic Modified Foods' {st.session_state.int1topic}**."
            st.markdown(init_input)
        st.session_state.int1messages.append(
            {
                "role": "system",
                "content": "你是一位转基因食品领域的专家，请用150-200词回答用户的相关问题。"
                + st.session_state.personalized_profile
                + "请针对你要面对的用户的特点进行个性化地回复。",
            }
        )
        st.session_state.int1messages.append({"role": "user", "content": init_input})
        with st.chat_message("assistant"):
            response = st.write_stream(get_response(st.session_state.int1messages))
        st.session_state.int1messages.append({"role": "assistant", "content": response})
        st.rerun()

    user_input = st.chat_input(
        f"You can chat {5-st.session_state.int1conv_count} round(s), please input...",
        disabled=st.session_state.int1conv_disabled,
    )
    if user_input:
        st.session_state.int1conv_count += 1
        if st.session_state.int1conv_count >= 5:
            st.session_state.int1conv_disabled = True
        with st.chat_message("user"):
            st.markdown(user_input)
        st.session_state.int1messages.append({"role": "user", "content": user_input})
        with st.chat_message("assistant"):
            response = st.write_stream(get_response(st.session_state.int1messages))
        st.session_state.int1messages.append({"role": "assistant", "content": response})
        st.rerun()
    if st.session_state.int1conv_count >= 2:
        st.markdown(":blue-background[POST SURVEY HERE]")
