from gpt4all import GPT4All
import json

device = "gpu" if GPT4All.list_gpus() != [] else "cpu"

def main():
    #gpt = GPT4All(model_name="orca-2-13b.Q4_0.gguf", device=device)
    #gpt = GPT4All(model_name="mistral-7b-instruct-v0.1.Q4_0.gguf", device=device)
    gpt = GPT4All(model_name="Nous-Hermes-2-Mistral-7B-DPO.Q4_0.gguf", device=device)
    with open('template.json', 'r') as file:
        jsonTemp1 = json.load(file)
    jsonTemp = json.dumps(jsonTemp1)
    #print(jsonTemp)
    systemTemplate = "You are a model that should take in user input and process it into a json with fields to be specified."
    print("Please enter a description of your dream home:")
    user_input = input()  # Taking input from the user
    #print(user_input)
    with gpt.chat_session(systemTemplate):
        response1 = gpt.generate(prompt="Take the following user input and convert it into a json file in the format \"" + jsonTemp + "\" this has all possible values for the search field.",temp=0)
        jsontext = gpt.generate(prompt="Here is the user input to convert. \"" + user_input + "\" put it in the format specified earlier. only respond with the full json text of the fields with only the necessary values filled out.", temp=0, max_tokens=500)
        #print(gpt.current_chat_session)
    print(jsontext)
    #print(jsontext[jsontext.index('{')])
    data = json.loads(jsontext[jsontext.index('{'):jsontext.rindex('}') + 1])
    with open("output.json", 'w') as file:
        json.dump(data, file, indent=4)

if __name__ == "__main__":
    main()
