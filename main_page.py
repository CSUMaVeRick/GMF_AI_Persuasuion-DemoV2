import streamlit as st
import pandas as pd


if "personalized_profile" not in st.session_state:
    st.session_state.personalized_profile = None

if "dem_gender" not in st.session_state:
    st.session_state.dem_gender = None
    st.session_state.dem_gender_others = None

if "dem_age" not in st.session_state:
    st.session_state.dem_age = None

if "dem_edu" not in st.session_state:
    st.session_state.dem_edu = None

if "ts_expert" not in st.session_state:
    st.session_state.ts_expert = None

if "ts_honest" not in st.session_state:
    st.session_state.ts_honest = None
if "pb" not in st.session_state:
    st.session_state.pb = None

# ItTypes = [None, "Limited topics", "Open topics", "Costello et al.(2024) like"]

## 页面变量设置
st.set_page_config(page_title="GM foods Survey-Demo", page_icon=":green_salad:")

## 隐藏 streamlit 默认的 menu
st.markdown(
    """
    <style>
        .reportview-container {
            margin-top: -2em;
        }
        #MainMenu {visibility: hidden;}
        .stAppDeployButton {display:none;}
        footer {visibility: hidden;}
        #stDecoration {display:none;}
        stSidebar {visibility: hidden;}
        div[data-testid="stMarkdownContainer"] {font-size: 12pt;}
        # div[data-testid="stSidebarContent"] {display: none;}
        # section[data-testid="stSidebar"] {display: none;}
        # div[data-testid="stSidebarCollapsedControl"] {display: none;}
    </style>
""",
    unsafe_allow_html=True,
)


# st.write(st.session_state.interaction_type)


def intro():
    st.title("GM foods Survey-Demo")
    # st.header("Different Interaction Designs")
    st.radio(
        "你认为自己是什么性别？",
        ["女性", "男性", "其他（请填写）", "不愿意透露"],
        key="dem_gender",
    )
    if st.session_state.dem_gender == "其他（请填写）":
        st.text_input("请填写您的性别：", None, key="dem_gender_others")
    st.number_input("你的年龄多大？", min_value=1, max_value=120, step=1, key="dem_age")
    st.radio(
        "你最高教育水平是什么？",
        [
            "初级教育",
            "中等教育（例如，高中）",
            "高等教育（例如，大学学位或高等教育文凭）",
            "没有上学",
        ],
        key="dem_edu",
    )
    st.write("在这项调查中，我们将向你提出有关科学和科学家的问题。")
    st.write(
        "当我们说“科学”时，我们指的是我们通过观察和测试对世界的理解。当我们说“科学家”时，我们指的是研究自然、医学、物理学、经济学、历史和心理学以及其他事物的人。"
    )
    st.write(
        "我们想知道您对贵国科学家的看法，包括在大学、政府、公司和非营利组织工作的科学家。"
    )
    st.segmented_control(
        "大多数科学家是专家还是非专家？",
        options=[
            "非常不专业",
            "有点不专业",
            "谈不上专业，也不算不专业",
            "比较专业",
            "非常专业",
        ],
        key="ts_expert",
        help="从非常不专业到非常专业",
    )
    st.select_slider(
        "大多数科学家的诚实或不诚实程度如何？",
        options=[
            "非常不诚实",
            "有点不诚实",
            "谈不上诚实，也不算不诚实",
            "比较诚实",
            "非常诚实",
        ],
        key="ts_honest",
    )
    st.write("我们想知道您对转基因食品的看法，包括原材料及加工品。")
    st.pills(
        "您对转基因食品的看法是？（多选）",
        ["不安全的", "不健康的", "不环保的", "不自然的", "不经济的"],
        selection_mode="multi",
        key="pb",
    )
    personalized_profile = f"你将面对的用户是一位{st.session_state.dem_age}岁受过{st.session_state.dem_edu}的{st.session_state.dem_gender}。"
    personalized_profile += (
        f"ta认为科学家是{st.session_state.ts_honest}和{st.session_state.ts_expert}的。"
    )
    personalized_profile += f"ta觉得转基因食品是{'、'.join(st.session_state.pb)}。"
    st.session_state.personalized_profile = personalized_profile
    st.divider()
    st.markdown(":blue-background[Personalized Profile]")
    st.write(personalized_profile)


intType1 = st.Page("limited.py", title="Limited Topics")
intType2 = st.Page("open.py", title="Open Conversing")
intType3 = st.Page("costello.py", title="Costello et al. Like")
pg = st.navigation([st.Page(intro, title="Homepage"), intType1, intType2, intType3])

pg.run()
