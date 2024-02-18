import json
import requests

from flask import Flask, request
from openai import OpenAI

app = Flask(__name__)

BOTTOKEN = '<TOKEN>'  # TelegramBotToken xxxxx:xxxxxxxxxxx

API_URL = f'https://api.telegram.org/bot{BOTTOKEN}'
APIKEY = '<api_key>'  # api_key
BASEURL = '<base_url>'  # base_url,like https://api.aiproxy.io/v1
PORT = 8443  # webhook port
MODEL = 'gpt-3.5-turbo'


# the model you want to use
# "gpt-4-0125-preview",
# "gpt-4-turbo-preview",
# "gpt-4-1106-preview",
# "gpt-4-vision-preview",
# "gpt-4",
# "gpt-4-0314",
# "gpt-4-0613",
# "gpt-4-32k",
# "gpt-4-32k-0314",
# "gpt-4-32k-0613",
# "gpt-3.5-turbo",
# "gpt-3.5-turbo-16k",
# "gpt-3.5-turbo-0301",
# "gpt-3.5-turbo-0613",
# "gpt-3.5-turbo-1106",
# "gpt-3.5-turbo-0125",
# "gpt-3.5-turbo-16k-0613",

def sendMessage(chat_id, text):
    requests.get(f'{API_URL}/sendMessage', params={
        'chat_id': chat_id,
        'text': text
    })


@app.route("/webhook/event", methods=['POST'])  # receive messages
def event():
    data = request.json
    text = "I can only understand pure text messages."
    userid = str(data['message']['chat']['id'])
    if 'text' in data['message']:
        text = data['message']['text']
        client = OpenAI(
            api_key=APIKEY,
            base_url=BASEURL
        )

        chat_completion = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": ""},  # System prompt
                {"role": "user", "content": text}
            ]
        )
        sendMessage(userid, chat_completion.choices[0].message.content)
    else:
        sendMessage(userid, text)
    return json.dumps(data)


if __name__ == '__main__':
    app.run(port=PORT)
