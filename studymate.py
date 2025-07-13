
import gradio as gr
import google.generativeai as genai
from gtts import gTTS
import os
import speech_recognition as sr
import tempfile

# 🔐 Gemini API Configuration
genai.configure(api_key="your_gemini_api_key")
model = genai.GenerativeModel("gemini-1.5-flash")

# 🎤 Voice Input Function
def record_voice():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        try:
            print("🎤 Listening... Please speak.")
            audio = recognizer.listen(source, timeout=6)
            text = recognizer.recognize_google(audio, language="hi-IN")
            return text
        except sr.UnknownValueError:
            return "⚠ Could not understand. Try again."
        except sr.RequestError:
            return "❌ STT error. Check mic or internet."
        except Exception as e:
            return f"❌ Mic Error: {str(e)}"

# 🤖 Gemini AI Response
def get_ai_response(user_input):
    if not user_input.strip():
        return "⚠ Please ask something..."
    try:
        response = model.generate_content(user_input)
        return response.text.strip() if hasattr(response, 'text') else "⚠ No response received."
    except Exception as e:
        return f"❌ Gemini Error: {str(e)}"

# 🔊 Text-to-Speech
def speak_text(text):
    try:
        lang = 'hi' if any(char in text for char in "कखगघअआइईउऊएऐओऔ") else 'en'
        tts = gTTS(text=text, lang=lang)
        file_path = tempfile.mktemp(suffix=".mp3")
        tts.save(file_path)
        return file_path
    except Exception as e:
        print("❌ TTS Error:", e)
        return None

# 💾 Save Answer
def save_answer(text):
    file_path = tempfile.mktemp(suffix=".txt")
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(text)
    return file_path

# 🚀 Gradio App
def launch_app():
    with gr.Blocks(theme=gr.themes.Soft()) as app:
        gr.Markdown("## 📚 StudyMate AI – Gemini Based Smart Assistant")

        with gr.Row():
            mic_button = gr.Button("🎤 Speak Your Question")
            user_input = gr.Textbox(placeholder="Ask any question...", label="🧠 Your Question")
            submit_button = gr.Button("🔍 Ask Gemini")

        ai_output = gr.Textbox(label="📘 Gemini's Answer", lines=8)
        tts_button = gr.Button("🔊 Speak Answer")
        save_button = gr.Button("💾 Save Answer")
        audio_output = gr.Audio(label="🔈 Audio Output", autoplay=True)

        # 🔁 Event Bindings
        mic_button.click(fn=record_voice, outputs=user_input)
        submit_button.click(fn=get_ai_response, inputs=user_input, outputs=ai_output)
        tts_button.click(fn=speak_text, inputs=ai_output, outputs=audio_output)
        save_button.click(fn=save_answer, inputs=ai_output, outputs=gr.File(label="📥 Download Answer"))

    app.launch()
# 🟢 Run
if __name__ == "__main__":
    launch_app()

 