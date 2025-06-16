from flask import Flask, render_template, request, jsonify, session
from datetime import datetime
import requests

app = Flask(__name__)
app.secret_key = "super-secret-key"

def get_time_greeting():
    hour = datetime.now().hour
    if hour < 12:
        return "bonjour", "Good morning! Or shall I say Bonjour?"
    elif 12 <= hour < 17:
        return "bon après-midi", "Good afternoon! Or shall I say Bon après-midi?"
    elif 17 <= hour < 21:
        return "bonsoir", "Good evening! Or shall I say Bonsoir?"
    else:
        return "bonne nuit", "Oh hey... it's after 21:00. Bonne nuit means Good night!"

def get_day_and_month_french():
    french_days = ['lundi', 'mardi', 'mercredi', 'jeudi', 'vendredi', 'samedi', 'dimanche']
    french_months = ['janvier', 'février', 'mars', 'avril', 'mai', 'juin','juillet', 'août', 'septembre', 'octobre', 'novembre', 'décembre']
    now = datetime.now()
    day = french_days[now.weekday()]
    month = french_months[now.month - 1]
    return f"Aujourd'hui, c'est {day} {now.day} {month} {now.year}."

def should_end_conversation(msg):
    phrases = ["au revoir", "à demain", "a demain", "à bientôt", "a bientôt", "a bientot", "à bientot", "bye", "goodbye"]
    return any(phrase in msg for phrase in phrases)

