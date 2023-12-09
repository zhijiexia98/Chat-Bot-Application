from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import openai
import os
from textblob import TextBlob
from googletrans import Translator, LANGUAGES

app = Flask(__name__)

# Set up OpenAI API credentials
# <<<<<<< HEAD
openai.api_key = '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'
# Use environment variables or config files would store keys more securely.
# But here just used the key directly for simplicity.

# Define the default route to return the index.html file

# Configuration for SQLAlchemy
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://xiazhijie:Shinyway123!@localhost:5432/xiazhijie'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://fanmuq:mypassword@localhost/chatdb'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Initialize Google Translate
translator = Translator()

# Initialize Flask-Limiter
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["200 per day", "60 per hour"]  
    # We can always customize these values as needed
)


# Model to store messages and responses
class ChatHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_message = db.Column(db.String(), nullable=False)
    ai_response = db.Column(db.String(), nullable=False)

# # Create the database tables if they don't exist
# with app.app_context():
#     db.create_all()

# >>>>>>> 655a3781b588c6be4de36300732bcfa841e8d4d0
@app.route("/")
@limiter.limit("10 per minute")  
# Rate limit for this specific route
def index():
    chat_history = ChatHistory.query.all()
    return render_template("index.html", chat_history=chat_history)

@app.route("/api", methods=["POST"])
def api():
    try:
        data = request.json
        message = data.get("message")
        target_language = data.get("language", "en")  # Default to English if no language is provided

        # Translate message to English before sending to GPT-3
        translated_message = translator.translate(message, dest='en').text

         # Perform sentiment analysis on the message
        analysis = TextBlob(message)
        sentiment = analysis.sentiment
        print(f"Sentiment Polarity: {sentiment.polarity}")  
        # For debugging

        # Modify the response based on the sentiment
        if sentiment.polarity < -0.5:
            ai_response = "I sense that you're upset. I'm here to help you. What can I do for you?"
        else:
            # For neutral and positive sentiment, proceed with translation and API call
            completion = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": translated_message}]
            )

            if 'choices' in completion and completion.choices:
                ai_response = completion.choices[0].message['content']
            else:
                ai_response = "I'm not sure how to respond to that."

        # Translate AI response back to the target language
        translated_response = translator.translate(ai_response, dest=target_language).text

        # Store the original message and translated response in the database
        chat_entry = ChatHistory(user_message=message, ai_response=translated_response)
        db.session.add(chat_entry)
        db.session.commit()

        return jsonify({"response": translated_response})

    except Exception as e:
        app.logger.error(f"Exception occurred: {e}")
        return jsonify({"error": "Failed to generate response!"}), 500

if __name__ == '__main__':
    app.run()
