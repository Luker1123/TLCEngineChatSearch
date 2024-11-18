from flask import Flask, request
from flask_cors import CORS
import json
import requests
import os
from dotenv import load_dotenv


app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

load_dotenv()
envApiKey = os.getenv("API_KEY")
envModel = os.getenv("MODEL")
envPort = os.getenv("PORT")

def sendMessage(message):
    # Define the URL and headers
    model = envModel
    url = "http://ollama.tlcengine.com:8080/api/chat/completions"
    headers = {
        "Authorization": f"Bearer {envApiKey}",
        "Content-Type": "application/json"
    }
    data = {
        "model": model,
        "messages": [
            {
            "role": "user",
            "content": message
            }
        ]
    }
    response = requests.post(url=url, headers=headers, json=data)
    if response.status_code == 200:
        return("Response:", response.json())
    else:
        return("Error:", response.status_code, response.text)

def getTemplateString(template):
    with open(template, "r") as file:
        dict = json.load(file)
        string = json.dumps(dict)
        return string

def convertResponseToJson(response):
    json_string = response[1]['choices'][0]['message']['content']
    json_string = json_string.replace("```", "").strip()
    return json.loads(json_string)

@app.route("/search")
def search():
    json_template = getTemplateString("outputTemplate.json")
    user_prompt = request.args.get("prompt")
    print(f"User prompt: {user_prompt}")
    
    # Sometimes this propmpt causes it to randomly errors so need to find a more robust way
    prompt=f"You are a model that should take in user input and process it into a json with fields to be specified. Take the following user input and convert it into a json file in the format \"{json_template}\" this has all possible values for the search field. Here is the user input to convert. \"{user_prompt}\" put it in the format specified earlier. only respond with the full json text of the fields with only the necessary values filled out."
    response = sendMessage(prompt)
    # Need to handle response for errors
    print(response)
    json_text = convertResponseToJson(response)
    # Step 1: While there are too many null values in the json_text, the chatbot will ask specific questions and update the json_text accordingly
    # Step 2: Once we have a sufficient amount of null values we will send postman queries utilizing this json_text to retrieve real housing entries
    # Step 3: Have the chatbot show the houses in a readable format
    # Step 4: The chatbot will ask the client what they like and don't like about the houses and update the json_text accordingly 
    # Step 5: Loop back to Step 2
    return json_text

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=envPort)