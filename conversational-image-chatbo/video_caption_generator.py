# video_caption_generator.py
import os
from typing import List, Optional
from PIL import Image
import cv2
from transformers import BlipProcessor, BlipForConditionalGeneration, pipeline

class VideoCaptionGenerator:
    def __init__(self):
        print("Loading models...")
        self.caption_processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
        self.caption_model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")
        self.text_gen = pipeline("text2text-generation", model="facebook/bart-large-cnn")
        print("Models loaded.")

    def extract_frames(self, video_path, num_frames=10):
        cap = cv2.VideoCapture(video_path)
        total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        step = max(total // num_frames, 1)
        frames = []

        for i in range(0, total, step):
            cap.set(cv2.CAP_PROP_POS_FRAMES, i)
            ret, frame = cap.read()
            if ret:
                rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frames.append(Image.fromarray(rgb))
            if len(frames) >= num_frames:
                break
        cap.release()
        return frames

    def generate_captions(self, video_path, num_frames=10):
        frames = self.extract_frames(video_path, num_frames)
        captions = []
        for frame in frames:
            inputs = self.caption_processor(frame, return_tensors="pt")
            out = self.caption_model.generate(**inputs)
            caption = self.caption_processor.decode(out[0], skip_special_tokens=True)
            captions.append(caption)
        return captions

    def summarize(self, captions: List[str]):
        text = " ".join(captions)
        summary = self.text_gen(f"summarize: {text}", max_length=60, do_sample=False)[0]['generated_text']
        return summary

    def answer_question(self, question: str, captions: List[str], summary: str) -> str:
        q_lower = question.lower()
        if "frame" in q_lower:
            num = next((int(s) for s in q_lower.split() if s.isdigit()), None)
            if num and 1 <= num <= len(captions):
                return f"Frame {num}: {captions[num-1]}"
            return "Please specify a valid frame number."
        elif "color" in q_lower:
            return self.detect_colors(captions)
        else:
            context = f"{summary} {' '.join(captions[:3])}"
            return self.text_gen(f"Question: {question} Context: {context}", max_length=50)[0]['generated_text']

    def detect_colors(self, captions: List[str]) -> str:
        colors = ["brown", "black", "white", "gray", "green", "blue", "red", "yellow"]
        found = set()
        for c in captions:
            for color in colors:
                if color in c.lower():
                    found.add(color)
        if found:
            return f"Detected colors: {', '.join(found)}"
        return "Couldn't detect specific colors."
