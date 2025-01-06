import pytest
import tkinter as tk
import numpy as np
from unittest import mock
from transcribe import TranscriptionApp, Translator

@pytest.fixture
def app():
    root = tk.Tk()
    app = TranscriptionApp(root)
    yield app
    root.destroy()

def test_app_initialization(app):
    """Test if the app initializes correctly"""
    assert app.transcription_in_progress == False
    assert app.transcription_thread is None
    assert app.translation_active == False
    assert app.translator is None

def test_microphone_selection(app):
    """Test microphone dropdown initialization"""
    assert app.mic_dropdown is not None
    assert app.mic_var is not None

def test_model_selection(app):
    """Test model dropdown initialization"""
    assert app.model_dropdown is not None
    assert app.model_var is not None
    assert app.model_var.get() == "base"  # Default model

def test_translation_options(app):
    """Test translation checkbox initialization"""
    assert app.translation_var is not None
    assert app.translation_var.get() == False  # Default disabled

def test_toggle_transcription(app):
    """Test transcription button state changes"""
    initial_text = app.start_button.cget("text")
    app.toggle_transcription()
    assert app.transcription_in_progress == True
    assert app.start_button.cget("text") != initial_text
    app.toggle_transcription()
    assert app.transcription_in_progress == False
    assert app.start_button.cget("text") == initial_text

@pytest.mark.skip(reason="Requires audio input")
def test_transcribe_audio(app):
    """Test audio transcription (requires audio input)"""
    app.start_transcription()
    assert app.transcription_thread is not None
    app.stop_transcription()
    assert app.transcription_in_progress == False

def test_translator_initialization():
    """Test translator initialization"""
    translator = Translator("en", "es")
    assert translator.model is not None
    assert translator.tokenizer is not None

@pytest.mark.skip(reason="Requires model download")
def test_translation():
    """Test text translation"""
    translator = Translator("en", "es")
    english_text = ["Hello, how are you?"]
    spanish_text = translator.translate(english_text)
    assert len(spanish_text) == 1
    assert isinstance(spanish_text[0], str)
    assert len(spanish_text[0]) > 0
