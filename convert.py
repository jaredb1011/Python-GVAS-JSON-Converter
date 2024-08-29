'''
Convert Operation Harsh Doorstop Waldo Mod UE4 GVAS (.sav) Savegame files to JSON
'''
import json
import sys
from datetime import datetime
from SavConverter.SavReader import read_sav
from visualize import visualize_timeline

def get_player_data_array(gvas_properties: list) -> list | None:
    "Get the PlayerData array from the parsed GVAS properties"
    for prop in gvas_properties:
        if (prop.type == 'ArrayProperty') and (prop.name == 'PlayerData'):
            return prop.value
    return None

def parse_fields_to_dict(fields: list) -> dict | None:
    "Parse the fields in the PlayerData array into a dict"
    field_dict = {}
    for field in fields:
        key = field.split(":")[0]
        value = ":".join(field.split(":")[1:]).strip()

        if (key == 'PlayerName') and (value == ""):
            # skip empty player entries
            return None

        if key == 'Datetime':
            # fix weird timestamp & convert to datetime
            value = value.replace(',', '')
            value = datetime.strptime(value, '%Y/%m/%d %H:%M:%S.%f')
            value = value.strftime('%Y-%m-%d %H:%M:%S.%f')

        elif key in ['DeltaPos', 'DeltaRot']:
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
            value = float(value.replace(',', ''))
        elif key in ['K', 'D', 'A']:
            value = int(value)

        field_dict[key] = value
    return field_dict

def data_array_to_dict(data_array: list) -> dict:
    "Convert the data in the PlayerData array to json"
    player_entries = []
    for msg in data_array:
        msg = msg.split("[WALDO]")[-1].strip()
        players = msg.split(";")
        for player_msg in players:
            fields = player_msg.split("|")
            field_dict = parse_fields_to_dict(fields)
            if field_dict is None:
                continue
            player_entries.append(field_dict)

    # sort list by datetime
    player_entries = sorted(player_entries, key=lambda x: x['Datetime'])

    # convert to json
    out_dict = {
        "PlayerData": player_entries
    }
    return out_dict

def convert_sav_to_dict(sav_file_path: str) -> dict:
    "Convert the given .sav file to a .json file"
    # Read sav file
    gvas_props: list = read_sav(sav_file_path)

    # parse data into dict
    player_data: list | None = get_player_data_array(gvas_props)
    if player_data is None:
        print('PlayerData array not found')
        sys.exit(1)
    data_dict: dict = data_array_to_dict(player_data)

    return data_dict

def output_json(data_dict: dict, json_file_path: str) -> None:
    "Write the json data to the given file"
    json_str: str = json.dumps(data_dict, indent=2)
    with open(json_file_path, 'w', encoding='utf-8') as json_file:
        json_file.write(json_str)

if __name__ == '__main__':
    VISUALIZE_TIMELINE = True

    FILE_NAME = 'WaldoData%AAS-TestMap%2,024_8_29-1_31'
    SAVE_FILE = f'SavFiles/{FILE_NAME}.sav'
    WRITE_FILE = f'JsonFiles/{FILE_NAME}.json'

    player_dict = convert_sav_to_dict(SAVE_FILE)
    output_json(player_dict, WRITE_FILE)

    if VISUALIZE_TIMELINE:
        visualize_timeline(player_dict)
