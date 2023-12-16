import streamlit as st
import os
from PIL import Image
import google.generativeai as genai

st.set_page_config(page_title="Gemini Pro with Streamlit",page_icon="♊")

st.write("Welcome to the Gemini Pro Dashboard. You can proceed by providing your Google API Key")

with st.expander("Provide Your Google API Key"):
     # google_api_key = st.text_input("Google API Key", key="google_api_key", type="password")
     
if not google_api_key:
    st.info("Enter the Google API Key to continue")
    st.stop()

genai.configure(api_key=google_api_key)

st.title("Gemini Pro with Streamlit Dashboard")

with st.sidebar:
    option = st.selectbox('Choose Your Model',('gemini-pro', 'gemini-pro-vision'))

    if 'model' not in st.session_state or st.session_state.model != option:
        st.session_state.chat = genai.GenerativeModel(option).start_chat(history=[])
        st.session_state.model = option
    
    st.write("Adjust Your Parameter Here:")
    temperature = st.number_input("Temperature", min_value=0.0, max_value= 1.0, value =0.5, step =0.01)
    max_token = st.number_input("Maximum Output Token", min_value=0, value =100)
    gen_config = genai.types.GenerationConfig(max_output_tokens=max_token,temperature=temperature)

    st.divider()
    st.markdown("""<span ><font size=1>Connect With Me</font></span>""",unsafe_allow_html=True)
    "[Linkedin](https://www.linkedin.com/in/cornellius-yudha-wijaya/)"
    "[GitHub](https://github.com/cornelliusyudhawijaya)"
    
    st.divider()
    
    upload_image = st.file_uploader("Upload Your Image Here", accept_multiple_files=False, type = ['jpg', 'png'])
    
    if upload_image:
        image = Image.open(upload_image)
    st.divider()

    if st.button("Clear Chat History"):
        st.session_state.messages.clear()
        st.session_state["messages"] = [{"role": "assistant", "content": "Hi there. Can I help you?"}]

 
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "Hi there. Can I help you?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if upload_image:
    if option == "gemini-pro":
        st.info("Please Switch to the Gemini Pro Vision")
        st.stop()
    if prompt := st.chat_input():
            st.session_state.messages.append({"role": "user", "content": prompt})
            st.chat_message("user").write(prompt)
            response=st.session_state.chat.send_message([prompt,image],stream=True,generation_config = gen_config)
            response.resolve()
            msg=response.text

            st.session_state.chat = genai.GenerativeModel(option).start_chat(history=[])
            st.session_state.messages.append({"role": "assistant", "content": msg})
            
            st.image(image,width=300)
            st.chat_message("assistant").write(msg)

else:
    if prompt := st.chat_input():
            
            st.session_state.messages.append({"role": "user", "content": prompt})
            st.chat_message("user").write(prompt)
            
            response=st.session_state.chat.send_message(prompt,stream=True,generation_config = gen_config)
            response.resolve()
            msg=response.text
            st.session_state.messages.append({"role": "assistant", "content": msg})
            st.chat_message("assistant").write(msg)
    
    
