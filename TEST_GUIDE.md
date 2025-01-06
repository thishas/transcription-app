# Transcription App Test Guide

## Table of Contents
- [Test Environment Setup](#test-environment-setup)
- [Testing Strategy](#testing-strategy)
- [Test Cases](#test-cases)
- [Performance Testing](#performance-testing)
- [Continuous Integration](#continuous-integration)

## Test Environment Setup

### Prerequisites
```bash
# Install test dependencies
pip install pytest
pip install pytest-cov
pip install pytest-mock
```

### Test Configuration
```python
# pytest.ini
[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
```

## Testing Strategy

### 1. Unit Tests
Test individual components in isolation:
- GUI elements
- Audio processing
- Transcription logic
- Translation functionality

### 2. Integration Tests
Test component interactions:
- Audio capture → Transcription
- Transcription → Translation
- GUI → Backend communication

### 3. System Tests
Test complete workflows:
- End-to-end transcription
- Full translation pipeline
- GUI functionality

### 4. Performance Tests
- Response time
- Resource usage
- Memory leaks
- Long-running stability

## Test Cases

### 1. GUI Tests
```python
def test_gui_initialization():
    """Test GUI component initialization"""
    app = TranscriptionApp(tk.Tk())
    assert app.mic_dropdown is not None
    assert app.model_dropdown is not None
    assert app.translation_var is not None

def test_button_states():
    """Test button state changes"""
    app = TranscriptionApp(tk.Tk())
    assert app.start_button.cget("text") == "Start Transcription"
    app.toggle_transcription()
    assert app.start_button.cget("text") == "Stop Transcription"
```

### 2. Audio Processing Tests
```python
def test_audio_capture():
    """Test microphone input capture"""
    with mock.patch('speech_recognition.Recognizer') as mock_recognizer:
        mock_recognizer.return_value.listen.return_value = mock_audio_data
        # Test implementation

def test_audio_conversion():
    """Test audio data conversion"""
    audio_data = get_test_audio()
    numpy_array = convert_to_numpy(audio_data)
    assert numpy_array.dtype == np.float32
```

### 3. Transcription Tests
```python
def test_whisper_model():
    """Test Whisper model transcription"""
    model = whisper.load_model("tiny")
    result = model.transcribe(test_audio_data)
    assert isinstance(result["text"], str)
    assert len(result["text"]) > 0

def test_transcription_accuracy():
    """Test transcription accuracy with known audio"""
    known_text = "Hello, this is a test."
    audio = generate_test_audio(known_text)
    result = transcribe_audio(audio)
    assert result.lower() == known_text.lower()
```

### 4. Translation Tests
```python
def test_translator_initialization():
    """Test translator setup"""
    translator = Translator("en", "es")
    assert translator.model is not None
    assert translator.tokenizer is not None

def test_translation_accuracy():
    """Test translation accuracy"""
    translator = Translator("en", "es")
    english_text = "Hello, how are you?"
    spanish_text = translator.translate([english_text])[0]
    assert spanish_text == "¿Hola, cómo estás?"
```

## Performance Testing

### 1. Response Time Tests
```python
def test_transcription_speed():
    """Test transcription response time"""
    start_time = time.time()
    result = transcribe_audio(test_audio)
    end_time = time.time()
    assert end_time - start_time < 5.0  # Max 5 seconds
```

### 2. Memory Usage Tests
```python
def test_memory_usage():
    """Test memory consumption"""
    import memory_profiler
    
    @memory_profiler.profile
    def measure_memory():
        app = TranscriptionApp(tk.Tk())
        app.start_transcription()
        time.sleep(60)
        app.stop_transcription()
```

### 3. Load Tests
```python
def test_continuous_operation():
    """Test long-running stability"""
    app = TranscriptionApp(tk.Tk())
    for _ in range(100):
        app.start_transcription()
        time.sleep(10)
        app.stop_transcription()
        assert app.transcription_thread is None
```

## Continuous Integration

### GitHub Actions Workflow
```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.10'
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
        pip install -r test-requirements.txt
    - name: Run tests
      run: |
        pytest --cov=. --cov-report=xml
    - name: Upload coverage
      uses: codecov/codecov-action@v2
```

## Test Data

### Sample Audio Files
- `test_audio/clear_speech.wav`
- `test_audio/background_noise.wav`
- `test_audio/multiple_speakers.wav`

### Expected Results
```json
{
  "clear_speech.wav": {
    "text": "This is a test audio file",
    "confidence": 0.95
  },
  "background_noise.wav": {
    "text": "Testing with background noise",
    "confidence": 0.75
  }
}
```

## Bug Reporting

When filing bug reports, include:
1. Test case that reproduces the bug
2. Expected vs actual behavior
3. System information
4. Relevant logs

## Test Coverage Goals

Maintain minimum coverage:
- Lines: 80%
- Branches: 70%
- Functions: 90%

## Automated Testing Schedule

1. **On Every Push**
   - Unit tests
   - Integration tests
   - Linting

2. **Nightly**
   - Performance tests
   - Memory tests
   - Long-running tests

3. **Weekly**
   - Full system tests
   - Coverage analysis
   - Dependency updates
