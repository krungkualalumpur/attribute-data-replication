# attribute-data-replication
A tool to automate attribute-based Roblox data replication by inputting simple JSON data to luau.

# Installation
IMPORTANT: Make sure to use bash for the installation.

Clone the repository with this command:

git clone https://github.com/krungkualalumpur/attribute-data-replication

# Usage
The module detects through JSON file, through this template:
{
    "UtilName" : "DataNameHere",
    "Data" : {
        "NumberAttributeNameHere" : 1,
        "BooleanAttributeNameHere" : true,
        "StringAttributeNameHere" : "Attribute",
        "OptionalAttribute?" : "IAmAnOptionalStringAttribute"
    }
}

Create input path of json file with the content using the given template above. 
Then, within the cloned folder directory, run execute.sh under Scripts through this command:

Scripts/execute.sh $INPUT_PATH $OUTPUT_PATH