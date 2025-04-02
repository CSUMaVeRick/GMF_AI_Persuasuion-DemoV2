import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage

model = ChatOpenAI(
    openai_api_base="https://api.deepseek.com/",
    openai_api_key=st.secrets["key"],
    model_name="deepseek-chat",
)


if "int3text_disabled" not in st.session_state:
    st.session_state.int3text_disabled = False

if "int3text_confirmed" not in st.session_state:
    st.session_state.int3text_confirmed = False

if "int3conv_count" not in st.session_state:
    st.session_state.int3conv_count = 1
if "int3messages" not in st.session_state:
    st.session_state.int3messages = []
if "int3conv_disabled" not in st.session_state:
    st.session_state.int3conv_disabled = False

if "int3conv_default" not in st.session_state:
    st.session_state.int3conv_default = True

if "int3text_processed" not in st.session_state:
    st.session_state.int3text_processed = ""


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


def click_int3button():
    st.session_state.int3text_confirmed = True
    st.session_state.int3text_disabled = True


st.header("Limited Topics")

st.write(st.session_state.personalized_profile)

st.write(
    "Here, participants are required to report concerned issue about GM foods. And then we use AI to summarize it."
)

int3text = st.text_input(
    "Could you tell us what you concerned about GM foods?",
    "Please input...",
    disabled=st.session_state.int3text_disabled,
)

st.button("Confirm", on_click=click_int3button)
st.write(f"What you are curious about is:{st.session_state.int3text_processed}")
if st.session_state.int3text_confirmed:
    for message in st.session_state.int3messages:
        if message["role"] == "system":
            continue
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    if st.session_state.int3conv_default:
        st.session_state.int3conv_default = False
        processed_text = model.invoke(
            [
                {
                    "role": "system",
                    "content": "You are an expert in proofreading. Please summarize the expression to one condensed sentence. ANSWER ONLY.",
                },
                {"role": "user", "content": int3text},
            ]
        ).content
        st.session_state.int3text_processed = processed_text
        with st.chat_message("user"):
            init_input = f"Hello, I want know something about **Genetic Modified Foods', like {st.session_state.int3text_processed}**."
            st.markdown(init_input)
        st.session_state.int3messages.append(
            {
                "role": "system",
                "content": "你是一位转基因食品领域的专家，请用150-200词回答用户的相关问题。"
                + st.session_state.personalized_profile
                + "请针对你要面对的用户的特点进行个性化地回复。",
            }
        )
        st.session_state.int3messages.append({"role": "user", "content": init_input})
        with st.chat_message("assistant"):
            response = st.write_stream(get_response(st.session_state.int3messages))
        st.session_state.int3messages.append({"role": "assistant", "content": response})
        st.rerun()
    user_input = st.chat_input(
        f"You can chat {5-st.session_state.int3conv_count} round(s), please input...",
        disabled=st.session_state.int3conv_disabled,
    )
    if user_input:
        st.session_state.int3conv_count += 1
        if st.session_state.int3conv_count >= 5:
            st.session_state.int3conv_disabled = True
        with st.chat_message("user"):
            st.markdown(user_input)
        st.session_state.int3messages.append({"role": "user", "content": user_input})
        with st.chat_message("assistant"):
            response = st.write_stream(get_response(st.session_state.int3messages))
        st.session_state.int3messages.append({"role": "assistant", "content": response})
        st.rerun()
    if st.session_state.int3conv_count >= 2:
        st.markdown(":blue-background[POST SURVEY HERE]")
