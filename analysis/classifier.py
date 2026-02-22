import csv

class CLODClassifier:
    def __init__(self):
        # A simple keyword-based mock classification for Japanese text
        self.l1_mapping = {
            "汚い": "環境",
            "ごみ": "環境",
            "おちば": "環境",
            "木": "環境",
            "信号": "インフラ",
            "壊れ": "インフラ",
            "道路": "インフラ",
            "予算": "ガバナンス",
            "透明": "ガバナンス",
            "理念": "抽象・コミュニティ",
            "方針": "抽象・コミュニティ"
        }
        
    def process_layer_1(self, data):
        # L1: Keyword Extraction / Basic Topic
        text = data.get("voice", "")
        topic = "その他"
        for kw, cat in self.l1_mapping.items():
            if kw in text:
                topic = cat
                break
        data["L1_Topic"] = topic
        return data
        
    def process_layer_2(self, data):
        # L2: Urgency/Sentiment (Mock logic)
        text = data.get("voice", "")
        urgency = "高" if "壊れ" in text or "汚い" in text or "緊急" in text else "通常"
        data["L2_Urgency"] = urgency
        return data
        
    def process_layer_3(self, data):
        # L3: Actionability (Mock logic)
        topic = data.get("L1_Topic", "")
        action = "直接介入" if topic in ["環境", "インフラ"] else "戦略的計画"
        data["L3_Actionability"] = action
        return data
        
    def process_layer_4(self, data):
        # L4: Final Categorization output
        data["L4_Final_Status"] = "処理済み"
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
