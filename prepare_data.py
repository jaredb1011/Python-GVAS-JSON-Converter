'''
Prepare Operation Harsh Doorstop Waldo Mod UE4 GVAS (.sav) Savegame files
'''
import json
import os
from DataPrep.convert_sav_to_json import convert_sav_to_dict, output_json
from DataPrep.visualize_data import visualize_timeline
from DataPrep.clean_data import get_valid_kill_events

def convert_savs(sav_files_path, json_files_path, visualize=False):
    "Convert .sav files to .json files"
    errors = []
    if os.path.isdir(sav_files_path):
        file_objs = os.scandir(sav_files_path)
        sav_files = [obj.path for obj in file_objs if obj.name.endswith('.sav')]
    else:
        raise FileNotFoundError(f'{sav_files_path} does not exist')

    if len(sav_files) == 0:
        raise FileNotFoundError(f'No .sav files found in {sav_files_path}')

    for sav_file in sav_files:
        filename = os.path.basename(os.path.splitext(sav_file)[0])
        writefile = os.path.join(json_files_path, f'{filename}.json')

        try:
            player_dict = convert_sav_to_dict(sav_file)
        except (UnicodeDecodeError, KeyError) as e:
            print(f'Error converting {sav_file}: {e}')
            errors.append((sav_file, e))
            continue
        output_json(player_dict, writefile)

        if visualize:
            visualize_timeline(player_dict)

    return errors

def clean_data(json_files_path, cleaned_files_path):
    "Clean up the JSON data and process into kill events"
    errors = []
    if os.path.isdir(json_files_path):
        file_objs = os.scandir(json_files_path)
        json_files = [obj.path for obj in file_objs if obj.name.endswith('.json')]
    else:
        raise FileNotFoundError(f'{json_files_path} does not exist')

    if len(json_files) == 0:
        raise FileNotFoundError(f'No .json files found in {json_files_path}')

    for json_file in json_files:
        filename = os.path.basename(os.path.splitext(json_file)[0])
        writefile = os.path.join(cleaned_files_path, f'{filename}-killevents.json')

        # Load the JSON data
        filepath = os.path.join(json_files_path, json_file)
        with open(filepath, 'r', encoding='utf-8') as file:
            data = json.load(file)

        try:
            cleaned = get_valid_kill_events(data)
            json_out = {
                'KillEvents': cleaned
            }
        except (UnicodeDecodeError, KeyError) as e:
            print(f'Error converting {json_file}: {e}')
            errors.append((json_file, e))
            continue
        output_json(json_out, writefile)

    return errors

if __name__ == '__main__':

    SAV_FILE_FOLDER     = r"C:\Users\jared\Desktop\basicallyhomeless\WALDO\Game_Servers\OHD\OHDSavesFromServer\Raw\WaldoData_OHD_Risala"
    JSON_FILE_FOLDER    = r"C:\Users\jared\Desktop\basicallyhomeless\WALDO\Game_Servers\OHD\OHDSavesFromServer\Converted\WaldoData_OHD_Risala"
    CLEANED_FILE_FOLDER = r"C:\Users\jared\Desktop\basicallyhomeless\WALDO\Game_Servers\OHD\OHDSavesFromServer\Cleaned\WaldoData_OHD_Risala"

    VISUALIZE_TIMELINE = False

    convert_errors = convert_savs(SAV_FILE_FOLDER, JSON_FILE_FOLDER, VISUALIZE_TIMELINE)
    clean_errors   = clean_data(JSON_FILE_FOLDER, CLEANED_FILE_FOLDER)

    if len(convert_errors) > 0:
        print('Errors converting .sav files:')
        for error in convert_errors:
            print(f'{error[0]}: {error[1]}')

    if len(clean_errors) > 0:
        print('Errors cleaning .json files:')
        for error in clean_errors:
            print(f'{error[0]}: {error[1]}')