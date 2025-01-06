@echo off
call %UserProfile%\Miniconda3\Scripts\activate.bat
call conda activate transcribe
python transcribe.py
pause
