import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage

model = ChatOpenAI(
    openai_api_base="https://api.deepseek.com/",
    openai_api_key=st.secrets["key"],
    model_name="deepseek-chat",
)

if "int2conv_count" not in st.session_state:
    st.session_state.int2conv_count = 0
if "int2messages" not in st.session_state:
    st.session_state.int2messages = []
if "int2conv_disabled" not in st.session_state:
    st.session_state.int2conv_disabled = False

if "int2conv_default" not in st.session_state:
    st.session_state.int2conv_default = True


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


st.header("Open Conversing")

st.write(
    "In this page, participants  conversed freely with the bot. We ensured that the discussion remained focused on the topic through posthoc checks. "
)

st.write(
    "Next, you have up to 5 chances to converse with AI. Please ask AI questions related to the topic."
)
## 显示聊天历史
for message in st.session_state.int2messages:
    if message["role"] == "system":
        continue
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if st.session_state.int2conv_default:
    st.session_state.int2conv_default = False
    st.session_state.int2messages.append(
        {
            "role": "system",
            "content": "你是一位转基因食品领域的专家，请用150-200词回答用户的相关问题。"
            + st.session_state.personalized_profile
            + "请针对你要面对的用户的特点进行个性化地回复。",
        }
    )


user_input = st.chat_input(
    f"You can chat {5-st.session_state.int2conv_count} round(s), please input...",
    disabled=st.session_state.int2conv_disabled,
)
if user_input:
    st.session_state.int2conv_count += 1
    if st.session_state.int2conv_count >= 5:
        st.session_state.int2conv_disabled = True
    with st.chat_message("user"):
        st.markdown(user_input)
    st.session_state.int2messages.append({"role": "user", "content": user_input})
    with st.chat_message("assistant"):
        response = st.write_stream(get_response(st.session_state.int2messages))
    st.session_state.int2messages.append({"role": "assistant", "content": response})
    st.rerun()
if st.session_state.int2conv_count >= 2:
    st.markdown(":blue-background[POST SURVEY HERE]")
