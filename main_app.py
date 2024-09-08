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

# Initialize key num and login
if "unique_num" not in st.session_state:
    st.session_state["unique_num"] = []

if "login" not in st.session_state:
    st.session_state["login"] = "False"

# Initial Account

if "user" not in st.session_state:
    st.session_state["user"] = {}

    # Open the file and load the data
    with open("cache/account.json", 'r') as file:
        list_account = json.load(file)

    for key in list_account.keys():
        st.session_state["user"][key] = list_account[key]

if st.session_state["login"] == "False":
    placeholder = st.empty()

    with placeholder.form(key='Login'):
        username = st.text_input('Username')
        password = st.text_input('Password', type='password')
        submit = st.form_submit_button(
            'Login',
            use_container_width=True
        )

        st.write("Have you registered account in GenGrav app before? "
                 "If you haven't do yet, please contact us!")

    if submit:
        if username in list(st.session_state["user"].keys()) and password == st.session_state["user"][username]:
            st.session_state["login"] = "True"

            placeholder.empty()
            st.success('Login successfully')
            st.rerun()

        elif username not in list(st.session_state["user"].keys()) or password != st.session_state["user"][username]:
            st.error("You haven't registered in GenGrav app! Please contact us!")

        else:
            st.error("Please input username and password!")

else:
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

                data_type = st.session_state["RawDataType"]
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
        prompt = ("Welcome to GenGrav! "
                  "GenGrav is your cutting-edge generative AI companion designed to streamline and "
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
            if st.session_state['question'] == 'True':
                if "bouger" in prompt or "bouger density" in prompt or "densitas" in prompt:
                    label = 2
                else:
                    label = 1

            # Classification Text
            if label == 1:
                response, result, cache = GetMessageAPI.GetDataTopexMessage(prompt, st.session_state)
            elif label == 2:
                response, result, cache = GetMessageAPI.GetBougerDensityMessage(prompt, st.session_state)

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
            "label": label
        })
