# Local Multimodal AI Chat
## Getting Started

To get started with Local Multimodal AI Chat, follow these simple steps:

### Prerequisites

1. **Python**: Python 3.8 or higher is required
2. **Ollama**: Install [Ollama](https://ollama.com/download) for your platform

### Installation and Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Leon-Sander/Local-Multimodal-AI-Chat.git
   cd Local-Multimodal-AI-Chat
   ```

2. **Run the setup script**:
   ```bash
   python setup.py
   ```
   This will:
   - Install all required dependencies
   - Check if Ollama is running
   - Initialize the database

3. **Start the application**:
   ```bash
   streamlit run app.py
   ```

4. **Pull Required Models**: 
   - Open [localhost:8501](http://localhost:8501) in your browser
   - Go to https://ollama.com/library and choose the models you want to use
   - Enter `/pull MODEL_NAME` in the chat bar
   - You need:
     - One embedding model (e.g. [nomic-embed-text](https://ollama.com/library/nomic-embed-text)) for PDF files
     - One model that understands images (e.g. [llava](https://ollama.com/library/llava))

5. **Optional Configuration**: 
   - Check the `config.yaml` file and adjust settings to your needs
   - Place your custom `user_image.png` and/or `bot_image.png` inside the `chat_icons` folder

## Overview

Local Multimodal AI Chat is a multimodal chat application that integrates various AI models to manage audio, images, and PDFs seamlessly within a single interface. This application is ideal for those passionate about AI and software development, offering a comprehensive solution that employs Whisper AI for audio processing, LLaVA for image management, and Chroma DB for handling PDFs.

The application has been enhanced with the Ollama server and the OpenAI API, boosting its functionality and performance. You can find a detailed tutorial on the development of this repository on my [youtube channel](https://youtu.be/CUjO8b6_ZuM). While significant advancements have been made, the project is still open to further development and refinement.

I welcome contributions of all forms. Whether you're introducing new features, optimizing the code, or correcting bugs, your participation is valued. This project thrives on community collaboration and aims to serve as a robust resource for those interested in the practical application of multimodal AI technologies.


## Features

- **Local Model Processing with Ollama**: This app utilizes the Ollama server for running local instances of models, providing a powerful and customizable AI experience without the need for external cloud dependencies. This setup is ideal for maintaining data privacy and improving response times.

- **Integration with OpenAI API**: For broader AI capabilities, this application also connects to the OpenAI API, enabling access to a wide range of cutting-edge AI models hosted externally. This feature ensures the app remains versatile and capable of handling a variety of tasks and queries efficiently.

- **Audio Chatting with Whisper AI**: Leveraging Whisper AI's robust transcription capabilities, this app offers a sophisticated audio messaging experience. The integration of Whisper AI allows for accurate interpretation and response to voice inputs, enhancing the natural flow of conversations.
[Whisper models](https://huggingface.co/collections/openai/whisper-release-6501bba2cf999715fd953013)

- **PDF Chatting with Chroma DB**: The app is tailored for both professional and academic uses, integrating Chroma DB as a vector database for efficient PDF interactions. This feature allows users to engage with their own PDF files locally on their device. This makes it a valuable tool for personal use, where one can extract insights, summaries, and engage in a unique form of dialogue with the text in their PDF files. [Chroma website](https://docs.trychroma.com/)

## Changelog

### 16.09.2024:
- **Big Update**: Model Serving based on Ollama API now. Added Openai API.

<details>
  <summary>Click to see more!</summary>

### 24.08.2024:
- **Docker Compose Added**

### 17.02.2024:
- **Input Widget Update**: Replaced st.text_input with st.chat_input to enhance interaction by leveraging a more chat-oriented UI, facilitating user engagement.
- **Sidebar Adjustment**: Relocated the audio recording button to the sidebar for a cleaner and more organized user interface, improving accessibility and user experience.

### 10.02.2024:
- **License Added**: Implemented the GNU General Public License v3.0 to ensure the project is freely available for use, modification, and distribution under the terms of this license. A comprehensive copyright and license notice has been included in the main file (app.py) to clearly communicate the terms under which the project is offered. This addition aims to protect both the contributors' and users' rights, fostering an open and collaborative development environment. For full license details, refer to the LICENSE file in the project repository.
- **Caching for Chat Model**: Introduced caching for the chat model to prevent it from being reloaded with every script execution. This optimization significantly improves performance by reducing load times 
- **Config File Expansion**: Expanded the configuration file to accommodate new settings and features, providing greater flexibility and customization options for the chat application.


### 09.02.2024:

- **SQLite Database for Chat History**: Implemented a SQLite database to store the chat history.
- **Displaying Images and Audio Files in Chat**: Chat history now supports displaying images and audio files.
- **Added Button to delete Chat History**
- **Updated langchain**: Runs now with the current langchain version 0.1.6

### 16.01.2024:
- **Windows User DateTime Format Issue:** Windows users seemed to have problems with the datetime format of the saved JSON chat histories. I changed the format in the `ultis.py` file to `"%Y_%m_%d_%H_%M_%S"`, which should solve the issue. Feel free to change it to your liking.
- **UI Adjustment for Chat Scrolling:** Scrolling down in the chat annoyed me, so the text input box and the latest message are at the top now.

### 12.01.2024:
- **Issue with Message Sending:** After writing in the text field and pressing the send button, the LLM would not generate a response. 
- **Cause of the Issue:** This happened because the `clear_input_field` callback from the button changes the text field value to an empty string after saving the user question. However, changing the text field value triggers the callback from the text field widget, setting the `user_question` to an empty string again. As a result, the LLM is not called.
- **Implemented Workaround:** As a workaround, I added a check before changing the `user_question` value.
</details>


## Possible Improvements
- ~~Add Model Caching.~~
- ~~Add Images and Audio to Chat History Saving and Loading.~~
- ~~Use a Database to Save the Chat History.~~
- Integrate ~~Ollama, OpenAI,~~ Gemini, or Other Model Providers.
- Add Image Generator Model.
- Authentication Mechanism.
- Change Theme.
- ~~Separate Frontend and Backend Code for Better Deployment.~~

## Contact Information

If you're interested in working with me, feel free to contact me via email.
Before contacting me because of errors you're encountering, make sure to check the github issues first: https://github.com/Leon-Sander/Local-Multimodal-AI-Chat/issues?q=

- Email: leonsander.consulting@gmail.com
- Twitter: [@leonsanderai](https://twitter.com/leonsanderai)
