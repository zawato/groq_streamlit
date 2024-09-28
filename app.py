import os
import streamlit as st
from groq import Groq

# メインタイトル
st.title("Hello Streamlit!")

# メッセージの値を保持
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "何か気になることはありますか？"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# サイドバー
with st.sidebar.container():
    ### サイドバータイトル
    st.title("各種設定")
    ### Groq APIキーの入力
    api_key = st.text_input('APIキー', placeholder='APIキーを入力してください')
    st.divider()
    ### モデル選択
    selected_model = st.selectbox(
        'モデル',
        ['llama3-70b-8192', 'llama-3.1-70b-versatile']
    )
    st.divider()
    ### 最大トークン数
    max_tokens = st.slider('最大トークン数', 100, 1000, 100)
    st.divider()
    ### Tempperature
    temperature = st.slider('Temperature', 0.0, 2.0, 1.0)

# ユーザーの入力が送信された際に実行される処理
if prompt := st.chat_input("Groqにメッセージを送信する"):
    client = Groq(
        api_key=api_key
    )
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    # Set the system prompt
    system_prompt = {
        "role": "system",
        "content": "あなたは日本語で回答する便利なアシスタントです。"
    }

    # ユーザのプロンプトをセット
    user_input = prompt
    user_prompt = {
        "role": "user", "content": user_input
    }

    # チャット履歴を格納
    chat_history = [system_prompt, user_prompt]

    # 回答を格納
    response = client.chat.completions.create(model=selected_model,
                                                messages=chat_history,
                                                max_tokens=max_tokens,
                                                temperature=temperature)
    
    # メッセージを取得
    msg = response.choices[0].message
    # セッションにメッセージを追加
    st.session_state.messages.append({"role": "assistant", "content": msg.content})
    # メッセージを出力
    st.chat_message("assistant").write(msg.content)