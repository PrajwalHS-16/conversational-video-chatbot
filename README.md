🎬 Video Q&A Chatbot
An AI-powered chatbot to watch your video, summarize it, and answer your questions about frames, objects, and colors — built with Python, 🤗 Transformers, and Gradio.

✨ Features
✅ Upload a short video (.mp4)
✅ Generates frame-by-frame captions using BLIP
✅ Summarizes the video with a text generation model
✅ Ask questions like:

"Describe frame 2"

"What color is the horse?"

"What is happening?"

✅ Simple web UI using Gradio

🛠 Requirements
Python 3.8+

pip

📦 Installation
Clone this repo:

bash
Copy code
git clone https://github.com/yourname/video-qa-bot.git
cd video-qa-bot
Install dependencies:

bash
Copy code
pip install -r requirements.txt
Note: First run may download ~1–2 GB of pre-trained models (only once).

▶ Usage
Run the app:

bash
Copy code
python app.py
Then open the link shown in terminal (e.g., http://127.0.0.1:7860).

📂 Project structure
bash
Copy code
video_qa_bot/
├── app.py                   # Gradio UI
├── video_caption_generator.py  # Captioning & Q&A logic
├── requirements.txt
└── README.md
⚙ How it works
Extracts frames from your video (default: 10 frames)

Generates captions using Salesforce/blip-image-captioning-base

Summarizes with facebook/bart-large-cnn

Answers questions with rule-based logic + text generation

💡 Tips
✅ Keep videos short (10–20 sec) for faster processing
✅ You only need to download models once
✅ You can replace models with smaller ones to save space

📜 License
MIT
