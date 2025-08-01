import streamlit as st
from utils import (
    extract_text_from_pdf, extract_text_from_image,
    detect_language, translate_to_multiple_languages,
    save_translation_history
)
import json

st.set_page_config(
    page_title="🌍 Multilingual Document Translator",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Custom CSS for better look
st.markdown("""
    <style>
    .stApp {
        background-color: #f2f2f2;
    }
    .main-title {
        font-size:40px;
        color:#003366;
        text-align:center;
    }
    .footer {
        text-align:center;
        margin-top: 30px;
        color: grey;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">📘 Multilingual Document Translator</div>', unsafe_allow_html=True)
st.markdown("Translate your PDFs or scanned documents to multiple languages in seconds!")

uploaded_file = st.file_uploader("📂 Upload your document (PDF, JPG, PNG)", type=['pdf', 'jpg', 'jpeg', 'png'])

target_langs = st.multiselect(
    "🌐 Select Target Languages",
    ["en", "hi", "fr", "ar", "ja", "zh", "es", "de", "ru"],
    default=["en", "hi", "fr"]
)

if st.button("🚀 Translate"):
    if uploaded_file:
        with st.spinner("Extracting and translating..."):
            if uploaded_file.type == "application/pdf":
                extracted_text = extract_text_from_pdf(uploaded_file)
            else:
                extracted_text = extract_text_from_image(uploaded_file)

            detected_lang = detect_language(extracted_text)
            translations = translate_to_multiple_languages(extracted_text, detected_lang, target_langs)
            save_translation_history(extracted_text, detected_lang, translations)

            st.success(f"✅ Detected Language: `{detected_lang}`")

            for lang, translated_text in translations.items():
                st.markdown(f"### 🔸 {lang.upper()} Translation")
                st.text_area(f"{lang.upper()} Output", translated_text, height=250)
                st.download_button(
                    label=f"⬇ Download {lang.upper()}",
                    data=translated_text,
                    file_name=f"translated_{lang}.txt"
                )
    else:
        st.warning("⚠️ Please upload a document first.")

# Translation history section
st.markdown("---")
if st.checkbox("📖 Show Translation History"):
    try:
        with open("history.json", "r", encoding="utf-8") as f:
            history = json.load(f)
        for entry in reversed(history[-5:]):
            st.markdown(f"**🕒 {entry['timestamp']}** — From `{entry['source_lang']}`")
            for lang, text in entry["translations"].items():
                st.markdown(f"- `{lang}`: {text[:100]}...")
    except FileNotFoundError:
        st.warning("No history found.")

st.markdown('<div class="footer">Made with ❤️ using Facebook M2M-100 and Streamlit</div>', unsafe_allow_html=True)
