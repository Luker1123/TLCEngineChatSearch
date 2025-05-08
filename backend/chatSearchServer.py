from flask import Flask, request
from flask_cors import CORS
import json
import requests
import os
from dotenv import load_dotenv
from instructions import instructions_text

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

load_dotenv()
envApiKey = os.getenv("API_KEY")
envModel = os.getenv("MODEL")
envPort = os.getenv("PORT")

def sendMessage(message):
    model = envModel  # e.g., "gpt-4" or "gpt-3.5-turbo"
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {envApiKey}",
        "Content-Type": "application/json"
    }
    data = {
        "model": model,
        "messages": [
            {
                "role": "system",
                "content": "You are a helpful assistant that only returns structured JSON objects."
            },
            {
                "role": "user",
                "content": message
            }
        ],
        "temperature": 0.2  # Optional, controls creativity
    }
    response = requests.post(url=url, headers=headers, json=data)
    if response.status_code == 200:
        return ("Response:", response.json())
    else:
        return ("Error:", response.status_code, response.text)

def getTemplateString(template):
    with open(template, "r") as file:
        dict = json.load(file)
        string = json.dumps(dict)
        return string

def convertResponseToJson(response):
    json_string = response[1]['choices'][0]['message']['content']
    json_string = json_string.replace("```", "").strip()
    print(json_string)
    return json.loads(json_string)

def getMissingFields(json):
    acc = []
    for x in json:
        if json[x] == "Missing":
            acc.append(x)
    return acc

import urllib.parse

def build_simple_url(data):
    base_url = "https://krishnam.tlcengine.com/search/"
    params = {
        "orderby": "newest",
        "orderbydirection": "DESC",
        "page_number": "1",
        "searchmap": "true",
        "skip": "0",
        "view": "maplist",
        "propertytype": "sf,cnd,mf"  # This is hardcoded as in your example
    }

    # Handle inputs from the dictionary
    if "baths" in data and data["baths"] != "Missing":
        params["baths"] = data["baths"]
    if "beds" in data and data["beds"] != "Missing":
        params["beds"] = data["beds"]
    if "city" in data and data["city"] != "Missing":
        params["city"] = data["city"]
    if "garages" in data and data["garages"] != "Missing":
        params["garages"] = data["garages"]

    # Encode the URL parameters
    query_string = urllib.parse.urlencode(params, quote_via=urllib.parse.quote)
    return f"{base_url}?{query_string}"


@app.route("/search")
def search():
    user_prompt = request.args.get("prompt")
    print(f"User prompt: {user_prompt}")
    
    # Still need to improve Instructions Text
    # It will still populate certain fields even when the client does not request them
    prompt = (
    "{instructions_text}"
    "Take the user input: \"{user_prompt}\", and process it using the instructions. "
    "The only information you should respond with is a object, with no additional text, explanations, or formatting."
    "You should ONLY return a object that follows the structure of the example output in the instructions, with no additional text"
    "Do not attempt to solve this with code. As the chatbot you should do the computing and then return the JSON object"
    "Do not prepend the JSON with any information"
    ).format(instructions_text=instructions_text, user_prompt=user_prompt)
    response = sendMessage(prompt)
    try:
        json_text = convertResponseToJson(response)
    except: 
        return "Error Proccessing JSON" # Keeping for testing purposes, should probably do something else
    missingFields = getMissingFields(json_text)
    print(missingFields)
    # Step 1: While there are too many missing values in the json_text, the chatbot will ask specific questions and update the json_text accordingly
    # Step 2: Once there are no more missing values we will send postman queries utilizing this json_text to retrieve real housing entries
        # Use GenerateURL.py, the file probably does not work in the current stage so will need some work here
        # For the sake of prototype this semester, we could just redirect to this page and ignore the remaining steps 
        # I think the remaining steps would probably be a good idea to work on next semester.
    # Step 3: Have the chatbot show the houses in a readable format
    # Step 4: The chatbot will ask the client what they like and don't like about the houses and update the json_text accordingly 
    # Step 5: Loop back to Step 2
    print(json_text)
    print(build_simple_url(json_text))
    return build_simple_url(json_text)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=envPort)