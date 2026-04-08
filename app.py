import gradio as gr
import requests

BACKEND = "http://127.0.0.1:8000"  # change after deploy

def login():
    return f"{BACKEND}/auth/login"

def fetch_data(max_results, keyword, category):
    try:
        url = f"{BACKEND}/gmail-dashboard?max_results={max_results}"

        if keyword:
            url += f"&keyword={keyword}"
        if category:
            url += f"&category_filter={category}"

        res = requests.get(url)
        return res.json()

    except:
        return {"error": "Login first"}

with gr.Blocks() as demo:
    gr.Markdown("# 📧 AI Email Intelligence Dashboard")

    gr.Markdown("### 🔐 Step 1: Login with Gmail")
    login_btn = gr.Button("Login with Gmail")
    login_btn.click(lambda: login(), None, None)

    gr.Markdown("### 📊 Step 2: View Emails")

    max_results = gr.Slider(5, 50, value=10, label="Load Emails")
    keyword = gr.Textbox(label="Keyword Filter")
    category = gr.Dropdown(
        ["", "Promotions", "Work", "Finance", "Social", "Job"],
        label="Category Filter"
    )

    fetch_btn = gr.Button("Fetch Emails")
    output = gr.JSON()

    fetch_btn.click(fetch_data, [max_results, keyword, category], output)

demo.launch()