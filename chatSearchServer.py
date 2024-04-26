from gpt4all import GPT4All
from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
import json

def get_template_string():
    with open("template.json", "r") as file:
        dict = json.load(file)
        string = json.dumps(dict)
        return string

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

json_template = get_template_string()
systemTemplate = "You are a model that should take in user input and process it into a json with fields to be specified."
device = "gpu" if GPT4All.list_gpus() != [] else "cpu"
gpt = GPT4All(model_name="Nous-Hermes-2-Mistral-7B-DPO.Q4_0.gguf", device=device, model_path='.')

@app.route("/search")
def hello_world():
    user_prompt = request.args.get("prompt")
    print(f"User prompt: {user_prompt}")
    
    # quick test response bc my computer takes eons to actually run a chat session
    #response = "{ \"message\": \"test\"}"
    #return response

    with gpt.chat_session(systemTemplate):
        _ = gpt.generate(prompt=f"Take the following user input and convert it into a json file in the format \"{json_template}\" this has all possible values for the search field.", temp=0)
        json_text = gpt.generate(prompt=f"Here is the user input to convert. \"{user_prompt}\" put it in the format specified earlier. only respond with the full json text of the fields with only the necessary values filled out.", temp=0, max_tokens=500)
        response = json.loads(json_text[json_text.index("{"):json_text.rindex("}") + 1])
        print(f"JSON response: {response}")
        return response

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)