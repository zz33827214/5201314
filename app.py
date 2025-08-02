import streamlit as st
import json
import os

DATA_FILE = 'data.json'

# 預設資料
default_data = {
    'fu_days': 0,
    'chen_days': 0,
    'chen_tasks': 0,
    'violation_count': 0
}

# 讀取資料
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    else:
        return default_data.copy()

# 儲存資料
def save_data():
    with open(DATA_FILE, 'w') as f:
        json.dump(st.session_state.data, f)

# 初始化 Session State
if 'data' not in st.session_state:
    st.session_state.data = load_data()
    st.session_state.page = 'main'

# 主頁
def main_page():
    st.title("今晚該回誰房間睡？💤")

    fu_days = st.session_state.data['fu_days']
    chen_days = st.session_state.data['chen_days']
    chen_tasks = st.session_state.data['chen_tasks']

    # 自動判斷房間
    if fu_days > chen_days:
        suggestion = "今晚該回：傅鼻鼻房間 🐻"
    elif chen_days > fu_days:
        suggestion = "今晚該回：陳龍龍房間 🐉"
    else:
        suggestion = "目前平手！雙方協調 💞"

    st.subheader(suggestion)

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("傅鼻鼻")
        st.write(f"總天數：{fu_days} 天")
        if st.button("進入傅鼻鼻頁面"):
            st.session_state.page = 'fu'
    with col2:
        st.subheader("陳龍龍")
        st.write(f"總天數：{chen_days} 天")
        st.write(f"需滿足條件數：{chen_tasks}")
        if st.button("進入陳龍龍頁面"):
            st.session_state.page = 'chen'

    # 重置按鈕
    with st.sidebar:
        st.subheader("⚙️ 系統操作")
        if st.button("🔄 重置所有紀錄"):
            st.session_state.data = default_data.copy()
            save_data()
            st.rerun()



    st.markdown("---")
    st.subheader("🏷️ 今晚房間協商與兌換機制")

    col3, col4 = st.columns(2)
    with col3:
        default_choice = st.radio("今晚誰**本來**要去誰房間？", ["傅鼻鼻 去 陳龍龍房間", "陳龍龍 去 傅鼻鼻房間"])
    with col4:
        exchange_who = st.radio("誰想要發動【兌換】，改為來自己房間？", ["無", "傅鼻鼻", "陳龍龍"])

    if exchange_who != "無":
        if exchange_who == "傅鼻鼻":
            if st.session_state.data['fu_days'] >= 1:
                if st.button("✅ 傅鼻鼻使用 1 天數兌換 陳龍龍過來"):
                    st.session_state.data['fu_days'] -= 1
                    save_data()
                    st.rerun()
                    st.success("傅鼻鼻成功兌換！陳龍龍今晚過來 🐉 ➜ 🐻")
            else:
                st.error("傅鼻鼻沒有足夠的天數可兌換 😢")
        elif exchange_who == "陳龍龍":
            if st.session_state.data['chen_days'] >= 1:
                if st.button("✅ 陳龍龍使用 1 天數兌換 傅鼻鼻過來"):
                    st.session_state.data['chen_days'] -= 1
                    save_data()
                    st.success("陳龍龍成功兌換！傅鼻鼻今晚過來 🐻 ➜ 🐉")
            else:
                st.error("陳龍龍沒有足夠的天數可兌換 😢")

# 陳龍龍頁面
def chen_page():
    st.title("🐉 陳龍龍的紀錄頁面")
    data = st.session_state.data

    if st.button("鼻鼻未達成每日喝一壺水 +1天"):
        data['chen_days'] += 1
        save_data()
        st.session_state.page = 'main'


    if st.button("未遵守留在陳龍龍房間 +1天（會累犯）"):
        data['chen_days'] += 1
        data['violation_count'] += 1
        if data['violation_count'] > 1:
                        st.warning("❗ 累犯！需滿足陳龍龍的一件事")
                        data['chen_tasks'] += 1
        save_data()
        st.session_state.page = 'main'


    if st.button("曠課並被登錄系統 +1天"):
        data['chen_days'] += 1
        save_data()
        st.session_state.page = 'main'


    if st.button("⬅️ 返回主頁"):
        st.session_state.page = 'main'

# 傅鼻鼻頁面
def fu_page():
    st.title("🐻 傅鼻鼻的紀錄頁面")
    data = st.session_state.data

    if st.button("咬一下 +1天"):
        data['fu_days'] += 1
        save_data()
        st.session_state.page = 'main'


    if st.button("小生氣 +1天"):
        data['fu_days'] += 1
        save_data()
        st.session_state.page = 'main'


    if st.button("講話破 +1天"):
        data['fu_days'] += 1
        save_data()
        st.session_state.page = 'main'


    if st.button("不聽話 +1天"):
        data['fu_days'] += 1
        save_data()
        st.session_state.page = 'main'


    if st.button("沒帶肉 +10天"):
        data['fu_days'] += 10
        save_data()
        st.session_state.page = 'main'


    if st.button("⬅️ 返回主頁"):
        st.session_state.page = 'main'

# 頁面導向邏輯控制
if st.session_state.page == 'main':
    main_page()
elif st.session_state.page == 'chen':
    chen_page()
elif st.session_state.page == 'fu':
    fu_page()




