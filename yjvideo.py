import cv2
import numpy as np
import os
from pydub import AudioSegment

video_path = input("Enter the path to the video file: ").strip()
if not os.path.exists(video_path):
    print("Error: Video file not found.")
    exit()

audio_path = input("Enter the path to the background music file (optional, press Enter to skip): ").strip()
if audio_path and not os.path.exists(audio_path):
    print("Error: Audio file not found.")
    exit()
intervals = []
print("Enter the time intervals for interesting clips in the format 'start end' (in seconds). Type 'done' when finished.")
while True:
    time_input = input("Enter interval (start end): ").strip()
    if time_input.lower() == "done":
        break
    try:
        start, end = map(float, time_input.split())
        intervals.append((start, end))
    except ValueError:
        print("Invalid format. Please enter two numbers separated by a space.")

if not intervals:
    print("No intervals provided. Exiting.")
    exit()

video = cv2.VideoCapture(video_path)
fps = video.get(cv2.CAP_PROP_FPS)
frame_width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
frame_size = (frame_width, frame_height)

output_path = "short_video.mp4"
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter(output_path, fourcc, fps, frame_size)

def extract_subclip(start_time, end_time):
    start_frame = int(start_time * fps)
    end_frame = int(end_time * fps)
    
    video.set(cv2.CAP_PROP_POS_FRAMES, start_frame)
    frames = []
    while video.get(cv2.CAP_PROP_POS_FRAMES) < end_frame:
        ret, frame = video.read()
        if not ret:
            break
        frames.append(frame)
    return frames
clips = []
for start, end in intervals:
    frames = extract_subclip(start, end)
    clips.extend(frames)

def add_text_to_frame(frame, text="Exciting Moments!"):
    font = cv2.FONT_HERSHEY_SIMPLEX
    color = (255, 255, 255) 
    thickness = 2
    position = (50, 50)
    cv2.putText(frame, text, position, font, 1, color, thickness)
    return frame

for frame in clips:
    frame_with_text = add_text_to_frame(frame)
    out.write(frame_with_text)

video.release()
out.release()

if audio_path:
    video_audio = AudioSegment.from_file(audio_path)
    video_audio = video_audio[:len(clips) * 1000 // fps]
    video_audio.export("background_audio.mp3", format="mp3")
    print("Background audio added successfully.")

print(f"Short video created successfully: {output_path}")
