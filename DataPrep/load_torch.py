'''
Load data into a PyTorch DataLoader
'''

from datetime import datetime
import json
import os
import torch
from torch.utils.data import Dataset, DataLoader

class KillEventDataset(Dataset):
    def __init__(self, json_file):
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        self.kill_events = data['KillEvents']

    def __len__(self):
        return len(self.kill_events)

    def __getitem__(self, idx):
        kill_event = self.kill_events[idx]

        # Process each entry in the kill event
        event_data = []
        for entry in kill_event:
            # Convert datetime string to timestamp
            timestamp = datetime.strptime(entry['Datetime'], "%Y-%m-%d %H:%M:%S.%f").timestamp()

            # Extract features
            features = [
                timestamp,
                entry['DeltaPos']['X'],
                entry['DeltaPos']['Y'],
                entry['DeltaPos']['Z'],
                entry['DeltaRot']['X'],
                entry['DeltaRot']['Y'],
                entry['DeltaRot']['Z'],
                int(entry['isADS']),
                int(entry['isCrouched']),
                int(entry['isProne']),
                int(entry['isSprinting']),
                entry['Health'],
                entry['LastShotFireTime'],
                entry['K'],
                entry['A'],
                entry['D']
            ]
            event_data.append(features)

        return torch.tensor(event_data, dtype=torch.float32)

def collate_fn(batch):
    # This function will be used to collate the data into the desired shape
    return torch.stack(batch)  # [batch_size, num_ticks, num_features]

# Create DataLoader
def create_dataloader(json_file, batch_size=32):
    dataset = KillEventDataset(json_file)
    print(f'Loaded {len(dataset)} entries from {json_file}')
    return DataLoader(dataset, batch_size=batch_size, collate_fn=collate_fn, shuffle=True)

# Usage
CLEANED_FOLDER = r"C:\Users\jared\Desktop\basicallyhomeless\WALDO\repos\Python-GVAS-JSON-Converter\CleanedJsonFiles"
JSON_FILE = 'WaldoData%Argonne%2,024_8_29-2_6-killevents.json'
json_path = os.path.join(CLEANED_FOLDER, JSON_FILE)
dataloader = create_dataloader(json_path)

# Example of iterating through the dataloader
for loaded_batch in dataloader:
    print(loaded_batch.shape)  # Should be [batch_size, num_ticks, num_features]
    # Your training loop here
