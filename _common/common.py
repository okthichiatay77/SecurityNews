import re
import requests


def build_url_news(title):
    mapping_chars = {
        "àáảãạâầấẩẫậăằắẳẵặ": "a",
        "èéẻẽẹêềếểễệ": "e",
        "đ": "d",
        "ìíỉĩị": "i",
        "òóỏõọôồốổỗộơờớởỡợ": "o",
        "ùúủũụưừứửữự": "u",
        "ỳýỷỹỵ": "y"
    }
    title = title.lower()
    for k, v in mapping_chars.items():
        title = re.sub(r"[{}]+".format(k), v, title)

    result = "-".join(re.findall("[\w\d]+", title))

    return result


def send_message_telegram(message, token, chat_id):
	# TOKEN = "6362790580:AAHdKkpldUflGnyqpMtqsgVHQnDqL8fLSEQ"
	# chat_id = "5342781051"
	url = f"https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text={message}"
	response = requests.get(url)
	return response.json()


