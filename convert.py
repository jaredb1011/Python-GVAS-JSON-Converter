'''
Convert Operation Harsh Doorstop Waldo Mod UE4 .sav files to .json
'''
import json
from SavConverter.SavReader import read_sav

def get_player_data_array(gvas_properties: list) -> list:
    "Get the PlayerData array from the parsed GVAS properties"
    for prop in gvas_properties:
        if prop.type == 'ArrayProperty' and prop.name == 'PlayerData':
            return prop.value

def data_array_to_json(data_array: list) -> str:
    "Parse the data in the PlayerData array into a dict and convert to json"
    player_entries = []
    for msg in data_array:
        msg = msg.split("[WALDO]")[-1].strip()
        players = msg.split(";")
        for player_msg in players:
            fields = player_msg.split("|")
            field_dict = {}
            for field in fields:
                key = field.split(":")[0]
                value = ":".join(field.split(":")[1:]).strip()
                if key == 'Datetime':
                    # fix weird timestamp
                    value = value.replace(',', '')
                field_dict[key] = value
            player_entries.append(field_dict)

    # sort list by datetime
    player_entries = sorted(player_entries, key=lambda x: x['Datetime'])

    # convert to json
    out_json = {
        "PlayerData": player_entries
    }
    return json.dumps(out_json, indent=2)

if __name__ == '__main__':
    FILE_NAME = 'WaldoData10'
    SAVE_FILE = f'ExampleSavFiles/{FILE_NAME}.sav'
    WRITE_FILE = f'ExampleSavFiles/{FILE_NAME}.json'

    # Read sav file
    gvas_props = read_sav(SAVE_FILE)

    # parse data into json
    player_data = get_player_data_array(gvas_props)
    json_str = data_array_to_json(player_data)

    # Write json string to file
    with open(WRITE_FILE, 'w', encoding='utf-8') as json_file:
        json_file.write(json_str)
