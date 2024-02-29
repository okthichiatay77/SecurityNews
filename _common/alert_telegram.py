import requests


def send_message_telegram(title, TOKEN, chat_id):
	# TOKEN = "6362790580:AAHdKkpldUflGnyqpMtqsgVHQnDqL8fLSEQ"
	# chat_id = "5342781051"
	# message = "hello from your telegram bot"
	message = "CVE'S DAILY ALERT: Affected you have follow create new CVE, name: '{}'".format(title)
	url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={message}"
	requests.get(url).json()

