import streamlit as st
import yaml
from PIL import Image



# 加载配置文件
with open('config.yaml', 'r') as f:
    config = yaml.load(f, Loader=yaml.FullLoader)
    
from Models.EchoModel import EchoModel
@st.cache_resource
def get_model():
    return None, EchoModel()

tokenizer, model = get_model()

def multiMediaInput() :
    uploaded_file = st.file_uploader("Choose an image/video/audio...", key="iva_uploader", accept_multiple_files=False, )
    input_type = "FILE"
    if uploaded_file :
        file_type_guess = uploaded_file.type
        input_type = "Audio" if "audio" in file_type_guess else \
                    "Image" if "image" in file_type_guess else \
                    "Video" if "video" in file_type_guess else \
                    "FILE" 
        print(input_type, file_type_guess)
    if input_type == "Audio" :
        # uploaded_file = st.file_uploader("Choose an audio...", type=["wav", "mp3", "wma"], key="audio_uploader")
        if uploaded_file:
            audio = uploaded_file
            
            def upload_audio() :
                st.session_state.messages.append({"role": "user", "audio": audio})
                
            st.button("confirm", on_click=upload_audio) 
    elif input_type == "Image" :
        # uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "png", "jpeg"], key="image_uploader")
        if uploaded_file:
            image = Image.open(uploaded_file)
            
            def upload_image() :
                st.session_state.messages.append({"role": "user", "image": image})
                
            st.button("confirm", on_click=upload_image) 
    elif input_type == "Video" :
        # uploaded_file = st.file_uploader("Choose an video...", type=["mp4", "mov", "avi"], key="video_uploader")
        if uploaded_file:
            video = uploaded_file
            
            def upload_video() :
                st.session_state.messages.append({"role": "user", "video": video})
                
            st.button("confirm", on_click=upload_video) 
    else :
        assert input_type == "FILE" 
        if uploaded_file:
            file = uploaded_file

            def upload_file() :
                st.session_state.messages.append({"role": "user", "file": file})
                
            st.button("confirm", on_click=upload_file) 

def showAllMessage() :
    # 遍历session_state中的所有消息，并显示在聊天界面上
    for msg in st.session_state.messages:
        if msg["role"] == "assistant":
            st.chat_message(msg["role"]).write(msg["content"])
        elif msg["role"] == "user":
            if "text" in msg:
                st.chat_message("user").write(msg["text"])
            elif "image" in msg:
                st.chat_message("user").image(msg["image"])
            elif "video" in msg:
                st.chat_message("user").video(msg["video"])
            elif "audio" in msg:
                st.chat_message("user").audio(msg["audio"])
            elif "file" in msg:
                st.chat_message("user").write(f"{msg['file'].name} is not a valid media type")

# 在侧边栏中创建一个标题和一个链接
with st.sidebar:
    "[关于我们](https://smzzl.github.io/page-html/)"
    st.markdown("## taichu MLLM")
    
    model_names = config["model_names"]
    model_name = st.selectbox("select your model", model_names)
    # multiMediaInput()
    # input_type = st.radio("add media input", ("None", "Audio", "Image", "Video"))

# 创建一个标题和一个副标题
st.title("🤖 taichu Chatbot")
st.caption("🚀 a MLLM by casia")

# 如果session_state中没有"messages"，则创建一个包含默认消息的列表
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "有什么可以帮您的？"}]

showAllMessage()
# st.markdown(
#     """
#     <style>
#     .fixed-bottom {
#         position: fixed;
#         bottom: 0;
#     }
#     </style>
#     """,
#     unsafe_allow_html=True
# )

# 将container固定在页面底部
# container = st.container()
# with container:
#     message = file_chat_input("Type a message...")

# if message :
#     prompt = message["message"]
#     if len(prompt) > 0 :
#         st.session_state.messages.append({"role": "user", "text": prompt})
#         st.chat_message("user").write(prompt)
        
#         response = model.generate(st.session_state.messages[-1]["text"])
        
#         st.session_state.messages.append({"role": "assistant", "content": response})
#         st.chat_message("assistant").write(response)
        # st.markdown(scroll_script, unsafe_allow_html=True)

# scroll_script = f"""
# <script>
#   var textArea = document.getElementById("file_chat_input");
#   textArea.scrollTop = textArea.scrollHeight;
# </script>
# """

# container.float("bottom: 0")
        
#     st.
    
if prompt := st.chat_input() :
    st.session_state.messages.append({"role": "user", "text": prompt})
    st.chat_message("user").write(prompt)
    
    response = model.generate(st.session_state.messages[-1]["text"])
    
    st.session_state.messages.append({"role": "assistant", "content": response})
    st.chat_message("assistant").write(response)
    
multiMediaInput()
    



# 注释掉的代码片段是用于文本生成的，可以根据需要启用
# input_ids = tokenizer.apply_chat_template(st.session_state.messages,tokenize=False,add_generation_prompt=True)
# model_inputs = tokenizer([input_ids], return_tensors="pt").to('cuda')
# generated_ids = model.generate(model_inputs.input_ids, max_new_tokens=512)
# generated_ids = [
#     output_ids[len(input_ids):] for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)
# ]
# response = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]
# st.session_state.messages.append({"role": "assistant", "content": response})
# st.chat_message("assistant").write(response)