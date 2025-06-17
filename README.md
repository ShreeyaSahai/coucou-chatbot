# Coucou: Your French Chatbot

Bonjour! 

Welcome to Coucou, an interactive web rule-based chatbot designed to make learning basic French conversational phrases fun and engaging.

Whether you're starting from scratch or just looking to practice daily phrases, Coucou guides you through interactive dialogues and provides real-time translations.

# Features

* **Personalized Greetings:** Coucou greets you uniquely based on the time of day (Bonjour, Bon après-midi, Bonsoir, Bonne nuit).

* **Guided Conversations:** Navigate through basic French interactions, from saying hello and asking "How are you?" to introducing yourself.

* **Real-time English-to-French Translation:** Type any English sentence, and Coucou instantly translates it into French.

* **Engaging & Humorous:** Features fun, relevant memes to make the learning journey lighthearted and memorable.

* **Flexible Control:** Easily restart the conversation at any point or end the chat with a polite farewell.

# Technologies Used

This project leverages a modern web stack to deliver a seamless user experience:

* **Backend:** Python with Flask

* **Frontend:** HTML, CSS (style.css), and JavaScript (script.js)

* **Translation API:** Utilizes a self-hosted LibreTranslate instance (containerized with Docker) for powerful, on-demand language translation.

# Getting Started
Follow these steps to get Coucou up and running on your local machine.

# Prerequisites
Make sure you have the following installed:

* Python 3.x

* pip (Python package installer)

* Docker Desktop (or Docker Engine) - ensure it's running!

**1. Clone the Repository**

Open your terminal or command prompt and clone this project:
```
git clone https://github.com/ShreeyaSahai/coucou-chatbot.git
cd coucou-chatbot
```
**2. Launch the LibreTranslate Service**

Coucou relies on a local translation service. Open a separate terminal window and run the following Docker command:
```
docker run -it --rm -p 5004:5000 libretranslate/libretranslate
```
*Keep this terminal open and running while you're using the chatbot.*

**3. Set Up the Python Environment**

Back in your project's terminal (coucou-chatbot directory):

Create a Python Virtual Environment (recommended):
```
python -m venv venv
```
Activate the Virtual Environment:

* macOS / Linux:
```
source venv/bin/activate
```
* Windows (Command Prompt):
```
.\venv\Scripts\activate
```
Install Required Python Packages:
```
pip install -r requirements.txt
```
**4. Run the Flask Application**

Once the dependencies are installed and LibreTranslate is active in its own terminal, start the Flask app:
```
python app.py
```
**5. Access Coucou in Your Browser**

Open your web browser and navigate to:
```
http://127.0.0.1:5000/
```
You should now see the Coucou chatbot interface, ready to chat!

#Demo

(https://raw.githubusercontent.com/ShreeyaSahai/coucou-chatbot/main/assets/coucou_chatbot_demo.mp4)


