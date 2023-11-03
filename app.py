from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import openai

app = Flask(__name__)

# Set up OpenAI API credentials
openai.api_key = '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'  # Use environment variables or config files to store keys securely.

# Configuration for SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://xiazhijie:Shinyway123!@localhost:5432/xiazhijie'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Model to store messages and responses
class ChatHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_message = db.Column(db.String(), nullable=False)
    ai_response = db.Column(db.String(), nullable=False)

@app.route("/")
def index():
    chat_history = ChatHistory.query.all()
    return render_template("index.html", chat_history=chat_history)

@app.route("/api", methods=["POST"])
def api():
    message = request.json.get("message")

    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": message}
        ]
    )

    if completion.choices[0].message:
        ai_response = completion.choices[0].message['content']

        # Store the message and response in the database
        chat_entry = ChatHistory(user_message=message, ai_response=ai_response)
        db.session.add(chat_entry)
        db.session.commit()

        return ai_response
    else:
        return 'Failed to Generate response!'

if __name__ == '__main__':
    app.run()
