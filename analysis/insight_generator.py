import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

# Initialize API Key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

def generate_insight(speech_text, keyword, statistic_title):
    """
    Generates an empathetic, middle-school level summary and gap analysis 
    comparing the speech text and the statistical context.
    """
    if not GEMINI_API_KEY:
        return "⚠️ Gemini APIキーが設定されていません。`.env` ファイルに `GEMINI_API_KEY` を設定してください。"

    try:
        model = genai.GenerativeModel("gemini-1.5-flash") # Use flash for quicker standard responses

        prompt = f"""
あなたは中学生にも分かるような、とても優しくて分かりやすい言葉で政治とデータについて解説する「AIガイド」です。
以下の「政治家の発言」と、現実の「関連する統計データ」を比較して、市民に向けた「やさしい要約」を作ってください。

【政治家の発言 (テーマ: {keyword})】
「{speech_text}」

【現実の統計データ】
{statistic_title}

以下の3つのポイントを含めて、柔らかい語り口（〜ですね、〜ですよ）で3〜4段落程度にまとめてください。
1. **発言の要約**: この政治家は、簡単に言うと何をしようとしているか？
2. **Reality Gap（言葉と現実のギャップ）**: 政治家はこう言っているけれど、実際の統計（{statistic_title}）の状況を考えると、何か矛盾や足りないことはあるか？（例: 「頑張ると言っているけれど、実際にはまだ数字は下がっているんです」など）
3. **市民へのワンポイントアドバイス**: 最後に、私たち市民はこれから何に注目すればいいか？（例: 「今後の予算が本当に使われるか見守りましょう！」など）

では、生成をお願いします。
"""
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"AIの要約生成中にエラーが発生しました。時間を置いて再度お試しください。({str(e)})"
