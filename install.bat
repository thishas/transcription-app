@echo off
echo Installing Miniconda...
powershell -Command "Invoke-WebRequest -Uri https://repo.anaconda.com/miniconda/Miniconda3-latest-Windows-x86_64.exe -OutFile miniconda.exe"
start /wait "" miniconda.exe /S /D=%UserProfile%\Miniconda3
del miniconda.exe

echo Creating conda environment...
call %UserProfile%\Miniconda3\Scripts\activate.bat
call conda create -n transcribe python=3.10 -y
call conda activate transcribe

echo Installing requirements...
pip install -r requirements.txt

echo Installation complete!
pause
