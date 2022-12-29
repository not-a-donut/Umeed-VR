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
    # global user_input
    user_input = ""
    error_count = 0
    count = 0
    while user_input != "exit":
        if request.method == 'POST':
            # global user_input
            user_input = request.form.get("user_input")
            print(user_input)

            # user_input = request.form['user_input']

            querystring = {
                "message": user_input,
                "uid": "user1"
            }

            response = requests.request(
                "GET", url, headers=headers, params=querystring).text

            dic2 = json.loads(response)
            print("Bot:", dic2.get("chatbot").get("response", "NULL"))

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

            errors = []

            for i in range(len(temp)):
                c = temp[i]
                print(c.get("message"))
                grammatical_errors.append(c.get("message"))
                errors.append(c.get("shortMessage"))

            if b == user_input:
                print("Great job!! No corrections required.")
                computer_response3 = "Greate Job !! No corrections required."
                return render_template('app.html', user_input=user_input, computer_response1="Bot: " + dic2.get("chatbot").get("response", "NULL"), computer_response2=grammatical_errors, computer_response3=computer_response3, error_count = error_count)
            else:
                print("Correct: ", b)
                computer_response4 = "Correct: " + b
                return render_template('app.html', user_input=user_input, computer_response1="Bot: " + dic2.get("chatbot").get("response", "NULL"), computer_response2=grammatical_errors, computer_response4=computer_response4, error_count = error_count)

        for i in errors:
            if i != "":
                error_count += 1

        count += 1

    else:
        print("else statement executed")
        return render_template('app.html')
    


if __name__ == '__main__':
    app.run(debug=True)
