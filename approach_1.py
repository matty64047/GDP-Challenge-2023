# Import necessary libraries
from bs4 import BeautifulSoup
import json
import re
import glob
import json

# Define a dictionary of keywords and initialize their count to 0 - keys for singular and plurals 
keyword_dict = {
    "Viruses":0 ,
    "Bugs":0 ,
    "DDOS":0 ,
    "Patches":0,
    "Vulnerabilities":0,
    "Threats":0,
    "Virus":0,
    "Bug":0,
    "Patch":0,
    "Vulnerability":0,
    "Threat": 0,
}

# Define a function to read XML files and update the keyword_dict dictionary
def xml_reader(keyword_dict, xml_file):
    # Read the contents of the XML file
    with open(xml_file, 'r') as f:
            data = f.read() 

    # Parse the XML data using BeautifulSoup
    bs_data = BeautifulSoup(data, 'xml') 

    # Find the "software" tag in the XML data and iterate over its children
    software = bs_data.find("software")
    for child in software.findChildren():
            # Try to update the count of the corresponding keyword in the keyword_dict dictionary
            try:
                    keyword_dict[child.find("item").text] += int(child.find("amount").text)     
            except:
                    pass

# Define a function to read JSON files and update the keyword_dict dictionary
def json_reader(keyword_dict, json_file):
    # Open the JSON file
    f = open(json_file)
    
    # Load the JSON data as a dictionary
    data = json.load(f)
        
    # Iterate over the keywords in the keyword_dict dictionary
    for keyword in keyword_dict.keys():
        # Try to update the count of the corresponding keyword in the keyword_dict dictionary
        try:
            if type(data[keyword]) is list:
                # If the value associated with the keyword is a list, add the length of the list to the count
                keyword_dict[keyword] += len(data[keyword])
            else: 
                # Otherwise, add 1 to the count
                keyword_dict[keyword] += 1
        except:
            # If the keyword is not found in the JSON data, ignore the exception
            pass

    # Close the JSON file
    f.close()
    
# Define a function to read text files and update the keyword_dict dictionary
def txt_reader(keyword_dict, text_file):
    # Open the text file
    with open(text_file, 'r') as file:
        # Read the contents of the file
        text = file.read()

    # Define the regex pattern to match a number followed by a space and then a word
    pattern = r'\d+\s\w+'

    # Use the findall method from the re module to find all occurrences of the pattern in the text
    matches = re.findall(pattern, text)

    # Iterate over the matches and update the count of the corresponding keyword in the keyword_dict dictionary
    for _match in matches:
        _match = _match.split(" ")
        try:
            keyword_dict[_match[1]] += int(_match[0])
        except:
            pass
    
# Iterate over all the text files in the current directory and update the keyword_dict dictionary
data_path = "data/"

for txt in glob.glob(data_path+"*.txt"):
    txt_reader(keyword_dict, txt)

# Iterate over all the XML files in the current directory and update the keyword_dict dictionary
for xml in glob.glob(data_path+"*.xml"):
    xml_reader(keyword_dict, xml)

# Iterate over all the JSON files in the current directory and update the keyword_dict dictionary
for _json in glob.glob(data_path+"*.json"):
    json_reader(keyword_dict, _json)


# New dictionary with signular and plural keys compiled together

compiled_dict = {}

for key in keyword_dict:
        # Check if the key has already been compiled
        compiled_key = None
        for c_key in compiled_dict:
                if key[:-2] in c_key:
                        compiled_key = c_key
                        break
        
        # If the key has already been compiled, add the value to the existing key
        if compiled_key:
                compiled_dict[compiled_key] += keyword_dict[key]
        else:
                compiled_dict[key] = keyword_dict[key]

# Print the compiled dictionary
output = ""
for key in compiled_dict.keys():
    output += str(key)+" = "+str(compiled_dict[key]) +" "
    
print(output)