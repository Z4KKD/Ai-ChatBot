# OpenAI OMDb Chatbot

A simple Django-based chatbot powered by OpenAI's GPT model and integrated with the OMDb API to fetch movie details. Users can chat with the bot or ask for information about movies directly.

---

## 💬 Features

- 🔗 Integrated with OpenAI GPT (text-davinci-003)
- 🎬 Movie info lookup using OMDb API
- 🧠 Maintains conversation history (limited to recent messages)
- 💻 Built with Django (Python web framework)
- 🖥️ Simple HTML frontend with JavaScript for real-time interaction

---

## 🛠️ Tech Stack

- **Backend**: Django (Python)
- **Frontend**: HTML + JavaScript
- **APIs**: OpenAI, OMDb

---

## 🚀 Getting Started

### 1. Clone the repo

```bash
git clone https://github.com/your-username/openai-omdb-chatbot.git
cd openai-omdb-chatbot
```

### 2. Install dependencies

Make sure you have Python & pipenv or virtualenv:

```bash
pip install -r requirements.txt
```

### 3. Add your API keys

In your `views.py`:

- Replace `"your_openai_api_key_here"` with your actual OpenAI API key
- Replace `"your_omdb_api_key_here"` with your OMDb API key

Alternatively, you can refactor this to use environment variables for better security.

### 4. Run the server

```bash
python manage.py runserver
```

Navigate to `http://127.0.0.1:8000` in your browser.

---

## 🧪 Running Tests

Basic tests can be run with:

```bash
python manage.py test
```

---

## 📂 Project Structure

```
chatbot_project/
│
├── chatbot_app/
│   ├── views.py         # Core logic for chatbot & API handling
│   ├── templates/
│   │   └── chatbot_app/
│   │       └── chatbot.html  # Frontend UI
│   └── tests/
│       └── test_views.py     # View tests
│
├── manage.py
├── requirements.txt
└── README.md
```

---

## ✨ Future Improvements

- Add persistent conversation history (DB or session)
- Switch to `gpt-3.5-turbo` or `gpt-4` with chat-based API
- Refactor API keys to use environment variables
- Improve UI with CSS framework (Bootstrap, Tailwind)
- Add Docker support
- Add more test cases


## 🤖 Built by Z4KKD
