from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Replace with your bot token and Telegram ID
BOT_TOKEN = '7680394855:AAFVjKErGVwWg9bZ49BnChVgCLnv1xA3MRw'
TELEGRAM_ID = '8101143576'  # Your Telegram ID to receive form data
TELEGRAM_API_URL = f'https://api.telegram.org/bot{BOT_TOKEN}/'

# Start command handler
@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    chat_id = data['message']['chat']['id']
    text = data['message'].get('text', '')

    if text == '/start':
        # Send a message with a button to show the form
        show_form_button = {
            'text': 'Welcome! Click the button below to fill out the form.',
            'reply_markup': {
                'inline_keyboard': [[
                    {
                        'text': 'Show Form',
                        'web_app': {'url': 'https://your-github-page-url.com/form.html'}  # Replace with your form URL
                    }
                ]]
            }
        }
        send_message(chat_id, show_form_button)
    return jsonify({'status': 'ok'})

# Function to send a message
def send_message(chat_id, message_data):
    url = TELEGRAM_API_URL + 'sendMessage'
    payload = {
        'chat_id': chat_id,
        'text': message_data.get('text', ''),
        'reply_markup': json.dumps(message_data.get('reply_markup', {}))
    }
    requests.post(url, json=payload)

# Function to handle form data submission
@app.route('/submit-form', methods=['POST'])
def submit_form():
    form_data = request.json
    user_info = form_data.get('user_info', {})
    service = form_data.get('service', '')

    # Prepare the message to send to your Telegram ID
    message = (
        f"New Form Submission:\n\n"
        f"Name: {user_info.get('name', 'N/A')}\n"
        f"Username: {user_info.get('username', 'N/A')}\n"
        f"Service: {service}"
    )

    # Send the form data to your Telegram ID
    send_message(TELEGRAM_ID, {'text': message})

    return jsonify({'status': 'ok'})

if __name__ == '__main__':
    app.run(port=5000)
