# pip install spacy
# python -m spacy download en_core_web_sm
# If you need to install pip, run script in Windows Powershell as administrator (https://bootstrap.pypa.io/get-pip.py)

# Does work for  basic featires but
import spacy

# Load English language model
nlp = spacy.load("en_core_web_sm")

# Define a custom pipeline component to recognize zip codes
@spacy.Language.component("zip_code_component")
def zip_code_component(doc):
    for token in doc:
        if len(token.text) == 5 and token.text.isdigit(): # Assuming zipcode is a 5-digit number
            token.ent_type_ = "ZIPCODE"
    return doc

# Add the custom component to the pipeline
nlp.add_pipe("zip_code_component", last=True)

# Define function to extract number of bedrooms based on household description
def extract_bedrooms(text):
    doc = nlp(text.lower())
    num_bedrooms = None

    # Rules for inferring number of bedrooms based on household description
    for token in doc:
        if token.text in ["couple", "single", "person"]:
            num_bedrooms = 1  # Single person or couple typically need 1 bedroom
        elif token.text == "children" or token.text == "child":
            # Look for numbers indicating the number of children
            for child in token.children:
                if child.pos_ == "NUM":
                    num_children = int(child.text)
                    # Additional bedrooms may be needed depending on the number of children
                    num_bedrooms = max(2, num_children + 1)  # Minimum 2 bedrooms for children
        elif token.text == "grandparents":
            num_bedrooms = 2  # Grandparents may need 2 bedrooms
        
    return num_bedrooms

# https://stackoverflow.com/questions/493174/is-there-a-way-to-convert-number-words-to-integers
def text2int(textnum, numwords={}):
    if not numwords:
        units = [
            "zero", "one", "two", "three", "four", "five", "six", "seven", "eight",
            "nine", "ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen",
            "sixteen", "seventeen", "eighteen", "nineteen",
        ]

        tens = ["", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]

        scales = ["hundred", "thousand", "million", "billion", "trillion"]

        # Changed this so it does not replace and (assuming the numbers never get that big)
        for idx, word in enumerate(units):    numwords[word] = (1, idx)
        for idx, word in enumerate(tens):     numwords[word] = (1, idx * 10)
        for idx, word in enumerate(scales):   numwords[word] = (10 ** (idx * 3 or 2), 0)

    current = result = 0
    for word in textnum.split():
        if word not in numwords:
          # Changed this so it returns the original word if it is not a number
          return textnum

        scale, increment = numwords[word]
        current = current * scale + increment
        if scale > 100:
            result += current
            current = 0

    return result + current

# Sample text
# "A 5 bed and 2 bath in 07030 with a fireplace and dishwasher."
text = "I'm a single person looking for an apartment in 07030 with a fireplace and dishwasher."

# Preprocess the text to remove commas
text = text.replace(',', '')

# Process the text with SpaCy
doc = nlp(text)

# Initialize variables
num_bedrooms = None
num_bathrooms = None
city = None
zipcode = None
has_fireplace = False
has_waterfront = False
has_dishwasher = False
has_air_conditioning = False

# Function to convert written numbers to digits
def convert_to_digits(text):
    words = text.split()
    for i, word in enumerate(words):
        if word.isdigit():
            continue
        try:
            num = str(text2int(word))
            if num.isdigit():
                words[i] = num
        except ValueError:
            pass
    return " ".join(words)

# Preprocess text to convert written numbers to digits
text = convert_to_digits(text)

# Extract entities and features
for token in doc:
    # Check for words similar to "bedroom" and "bathroom" and their associated numbers
    if token.pos_ == "NOUN" and ("bed" in token.text.lower() or "bath" in token.text.lower()):
        for child in token.children:
            if child.pos_ == "NUM":
                if "bed" in token.text.lower():
                    num_bedrooms = int(child.text)
                elif "bath" in token.text.lower():
                    num_bathrooms = int(child.text)
                break # Stop searching for numbers after finding the first one
    # Extract city and zipcode
    elif token.ent_type_ == "GPE":
        city = token.text
    elif token.ent_type_ == "ZIPCODE":
        zipcode = token.text
    # Extract lot features
    elif token.lower_ in ["fireplace", "fireplaces"]:
        has_fireplace = True
    elif token.lower_ in ["waterfront", "waterfronts"]:
        has_waterfront = True
    elif token.lower_ in ["dishwasher", "dishwashers"]:
        has_dishwasher = True
    elif token.lower_ in ["air", "conditioning"]:
        has_air_conditioning = True

# Print extracted entities and features
if num_bedrooms == None:
    num_bedrooms = extract_bedrooms(text)
print("Number of bedrooms:", num_bedrooms)
print("Number of bathrooms:", num_bathrooms)
print("City:", city)
print("Zipcode:", zipcode)
print("Has fireplace:", has_fireplace)
print("Has waterfront:", has_waterfront)
print("Has dishwasher:", has_dishwasher)
print("Has air conditioning:", has_air_conditioning)
