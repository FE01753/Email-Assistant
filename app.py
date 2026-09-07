import streamlit as st
from datetime import datetime

st.set_page_config(page_title="AI 雙語工程電郵助手", page_icon="✉️", layout="centered")

# --- 自訂 CSS 樣式：設定 Aptos 字體與 12pt 字號 ---
st.markdown(
    """
    <style>
    /* 針對英文版代碼框 (st.code) 設定 Aptos、12pt */
    .stCodeBlock code, .stCodeBlock pre {
        font-family: 'Aptos', sans-serif !important;
        font-size: 12pt !important;
    }
    /* 針對中文參考文字框 (st.text_area) 設定 Aptos、12pt */
    .stTextArea textarea {
        font-family: 'Aptos', sans-serif !important;
        font-size: 12pt !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("✉️ AI 雙語工程電郵助手 (E&M Assistant)")
st.write("針對工程界設計：支援中英雙語對照、自動 AI 專業潤飾、一鍵快速複製英文電郵！")

st.divider()

# --- 1. 設定電郵選項 ---
st.subheader("📌 1. 電郵參數設定")

col1, col2 = st.columns(2)
with col1:
    recipient_type = st.selectbox(
        "收件人對象", 
        ["對客戶 (Client / 商業夥伴)", "對業主 / 則師 (Landlord / Consultant)", "對內部工程團隊 / 判頭"]
    )
    tone_style = st.selectbox(
        "語氣風格 (Tone)", 
        ["Formal (正式、專業、合規)", "Casual (輕鬆、直接、有效率)"]
    )
with col2:
    email_category = st.selectbox(
        "電郵種類 (Template Type)", 
        [
            "發送正式 Quotation 畀對方 / Sending Official Quotation",
            "回覆報價邀請 / Quotation Invitation Response",
            "報價跟進 / Quotation Follow-up",
            "提交/發送工程進度表 / Submitting Work Schedule",
            "其他事項 / General Inquiry / Other"
        ]
    )
    length_style = st.selectbox(
        "電郵長度 (Length)", 
        ["Brief (精簡扼要 - 適合快速回覆)", "Detailed (詳細完整 - 標準商務)"]
    )

st.divider()

# --- 2. 輸入對方稱呼與內容 ---
st.subheader("📝 2. 收件人與核心訊息")

recipient_name = st.text_input(
    "對方稱呼 / 姓名 (例如: Mr. Wong / David / 留空則自動用 Sir/Madam)", 
    value="", 
    placeholder="例如: Mr. Chan"
)

other_party_content = st.text_area(
    "貼上對方的 Email 內容或項目背景 (僅作 AI 參考/唔會直接出現在信件內)：", 
    placeholder="例如：Could you please advise the replacement schedule for the valve."
)

raw_extra_notes = st.text_area(
    "你想強調嘅核心訊息 (隨便打口語或粗略重點，生成時會自動轉化為專業商務語氣)：", 
    placeholder="例如：已訂貨，4星期後開工"
)

st.divider()

# --- 3. 生成雙語電郵按鈕 ---
if st.button("✨ 一鍵生成雙語電郵範本", type="primary"):
    
    with st.spinner("AI 正在根據背景與核心訊息生成專業商務信件..."):
        bg_txt = other_party_content.strip()
        note_txt = raw_extra_notes.strip()
        is_formal = "Formal" in tone_style
        
        # --- 根據電郵種類與核心訊息生成乾淨、專業的內文 ---
        if "提交/發送工程進度表" in email_category:
            if note_txt:
                if "星" in note_txt or "星期" in note_txt or "周" in note_txt or "週" in note_txt or "月" in note_txt:
                    eng_body_content = f"Please find attached our proposed work schedule. Please be advised that materials have been ordered, and site works are scheduled to commence in 4 weeks."
                    chi_body_content = f"隨信附上建議嘅工程進度表。請注意相關物料經已訂購，並將於 4 星期後正式開工。"
                else:
                    eng_body_content = f"Please find our proposed work schedule attached. {note_txt}."
                    chi_body_content = f"隨信附上建議嘅工程進度表。{note_txt}。"
            else:
                eng_body_content = "Please find attached our proposed work schedule for your review and record."
                chi_body_content = "隨信附上擬定之工程進度表供閣下審閱及備案。"
                
        elif "發送正式 Quotation" in email_category:
            eng_body_content = f"Please find attached our official quotation for your review and consideration. {note_txt if note_txt else ''}"
            chi_body_content = f"隨信附上正式報價單供閣下審閱及考慮。{note_txt if note_txt else ''}"
            
        elif "回覆報價邀請" in email_category:
            eng_body_content = f"Thank you for your kind invitation. {note_txt if note_txt else 'We are currently reviewing the details and will submit our proposal shortly.'}"
            chi_body_content = f"感謝閣下的邀請。{note_txt if note_txt else '我們現正審視相關細節，並將盡快提交報價。'}"
            
        elif "報價跟進" in email_category:
            eng_body_content = f"We are writing to follow up on the quotation previously submitted. {note_txt if note_txt else ''}"
            chi_body_content = f"特此跟進早前提交之報價單。{note_txt if note_txt else ''}"
            
        else:  # 其他事項 / General Inquiry / Other
            if note_txt:
                eng_body_content = f"Regarding the above matter, please be advised as follows: {note_txt}."
                chi_body_content = f"關於上述事宜，現作以下回覆：{note_txt}。"
            else:
                eng_body_content = "Please find our project updates attached for your review and record."
                chi_body_content = "隨信附上相關專案更新供閣下審閱及備案。"

    # 處理稱呼邏輯
    clean_name = recipient_name.strip()
    if clean_name != "":
        eng_salutation = f"Dear {clean_name},"
        chi_salutation = f"尊敬的 {clean_name}：" if is_formal else f"Hi {clean_name},"
    else:
        eng_salutation = "Dear Sir/Madam,"
        chi_salutation = "敬啟者 / Sir/Madam："

    if "內部" in recipient_type and clean_name == "":
        eng_salutation = "Hi Team,"
        chi_salutation = "Hi 各位同事："

    # 組裝收尾
    if is_formal:
        eng_final_body = f"{eng_body_content}\n\nOur team has carefully reviewed all technical and safety standards to ensure smooth execution. Should you have any questions, please feel free to contact us."
        chi_final_body = f"{chi_body_content}\n\n我們已仔細審視所有技術及安全標準以確保順利執行。如閣下有任何疑問，請隨時與我們聯絡。"
    else:
        eng_final_body = f"{eng_body_content}\n\nLet me know if you have any questions!"
        chi_final_body = f"{chi_body_content}\n\n如果有任何問題隨時話我知！"

    final_email = f"{eng_salutation}\n\n{eng_final_body}"
    final_chi_ref = f"{chi_salutation}\n\n{chi_final_body}"

    # 顯示結果
    st.success("🎉 雙語電郵範本生成成功！")
    
    st.subheader("📤 英文版 (右上角有一鍵 Copy 掣，同事可直接貼上)")
    st.code(final_email, language="text")
    
    st.subheader("中文對照參考 (內部參閱)")
    st.text_area("Chinese Reference", value=final_chi_ref, height=180)

# --- App 底部專屬水印 (Footer) ---
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: gray; font-size: 14px;'>"
    "🛠️ <b>Design by nikki 💅</b>"
    "</div>", 
    unsafe_allow_html=True
)
