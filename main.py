import io
from PIL import Image
import requests
import streamlit as st

API_TOKEN = "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"

def generate_text(prompt):
    API_URL = "https://api-inference.huggingface.co/models/tiiuae/falcon-7b-instruct"
    headers = {"Authorization": f"Bearer {API_TOKEN}"}
    payload = {"inputs": prompt}
    
    response = requests.post(API_URL, headers=headers, json=payload)
    generated_text = response.json()[0]["generated_text"]
    return generated_text

def generate_image(description):
    API_URL = "https://api-inference.huggingface.co/models/CompVis/stable-diffusion-v1-4"
    headers = {"Authorization": f"Bearer {API_TOKEN}"}
    payload = {"inputs": description,}
    
    response = requests.post(API_URL, headers=headers, json=payload)
    image_bytes = response.content
    image = Image.open(io.BytesIO(image_bytes))
    return image

def main():
    st.title("AI-Generated Blog Generator")

    keywords = st.text_input("Enter title blog (at least 4 words):")
    if keywords:
        intro_text = generate_text(keywords)
        intro_image = generate_image(intro_text)

        body_text = generate_text(intro_text)
        body_image = generate_image(body_text)

        conclusion_text =  generate_text(body_text)
        conclusion_image = generate_image(conclusion_text)

        col1, col2 = st.columns(2)
        col1.write(f"**Introduction:**\n\n {intro_text}")
        col2.image(intro_image, caption='Introduction Image', use_column_width=True)

        col1.write(f"**Body:**\n\n {body_text}")
        col2.image(body_image, caption='Body Image', use_column_width=True)

        col1.write(f"**Conclusion:**\n\n {conclusion_text}")
        col2.image(conclusion_image, caption='Conclusion Image', use_column_width=True)

if __name__ == "__main__":
    main()
