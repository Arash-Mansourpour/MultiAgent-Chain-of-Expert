MultiAgent Chain of Expert
A sophisticated Python application that leverages the Groq API to provide advanced text processing through a dual-model architecture. The system employs the Gemma model for in-depth input analysis and the LLaMA model for generating comprehensive final responses, all within a modern, user-friendly GUI built with tkinter and styled using ttkbootstrap. The application supports history tracking, file import/export, and customizable AI parameters for an enhanced user experience.
Features

Dual-Model Processing: Utilizes Gemma for detailed analysis and LLaMA for polished, context-aware responses.
Modern GUI: Dark-themed, responsive interface with intuitive controls and progress feedback.
History Management: Stores processing history in JSON format for easy retrieval and review.
Configurable Settings: Adjust AI parameters like temperature and max tokens through a dedicated settings tab.
File Handling: Supports loading text files, saving results in TXT or JSON formats, and clipboard operations.
Error Handling: Robust error management with user-friendly feedback and API connection status monitoring.

Installation

Clone the repository:git clone https://github.com/your-username/MultiAgent-Chain-of-Expert.git


Install dependencies:pip install -r requirements.txt


Set your Groq API key in a .env file:GROQ_API_KEY=your-api-key-here



Usage
Run the application:
python main.py

Enter your text in the input area, configure settings if needed, and click "Process Text" to generate analysis and final responses. Results can be copied, saved, or reviewed from the history tab.
Requirements

Python 3.8+
Dependencies: ttkbootstrap, groq, python-dotenv (see requirements.txt)

Security Note
For security, the Groq API key is not hardcoded and should be stored in a .env file, which is excluded from version control via .gitignore.
License
MIT License
