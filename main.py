import streamlit as st
import requests
import io
from PIL import Image
from streamlit_option_menu import option_menu
from functions import html



style = html.STYLE
about_dev = html.ABOUT_DEVELOPER
about_app = html.ABOUT_APP
link = html.LINK

def query_stabilitydiff(payload, headers):
    API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.content



# interface
with st.sidebar:
    info = option_menu("Info", ["App", "About the app","About the Developer"],
                    icons=['joystick', 'book', 'person lines fill'],
                    menu_icon="cast", default_index=0,
                    styles={
                        "container": {"padding": "5!important", "background-color": "white"},
                        "icon": {"color": "black", "font-size": "25px"},
                        "nav-link": {"font-size": "16px", "text-align": "left", "margin": "0px",
                                    "--hover-color": "orange"},
                                    "nav-link-selected": {"background-color": "red", "color": "white", "font-size": "16px",
                                                            "text-align": "left", "margin": "0px", "border-radius": "5px", "--hover-color": "orange"},
                    }
                    )
    

    # app info
if info == "About the app":
    st.markdown(""" <style> .font {
    font-size:30px ; font-family: 'Cooper Black'; color: black;} 
    </style> """, unsafe_allow_html=True)
    st.markdown('<h2 class="font"> About the App </h2>', unsafe_allow_html=True)
    st.markdown(style, unsafe_allow_html= True)
    st.markdown(about_app, unsafe_allow_html=True)


elif info == "About the Developer":
    st.markdown(""" <style> .font {
    font-size:30px ; font-family: 'Cooper Black'; color: black;} 
    </style> """, unsafe_allow_html=True)
    st.markdown('<h2 class="font"> About the Developer </h2>', unsafe_allow_html=True)
    st.markdown(style, unsafe_allow_html= True)
    st.markdown(about_dev, unsafe_allow_html=True)
    st.markdown(link, unsafe_allow_html=True)

elif info == "App":
    st.title("💬 Image Chatbot - Convert your text to Image")
    st.caption("🚀 A Streamlit image chatbot powered by Stable Diffusion")

    if "messages" not in st.session_state:
        st.session_state["messages"] = [
            {"role": "assistant", "content": "What kind of image do you wish to generate?"}]

    for message in st.session_state.messages:
        st.chat_message(message["role"]).write(message["content"])
        if "image" in message:
            st.chat_message("assistant").image(message["image"], caption=message["prompt"], use_column_width=True)


    if prompt := st.chat_input():

        # if not st.secrets.hugging_face_token.api_key:
        #     st.info("Please add your Hugging Face Token to continue.")
        #     st.stop()

        # Input prompt
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)

        # Query Stable Diffusion
        headers = {"Authorization": f"Bearer {st.secrets.hugging_face_token.api_key}"}
        image_bytes = query_stabilitydiff({
            "inputs": prompt,
        }, headers)

        image = Image.open(io.BytesIO(image_bytes))
        msg = f'here is your image... "{prompt}"'
        # Convert image to bytes
        img_bytes = io.BytesIO()
        image.save(img_bytes, format='JPEG')
        img_bytes = img_bytes.getvalue()

        # Show Result
        st.session_state.messages.append({"role": "assistant", "content": msg, "prompt": prompt, "image": image})
        st.chat_message("assistant").write(msg)
        st.chat_message("assistant").image(image, caption=prompt, use_column_width=True)
        # download the image
        if image:
            download_button = st.download_button(label="Download Image", data=img_bytes, file_name=prompt, mime="image/jpeg")
            if download_button:
                st.success("Downloaded!", icon="✅")
            
else:
    pass

