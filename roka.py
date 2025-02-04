import streamlit as st
import requests

# Set page config
st.set_page_config(page_title="Shoe Store", page_icon="👟")

# Set background image and text color using CSS
st.markdown(
    """
    <style>
    .stApp {
        background-image: url('https://runkeeper.com/cms/wp-content/uploads/sites/4/2021/12/ASICS_Color-Injection-Pack_Highlight_0253-scaled.jpg');
        background-size: cover;
        background-position: center center;
        background-attachment: fixed;
    }

    /* Set the text color to white */
    .stApp, .stMarkdown, .stHeader, .stTitle, .stButton, .stTextInput, .stTextArea {
        color: white;
    }

    /* Specific styling for buttons */
    .stButton>button {
        background-color: rgba(0, 0, 0, 0.6); /* Transparent background for buttons */
        color: white;
        border: 1px solid white;
    }

    /* Style the header */
    .stTitle {
        color: white;
    }
    
    </style>
    """,
    unsafe_allow_html=True,
)

# Store chat history in session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "show_chat_window" not in st.session_state:
    st.session_state.show_chat_window = False

# Function to handle chatbot responses
def send_message(user_message):
    try:
        response = requests.post("http://127.0.0.1:5005/get_answer", json={"question": user_message})
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
        return f"background-color: #D3D3D3; padding: 10px; border-radius: 10px; text-align: left; width: {width}px; color: black;"
    else:
        return f"background-color: #ADD8E6; padding: 10px; border-radius: 10px; text-align: right; width: {width}px; color: black;"

# Display the buttons to navigate between pages
if "current_page" not in st.session_state:
    st.session_state.current_page = "main_page"

# Main Store Page
if st.session_state.current_page == "main_page":
    # Header & Welcome Message with Sign Up / Log In button
    col1, col2, col3 = st.columns([8, 2, 1])
    with col1:
        st.title("👟 مرحبًا بك في متجر الأحذية")
    with col2:
        if st.button("تسجيل الدخول / تسجيل جديد"):
            st.session_state.current_page = "login_page"
    
    st.markdown("### Hello to store")
    st.image("https://source.unsplash.com/1000x400/?shoes", use_container_width=True)

    # Display Products
    st.header("🛒 الأحذية المميزة")
    col1, col2, col3, col4, col5 = st.columns(5)

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
    with col4:
        st.image("https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTHX9Q5K3fwfWoTFE-Wa2cHat0rEUt90cnCrg&s")
        st.write("حذاء رياضي فاخر")
        st.button("🛍 شراء الآن", key="p4")
    with col5:
        st.image("https://www.intersport.com.eg/cdn/shop/products/7624769427347a_1.jpg?v=1703042070&width=2048")
        st.write("حذاء جري احترافي")
        st.button("🛍 شراء الآن", key="p5")

    # Chat button to navigate to the chat page
    if st.button("💬 دعم العملاء"):
        st.session_state.current_page = "chat_page"

# Login Page (for decoration)
elif st.session_state.current_page == "login_page":
    st.title("تسجيل الدخول / تسجيل جديد")
    st.markdown("### مرحبًا بك! هنا يمكنك تسجيل الدخول أو إنشاء حساب جديد.")
    
    # Sample login form (just for decoration)
    with st.form(key='login_form'):
        username = st.text_input("اسم المستخدم")
        password = st.text_input("كلمة المرور", type="password")
        submit_button = st.form_submit_button("تسجيل الدخول")

    # Back Button to return to main page
    if st.button("🔙 العودة إلى المتجر"):
        st.session_state.current_page = "main_page"

# Chat Page
elif st.session_state.current_page == "chat_page":
    # Chat Window Page
    st.title("🗨️ الدردشة مع الدعم")
    
    # Display chat history with older messages at the top and new messages at the bottom
    for message in st.session_state.chat_history:
        style = get_message_style(message['text'], message['role'])
        st.markdown(f"<div style='{style}'>{message['text']}</div>", unsafe_allow_html=True)

    # Input field and send button
    user_input = st.text_input("اكتب سؤالك هنا...")
    if st.button("إرسال"):
        if user_input:
            st.session_state.chat_history.append({'role': 'user', 'text': user_input})
            bot_response = send_message(user_input)
            st.session_state.chat_history.append({'role': 'bot', 'text': bot_response})

    # Back Button to return to main page
    if st.button("🔙 العودة إلى المتجر"):
        st.session_state.current_page = "main_page"
