 ![Python](https://img.shields.io/badge/Python-3.8+-3776AB.svg?logo=python&logoColor=white)
 ![License](https://img.shields.io/badge/License-MIT-blue.svg)
 ![Groq API](https://img.shields.io/badge/Groq-API-4B9B5F.svg)
 ![Status](https://img.shields.io/badge/Status-Active-green.svg)

 **MultiAgent Chain of Expert** is an advanced Python application designed for sophisticated text processing using the Groq API. It employs a dual-model architecture, leveraging Gemma for in-depth input analysis and LLaMA for generating polished, context-aware responses. The application features a modern, dark-themed GUI built with `tkinter` and `ttkbootstrap`, offering a seamless user experience with history tracking, file handling, and customizable AI parameters.

 ## 🌟 Features

 - **Dual-Model AI Processing**: Combines Gemma for structured analysis and LLaMA for comprehensive responses.
 - **Modern User Interface**: Sleek, dark-themed GUI with intuitive controls, progress bars, and real-time feedback.
 - **History Management**: Saves processing history in JSON format for easy review and retrieval.
 - **Flexible Configuration**: Adjust AI parameters (temperature, max tokens) via a dedicated settings panel.
 - **Robust File Handling**: Supports loading text files, saving results as TXT or JSON, and clipboard operations.
 - **Secure API Integration**: Manages Groq API keys securely using `python-dotenv` and `.env` files.
 - **Error Handling & Feedback**: Provides clear error messages and API connection status monitoring.

 ## 📦 Installation

 Follow these steps to set up the project locally:

 1. **Clone the Repository**:
    ```bash
    git clone https://github.com/Arash-Mansourpour/MultiAgent-Chain-of-Expert.git
    cd MultiAgent-Chain-of-Expert
    ```

 2. **Install Dependencies**:
    Ensure Python 3.8+ is installed, then run:
    ```bash
    pip install -r requirements.txt
    ```

 3. **Set Up Environment Variables**:
    Create a `.env` file in the project root and add your Groq API key:
    ```
    GROQ_API_KEY=your-groq-api-key-here
    ```

 4. **Run the Application**:
    ```bash
    python multi-agent.py
    ```

 ## 🚀 Usage

 1. **Input Text**: Enter your query or text in the input area.
 2. **Configure Settings**: Adjust AI parameters (temperature, max tokens) in the Settings tab if needed.
 3. **Process**: Click "Process Text" to generate analysis (Gemma) and final response (LLaMA).
 4. **Review & Save**: View results in dedicated panels, copy to clipboard, save as TXT/JSON, or access past interactions via the History tab.

 ## 📋 Requirements

 - **Python**: 3.8 or higher
 - **Dependencies**:
   - `ttkbootstrap`: For modern GUI styling
   - `groq`: For API integration
   - `python-dotenv`: For secure API key management
   - See `requirements.txt` for a complete list

 Install dependencies:
 ```bash
 pip install ttkbootstrap groq python-dotenv
 ```

 ## 🔒 Security

 - **API Key**: Store your Groq API key in a `.env` file, which is excluded from version control via `.gitignore`.
 - **Data Privacy**: History and configuration files (`ai_processor_history.json`, `ai_processor_config.json`) are stored locally and not tracked in the repository.

 ## 🛠 Project Structure

 ```
 MultiAgent-Chain-of-Expert/
 ├── multi-agent.py         # Main application code
 ├── requirements.txt       # Project dependencies
 ├── .gitignore            # Ignored files and directories
 ├── .env.example          # Sample environment file
 ├── LICENSE               # MIT License
 └── README.md             # Project documentation
 ```

 ## 🤝 Contributing

 Contributions are welcome! To contribute:

 1. Fork the repository.
 2. Create a new branch (`git checkout -b feature/your-feature`).
 3. Commit your changes (`git commit -m "Add your feature"`).
 4. Push to the branch (`git push origin feature/your-feature`).
 5. Open a Pull Request.

 Please ensure your code adheres to PEP 8 guidelines and includes appropriate documentation.

 ## 📜 License

 This project is licensed under the [MIT License](LICENSE).

 ## 📬 Contact

 For questions or feedback, reach out to [Arash Mansourpour](https://github.com/Arash-Mansourpour) or open an issue on this repository.

 ---

 **Built with 💡 and powered by Groq API**
