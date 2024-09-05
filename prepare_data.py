'''
Prepare Operation Harsh Doorstop Waldo Mod UE4 GVAS (.sav) Savegame files
'''
import json
import os
from DataPrep.convert_sav_to_json import convert_sav_to_dict, output_json
from DataPrep.visualize_data import visualize_timeline
from DataPrep.clean_data import get_valid_kill_events

VISUALIZE_TIMELINE = False

SAV_FILE_FOLDER = r"C:\Users\jared\Desktop\basicallyhomeless\WALDO\repos\Python-GVAS-JSON-Converter\SavFiles"
JSON_FILE_FOLDER = r"C:\Users\jared\Desktop\basicallyhomeless\WALDO\repos\Python-GVAS-JSON-Converter\JsonFiles"
CLEANED_FILE_FOLDER = r"C:\Users\jared\Desktop\basicallyhomeless\WALDO\repos\Python-GVAS-JSON-Converter\CleanedJsonFiles"

# convert SAV file data to JSON
if os.path.isdir(SAV_FILE_FOLDER):
    file_objs = os.scandir(SAV_FILE_FOLDER)
    sav_files = [obj.path for obj in file_objs if obj.name.endswith('.sav')]
else:
    raise FileNotFoundError(f'{SAV_FILE_FOLDER} does not exist')

if len(sav_files) == 0:
    raise FileNotFoundError(f'No .sav files found in {SAV_FILE_FOLDER}')

for sav_file in sav_files:
    FILE_NAME = os.path.basename(os.path.splitext(sav_file)[0])
    WRITE_FILE = os.path.join(JSON_FILE_FOLDER, f'{FILE_NAME}.json')

    player_dict = convert_sav_to_dict(sav_file)
    output_json(player_dict, WRITE_FILE)

    if VISUALIZE_TIMELINE:
        visualize_timeline(player_dict)

# Clean up the JSON data and process into kill events
if os.path.isdir(JSON_FILE_FOLDER):
    file_objs = os.scandir(JSON_FILE_FOLDER)
    json_files = [obj.path for obj in file_objs if obj.name.endswith('.json')]
else:
    raise FileNotFoundError(f'{JSON_FILE_FOLDER} does not exist')

if len(json_files) == 0:
    raise FileNotFoundError(f'No .json files found in {JSON_FILE_FOLDER}')

for json_file in json_files:
    FILE_NAME = os.path.basename(os.path.splitext(json_file)[0])
    WRITE_FILE = os.path.join(CLEANED_FILE_FOLDER, f'{FILE_NAME}-killevents.json')

    # Load the JSON data
    filepath = os.path.join(JSON_FILE_FOLDER, json_file)
    with open(filepath, 'r', encoding='utf-8') as file:
        data = json.load(file)

    cleaned = get_valid_kill_events(data)
    json_out = {
        'KillEvents': cleaned
    }

    output_json(json_out, WRITE_FILE)
