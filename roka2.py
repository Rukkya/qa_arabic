import streamlit as st
import requests

# Set page config
st.set_page_config(page_title="Shoe Store", page_icon="👟")

# Store chat history in session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "show_chat_window" not in st.session_state:
    st.session_state.show_chat_window = False

# Function to handle chatbot responses
def send_message(user_message):
    try:
        response = requests.post("http://127.0.0.1:5006/get_answer", json={"question": user_message})
        if response.status_code == 200:
            data = response.json()
            return data.get('answer', 'عذرًا، لم أتمكن من إيجاد إجابة على سؤالك.')
        else:
            return "حدث خطأ، يرجى المحاولة لاحقًا."
    except Exception:
        return "حدث خطأ في الاتصال بالخادم."

# Function to generate message styles
def get_message_style(message_text, role):
    message_length = len(message_text) * 10
    max_width = 400
    width = min(max(100, message_length), max_width)

    if role == "user":
        return f"background-color: #D3D3D3; padding: 10px; border-radius: 10px; text-align: left; width: {width}px;"
    else:
        return f"background-color: #ADD8E6; padding: 10px; border-radius: 10px; text-align: right; width: {width}px;"

# Header & Welcome Message
st.title("👟 مرحبًا بك في متجر الأحذية")
st.markdown("### Hello to store")
st.image("https://www.google.com/url?sa=i&url=https%3A%2F%2Frunkeeper.com%2Fcms%2Fhealth%2Fwhy-you-should-rotate-your-running-shoes%2F&psig=AOvVaw2KdAXFaOoJunGBxO1uDFVS&ust=1738712715637000&source=images&cd=vfe&opi=89978449&ved=0CBQQjRxqFwoTCPj9toXZqIsDFQAAAAAdAAAAABAh", use_container_width=True)

# Display Products
st.header("🛒 الأحذية المميزة")
col1, col2, col3 = st.columns(3)

with col1:
    st.image("https://baccabucci.com/cdn/shop/products/MG_5242.jpg?v=1633514122")
    st.write("حذاء رياضي مريح")
    st.button("🛍 شراء الآن", key="p1")
with col2:
    st.image("https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTmi6vNrTQ5vd755AEqcWMim9hbz_gHgfMBZg&s")
    st.write("حذاء جري خفيف")
    st.button("🛍 شراء الآن", key="p2")
with col3:
    st.image("https://5.imimg.com/data5/SELLER/Default/2022/11/YV/ZF/YO/116453489/white-casual-shoes-for-men.jpg")
    st.write("حذاء شتوي أنيق")
    st.button("🛍 شراء الآن", key="p3")

# Floating Chat Button
st.markdown("<br><br>", unsafe_allow_html=True)
col1, col2, col3 = st.columns([8, 2, 1])
with col3:
    if st.button("💬 دعم العملاء"):
        st.session_state.show_chat_window = not st.session_state.show_chat_window

# Chat Window
if st.session_state.show_chat_window:
    with st.expander("🗨️ الدردشة مع الدعم", expanded=True):
        for message in reversed(st.session_state.chat_history):
            style = get_message_style(message['text'], message['role'])
            st.markdown(f"<div style='{style}'>{message['text']}</div>", unsafe_allow_html=True)

        # Input field and send button
        user_input = st.text_input("اكتب سؤالك هنا...")
        if st.button("إرسال"):
            if user_input:
                st.session_state.chat_history.append({'role': 'user', 'text': user_input})
                bot_response = send_message(user_input)
                st.session_state.chat_history.append({'role': 'bot', 'text': bot_response})
                st.rerun()
