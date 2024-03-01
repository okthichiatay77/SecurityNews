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


def reformat_form_telegram(title, pk):
	message = """CVE'S DAILY ALERT\nAffected you have follow create new CVE\nName CVE: '{}'\nURL: http://127.0.0.1:8000/detail-cve/{}/""".format(title, pk)
	return message
