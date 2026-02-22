import csv
import os

def load_data(filepath):
    """
    Load citizen voice data from a CSV file.
    """
    print(f"Loading data from {filepath}...")
    if not os.path.exists(filepath):
        print(f"Error: File {filepath} not found.")
        return []
        
    records = []
    with open(filepath, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            records.append(row)
            
    return records

if __name__ == "__main__":
    # Test the loader
    data = load_data('../test_data.csv')
    print(f"Loaded {len(data)} records.")
    for d in data:
        print(d)
