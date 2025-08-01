import fitz  # PyMuPDF
import pytesseract
from PIL import Image
from langdetect import detect
from transformers import M2M100ForConditionalGeneration, M2M100Tokenizer
import json
import os
from datetime import datetime

model_name = "facebook/m2m100_418M"
tokenizer = M2M100Tokenizer.from_pretrained(model_name)
model = M2M100ForConditionalGeneration.from_pretrained(model_name)

def extract_text_from_pdf(pdf_file):
    doc = fitz.open(stream=pdf_file.read(), filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def extract_text_from_image(image_file):
    image = Image.open(image_file)
    return pytesseract.image_to_string(image)

def detect_language(text):
    return detect(text)

def translate_text(text, source_lang, target_lang):
    tokenizer.src_lang = source_lang
    encoded = tokenizer(text, return_tensors="pt", truncation=True, padding=True)
    generated_tokens = model.generate(
        **encoded,
        forced_bos_token_id=tokenizer.get_lang_id(target_lang)
    )
    return tokenizer.decode(generated_tokens[0], skip_special_tokens=True)

def translate_to_multiple_languages(text, source_lang, target_langs):
    results = {}
    for lang in target_langs:
        try:
            results[lang] = translate_text(text, source_lang, lang)
        except Exception as e:
            results[lang] = f"Error: {e}"
    return results

def save_translation_history(text, source_lang, translations):
    entry = {
        "timestamp": datetime.now().isoformat(),
        "source_lang": source_lang,
        "original_text": text[:1000],
        "translations": translations
    }
    history_file = "history.json"
    history = []
    if os.path.exists(history_file):
        with open(history_file, "r", encoding="utf-8") as f:
            history = json.load(f)
    history.append(entry)
    with open(history_file, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=4, ensure_ascii=False)
