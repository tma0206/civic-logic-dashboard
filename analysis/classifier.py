import csv

class CLODClassifier:
    def __init__(self):
        # A simple keyword-based mock classification for demonstration purposes
        self.l1_mapping = {
            "dirty": "Environment",
            "tree": "Environment",
            "traffic": "Infrastructure",
            "broken": "Infrastructure",
            "budget": "Governance",
            "philosophy": "Abstract/Community"
        }
        
    def process_layer_1(self, data):
        # L1: Keyword Extraction / Basic Topic
        text = data.get("voice", "").lower()
        topic = "Other"
        for kw, cat in self.l1_mapping.items():
            if kw in text:
                topic = cat
                break
        data["L1_Topic"] = topic
        return data
        
    def process_layer_2(self, data):
        # L2: Urgency/Sentiment (Mock logic)
        text = data.get("voice", "").lower()
        urgency = "High" if "broken" in text or "dirty" in text else "Normal"
        data["L2_Urgency"] = urgency
        return data
        
    def process_layer_3(self, data):
        # L3: Actionability (Mock logic)
        topic = data.get("L1_Topic", "")
        action = "Direct Intervention" if topic in ["Environment", "Infrastructure"] else "Strategic Planning"
        data["L3_Actionability"] = action
        return data
        
    def process_layer_4(self, data):
        # L4: Final Categorization output
        data["L4_Final_Status"] = "Processed"
        return data
        
    def predict(self, data):
        l1_out = self.process_layer_1(data.copy())
        l2_out = self.process_layer_2(l1_out)
        l3_out = self.process_layer_3(l2_out)
        l4_out = self.process_layer_4(l3_out)
        return l4_out

def run_test():
    classifier = CLODClassifier()
    results = []
    
    with open('../test_data.csv', mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            result = classifier.predict(row)
            results.append(result)
            
    # Print results as a markdown table
    print("| ID | Original Voice | L1 (Topic) | L2 (Urgency) | L3 (Action) | L4 (Status) |")
    print("|---|---|---|---|---|---|")
    for r in results:
        print(f"| {r['id']} | {r['voice']} | {r['L1_Topic']} | {r['L2_Urgency']} | {r['L3_Actionability']} | {r['L4_Final_Status']} |")

if __name__ == "__main__":
    run_test()
