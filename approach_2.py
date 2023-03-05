import os
import openai
import glob

SECRET_KEY_FILE = 'secret_key.txt'

if os.path.isfile(SECRET_KEY_FILE):
        # Read the secret key from the file
        with open(SECRET_KEY_FILE, 'r') as f:
                secret_key = f.read().strip()
else:
        # Prompt the user for the secret key
        secret_key = input('Enter the secret key: ')

        # Write the secret key to a file for future use
        with open(SECRET_KEY_FILE, 'w') as f:
                f.write(secret_key)
                
openai.api_key = secret_key

# Define a dictionary to store the counts of each keyword        
dict1 = {"Viruses": 0, 
        "Bugs": 0, 
        "DDOS": 0, 
        "Patches": 0, 
        "Vulnerabilities": 0, 
        "Threats": 0}

# Specify the path to the data files
data_path = "data/"

for file in glob.glob(data_path+"*.*"):
    with open(file, 'r') as file:
        # Read the contents of each of the files in the data folder
        text = file.read()
        
    # Use OpenAI's chat API to prompt the user to provide a Python dictionary with the counts of the keywords
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": "give your answer in python dict format, if theres none the answer is zero. find how many Viruses, Bugs, DDOS, Patches, Vulnerabilities, Threats there are in the following text."+text}
        ]
    )

    # Convert the returned dictionary string to a Python dictionary and update the keyword counts
    try:    
        dict2 = eval(completion.choices[0].message.content).items()
    except:
        pass
    for key, value in dict2:
        if key in dict1:
                dict1[key] += value
        else:
                dict1[key] = value

# Create a string representation of the final keyword counts
output = ""
for key in dict1.keys():
    output += str(key)+" = "+str(dict1[key]) +" "
print(output)
        