def translate_to_french(text):
    url = "http://localhost:5004/translate" #self-hosted LibreTranslate instance running in Docker
    payload = {
        "q": text,
        "source": "en",
        "target": "fr",
        "format": "text",
    }
    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            return response.json()["translatedText"]
        else:
            print(f"Local Translation API error: Status Code {response.status_code}, Response: {response.text}")
            return "Sorry, couldn't translate that right now. (Local API error)"
    except requests.exceptions.RequestException as e:
        print(f"Local Translation service connection error: {e}")
        return "Translation service unavailable. Is LibreTranslate running locally on port 5004? (Check your Docker terminal)"
    except Exception as e:
        print(f"An unexpected error occurred during local translation: {e}")
        return "Translation service unavailable due to an unexpected error."

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_msg = request.json['message'].lower()

    if should_end_conversation(user_msg):
        mood = session.get('mood', 'neutral')

        if mood == 'positive':
            reply = "Merci et à bientôt! (Thank you and see you soon!) You're doing great — keep learning! Bonne journée (Good day!)"
        elif mood == 'negative':
            reply = "Prends soin de toi. (Take care of yourself.) See you again soon, and I hope your day gets better."
        else:
            reply = "À la prochaine! (See you next time!)"
        session.clear()
        return jsonify({'reply': reply})

    if "start over" in user_msg:
        session.clear()
        return jsonify({'reply': "Let's begin again. Say 'hello' to start!"})

    time_greeting, bot_greeting = get_time_greeting()
    state = session.get('state', 'start')

    if state == "start":
        if "hello" in user_msg or "hi" in user_msg:
            reply = f"{bot_greeting} Try saying '{time_greeting}' in French!"
            session['state'] = "waiting_for_greeting"
        else:
            reply = "Say 'hello' or 'hi' to get started with a French greeting!"

    elif state == "waiting_for_greeting":
        if time_greeting in user_msg:
            reply = (f"Bravo! That's right — {time_greeting}!<br>"
                     "<img src='/static/images/bonjour_meme.jpg' alt='Bonjour Meme' width='300'><br>"
                     "Now, how are you? In French, we say Comment Ça va? or just Ça va? Try replying with Ça va.")
            session['state'] = "waiting_for_feeling"
        else:
            reply = f"Not quite! Try saying '{time_greeting}' based on the time of day."

    elif state == "waiting_for_feeling":
        if "ça va" in user_msg or "ca va" in user_msg:
            session['mood'] = 'neutral'
            reply = ("You just said I'm fine in French! Alternate responses are Bien (Well), Mal (Bad) etc <br>"
                     "<img src='/static/images/cava_meme.webp' alt='Ca Va Meme' width='300'><br>"
                     "Shall we move over to introductions? (yes/no)"
                     )
            session['state'] = "intro"
        elif "bien" in user_msg:
            session['mood'] = 'positive'
            reply = "Very good! Très bien! Good to know you're doing bien :) Tell me what you did today in English. I'll translate it for you."
            session['state'] = "freeform_translation"
        elif "mal" in user_msg:
            session['mood'] = 'negative'
            reply = "Oh no...I hope you feel better soon. This too shall pass. Tell me what you did today in English. I'll translate it for you."
            session['state'] = "freeform_translation"
        else:
            reply = "Try replying with 'Ça va' — that means you're doing fine!"
    
    elif state == "intro":
        if "yes" in user_msg:
            reply = "My name is Coucou! - Je m'appelle Coucou! Try introducing yourself, Comment vous appelez-vous? (What is your name?)"
            session['state'] = "day-month"
        if "no" in user_msg:
            reply = ("Would you like to know today's date in French? (oui/non)<br>"
                    "Yes is Oui and No is Non, please use these from now onwards :)")
            session['state'] = "day-month-french"

    elif state == "day-month":
        if "je m'appelle" in user_msg:
            reply = ("Yayy enchante! - that means Nice to meet you! Would you like to know today's date in French? (oui/non)<br>"
                     "Yes is Oui and No is Non, please use these from now onwards :)<br>"
                     "<img src='/static/images/Well-Yes-But-Actually-No.meme.webp' alt='oui but non meme' width='300'><br>")
            session['state'] = "day-month-french"
        else:
            reply = "Try replying with 'Je m'appelle {your name}'"

    elif state == "day-month-french":
        if "yes" in user_msg or "oui" in user_msg:
            reply = get_day_and_month_french() + "What's something you did today? I'll tell you the equivalent French translation."
            session['state'] = "freeform_translation"
        elif "no" in user_msg or "non" in user_msg:
            reply = "No worries. Tell me what you did today — in English."
            session['state'] = "freeform_translation"
        else:
            reply = "Please respond with 'oui' (yes) or 'non' (no)."

    elif state == "freeform_translation":
        translation = translate_to_french(user_msg)
        reply = (f"Here's how you'd say that in French:<br><strong>{translation}</strong><br>"
                 "Would you like to try another sentence or continue learning something else? (say 'another' or 'continue')")
        session['state'] = "after_translation"

    elif state == "after_translation":
        if "another" in user_msg:
            reply = "Great! Type another English sentence and I’ll translate it to French."
            session['state'] = "freeform_translation"
        elif "continue" in user_msg:
            reply = "Alright! What would you like to learn next? Colors, numbers, or specific words?"
            session['state'] = "topic_choice"
        else:
            reply = "Please say 'another' to translate more, or 'continue' to move on."

    elif state == "topic_choice":
        if "colors" in user_msg:
            reply = "Great! Let's learn colors. What color would you like to know in French?"
            session['state'] = "freeform_translation"
        elif "numbers" in user_msg:
            reply = ("Fantastic! Let's learn numbers. Say a number in English."
                     "<img src='/static/images/numbers.jpg' alt='french numbers meme' width='300'><br>")
            session['state'] = "freeform_translation"
        elif "words" in user_msg:
            reply = "What word would you like to know in French?"
            session['state'] = "freeform_translation"
        else:
            reply = "I didn't quite catch that. Please choose 'colors', 'numbers', or 'words'."

    else:
        reply = "Hmm, I got a bit lost. Let's start over — say 'hello'!"
        session['state'] = "start"

    return jsonify({'reply': reply})

if __name__ == '__main__':
    app.run(debug=True)