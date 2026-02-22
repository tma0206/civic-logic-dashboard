import streamlit as st
import pandas as pd
import altair as alt
import sys
import os
import json

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from ingestion.api_client import fetch_diet_records
from ingestion.estat_client import fetch_stats_for_keyword
from analysis.classifier import CLODClassifier
from analysis.insight_generator import generate_insight

st.set_page_config(page_title="C-LOD リアル分析", layout="wide", page_icon="🏛️")

@st.cache_data
def load_starter_pack():
    path = os.path.join(os.path.dirname(__file__), '..', 'data', 'starter_pack.json')
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def render_depth_gauge(score_text):
    if "Level 4" in score_text:
        pct, color = 100, "#28a745" # Green
    elif "Level 3" in score_text:
        pct, color = 75, "#007bff"  # Blue
    elif "Level 2" in score_text:
        pct, color = 50, "#ffc107"  # Yellow
    else:
        pct, color = 25, "#dc3545"  # Red
        
    html = f"""
    <div style="width: 100%; background-color: #333; border-radius: 5px; margin-bottom: 10px;">
      <div style="width: {pct}%; height: 24px; background-color: {color}; border-radius: 5px; text-align: center; color: { 'white' if pct != 50 else 'black' }; font-weight: bold; line-height: 24px;">
        {score_text}
      </div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)

def main():
    st.warning("**Current Version:** 1.1 Precision Update 🚀")
    st.title("🏛️ C-LOD: Policy vs. Reality (Gap Analysis) 🇯🇵")
    st.markdown("政治家の発言（Words）と現実の統計（Results）のギャップを即座に可視化し、発言の「論理的深度」を評価します。")

    # サイドバー：データソースと検索設定
    st.sidebar.header("⚙️ Data Source")
    data_mode = st.sidebar.radio("データソースを選択", ["Starter Pack (Demo)", "Live API Search (国会図書館)"])
    
    starter_data = load_starter_pack()
    
    keyword = "少子化"
    raw_records = []
    
    if data_mode == "Starter Pack (Demo)":
        st.sidebar.info("デモモード：保存済みのデータを高速表示します（APIキー不要）。")
        if starter_data:
            keyword = st.sidebar.selectbox("キーワード", list(starter_data.keys()))
            raw_records = starter_data[keyword]
        else:
            st.sidebar.error("Starter Packが見つかりません。")
    else:
        st.sidebar.warning("ライブモード：リアルタイムで国会APIをスキャンします。")
        keyword = st.sidebar.text_input("検索キーワード", value="少子化")
        limit = st.sidebar.slider("取得件数", min_value=1, max_value=30, value=5)
        
        if st.sidebar.button("🔍 ライブ検索実行", type="primary"):
            st.cache_data.clear()
            with st.spinner(f"「{keyword}」に関する国会発言を取得中... ⏳"):
                try:
                    raw_records = fetch_diet_records(keyword=keyword, max_records=limit)
                    st.session_state['live_records'] = raw_records
                    st.success(f"📺 デバッグ: `{keyword}` のデータを {len(raw_records)} 件取得しました！")
                except Exception as e:
                    st.error(f"国会会議録APIリクエストエラー: {e}")
                    
        # Button pressed logic memory
        if 'live_records' in st.session_state:
            raw_records = st.session_state['live_records']

    if not raw_records and data_mode == "Live API Search (国会図書館)":
        st.info("👈 サイドバーから「ライブ検索実行」をクリックしてデータを取得してください。")
        return
    elif not raw_records:
        st.warning("データがありません。")
        return

    # Metadata-First Search UI
    st.subheader(f"🗣️ 「{keyword}」に関する国会発言リスト")
    
    # Extract metadata for the table (excluding full voice text to keep it snappy)
    meta_df = pd.DataFrame(raw_records)[["date", "speaker", "meeting"]]
    meta_df.index = meta_df.index + 1 # 1-indexed for display
    
    st.dataframe(
        meta_df,
        column_config={
            "date": "発言日",
            "speaker": "発言者",
            "meeting": "会議名"
        },
        width="stretch"
    )
    
    # 選択した発言の分析 (Detailed Analysis)
    st.subheader("🧠 Deep Analysis (論理的深度の評価)")
    st.markdown("リストから発言を選んで、詳細な分析と現実データ（e-Stat）との比較を行います。")
    
    record_options = [f"[{r['date']}] {r['speaker']} ({r['meeting']})" for r in raw_records]
    selected_idx = st.selectbox("分析対象の発言を選択:", range(len(record_options)), format_func=lambda x: record_options[x])
    
    selected_record = raw_records[selected_idx]
    speech_year = selected_record['date'].split('-')[0] # Get the year for causality plot
    
    # 遅延評価：選択された時のみ L1-L4 分析を実行
    classifier = CLODClassifier()
    analyzed_record = classifier.predict(selected_record.copy())
    
    col_analysis, col_chart = st.columns([1, 1])
    
    with col_analysis:
        st.markdown("#### 発言内容 (Words)")
        st.info(f"「... {analyzed_record['voice'][:300]} ...」") # 抜粋表示
        
        # Evidence Badge
        if analyzed_record.get('Has_Evidence', False):
            st.markdown("### 🏅 Evidence Badge\n**[✅ Evidence Present]** 具体的な数値・データへの言及が確認されました。")
        else:
            st.markdown("### 🏅 Evidence Badge\n**[❌ No Evidence]** データに基づく客観的な裏付けが不足しています。")
        
        st.markdown("#### 論理的深度 (Logical Depth L1-L4)")
        render_depth_gauge(analyzed_record['L4_Final_Status'])
        
        st.markdown(f"**L2 (コミットメント):** {analyzed_record['L2_Urgency']}")
        if "Level 4" in analyzed_record['L4_Final_Status']:
            st.success("✅ **高評価**: 具体的なデータに基づいた実現性の高い公約です。")
        elif "Level 1" in analyzed_record['L4_Final_Status']:
            st.error("📉 **抽象的**: 具体性が欠けており、ポピュリズムの可能性があります。")

    with col_chart:
        st.markdown("#### 現実の統計推移 (Results - e-Stat)")
        
        with st.spinner("e-Statデータを取得中... ⏳"):
            stats_info = fetch_stats_for_keyword(keyword)
            
        st.markdown(f"**⚡ Causality Summary**\n- **Speech Topic:** `{keyword}`\n- **Statistic:** `{stats_info['title']}`")
        
        df_stats = pd.DataFrame(stats_info['data'])
        
        # Causality Visualization: Overlay the speech year on the reality chart
        base_chart = alt.Chart(df_stats).mark_line(point=True).encode(
            x=alt.X("year:O", title="年"),
            y=alt.Y("value:Q", title=stats_info['y_label'], scale=alt.Scale(zero=False)),
            tooltip=["year", "value"]
        ).properties( height=250 )
        
        # Highlight the year the speech was made
        try:
            speech_year_int = int(speech_year)
            # Find if speech year is in our stats data
            if str(speech_year) in df_stats['year'].values:
                highlight = alt.Chart(pd.DataFrame({'year': [str(speech_year)]})).mark_rule(color='red', strokeWidth=2).encode(
                    x='year:O'
                )
                final_chart = base_chart + highlight
                st.altair_chart(final_chart, width="stretch")
                st.caption(f"🔴 赤線: 発言が行われた年 ({speech_year}年)")
            else:
                st.altair_chart(base_chart, width="stretch")
                st.caption(f"（※発言年の{speech_year}年はグラフ表示範囲外です）")
        except:
            st.altair_chart(base_chart, width="stretch")

    st.markdown("---")
    st.subheader("🤖 AIのやさしい要約 (Gemini Insight)")
    with st.spinner("Geminiが発言とデータを読み解いています... ✨"):
        # We use the full text from analyzed_record['voice'] and the stats title
        insight_text = generate_insight(analyzed_record.get('voice', ''), keyword, stats_info.get('title', '関連統計'))
        st.info(insight_text, icon="💡")

if __name__ == "__main__":
    main()
