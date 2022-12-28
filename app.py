from flask import Flask, render_template, request
import requests
import json

from gingerit.gingerit import GingerIt

app = Flask(__name__)

url = "https://ai-chatbot.p.rapidapi.com/chat/free"


headers = {
    "X-RapidAPI-Key": "653db342bemsh971c29bdad7f814p178e70jsn2b31538fd4ba",
    "X-RapidAPI-Host": "ai-chatbot.p.rapidapi.com"
}

url2 = "https://dnaber-languagetool.p.rapidapi.com/v2/check"

headers2 = {
    "content-type": "application/x-www-form-urlencoded",
    "X-RapidAPI-Key": "653db342bemsh971c29bdad7f814p178e70jsn2b31538fd4ba",
    "X-RapidAPI-Host": "dnaber-languagetool.p.rapidapi.com"
}


@app.route('/', methods=['POST', 'GET'])
def index():


    if request.method == "POST":
        user_input = request.form.get("user_input")

    querystring = {"message": user_input, "uid": "user1"}

    response = requests.request(
        "GET", url, headers=headers, params=querystring).text
    dic2 = json.loads(response)
    print("Bot:", dic2.get("chatbot").get("response", "NULL"))  # 1
    parser = GingerIt()
    parser.parse(user_input)
    a = parser.parse(user_input)
    b = a.get("result")

    payload = "language=en-US&text=" + user_input

    response2 = requests.request(
        "POST", url2, data=payload, headers=headers2).text
    dic = json.loads(response2)
    temp = dic.get("matches")

    grammatical_errors = []

    for i in range(len(temp)):
        c = temp[i]
        print(c.get("message"))  # 2
        grammatical_errors.append(c.get("message"))

    if b == user_input:
        print("Great job!! No corrections required.")  # 3
    else:
        print("Correct:", b)  # 4

    return render_template('app.html', computer_response1="Bot: " + dic2.get("chatbot").get("response", "NULL"))
