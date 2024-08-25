import time
import json
import random
from PIL import Image
import streamlit as st
from function import GetMessageAPI, Helper


image = Image.open("image/GenGrav_logo.png")
st1, st2, st3 = st.columns(3)

with st2:
    st.image(image)

# Initialize key num
if "unique_num" not in st.session_state:
    st.session_state["unique_num"] = []

# Initialize chat history
if "container" not in st.session_state:
    st.session_state["container"] = []

    with open('cache/cache.json', 'r') as file:
        cache = json.load(file)

    for key, val in cache.items():
        st.session_state[key] = val

# Display chat messages from history on app rerun
for item in st.session_state["container"]:
    with st.chat_message(item["role"]):
        if item["label"] == 0 or str(item["content"]) == '':
            st.markdown(item["message"])

        elif item["label"] == 1:
            st.markdown(item["message"])
            st.dataframe(item["content"])

            data_type = st.session_state["raw_data_type"]
            data_num = Helper.GetNumberUnique(st.session_state["unique_num"])
            st.session_state["unique_num"].append(data_num)

            # Create a download button
            st.download_button(
                key=f'{data_type}_download_data_{data_num}',
                label=f'Download data as CSV',
                data=Helper.ConvertDataDownload(item["content"]),
                file_name=f'data_{data_type}.csv',
                mime='text/csv'
            )

# Display introduction GenGrav
if len(st.session_state["container"]) == 0:
    prompt = ("Welcome to GenGRav! "
              "GenGRav is your cutting-edge generative AI companion designed to streamline and "
              "enhance your data processing tasks in the field of gravity. "
              "How can I help you?")

    # Add user message to chat history
    st.session_state["container"].append({
        "role": "assistant",
        "message": prompt,
        "content": "",
        "label": 0
    })

    # Display user message in chat message container
    with st.chat_message("assistant"):
        st.write_stream(Helper.GeneratorMessage(prompt))

# Accept user input
if prompt := st.chat_input("Type your messages"):
    # Add user message to chat history
    st.session_state["container"].append({
        "role": "user",
        "message": prompt,
        "content": "",
        "label": 0
    })

    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        response, result, cache = GetMessageAPI.GetDataTopexMessage(prompt, st.session_state)

        for key, val in cache.items():
            try:
                st.session_state[key] = val
            except:
                pass

    # Add assistant response to chat history
    st.session_state["container"].append({
        "role": "assistant",
        "message": response,
        "content": result,
        "label": 1
    })
