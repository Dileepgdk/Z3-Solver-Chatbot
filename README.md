# 🔢 Z3 Equation Solver Chatbot (Flask + Z3 + JS)

This is a chatbot-style web app that allows users to solve equations (single or systems) using the Z3 Theorem Prover, powered by a Python Flask backend and a modern JavaScript frontend.

---

## ✨ Features

- Solve single equations like `2x + 3 = 9`
- Solve systems like: x + y = 10 x - y = 4

- - Evaluate arithmetic expressions: `4 + 5 * 3`
- Supports float and integer values
- Clean chat-like UI for interaction
- Frontend built in HTML/CSS/JavaScript
- Backend built with Python (Flask + Z3)

---

## 🧠 Technologies Used

- **Frontend**: HTML, CSS, JavaScript
- **Backend**: Python, Flask
- **Solver**: [Z3 Theorem Prover]
- **Deployment**: GitHub Pages (frontend) + Render (backend)

---

Deployment

Backend on Render
Add gunicorn to requirements.txt

Set start command as: gunicorn app:app

Enable CORS in app.py for frontend access:
from flask_cors import CORS
CORS(app)




🧮 Example Inputs
2x + 3 = 9

x + y = 10; x - y = 2

5 * (3 + 2)

a = b + 1; b = c + 2; c = 3
