import sys
import json
import os
import re
from typing import TypedDict, Dict, List, Any, Literal

class InputContent(TypedDict):
    UtilName: str
    Data: Dict[str, Any]

class AttributeData(TypedDict): 
    AttributeKey : str
    AttributeValue : Any

JSON_PATH = sys.argv[1] if len(sys.argv) > 1 else None
OUTPUT_PATH = sys.argv[2] if len(sys.argv) > 2 else None

if OUTPUT_PATH is None: 
    raise ValueError("Invalid Output Path Argument")

OUTPUT_DIR = os.path.dirname(OUTPUT_PATH)

def luaType(inst : Any) -> Literal["boolean", "string", "number", "unknown"]:
    return "number" if (isinstance(inst, (int, float)) and not isinstance(inst, (bool))) else "boolean" if isinstance(inst, bool) else "string" if isinstance(inst, str) else "unknown"

def nameToParams(name : str):
    first_char = name[0].lower()
    rest_of_char = name[1:] 

    return first_char + rest_of_char

def parser():
    output : str
    attributeTypesDetected : List[AttributeData] = []

    def isOptional(givenStr : str) -> bool:
        return True if re.search(r'\?$', givenStr) is not None else False
    
    def parseGivenKeyStr(givenStr : str) -> str: 
        return re.sub(r'\?$', "", givenStr)
    def getLuauTypeInStr(data : AttributeData) -> str: 
        return luaType(data["AttributeValue"]) + ("?" if isOptional(data["AttributeKey"]) else "")

    if JSON_PATH is None: 
        raise ValueError("Invalid Input Path Argument")
  

    with open(JSON_PATH, "r") as file:
        data : InputContent = json.load(file)     

        for k,v in data["Data"].items(): 
            attributeData : AttributeData = {
                "AttributeKey" : k,
                "AttributeValue" : v, 
            }
            attributeTypesDetected.append(attributeData)
        
        output = f""" 
--!strict
type {data["UtilName"]}Data = {{\n\t{("\n\t".join(f"{parseGivenKeyStr(v['AttributeKey'])}: {getLuauTypeInStr(data=v)}," for v in attributeTypesDetected))}\n}}

local util = {{}}

function util.create{data["UtilName"]}Data({f"{", ".join(f'{nameToParams(parseGivenKeyStr(v["AttributeKey"]))} : {getLuauTypeInStr(data=v)}' for v in attributeTypesDetected)}"}) : {data["UtilName"]}Data
    return {{
    \t{f"{("\n\t\t".join(f'{parseGivenKeyStr(v["AttributeKey"])} = {nameToParams(parseGivenKeyStr(v["AttributeKey"]))},' for v in attributeTypesDetected))}"}
    }}
end

function util.set{data["UtilName"]}Data(instance : Instance, data : {data['UtilName']}Data)
    {"\n\t".join(f'instance:SetAttribute("{parseGivenKeyStr(v["AttributeKey"])}", data.{parseGivenKeyStr(v["AttributeKey"])})' for v in attributeTypesDetected)}
end

function util.get{data["UtilName"]}Data(instance : Instance) : {data['UtilName']}Data
    return {{\n\t\t{"\n\t\t".join(f'{parseGivenKeyStr(v['AttributeKey'])} = instance:GetAttribute("{parseGivenKeyStr(v['AttributeKey'])}") :: never or {'nil' if isOptional(v["AttributeKey"]) else  f'"{v["AttributeValue"]}"' if luaType(v["AttributeValue"]) == "string" else str(v["AttributeValue"]).lower()},' for v in attributeTypesDetected)}\n\t}}
end

return util
"""     
    return output

def write(output : str):
    if OUTPUT_PATH is None: 
        raise ValueError("Invalid Output Path Argument")

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    with open(OUTPUT_PATH, "w") as file: 
        file.write(output)
        

def main():
    output = parser()
    write(output)
    
if __name__ == "__main__":
    main()