'''
Reorder player data in JSON
'''
import json
import os
from datetime import datetime

def get_valid_kill_events(json_data: dict,
                          exp_tickrate: int = 25,
                          tickrate_tolerance: float = 5.0,
                          window_secs: int = 2):
    '''
    Clean and extract only valid kill event data
    '''

    expected_tdelta = 1 / exp_tickrate # time in between entries
    upper_bound_t = expected_tdelta * (1 + tickrate_tolerance)
    expected_num_entries = window_secs * exp_tickrate
    expected_num_entries_total = expected_num_entries * 2

    # Extract PlayerData into map by player
    player_data = json_data['PlayerData']
    player_data_map = {}
    for entry in player_data:
        if entry['PlayerName'] not in player_data_map:
            player_data_map[entry['PlayerName']] = []
        player_data_map[entry['PlayerName']].append(entry)

    cleaned_data = []
    for name, pdata in player_data_map.items():
        # find continous data around one or more kills
        player_killchains = []
        last_time = None
        killchain = []
        for entry in pdata:
            if last_time is None:
                last_time = datetime.strptime(entry['Datetime'], '%Y-%m-%d %H:%M:%S.%f')
                killchain.append(entry)
                continue
            current_time = datetime.strptime(entry['Datetime'], '%Y-%m-%d %H:%M:%S.%f')
            delta = current_time - last_time
            if delta.total_seconds() < upper_bound_t:
                killchain.append(entry)
            else:
                if len(killchain) >= expected_num_entries_total:
                    player_killchains.append(killchain)
                killchain = [entry]
            last_time = current_time

        # get fixed number of data points around each kill
        kill_events = []
        k_val = 0
        for chain in player_killchains:
            kills = []
            for jdx, entry in enumerate(chain):
                if entry['K'] > k_val:
                    k_val = entry['K']
                    kills.append(jdx)
            for kill_idx in kills:
                lower_bound = kill_idx - expected_num_entries
                upper_bound = kill_idx + expected_num_entries
                kill_events.append(chain[lower_bound:upper_bound])

        for chain in kill_events:
            if len(chain) == expected_num_entries_total:
                cleaned_data.append(chain)

        print(f'\nPlayer: {name}, raw entry count: {len(pdata)}')

    return cleaned_data

if __name__ == '__main__':
    JSON_FOLDER = r"C:\Users\jared\Desktop\basicallyhomeless\WALDO\repos\Python-GVAS-JSON-Converter\JsonFiles"
    CLEANED_FOLDER = r"C:\Users\jared\Desktop\basicallyhomeless\WALDO\repos\Python-GVAS-JSON-Converter\CleanedJsonFiles"
    JSON_FILENAME = "WaldoData%Argonne%2,024_8_29-2_6.json"

    # Load the JSON data
    filepath = os.path.join(JSON_FOLDER, JSON_FILENAME)
    with open(filepath, 'r', encoding='utf-8') as file:
        data = json.load(file)

    # clean data
    cleaned = get_valid_kill_events(data)
    json_out = {
        'KillEvents': cleaned
    }

    # Save the cleaned data
    filename = os.path.splitext(JSON_FILENAME)[0]
    filepath = os.path.join(CLEANED_FOLDER, f'{filename}-killevents.json')
    with open(filepath, 'w', encoding='utf-8') as file:
        json.dump(json_out, file, indent=4)

    print(f'Saved cleaned data to {filepath}')
