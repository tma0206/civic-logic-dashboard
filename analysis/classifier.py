import csv

class CLODClassifier:
    def __init__(self):
        # 政治的発言の論理的深度（Logical Depth）を評価するためのキーワードベースモデル
        self.l1_mapping = {
            "少子化": "少子化対策",
            "子ども": "子育て支援",
            "教育": "教育政策",
            "予算": "財政・予算"
        }
        
    def process_layer_1(self, data):
        # L1: トピック (Topic)
        text = data.get("voice", "")
        topic = "その他"
        for kw, cat in self.l1_mapping.items():
            if kw in text:
                topic = cat
                break
        data["L1_Topic"] = topic
        return data
        
    def process_layer_2(self, data):
        # L2: コミットメントの強さ (Commitment Level)
        text = data.get("voice", "")
        # 具体的な行動や公約を示す強い言葉があるか？
        strong_keywords = ["約束", "実現", "達成", "目標", "法案", "引き上げ", "倍増"]
        urgency = "通常（検討・注視）"
        if any(kw in text for kw in strong_keywords):
            urgency = "高（具体的な公約・行動）"
            
        data["L2_Urgency"] = urgency
        return data
        
    def process_layer_3(self, data):
        # L3: エビデンス・検証可能性 (Actionability & Evidence)
        text = data.get("voice", "")
        # 数字や統計に言及しているか？
        evidence_keywords = ["％", "パーセント", "万人", "億円", "兆円", "低下", "減少", "統計", "推移"]
        action = "エビデンスなし（抽象的）"
        has_evidence = False
        if any(kw in text for kw in evidence_keywords):
            action = "エビデンスあり（データ言及）"
            has_evidence = True
            
        data["L3_Actionability"] = action
        data["Has_Evidence"] = has_evidence
        return data
        
    def process_layer_4(self, data):
        # L4: 論理的深度スコア (Logical Depth Score)
        urgency = data.get("L2_Urgency", "")
        evidence = data.get("L3_Actionability", "")
        
        # L2（コミットメント）と L3（エビデンス）の組み合わせでレベルを決定
        if urgency == "高（具体的な公約・行動）" and evidence == "エビデンスあり（データ言及）":
            score = "Level 4: データに基づく具体策"
        elif urgency == "高（具体的な公約・行動）":
            score = "Level 3: 強いコミットメント（根拠弱）"
        elif evidence == "エビデンスあり（データ言及）":
            score = "Level 2: 現状分析（具体策弱）"
        else:
            score = "Level 1: 抽象的な議論・ポピュリズム"
            
        data["L4_Final_Status"] = score
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
