instructions_text = """
### Instructions for Constructing Housing Data

#### Context  
- Objective:  
  Take a message as an input and return a JSON that has the exact format of exampleOutput and follow all the field instructions and constraints accordingly. Read through everything thoroughly.
- Constraints:  
  - Ensure all fields adhere to their specific rules (e.g., allowed values, data type).  
  - If the client's message does not provide enough information to populate a field, **leave the field as its Default Value**.
  - As the Chatbot you should ONLY return the resulting JSON object, structured like exampleOutput:  below:  
    {
        "garages": String,
        "beds": String,
        "baths": String,
        "city": String
    }
- Examples that have a Client Input and the resulting JSON Object:
  - Only use the following information to learn how to process data, do not keep any of the datapoints.
  - Example 1:
    - Client Input: "I want a 2 bedroom house in Hoboken."
    - Response: 
    {
          "garages": "Missing",
          "beds": "2e",
          "baths": "Missing",
          "city": "Hoboken"
    }
    - Notice how we only populate fields that have supporting evidence from the Clients' Input
  - Example 2: 
    - Client Input: "I want a house with at least 2 bathrooms"
    - Response: 
    {
          "garages": "Missing",
          "beds": "Missing",
          "baths": "2g",
          "city": "Missing"
    }
    - Notice how City is "Missing", because the Client never mentioned a city.
  - Example 2: 
    - Client Input: "I want a house with 1 bathroom and at least 2 bedrooms, and a garage that could fit at least 1 car"
    - Response: 
    {
          "garages": "1g",
          "beds": "2g",
          "baths": "1e",
          "city": "Missing"
    }

#### Field Instructions

1. Garages
   - Value Constraint: Constrained  
   - Allowed Values: ["Missing", 1g, 2g, 3g]  
   - Default Value: "Missing"  
   - Type: String  
   - Description: Number of cars that can fit in a garage.

2. Beds
   - Value Constraint: Constrained  
   - Allowed Values: ["Missing", 1e, 1g, 2e, 2g, 3e, 3g]  
   - Default Value: "Missing"  
   - Type: String  
   - Description: Number of bedrooms.
     - 'e': Exact number.
     - 'g': At least this number.
     - Example:
       - 2g: At least two beds.
       - 2e: Exactly two beds.

3. Baths
   - Value Constraint: Constrained  
   - Allowed Values: ["Missing", 1e, 1g, 2e, 2g, 3e, 3g]  
   - Default Value: "Missing"  
   - Type: String  
   - Description: Number of bathrooms.
     - 'e': Exact number.
     - 'g': At least this number.
     - Example:
       - 2g: At least two baths.
       - 2e: Exactly two baths.

4. City
   - Value Constraint: Unconstrained  
   - Default Value: "Missing"  
   - Type: String  
   - Description: The city where the house is located. Must be a valid City in America and properly spelled.
"""
