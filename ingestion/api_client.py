import requests
import json

DIET_API_URL = "https://kokkai.ndl.go.jp/api/meeting_list"

def fetch_diet_records(keyword="少子化", max_records=10):
    """Fetch recent Diet statements containing the given keyword."""
    params = {
        "any": keyword,
        "recordPacking": "json",
        "maximumRecords": 3  # Fetch a few meeting records
    }
    
    print(f"Fetching Diet records for keyword: '{keyword}'...")
    try:
        response = requests.get(DIET_API_URL, params=params)
        response.raise_for_status()
        data = response.json()
        
        records = []
        for meeting in data.get("meetingRecord", []):
            for speech in meeting.get("speechRecord", []):
                speech_text = speech.get("speech", "")
                if keyword in speech_text:
                    records.append({
                        "id": speech.get("speechID"),
                        "speaker": speech.get("speaker"),
                        "meeting": meeting.get("nameOfMeeting"),
                        "date": meeting.get("date"),
                        "voice": speech_text
                    })
                    if len(records) >= max_records:
                        return records
        return records
    except Exception as e:
        print(f"Error fetching from Diet API: {e}")
        return []

if __name__ == "__main__":
    records = fetch_diet_records(max_records=2)
    for r in records:
        print(f"[{r['date']}] {r['speaker']}: {r['voice'][:100]}...\n")
