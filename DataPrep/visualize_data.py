'''
Plot a timeline of player data from JSON data
'''
from datetime import datetime
import json
import os
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import mplcursors

def visualize_timeline(json_data: dict) -> None:
    '''
    Plot a timeline of player data from JSON data
    '''
    # Extract PlayerData
    player_data = json_data['PlayerData']

    # Sort the data by datetime
    player_data.sort(key=lambda x: x['Datetime'])

    previous_kill_count = {}
    player_names = list(set([entry['PlayerName'] for entry in player_data]))
    for name in player_names:
        previous_kill_count[name] = 0

    kill_entries = []
    other_entries = []
    for entry in player_data:
        entry['Datetime'] = datetime.strptime(entry['Datetime'], '%Y-%m-%d %H:%M:%S.%f')
        current_kill_count = entry['K']
        if current_kill_count > previous_kill_count[entry['PlayerName']]:
            previous_kill_count[entry['PlayerName']] = current_kill_count
            kill_entries.append(entry)
        else:
            other_entries.append(entry)

    # Extract datetime and player names
    kill_datetimes = [entry['Datetime'] for entry in kill_entries]
    kill_names = [entry['PlayerName'] for entry in kill_entries]
    kill_killcounts = [entry['K'] for entry in kill_entries]
    other_datetimes = [entry['Datetime'] for entry in other_entries]
    other_names = [entry['PlayerName'] for entry in other_entries]
    #other_killcounts = [entry['K'] for entry in other_entries]

    # Create the plot
    _, ax = plt.subplots(figsize=(12, 6))

    # Plot the data points
    ax.scatter(other_datetimes, other_names, color='blue', marker='o', label='Ticks')
    scatter_kills = ax.scatter(kill_datetimes, kill_names, color='red', edgecolor='black', s=100, marker='o', label='Kills')

    # Format the x-axis
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M:%S'))
    plt.xticks(rotation=45, ha='right')

    # Set labels and title
    plt.xlabel('Datetime')
    plt.ylabel('Player Name')
    plt.title('Player Activity Timeline')
    plt.legend()

    # add cursor
    kill_cursor = mplcursors.cursor(scatter_kills, hover=True)
    @kill_cursor.connect("add")
    def on_add(sel):
        index = sel.index
        sel.annotation.set(text=f"Kill Count: {kill_killcounts[index]}\nDatetime: {kill_datetimes[index]}")
        sel.annotation.get_bbox_patch().set(fc="white", alpha=0.8)

    # display the plot
    plt.show()

if __name__ == '__main__':
    # Load the JSON data
    BASE_DIR = r"C:\Users\jared\Desktop\basicallyhomeless\WALDO\Game_Servers\OHD\OHDSavesFromServer"
    CONVERTED_JSON_FILE_DIR = os.path.join(BASE_DIR, "Converted", "WaldoData_OHD_Risala")
    JSON_FILENAME = "WaldoData%Risala%2,024_9_13-16_46.json"

    filepath = os.path.join(CONVERTED_JSON_FILE_DIR, JSON_FILENAME)
    with open(filepath, 'r', encoding='utf-8') as file:
        data = json.load(file)

    visualize_timeline(data)
