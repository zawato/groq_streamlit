import streamlit as st
import pandas as pd
from PIL import Image, ImageDraw, ImageFont

# サンプルデータフレームの作成（例: ステータスが「未読」と「既読」）
data = {
    "ID": [1, 2, 3, 4, 5],
    "Status": ["未読", "既読", "未読", "既読", "未読"]
}
df = pd.DataFrame(data)

# 未読行のカウント
unread_count = df[df["Status"] == "未読"].shape[0]

# サイドバー
with st.sidebar.container():
    # # アイコンとバッジをHTMLで作成
    # badge_html = f"""
    #     <div style="position: relative; display: inline-block;">
    #         <img src="./icon_mail.png"/>
    #         <span style="
    #             position: absolute;
    #             top: -10px;
    #             right: -10px;
    #             background-color: red;
    #             color: white;
    #             border-radius: 50%;
    #             padding: 2px 6px;
    #             font-size: 12px;
    #         ">{unread_count}</span>
    #     </div>
    # """

    # # アイコンとバッジの表示
    # st.markdown(badge_html, unsafe_allow_html=True)

    # アイコン画像の読み込み（アイコン画像のパスを指定）
    icon_path = "icon_mail.png"  # ローカルに保存したアイコン画像のパス
    icon = Image.open(icon_path)

    # 画像に描画するためのオブジェクトを作成
    draw = ImageDraw.Draw(icon)

    # フォントの準備（デフォルトのフォントを使う）
    font = ImageFont.load_default()

    # バッジのサイズと色の設定
    badge_size = 100  # バッジのサイズ
    badge_color = "red"  # バッジの背景色
    text_color = "white"  # バッジ内の文字色

    # バッジを描くための円を描画
    draw.ellipse((icon.width - badge_size, 0, icon.width, badge_size), fill=badge_color)

    # 未読数を描画
    text = str(unread_count)

    # テキストのバウンディングボックスを取得してサイズ計算
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    # テキストの位置を計算して描画（センタリングを改善）
    text_position = (
        icon.width - badge_size + (badge_size - text_width) // 2,  # X方向のセンタリング
        (badge_size - text_height) // 2  # Y方向のセンタリング
    )
    draw.text(text_position, text, font=font, fill=text_color)

    # 画像をStreamlitで表示
    st.image(icon, width=50)

# データフレームの表示
st.write("DataFrame:")
st.dataframe(df)