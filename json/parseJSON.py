import json

CS_json_raw = open('CS.json')
CS_json_str = CS_json_raw.read()
print(CS_json_str)
CS_json = json.loads(CS_json_str)
print(CS_json)
print(CS_json["CS488"])
