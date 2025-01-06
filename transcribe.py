import argparse
import json
import numpy as np
import os
import speech_recognition as sr
import whisper
import torch
import pyautogui
import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from datetime import datetime, timedelta
from queue import Queue
from threading import Thread
from time import sleep
from transformers import MarianMTModel, MarianTokenizer
from PIL import Image
from faster_whisper import WhisperModel
import pyaudio
import wave


class Translator:
    def __init__(self) -> None:
        # Initialize English to Spanish translator
        self.model_name = 'Helsinki-NLP/opus-mt-en-es'
        print("Loading translation model...")
        self.model = MarianMTModel.from_pretrained(self.model_name)
        self.tokenizer = MarianTokenizer.from_pretrained(self.model_name)
        print("Translation model loaded")

    def translate(self, text):
        try:
            tokens = self.tokenizer([text], return_tensors="pt", padding=True)
            translate_tokens = self.model.generate(**tokens)
            return self.tokenizer.decode(translate_tokens[0], skip_special_tokens=True)
        except Exception as e:
            print(f"Translation error: {e}")
            return f"Translation error: {str(e)}"


class TranscriptionApp:
    def __init__(self, master):
        self.master = master
        self.master.title("English to Spanish Transcription")
        self.master.geometry("800x800")  # Made window even larger for better text display
        self.master.protocol("WM_DELETE_WINDOW", self.on_close)

        # Create necessary directories with timestamp-based naming
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.session_dir = os.path.join('sessions', self.timestamp)
        os.makedirs(self.session_dir, exist_ok=True)

        # Center window on screen
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        x = (screen_width - 800) // 2
        y = (screen_height - 800) // 2
        self.master.geometry("+{}+{}".format(x, y))

        # Create main frames
        control_frame = ctk.CTkFrame(self.master)
        control_frame.pack(fill="x", padx=10, pady=5)

        text_frame = ctk.CTkFrame(self.master)
        text_frame.pack(fill="both", expand=True, padx=10, pady=5)

        # Add controls to control frame
        self.create_microphone_selection(control_frame)
        self.create_model_selection(control_frame)
        
        # Status label with larger font
        self.status_label = ctk.CTkLabel(control_frame, text="Ready", font=("Arial", 14, "bold"))
        self.status_label.pack(pady=5)

        # Create text display
        self.create_text_display(text_frame)

        # Initialize components
        self.transcription_in_progress = False
        self.transcription_thread = None
        self.stop_transcription_flag = False
        print("Initializing translator...")
        self.translator = Translator()
        self.current_audio_file = None
        self.current_transcript_file = None
        self.recording_thread = None

        # Start/Stop button with larger font
        self.start_button = ctk.CTkButton(
            control_frame, 
            text="Start Recording", 
            command=self.toggle_transcription,
            font=("Arial", 14, "bold"),
            height=40
        )
        self.start_button.pack(pady=10)

    def get_microphone_list(self):
        try:
            p = pyaudio.PyAudio()
            input_devices = []
            
            for i in range(p.get_device_count()):
                try:
                    info = p.get_device_info_by_index(i)
                    if info.get('maxInputChannels', 0) > 0:
                        print(f"Found input device: {info['name']}")
                        input_devices.append(info['name'])
                except Exception as e:
                    print(f"Error checking device {i}: {e}")
                    continue
            
            p.terminate()
            return input_devices if input_devices else ["Default Microphone"]
            
        except Exception as e:
            print(f"Error getting microphones: {e}")
            return ["Default Microphone"]

    def create_microphone_selection(self, frame):
        mic_frame = ctk.CTkFrame(frame)
        mic_frame.pack(pady=5)

        mic_label = ctk.CTkLabel(mic_frame, text="Select Microphone:", font=("Arial", 12))
        mic_label.grid(row=0, column=0, padx=10)

        self.mic_var = ctk.StringVar()
        mic_options = self.get_microphone_list()
        self.mic_dropdown = ctk.CTkComboBox(
            mic_frame, 
            variable=self.mic_var, 
            values=mic_options, 
            state="readonly",
            font=("Arial", 12),
            width=300
        )
        self.mic_dropdown.set(mic_options[0])
        self.mic_dropdown.grid(row=0, column=1)

    def create_model_selection(self, frame):
        model_frame = ctk.CTkFrame(frame)
        model_frame.pack(pady=5)

        model_label = ctk.CTkLabel(model_frame, text="Select Model:", font=("Arial", 12))
        model_label.grid(row=0, column=0, padx=10)

        self.model_var = ctk.StringVar()
        model_options = ["tiny", "base", "small", "medium", "large"]
        self.model_dropdown = ctk.CTkComboBox(
            model_frame, 
            variable=self.model_var, 
            values=model_options, 
            state="readonly",
            font=("Arial", 12)
        )
        self.model_dropdown.set("base")
        self.model_dropdown.grid(row=0, column=1)

    def create_text_display(self, frame):
        # Create text widget for displaying transcription with larger font
        self.text_display = ctk.CTkTextbox(
            frame, 
            wrap="word", 
            height=500,  # Made taller
            font=("Arial", 14)  # Larger font
        )
        self.text_display.pack(fill="both", expand=True, padx=10, pady=5)
        self.text_display.configure(state="disabled")
        
        # Add initial instructions
        self.update_text_display(
            "Welcome to English to Spanish Transcription\n" + 
            "----------------------------------------\n" +
            "1. Select your microphone\n" +
            "2. Click 'Start Recording'\n" +
            "3. Speak in English\n" +
            "4. Your speech will be transcribed and translated in real-time\n" +
            "5. All recordings and transcripts are automatically saved\n\n"
        )

    def update_text_display(self, text, clear_first=False):
        self.text_display.configure(state="normal")
        if clear_first:
            self.text_display.delete("1.0", "end")
        self.text_display.insert("end", text + "\n")
        self.text_display.see("end")
        self.text_display.configure(state="disabled")
        # Force update the display
        self.master.update_idletasks()

    def toggle_transcription(self):
        if not self.transcription_in_progress:
            self.start_transcription()
        else:
            self.stop_transcription()

    def start_recording(self):
        # Create audio file with same timestamp
        self.current_audio_file = os.path.join(self.session_dir, f'recording.wav')
        self.recording_thread = Thread(target=self.record_audio, daemon=True)
        self.recording_thread.start()

    def record_audio(self):
        CHUNK = 1024
        FORMAT = pyaudio.paInt16
        CHANNELS = 1
        RATE = 44100

        p = pyaudio.PyAudio()
        selected_mic = self.mic_var.get()
        
        # Get the device index for the selected microphone
        mic_index = None
        for i in range(p.get_device_count()):
            info = p.get_device_info_by_index(i)
            if info.get('name') == selected_mic:
                mic_index = i
                break

        if mic_index is None:
            print("Error: Could not find selected microphone")
            return

        stream = p.open(format=FORMAT,
                       channels=CHANNELS,
                       rate=RATE,
                       input=True,
                       input_device_index=mic_index,
                       frames_per_buffer=CHUNK)

        frames = []
        self.status_label.configure(text="Recording...")

        while not self.stop_transcription_flag:
            try:
                data = stream.read(CHUNK)
                frames.append(data)
            except Exception as e:
                print(f"Error recording audio: {e}")
                break

        stream.stop_stream()
        stream.close()
        p.terminate()

        # Save the recorded audio
        if frames:
            wf = wave.open(self.current_audio_file, 'wb')
            wf.setnchannels(CHANNELS)
            wf.setsampwidth(p.get_sample_size(FORMAT))
            wf.setframerate(RATE)
            wf.writeframes(b''.join(frames))
            wf.close()

    def start_transcription(self):
        self.transcription_in_progress = True
        self.stop_transcription_flag = False
        self.start_button.configure(text="Stop Recording")
        self.status_label.configure(text="Loading model...")

        # Clear text display
        self.update_text_display("Starting new transcription session...\n", clear_first=True)

        # Create transcript file
        self.current_transcript_file = os.path.join(self.session_dir, 'transcript.txt')
        with open(self.current_transcript_file, 'w', encoding='utf-8') as f:
            f.write(f"Transcription Session - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")

        # Start recording
        self.start_recording()

        # Start transcription
        self.transcription_thread = Thread(
            target=self.transcribe_audio, daemon=True)
        self.transcription_thread.start()

    def stop_transcription(self):
        self.stop_transcription_flag = True
        self.transcription_in_progress = False
        self.start_button.configure(text="Start Recording")
        self.status_label.configure(text="Stopped")
        
        # Add end timestamp to transcript file
        if self.current_transcript_file:
            try:
                with open(self.current_transcript_file, 'a', encoding='utf-8') as f:
                    f.write(f"\nSession ended at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            except Exception as e:
                print(f"Error writing end timestamp: {e}")

    def save_transcription(self, english_text, spanish_text):
        if self.current_transcript_file:
            try:
                with open(self.current_transcript_file, 'a', encoding='utf-8') as f:
                    timestamp = datetime.now().strftime('%H:%M:%S')
                    f.write(f"\n[{timestamp}]\n")
                    f.write(f"English: {english_text}\n")
                    f.write(f"Spanish: {spanish_text}\n")
            except Exception as e:
                print(f"Error saving transcription: {e}")

    def transcribe_audio(self):
        model = whisper.load_model(self.model_var.get())
        self.status_label.configure(text="Transcribing...")

        r = sr.Recognizer()
        selected_mic = self.mic_var.get()
        
        # Get the device index for the selected microphone
        p = pyaudio.PyAudio()
        mic_index = None
        for i in range(p.get_device_count()):
            info = p.get_device_info_by_index(i)
            if info.get('name') == selected_mic:
                mic_index = i
                break
        p.terminate()
        
        if mic_index is None:
            self.status_label.configure(text="Error: Could not find selected microphone")
            return

        with sr.Microphone(device_index=mic_index) as source:
            while not self.stop_transcription_flag:
                try:
                    audio = r.listen(source, timeout=2.0)
                    audio_data = np.frombuffer(
                        audio.get_raw_data(), dtype=np.int16).flatten().astype(np.float32) / 32768.0

                    result = model.transcribe(audio_data)
                    english_text = result["text"].strip()

                    if english_text:
                        # Translate to Spanish
                        spanish_text = self.translator.translate(english_text)
                        
                        # Format display text with clear separation
                        timestamp = datetime.now().strftime('%H:%M:%S')
                        display_text = (
                            f"\n[{timestamp}]\n"
                            f"English: {english_text}\n"
                            f"Spanish: {spanish_text}\n"
                            f"----------------------------------------"
                        )
                        
                        # Update display immediately
                        self.master.after(0, self.update_text_display, display_text)
                        
                        # Save transcription
                        self.save_transcription(english_text, spanish_text)

                except sr.WaitTimeoutError:
                    continue
                except Exception as e:
                    print(f"Error during transcription: {str(e)}")
                    self.status_label.configure(text=f"Error: {str(e)}")
                    sleep(2)

    def on_close(self):
        self.stop_transcription()
        self.master.destroy()


def main():
    root = ctk.CTk()
    app = TranscriptionApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
