'''
Plot a timeline of player data from JSON data
'''
from datetime import datetime
import json
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

def visualize_timeline(json_data: dict) -> None:
    '''
    Plot a timeline of player data from JSON data
    '''
    # Extract PlayerData
    player_data = json_data['PlayerData']

    # Convert datetime strings to datetime objects
    for entry in player_data:
        entry['Datetime'] = datetime.strptime(entry['Datetime'], '%Y-%m-%d %H:%M:%S.%f')

    # Sort the data by datetime
    player_data.sort(key=lambda x: x['Datetime'])

    # Extract datetime and player names
    datetimes = [entry['Datetime'] for entry in player_data]
    player_names = [entry['PlayerName'] for entry in player_data]

    # Create the plot
    _, ax = plt.subplots(figsize=(12, 6))

    # Plot the data points
    ax.scatter(datetimes, player_names, marker='o')

    # Format the x-axis
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M:%S'))
    plt.xticks(rotation=45, ha='right')

    # Set labels and title
    plt.xlabel('Datetime')
    plt.ylabel('Player Name')
    plt.title('Player Activity Timeline')

    # Adjust layout and display the plot
    plt.tight_layout()
    plt.show()

if __name__ == '__main__':
    # Load the JSON data
    with open('JsonFiles/WaldoDataReworkEditor.json', 'r', encoding='utf-8') as file:
        data = json.load(file)

    visualize_timeline(data)
