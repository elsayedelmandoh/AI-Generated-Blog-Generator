import io
from PIL import Image
import requests
import streamlit as st
# import openai

API_TOKEN = "your_api_key"

def generate_text(prompt, model_url):
    API_URL = f"https://api-inference.huggingface.co/models/{model_url}"
    headers = {"Authorization": f"Bearer {API_TOKEN}"}
    # payload = {"inputs": prompt}
    payload = {"inputs": prompt, 
               "parameters": {"temperature": 0.7, "max_tokens": 200}}

    response = requests.post(API_URL, headers=headers, json=payload)
    generated_text = response.json()[0]["generated_text"]
    return generated_text

def generate_image(description, model_url):
    API_URL = f"https://api-inference.huggingface.co/models/{model_url}"
    headers = {"Authorization": f"Bearer {API_TOKEN}"}
    payload = {"inputs": description}
    
    response = requests.post(API_URL, headers=headers, json=payload)
    image_bytes = response.content
    image = Image.open(io.BytesIO(image_bytes))
    return image


def generate_intro(keywords, txt_model_url, img_model_url):
    intro_prompt = f"Explore {keywords} in a few sentences, highlighting its significance."
    intro_text = generate_text(intro_prompt,  txt_model_url)
    intro_image = generate_image(intro_text, img_model_url)
    return intro_text, intro_image

def generate_body(keywords, txt_model_url, img_model_url):
    body_prompt = f"Dive deep into {keywords}, providing insights, definitions, and examples. Uncover the nuances of this fascinating topic."
    body_text = generate_text(body_prompt,  txt_model_url)
    body_image = generate_image(body_text, img_model_url)
    return body_text, body_image

def generate_conclusion(keywords, txt_model_url, img_model_url):
    conclusion_prompt = f"Summarize the key points about {keywords}."
    conclusion_text = generate_text(conclusion_prompt, txt_model_url)
    conclusion_image = generate_image(conclusion_text, img_model_url)
    return conclusion_text, conclusion_image


def main():
    st.title("AI-Generated Blog Generator")

    keywords = st.text_input("Enter title blog:")
    if st.button("Generate Blog"):
        if len(keywords.split()) >= 2 and len(keywords.split()) < 10:
        
            txt_model_url = "tiiuae/falcon-7b-instruct"
            # txt_model_url = "google/flan-ul2"
            img_model_url = "CompVis/stable-diffusion-v1-4"
            
            intro_text, intro_image = generate_intro(keywords, txt_model_url, img_model_url)
            body_text, body_image = generate_body(keywords, txt_model_url, img_model_url)
            conclusion_text, conclusion_image = generate_conclusion(keywords, txt_model_url, img_model_url)

            col1, col2 = st.columns(2)
            col1.write(f"**Introduction:**\n\n {intro_text}")
            col2.image(intro_image, caption='Introduction Image', use_column_width=True)

            col3, col4 = st.columns(2)
            col3.write(f"**Body:**\n\n {body_text}")
            col4.image(body_image, caption='Body Image', use_column_width=True)

            col5, col6 = st.columns(2)
            col5.write(f"**Conclusion:**\n\n {conclusion_text}")
            col6.image(conclusion_image, caption='Conclusion Image', use_column_width=True)
        else:
            if len(keywords.split()) >= 2:
                st.warning("Please enter a title with at least two words.")
            else:
                st.warning("Title is long. Please enter a shorter title.")

if __name__ == "__main__":
    main()
