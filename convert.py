'''
Convert Operation Harsh Doorstop Waldo Mod UE4 GVAS (.sav) Savegame files to JSON
'''
import json
import sys
from datetime import datetime
from SavConverter.SavReader import read_sav

def get_player_data_array(gvas_properties: list) -> list | None:
    "Get the PlayerData array from the parsed GVAS properties"
    for prop in gvas_properties:
        if (prop.type == 'ArrayProperty') and (prop.name == 'PlayerData'):
            return prop.value
    return None

def parse_fields_to_dict(fields: list) -> dict:
    "Parse the fields in the PlayerData array into a dict"
    field_dict = {}
    for field in fields:
        key = field.split(":")[0]
        value = ":".join(field.split(":")[1:]).strip()

        if key == 'Datetime':
            # fix weird timestamp & convert to datetime
            value = value.replace(',', '')
            value = datetime.strptime(value, '%Y/%m/%d %H:%M:%S.%f')
            value = value.strftime('%Y-%m-%d %H:%M:%S.%f')

        elif key in ['Position', 'Rotation']:
            # convert to dict of x, y, z
            parts = value.replace(',', '').split(' ')
            value_dict = {}
            for part in parts:
                axis = part.split(':')[0]
                coord = float(part.split(':')[1])
                value_dict[axis] = coord
            value = value_dict

        # convert to native data types
        elif key in ['isADS', 'isCrouched', 'isProne', 'isSprinting']:
            if value.lower() == 'true':
                value = True
            elif value.lower() == 'false':
                value = False
            else:
                raise ValueError(f"Unknown value for {key}: {value}")
        elif key in ['Health', 'LastShotFireTime']:
            value = float(value)
        elif key in ['K', 'D', 'A']:
            value = int(value)

        field_dict[key] = value
    return field_dict

def data_array_to_json(data_array: list) -> str:
    "Connvert the data in the PlayerData array to json"
    player_entries = []
    for msg in data_array:
        msg = msg.split("[WALDO]")[-1].strip()
        players = msg.split(";")
        for player_msg in players:
            fields = player_msg.split("|")
            field_dict = parse_fields_to_dict(fields)
            player_entries.append(field_dict)

    # sort list by datetime
    player_entries = sorted(player_entries, key=lambda x: x['Datetime'])

    # convert to json
    out_json = {
        "PlayerData": player_entries
    }
    return json.dumps(out_json, indent=2)

def convert_sav_to_json(sav_file_path: str, json_file_path: str) -> None:
    "Convert the given .sav file to a .json file"
    # Read sav file
    gvas_props: list = read_sav(sav_file_path)

    # parse data into json
    player_data: list | None = get_player_data_array(gvas_props)
    if player_data is None:
        print('PlayerData array not found')
        sys.exit(1)
    json_str: str = data_array_to_json(player_data)

    # Write json string to file
    with open(json_file_path, 'w', encoding='utf-8') as json_file:
        json_file.write(json_str)

if __name__ == '__main__':
    FILE_NAME = 'WaldoDataClient'
    SAVE_FILE = f'SavFiles/{FILE_NAME}.sav'
    WRITE_FILE = f'JsonFiles/{FILE_NAME}.json'

    convert_sav_to_json(SAVE_FILE, WRITE_FILE)
