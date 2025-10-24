import sys
import json
import os
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
    return "number" if isinstance(inst, (int, float)) else "boolean" if isinstance(inst, bool) else "string" if isinstance(inst, str) else "unknown"

def nameToParams(name : str):
    first_char = name[0].lower()
    rest_of_char = name[1:] 

    return first_char + rest_of_char

def parser() -> str:
    output : str
    attributeTypesDetected : List[AttributeData] = []

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
type {data["UtilName"]}Data = {{\n\t{("\n\t".join(f"{v['AttributeKey']}: {luaType(v['AttributeValue'])}," for v in attributeTypesDetected))}\n}}

local util = {{}}

function util.create{data["UtilName"]}Data({f"{", ".join(f'{nameToParams(v["AttributeKey"])}' for v in attributeTypesDetected)}"}) : {data["UtilName"]}Data
    return {{
{f"\t\t{("\n\t\t".join(f'{v["AttributeKey"]} = {nameToParams(v["AttributeKey"])},' for v in attributeTypesDetected))}"}
    }}
end

function util.set{data["UtilName"]}Data(instance : Instance, data : {data['UtilName']}Data)
    {"\n\t".join(f'instance:SetAttribute("{v["AttributeKey"]}", data.{v["AttributeKey"]})' for v in attributeTypesDetected)}
end

function util.get{data["UtilName"]}Data(instance : Instance) : {data['UtilName']}Data
    return {{\n\t\t{"\n\t\t".join(f'{v['AttributeKey']} = instance:GetAttribute("{v['AttributeKey']}") :: {luaType(v['AttributeValue'])} or {f'"{v["AttributeValue"]}"' if luaType(v["AttributeValue"]) == "string" else v["AttributeValue"]},' for v in attributeTypesDetected)}\n\t}}
end

return util
    """     
    return output

def write(output : str) -> None:
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