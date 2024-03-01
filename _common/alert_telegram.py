import requests


def send_message_telegram(message, TOKEN, chat_id):
	# TOKEN = "6362790580:AAHdKkpldUflGnyqpMtqsgVHQnDqL8fLSEQ"
	# chat_id = "5342781051"
	# message = "hello from your telegram bot"
	url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={message}"
	requests.get(url).json()

