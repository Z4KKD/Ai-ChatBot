# OpenAI OMDb Chatbot

A Django-based chatbot powered by OpenAI's GPT-3.5-turbo model, integrated with the OMDb API to fetch movie details and provide personalized movie recommendations. Users can chat with the bot, ask for movie information, and get context-based follow-up responses.

---

## 💬 Features

- 🔗 **Powered by OpenAI GPT-3.5-turbo** for more efficient, multi-turn conversations
- 🎬 **Movie info lookup** using the OMDb API
- 🧠 **Intent Classification** to categorize user input (e.g., movie information, greetings, recommendations, etc.)
- 🧑‍💻 **Movie Recommendations** based on user input and preferences
- 🔁 **Contextual Q&A**: Ask follow-up questions like "Who directed it?" after receiving movie details
- 💾 **Stores conversation history** (for context-based responses and future improvements)
- 💻 **Built with Django (Python)** for easy setup and scalability
- 🎨 **Simple yet elegant UI** with a dark theme and green accents, designed for a smooth user experience

---

## 🛠️ Tech Stack

- **Backend**: Django (Python)
- **Frontend**: HTML, CSS, JavaScript
- **APIs**: OpenAI GPT-3.5-turbo, OMDb
- **Machine Learning**: Scikit-learn for intent classification
- **Database**: SQLite (Optional for storing conversation history)

---

## 🚀 Getting Started

### 1. Clone the repo

git clone https://github.com/Z4KKD/Ai-ChatBot  
cd openai-omdb-chatbot

### 2. Install dependencies

Make sure you have Python and pip:

pip install -r requirements.txt

### 3. Add your API keys

In `views.py`:

- Replace `"your_openai_api_key_here"` with your actual OpenAI API key
- Replace `"your_omdb_api_key_here"` with your OMDb API key

For improved security, consider using environment variables instead of hardcoding the keys.

### 4. Run the server

python manage.py runserver

Navigate to `http://127.0.0.1:8000` in your browser to start chatting!

---

## 🧪 Running Tests

You can run basic tests with:

python manage.py test

---

## 📂 Project Structure

chatbot_project/  
│  
├── chatbot_app/  
│   ├── views.py         # Core logic for chatbot & API handling  
│   ├── templates/  
│   │   └── chatbot_app/  
│   │       └── chatbot.html  # Frontend UI  
│   ├── static/  
│   │   └── chatbot_app/  
│   │       ├── styles.css  # CSS for the UI  
│   │       └── chatbot.js  # JavaScript for frontend interaction  
│   └── tests/  
│       └── test_views.py     # View tests  
│  
├── manage.py  
├── requirements.txt  
└── README.md

---

## ✨ Future Improvements

- **Persistent conversation history** with a database or session management
- **Switch to GPT-4** for even more powerful conversational abilities
- **Refactor UI** with a CSS framework (e.g., Bootstrap, Tailwind) for a more polished look
- **Docker support** for easier deployment
- **Add more test cases** to ensure robustness

---

## 🤖 Built by Z4KKD
