import gradio as gr
import requests
from PIL import Image
import io

# Your OpenAI API Key
API_KEY = "AIzaSyB49eoNNg_QTuru52PmkTKCQb8OpXnq164"
OPENAI_API_URL =  "https://generativelanguage.googleapis.com/v1beta/openai/chat/completions"


def generate_caption(image):
    """
    Directly process the image in Gradio and generate a prompt dynamically.
    """
    # Convert image to bytes
    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format="JPEG")
    img_byte_arr = img_byte_arr.getvalue()

    # Auto-generated prompt for OpenAI API
    prompt = "Generate a viral caption with relevant hashtags based on this image."

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
    "model": "gemini-2.5-flash-preview-05-20",  # Ensure you're using a valid model
    "reasoning_effort": "low",
    "messages": [
        {"role": "user", "content": "Generate a viral caption and hashtags for this image."}
    ]
    }

    response = requests.post(OPENAI_API_URL, headers=headers, json=payload)

    if response.status_code == 200:
        data = response.json()
        caption = data.get("choices", [{}])[0].get("message", {}).get("content", "No caption generated")
        hashtags = ["#viral", "#trend", "#popular"]  # Example hashtags (can refine further)
        hashtags_str = " ".join(hashtags)
        return caption, hashtags_str
    else:
        return f"API Error: {response.status_code}", ""

# Gradio Interface
interface = gr.Interface(
    fn=generate_caption,
    inputs=gr.Image(type="pil"),
    outputs=["text", "text"],
    title="Viral Image Caption Generator",
    description="Upload an image and get AI-generated captions & hashtags!",
)

interface.launch()