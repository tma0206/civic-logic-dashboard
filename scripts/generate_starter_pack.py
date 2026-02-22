import os
import json
import sys

# Ensure imports work
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from ingestion.api_client import fetch_diet_records

def main():
    keywords = ["少子化", "防衛費", "DX"]
    starter_pack = {}
    
    print("Generating Starter Pack Data...")
    for kw in keywords:
        print(f"Fetching data for: {kw}")
        # Fetch a reasonable number of records for the starter pack (e.g., 5)
        records = fetch_diet_records(keyword=kw, max_records=5)
        starter_pack[kw] = records
        
    data_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
    os.makedirs(data_dir, exist_ok=True)
    
    output_file = os.path.join(data_dir, 'starter_pack.json')
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(starter_pack, f, ensure_ascii=False, indent=2)
        
    print(f"Starter pack saved to {output_file}")

if __name__ == "__main__":
    main()
