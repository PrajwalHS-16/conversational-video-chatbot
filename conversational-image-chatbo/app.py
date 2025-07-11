# app.py
import gradio as gr
import tempfile
from video_caption_generator import VideoCaptionGenerator

generator = VideoCaptionGenerator()
state = {"captions": [], "summary": ""}

def process_video(video_file):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp:
        tmp.write(video_file)
        video_path = tmp.name
    captions = generator.generate_captions(video_path)
    summary = generator.summarize(captions)
    state['captions'] = captions
    state['summary'] = summary
    msg = f"Video processed! ✨\n\n**Summary:** {summary}\n\nAsk me anything!"
    return msg, gr.update(interactive=True)

def answer(message):
    if not state["captions"]:
        return "Please upload and process a video first!"
    answer = generator.answer_question(message, state["captions"], state["summary"])
    return answer

with gr.Blocks(title="🎥 Video Q&A Bot") as demo:
    gr.Markdown("# 🎬 Video Q&A Chatbot\nUpload a video and ask questions!")
    
    video_input = gr.File(label="Upload Video", file_types=["video"], type="binary")
    process_btn = gr.Button("Process Video")
    summary_box = gr.Textbox(label="Summary", interactive=False)
    
    chatbot = gr.Chatbot(height=400)
    question = gr.Textbox(label="Ask a question...", interactive=False)
    send_btn = gr.Button("Send")

    process_btn.click(process_video, inputs=video_input, outputs=[summary_box, question])
    send_btn.click(lambda m, h: (h + [[m, answer(m)]], ""), inputs=[question, chatbot], outputs=[chatbot, question])
    question.submit(lambda m, h: (h + [[m, answer(m)]], ""), inputs=[question, chatbot], outputs=[chatbot, question])

demo.launch()
