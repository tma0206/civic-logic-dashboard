import streamlit as st
import pandas as pd
import altair as alt
import sys
import os

# sys.path に親ディレクトリを追加しモジュールをインポート可能にする
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from ingestion.loader import load_data
from analysis.classifier import CLODClassifier

# ページの基本設定（モダンなレイアウトとアイコン）
st.set_page_config(page_title="C-LOD ダッシュボード", layout="wide", page_icon="🌸")

def main():
    st.title("🏛️ Civic Logic Dashboard (C-LOD) 🌸")
    st.markdown("市民の声を分析し、アクション可能なインサイトを提供します。 ✨")

    # --- 1. データ読み込み ---
    data_path = os.path.join(os.path.dirname(__file__), '..', 'test_data.csv')
    
    with st.spinner("データを読み込み中... ⏳"):
        raw_data = load_data(data_path)
    
    if not raw_data:
        st.error(f"データの読み込みに失敗しました。`test_data.csv` がルートディレクトリに存在するか確認してください。 🚨")
        return

    # --- 2. データ処理 ---
    classifier = CLODClassifier()
    processed_records = []
    
    with st.spinner("市民の声を分析中... 🧠"):
        for row in raw_data:
            result = classifier.predict(row.copy())
            processed_records.append(result)

    # DataFrameへの変換
    df = pd.DataFrame(processed_records)

    # --- 3. 概要（Overview） ---
    st.subheader("📊 プロジェクト概要")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("🗣️ フィードバック総数", len(df))
    with col2:
        high_urgency = len(df[df["L2_Urgency"] == "High"])
        st.metric("🚨 緊急案件", high_urgency)
    with col3:
        direct_actions = len(df[df["L3_Actionability"] == "Direct Intervention"])
        st.metric("⚡ 直接介入が必要な件数", direct_actions)

    st.divider()

    # --- 4. グラフ可視化 ---
    st.subheader("📈 トピック別分布 ＆ アクション")
    
    chart_col1, chart_col2 = st.columns(2)
    
    with chart_col1:
        # トピック別棒グラフ
        topic_counts = df["L1_Topic"].value_counts().reset_index()
        topic_counts.columns = ["Topic", "Count"]
        
        topic_chart = alt.Chart(topic_counts).mark_bar(cornerRadiusTopLeft=5, cornerRadiusTopRight=5).encode(
            x=alt.X("Topic", sort="-y", title="L1 トピックカテゴリ"),
            y=alt.Y("Count", title="件数"),
            color=alt.Color("Topic", legend=None, scale=alt.Scale(scheme="teals")),
            tooltip=["Topic", "Count"]
        ).properties(
            title="🏷️ トピックごとの声の数",
            height=320
        )
        st.altair_chart(topic_chart, use_container_width=True)

    with chart_col2:
        # アクション別ドーナツチャート
        action_counts = df["L3_Actionability"].value_counts().reset_index()
        action_counts.columns = ["Action", "Count"]
        
        action_chart = alt.Chart(action_counts).mark_arc(innerRadius=60).encode(
            theta=alt.Theta(field="Count", type="quantitative"),
            color=alt.Color(field="Action", type="nominal", scale=alt.Scale(scheme="set2")),
            tooltip=["Action", "Count"]
        ).properties(
            title="🎯 アクションタイプ",
            height=320
        )
        st.altair_chart(action_chart, use_container_width=True)

    st.divider()

    # --- 5. 生データテーブル ---
    st.subheader("📋 詳細な分析結果")
    st.markdown("L1層からL4層までのカテゴリ分類結果の一覧です。")
    
    st.dataframe(
        df[["id", "voice", "L1_Topic", "L2_Urgency", "L3_Actionability", "L4_Final_Status"]],
        column_config={
            "id": st.column_config.NumberColumn("ID", format="%d"),
            "voice": st.column_config.TextColumn("市民の声 🗣️", width="large"),
            "L1_Topic": st.column_config.TextColumn("L1 (トピック 🏷️)"),
            "L2_Urgency": st.column_config.TextColumn("L2 (緊急度 🚨)"),
            "L3_Actionability": st.column_config.TextColumn("L3 (アクション 🎯)"),
            "L4_Final_Status": st.column_config.TextColumn("L4 (ステータス ✅)")
        },
        hide_index=True,
        use_container_width=True
    )

if __name__ == "__main__":
    main()
