import requests
import json

DIET_API_URL = "https://kokkai.ndl.go.jp/api/speech"

def fetch_diet_records(keyword="少子化", max_records=10):
    """Fetch recent Diet statements containing the given keyword directly from the speech API."""
    params = {
        "any": keyword,
        "recordPacking": "json",
        "maximumRecords": max_records
    }
    
    print(f"Fetching Diet records for keyword: '{keyword}'...")
    try:
        response = requests.get(DIET_API_URL, params=params)
        response.raise_for_status()
        data = response.json()
        
        records = []
        for speech in data.get("speechRecord", []):
            speech_text = speech.get("speech", "")
            # 只の挨拶や短い発言を除外するため少しフィルタリング
            if keyword in speech_text and len(speech_text) > 30:
                records.append({
                    "id": speech.get("speechID"),
                    "speaker": speech.get("speaker"),
                    "meeting": speech.get("nameOfMeeting"),
                    "date": speech.get("date"),
                    "voice": speech_text
                })
        return records
    except Exception as e:
        print(f"Error fetching from Diet API: {e}")
        return []

if __name__ == "__main__":
    records = fetch_diet_records(max_records=3)
    for r in records:
        print(f"[{r['date']}] {r['speaker']}: {r['voice'][:100]}...\n")
