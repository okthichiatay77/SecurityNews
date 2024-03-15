import openai

openai_api_key = 'THIS_IS_KEY_API_OPENAI'
openai.api_key = openai_api_key


def ask_openai(message):
	response = openai.ChatCompletion.create(
		model="gpt-3.5-turbo",
		messages=[
			{"role": "system", "content": "You are an helpful assistant."},
			{"role": "user", "content": message},
		]
	)

	answer = response.choices[0].message.content.strip()
	return answer
