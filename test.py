'''
Convert .sav files to .json
'''
import json
from SavConverter.SavReader import read_sav

SAVE_FILE = 'ExampleSavFiles/EditorWaldoData.sav'
WRITE_FILE = 'ExampleSavFiles/EditorWaldoData.json'

# Read sav file
properties = read_sav(SAVE_FILE)

# Get just the data properties
for prop in properties:
    if prop.type == 'ArrayProperty' and prop.name == 'PlayerData':
        log_msgs = prop.value

player_entries = []
for msg in log_msgs:
    msg = msg.split("[WALDO]")[-1].strip()
    players = msg.split(";")
    for player_msg in players:
        fields = player_msg.split("|")
        field_dict = {}
        for field in fields:
            key = field.split(":")[0]
            field_dict[key] = ":".join(field.split(":")[1:]).strip()
        player_entries.append(field_dict)
        #print(field_dict)

out_json = {
    "PlayerData": player_entries
}

# convert to json
json_str = json.dumps(out_json, indent=2)

# Write json string to file
with open(WRITE_FILE, 'w', encoding='utf-8') as json_file:
    json_file.write(json_str)

# Convert properties to json
#output = sav_to_json(data_props, string = True)
