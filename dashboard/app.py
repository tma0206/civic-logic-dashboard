import streamlit as st
import pandas as pd
import altair as alt
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from ingestion.api_client import fetch_diet_records
from ingestion.estat_client import fetch_birth_rate_stats
from analysis.classifier import CLODClassifier

st.set_page_config(page_title="C-LOD リアル分析", layout="wide", page_icon="🏛️")

def main():
    st.title("🏛️ C-LOD: 政治発言の論理的深度分析 🇯🇵")
    st.markdown("国会会議録とe-Stat（政府統計）を連携させ、政治家の発言の「論理的深度（L1-L4）」と現実のギャップを可視化します。")

    # サイドバーでキーワード設定
    st.sidebar.header("🔍 分析設定")
    keyword = st.sidebar.text_input("検索キーワード", value="少子化")
    limit = st.sidebar.slider("取得件数", min_value=1, max_value=30, value=10)
    
    # データの取得と分析
    classifier = CLODClassifier()
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("🗣️ 直近の国会発言（Diet Records）")
        
        # 開発用のキャッシュクリアボタン（強制リロード用）
        if st.sidebar.button("🔄 キャッシュをクリアして再取得", type="primary"):
            st.cache_data.clear()
            
        with st.spinner(f"「{keyword}」に関する国会発言を取得中... ⏳"):
            try:
                raw_records = fetch_diet_records(keyword=keyword, max_records=limit)
                # 追加: データをフロントエンドで正しく認識できているか確認するためのデバッグプリント
                st.success(f"📺 デバッグ: `{keyword}` のデータを {len(raw_records)} 件取得しました！")
            except Exception as e:
                st.error(f"国会会議録APIリクエストエラー: {e}")
                raw_records = []
            
        if not raw_records:
            st.warning("対象キーワードでの国会発言データが取得できませんでした。")
            st.info("💡 **ヒント**: \n- 検索期間内に該当の発言がない可能性があります。キーワードを「予算」や「教育」などに変えてみてください。\n- 実行環境（Windows PowerShell等）の文字コードの影響で日本語クエリが正しくAPIに送信されていない場合があります。その場合はコマンドプロンプトや `set PYTHONIOENCODING=utf-8` をお試しください。")
            return
            
        processed_records = [classifier.predict(r.copy()) for r in raw_records]
        df_diet = pd.DataFrame(processed_records)
        
        # 概要メトリクス
        st.write("### 📊 L4 深度分析スコア")
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Level 4 (データに基づく具体策)", len(df_diet[df_diet["L4_Final_Status"].str.contains("Level 4")]))
        m2.metric("Level 3 (強いコミットメント)", len(df_diet[df_diet["L4_Final_Status"].str.contains("Level 3")]))
        m3.metric("Level 2 (現状分析のみ)", len(df_diet[df_diet["L4_Final_Status"].str.contains("Level 2")]))
        m4.metric("Level 1 (抽象的・ポピュリズム)", len(df_diet[df_diet["L4_Final_Status"].str.contains("Level 1")]))
        
        # 発言データテーブル
        st.dataframe(
            df_diet[["date", "speaker", "voice", "L2_Urgency", "L3_Actionability", "L4_Final_Status"]],
            column_config={
                "date": "日付",
                "speaker": "発言者",
                "voice": st.column_config.TextColumn("発言内容", width="large"),
                "L2_Urgency": "コミットメント",
                "L3_Actionability": "エビデンス",
                "L4_Final_Status": "論理的深度 (L4)"
            },
            hide_index=True,
            use_container_width=True
        )

    with col2:
        st.subheader("📉 統計データとのギャップ検証")
        st.markdown("e-Statから取得した実際のデータ推移（例：出生数）")
        
        with st.spinner("e-Statデータを取得中... ⏳"):
            stats_data = fetch_birth_rate_stats()
            
        df_stats = pd.DataFrame(stats_data)
        
        # 折れ線グラフ
        chart = alt.Chart(df_stats).mark_line(point=True, color="firebrick").encode(
            x=alt.X("year:O", title="年"),
            y=alt.Y("births:Q", title="出生数", scale=alt.Scale(zero=False)),
            tooltip=["year", "births"]
        ).properties(
            title="日本の年間出生数推移",
            height=300
        )
        st.altair_chart(chart, use_container_width=True)
        
        st.info("💡 **Reality Gap Analysis**: \n\n国会での「強いコミットメント」や「論理的な具体策（L4）」が増えている一方で、実際の統計指標が改善されていない場合、そこには「実行プロセス」や「政策の有効性」における深刻なギャップが存在することを示唆しています。")

if __name__ == "__main__":
    main()
