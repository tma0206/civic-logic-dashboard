import requests
import json
import urllib.parse

DIET_API_URL = "https://kokkai.ndl.go.jp/api/speech"

def fetch_diet_records(keyword="少子化", max_records=10, is_fallback=False):
    """Fetch recent Diet statements containing the given keyword directly from the speech API."""
    
    # 1 & 2: URL-encode the keyword (UTF-8) explicitly to avoid Windows encoding issues
    encoded_keyword = urllib.parse.quote(keyword)
    
    # Construct exact URL manually to ensure requests doesn't mangle it
    url_with_params = f"{DIET_API_URL}?any={encoded_keyword}&recordPacking=json&maximumRecords={max_records}"
    
    # 3: Log the EXACT URL being called
    print(f"Fetching Diet records for keyword: '{keyword}'")
    print(f"Exact Request URL: {url_with_params}")
    
    try:
        response = requests.get(url_with_params)
        response.raise_for_status()
        data = response.json()
        
        records = []
        for speech in data.get("speechRecord", []):
            speech_text = speech.get("speech", "")
            # 只の挨拶や短い発言を除外するため少しフィルタリング
            if len(speech_text) > 30:
                records.append({
                    "id": speech.get("speechID"),
                    "speaker": speech.get("speaker"),
                    "meeting": speech.get("nameOfMeeting"),
                    "date": speech.get("date"),
                    "voice": speech_text
                })
                
        # 4: Fallback to ASCII keyword "GDP" if 0 results
        if not records and not is_fallback:
            print(f"Warning: 0 records found for '{keyword}'. Falling back to ASCII keyword 'GDP'...")
            return fetch_diet_records(keyword="GDP", max_records=max_records, is_fallback=True)
            
        return records
    except Exception as e:
        print(f"Error fetching from Diet API: {e}")
        # Fallback to UTF-8 safe ASCII keyword to test connection
        if not is_fallback:
            print(f"Exception caught. Falling back to ASCII keyword 'GDP'...")
            return fetch_diet_records(keyword="GDP", max_records=max_records, is_fallback=True)
        return []

if __name__ == "__main__":
    records = fetch_diet_records(max_records=3)
    print(f"\nTotal Records Fetched: {len(records)}")
    for r in records:
        print(f"[{r['date']}] {r['speaker']}: {r['voice'][:100]}...\n")
