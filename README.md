# Study Simplifier 🧠

Study Simplifier is an AI-powered educational tool designed to break down complex concepts, dense content, or difficult study questions into easy-to-understand explanations. Using Google's Gemini LLM, it tailors explanations specifically to a student's educational level.

## 🚀 Features

- **Multimodal Input Support**: 
  - **Text**: Paste complex paragraphs or specific questions.
  - **Documents**: Upload `.txt` or `.md` files for full-document analysis.
  - **Photos**: Upload photos of handwritten notes or textbooks (using AI-driven image analysis).
- **Customized Levels**: Choose from Elementary School through Expert/Professional to get the perfect explanation.
- **Modern UI**: A stunning Glassmorphism-inspired interface built with Streamlit.
- **AI-Driven Logic**: Uses `langchain` and `Gemini` for high-quality, factual simplifications with relevant analogies.

## 🛠️ Tech Stack

- **Core**: Python
- **LLM**: Google Gemini (via `langchain-google-genai`)
- **UI Framework**: Streamlit
- **Environment Management**: `uv`

## 📦 Installation

This project uses `uv` for lightning-fast dependency management.

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd Cognizant
   ```

2. **Install dependencies**:
   ```bash
   uv sync
   ```

3. **Set up Environment Variables**:
   Create a `.env` file in the root directory and add your Google API Key:
   ```env
   GEMINI_API_KEY=your_api_key_here
   ```

## 🏃 Usage

Run the application using `uv`:

```bash
uv run streamlit run simplifier_web_ui.py
```

After running, the app will be available at `http://localhost:8501`.

## 📁 Project Structure

- `simplifier_web_ui.py`: The main application entry point and UI logic.
- `pyproject.toml`: Project metadata and dependency definitions.
- `.env`: (Local only) Configuration for API keys.
- `.gitignore`: Standard git exclusions.

## 📄 License

This project is created for educational purposes.
