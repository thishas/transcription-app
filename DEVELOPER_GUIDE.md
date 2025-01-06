# Transcription App Developer's Guide

## Table of Contents
- [Architecture Overview](#architecture-overview)
- [Development Setup](#development-setup)
- [Code Structure](#code-structure)
- [Contributing Guidelines](#contributing-guidelines)
- [API Documentation](#api-documentation)
- [Testing Guidelines](#testing-guidelines)

## Architecture Overview

### Core Components

1. **GUI Layer** (`TranscriptionApp` class)
   - Built with CustomTkinter
   - Handles user interactions
   - Manages application state

2. **Audio Processing**
   - Uses `speech_recognition` for audio capture
   - Converts audio to numpy arrays
   - Handles real-time streaming

3. **Transcription Engine**
   - OpenAI's Whisper model
   - Supports multiple model sizes
   - Processes audio chunks

4. **Translation Service**
   - MarianMT transformer model
   - Handles English to Spanish translation
   - Asynchronous processing

### Data Flow
```
Microphone → Audio Capture → Whisper Model → Translation (optional) → Text Output
```

## Development Setup

### Prerequisites
```bash
# Required tools
- Python 3.10+
- Git
- Conda or Miniconda
```

### Environment Setup
```bash
# Clone repository
git clone [repository-url]
cd transcription-app

# Create conda environment
conda create -n transcribe python=3.10
conda activate transcribe

# Install dependencies
pip install -r requirements.txt
```

### IDE Configuration
- VSCode recommended settings:
  ```json
  {
    "python.linting.enabled": true,
    "python.linting.pylintEnabled": true,
    "python.formatting.provider": "black"
  }
  ```

## Code Structure

```
transcription-app/
├── transcribe.py      # Main application
├── requirements.txt   # Dependencies
├── assets/           # Static resources
│   └── images/       # UI images
├── tests/            # Test files
└── docs/            # Documentation
```

### Key Classes

1. **TranscriptionApp**
   ```python
   class TranscriptionApp:
       """Main application class handling GUI and coordination"""
   ```
   - Manages UI components
   - Coordinates audio processing
   - Handles user input

2. **Translator**
   ```python
   class Translator:
       """Handles text translation using MarianMT"""
   ```
   - Manages translation model
   - Processes text chunks
   - Handles errors

## Contributing Guidelines

### Code Style
- Follow PEP 8
- Use type hints
- Document all functions
- Keep functions focused and small

### Git Workflow
1. Fork repository
2. Create feature branch
3. Make changes
4. Run tests
5. Submit pull request

### Commit Messages
```
feat: Add new feature
fix: Fix bug
docs: Update documentation
test: Add tests
refactor: Refactor code
```

## API Documentation

### Audio Processing
```python
def transcribe_audio(self):
    """
    Captures and processes audio in real-time.
    
    Returns:
        str: Transcribed text
    
    Raises:
        sr.WaitTimeoutError: If no audio detected
    """
```

### Translation
```python
def translate(self, texts):
    """
    Translates text from English to Spanish.
    
    Args:
        texts (List[str]): Texts to translate
    
    Returns:
        List[str]: Translated texts
    """
```

## Performance Optimization

### Memory Management
- Use generators for large data
- Clear audio buffers regularly
- Implement proper cleanup

### CPU Usage
- Use appropriate model sizes
- Implement throttling
- Monitor resource usage

## Error Handling

### Best Practices
1. Use specific exceptions
2. Log errors properly
3. Provide user feedback
4. Implement graceful degradation

### Example
```python
try:
    audio = r.listen(source, timeout=2.0)
except sr.WaitTimeoutError:
    # Handle timeout
except Exception as e:
    # Log error
    logging.error(f"Error: {str(e)}")
```

## Security Considerations

1. **Input Validation**
   - Validate audio input
   - Check file permissions
   - Sanitize text output

2. **Resource Protection**
   - Limit CPU usage
   - Manage memory allocation
   - Handle large files safely

## Debugging Tips

1. Enable debug logging:
   ```python
   import logging
   logging.basicConfig(level=logging.DEBUG)
   ```

2. Use performance profiling:
   ```python
   import cProfile
   cProfile.run('main()')
   ```

## Future Development

### Planned Features
1. Multi-language support
2. Save transcriptions
3. Custom shortcuts
4. Cloud sync

### Technical Debt
- Refactor audio processing
- Improve error handling
- Add comprehensive tests
