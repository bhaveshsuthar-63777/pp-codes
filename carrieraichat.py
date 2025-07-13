import gradio as gr
import google.generativeai as genai
import requests
from bs4 import BeautifulSoup
import fitz  # PyMuPDF for PDF extraction

# Configure Gemini API
genai.configure(api_key="enter_your_API_key")
model = genai.GenerativeModel("openAI_version")

# Extract text from PDF
def extract_pdf_text(pdf_link):
    try:
        response = requests.get(pdf_link)
        with open("career_handbook.pdf", "wb") as f:
            f.write(response.content)
        doc = fitz.open("career_handbook.pdf")
        text = ""
        for page in doc:
            text += page.get_text()
        return text.strip()
    except Exception as e:
        return f"[PDF Extraction Error]: {e}"

# Extract text from web URLs
urls = [
    "https://www.foundit.in/career-advice/top-career-option-after-10th-and-career-counselling-for-10th-class/",
    "https://www.shiksha.com/careers",
    "https://www.ncs.gov.in/",
    "https://www.oecd.org/en/topics/policy-areas/education-and-skills.html",
]

def extract_web_text(url):
    try:
        res = requests.get(url, timeout=10)
        soup = BeautifulSoup(res.text, "html.parser")
        for tag in soup(["script", "style"]):
            tag.decompose()
        return ' '.join(soup.get_text().split())
    except Exception as e:
        return f"[Web Extraction Error {url}]: {e}"

# Summarize all content
career_knowledge_base = []
for url in urls:
    raw = extract_web_text(url)
    prompt = f"""
You are a female career counselor. Summarize the following career guidance content in bullet points:
{raw}
"""
    try:
        summary = model.generate_content(prompt).text.strip()
        career_knowledge_base.append(summary)
    except Exception as e:
        print(f"Gemini Summary Error for {url}: {e}")
        continue

# Add PDF content
pdf_url = "https://www.sdseed.in/docs/Career%20Handbook.pdf"
pdf_text = extract_pdf_text(pdf_url)
pdf_prompt = f"""
You are a female career counselor. Summarize the following career guidance content from the PDF in bullet points:
{pdf_text}
"""
try:
    pdf_summary = model.generate_content(pdf_prompt).text.strip()
    career_knowledge_base.append(pdf_summary)
except Exception as e:
    print(f"PDF Summary Error: {e}")

career_after_10th = """
1. 💰 Science Stream:
   - PCM: Engineering, Architecture, Merchant Navy, NDA
   - PCB: MBBS, BDS, Pharmacy, Nursing, Biotech
   - PCMB: Open for both options

2. 📊 Commerce Stream:
   - With Maths: CA, CS, CFA, BBA, Actuarial Science
   - Without Maths: Marketing, HR, Finance, E-commerce

3. 🎨 Arts/Humanities Stream:
   - Psychology, Sociology, Journalism, UPSC, Design, Law

4. 🛀 Diploma Courses (Polytechnic):
   - Mechanical, Civil, Computer, Electrical, Fashion, Interior

5. 🎓 Vocational & Skill Based:
   - Animation, Web Development, Hotel Management, Photography

6. 💻 Certificate Courses:
   - Graphic Design, UI/UX, Coding, Mobile Repairing
"""

chat_history_log = []


def career_chat(message, chat_history, lang):
    if chat_history and chat_history[-1][0] == message:
        return chat_history, ""

    chat_history_log.append(message)
    lang_map = {
        "Hindi": "Answer fully in Hindi.",
        "English": "Answer fully in English.",
        "Hinglish": "Answer in Hinglish (mix of Hindi + English)."
    }

    prompt = f"""
Act as a female career counselor for students who just passed 10th. Speak warmly and empathetically and give output in maximum 150 words. {lang_map.get(lang, 'Answer in Hinglish')} 

User's Question: {message}

Career After 10th:
{career_after_10th}

Knowledge Base:
{''.join(career_knowledge_base)}
"""
    try:
        response = model.generate_content(prompt)
        answer = response.text.strip()
        chat_history.append((message, answer))
        return chat_history, ""
    except Exception as e:
        return chat_history + [(message, f"Error generating response: {e}")], ""

def generate_chat_summary():
    summary_prompt = f"""
You are a career summary generator AI. Based on the conversation below, provide:
- Confidence Level (Low/Medium/High) about stream selection
- Suitable Streams
- Why AI recommended it (based on answers/questions)
- 3 Best Future Careers

Chat Transcript:
{''.join(chat_history_log)}
"""
    try:
        summary = model.generate_content(summary_prompt)
        return summary.text.strip()
    except Exception as e:
        return f"[Summary Error]: {e}"

with gr.Blocks(theme=gr.themes.Soft(), css="""
#title { font-size: 2.5rem; font-weight: bold; color: #3b82f6; text-align: center; margin-top: 20px; }
#desc { font-size: 1rem; text-align: center; color: #6b7280; margin-bottom: 20px; }
#summary-box { background-color: #f0f9ff; border-radius: 10px; padding: 10px; border: 1px solid #dbeafe; }
button { background-color: #2563eb !important; color: white !important; border-radius: 10px !important; }
""") as demo:
    gr.Markdown("""<div id='title'>🎓 CareerCraft AI</div>
<div id='desc'>Talk with AI to explore your best career path after 10th class. Get stream suggestions, trending jobs, and expert advice from a female career counselor.</div>""")

    with gr.Tab("💬 Career Chat"):
        lang_dropdown = gr.Dropdown(choices=["Hinglish", "Hindi", "English"], label="Select Language", value="Hinglish")
        chatbot = gr.Chatbot()
        msg = gr.Textbox(label="Your Question")
        send_btn = gr.Button("Send")

        send_btn.click(fn=career_chat, inputs=[msg, chatbot, lang_dropdown], outputs=[chatbot, msg])

        with gr.Row():
            summary_btn = gr.Button("📏 Show My Career Summary")
            summary_output = gr.Textbox(label="🌟 AI Career Summary", lines=10, elem_id="summary-box")
            summary_btn.click(fn=generate_chat_summary, outputs=summary_output)

    demo.launch(share=True)