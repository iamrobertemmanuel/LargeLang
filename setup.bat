@echo off
echo Creating virtual environment...
"C:\Users\benne\AppData\Local\Programs\Python\Python312\python.exe" -m venv .venv

echo Activating virtual environment...
call .venv\Scripts\activate.bat

echo Installing packages...
python -m pip install --upgrade pip
pip install google-generativeai streamlit pillow python-dotenv requests pypdfium2 pyyaml streamlit-mic-recorder pydub numpy

echo Setup complete! Run 'streamlit run app.py' to start the application. 