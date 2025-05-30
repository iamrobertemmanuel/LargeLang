import subprocess
import sys
import os

def check_ollama():
    try:
        import requests
        response = requests.get("http://localhost:11434/api/tags")
        if response.status_code == 200:
            print("✅ Ollama is running")
            return True
    except:
        print("❌ Ollama is not running")
        print("Please install Ollama from https://ollama.ai/download and start it")
        return False

def setup_environment():
    print("Setting up the environment...")
    
    # Check if Python version is compatible
    if sys.version_info < (3, 8):
        print("Python 3.8 or higher is required")
        sys.exit(1)
    
    # Install requirements
    print("Installing requirements...")
    subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
    
    # Check if Ollama is installed and running
    if not check_ollama():
        print("Please install and start Ollama before continuing")
        sys.exit(1)
    
    # Initialize the database
    print("Initializing database...")
    subprocess.run([sys.executable, "database_operations.py"])
    
    print("\n✨ Setup completed successfully!")
    print("\nTo start the application, run:")
    print("streamlit run app.py")

if __name__ == "__main__":
    setup_environment() 