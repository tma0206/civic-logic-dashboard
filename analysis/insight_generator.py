import os
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

# Initialize API Key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

try:
    if GEMINI_API_KEY:
        client = genai.Client(api_key=GEMINI_API_KEY)
    else:
        client = None
except Exception as e:
    print(f"Error initializing Gemini client: {e}")
    client = None

def generate_insight(speech_text, keyword, statistic_title):
    """
    Generates an empathetic, middle-school level summary and gap analysis 
    comparing the speech text and the statistical context.
    """
    if not client:
        return "⚠️ Gemini APIキーが設定されていないか、初期化に失敗しました。`.env` ファイルに正しい `GEMINI_API_KEY` を設定してください。"

    try:
        prompt = f"""
あなたは中学生にも分かるような、とても優しくて分かりやすい言葉で政治とデータについて解説する「AIガイド」です。
以下の「政治家の発言」と、現実の「関連する統計データ」を比較して、市民に向けた「やさしい要約」を作ってください。

【政治家の発言 (テーマ: {keyword})】
「{speech_text}」

【現実の統計データ】
{statistic_title}

以下の3つのポイントを含めて、柔らかい語り口で3〜4段落程度にまとめてください。
1. **発言の要約**: この政治家は、簡単に言うと何をしようとしているか？
2. **Reality Gap（言葉と現実のギャップ）**: 政治家はこう言っているけれど、実際の統計（{statistic_title}）の状況を考えると、何か矛盾や足りないことはあるか？
3. **市民へのワンポイントアドバイス**: 最後に、私たち市民はこれから何に注目すればいいか？
"""
        # Using gemini-2.5-flash for speed
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
        )
        return response.text
    except Exception as e:
        print(f"Gemini API Error: {e}")
        return f"AIの要約生成中にエラーが発生しました。時間を置いて再度お試しください。({str(e)})"
