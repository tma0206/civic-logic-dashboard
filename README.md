# Civic Logic & Outcome Dashboard (C-LOD)

## Project Overview
This is an open-source civic transparency system designed to visualize the correlation between official policy statements in public transcripts and subsequent public statistical data.

### 1. Analytical Framework: The 4-Layer Model
We categorize political discussions into four analytical layers using NLP to help citizens evaluate the depth of policy-making:
- **L1: Phenomenon** (Observed symptoms and immediate events)
- **L2: Mechanism** (Causal pathways and implementation methods)
- **L3: Structure** (Systemic causes and long-term patterns)
- **L4: Philosophy** (Core values and normative framing)

### 2. Technical Architecture
- **Data Ingestion**: Integrating Kokkai (Diet Record Search System) API and e-Stat (Government Statistics) API.
- **NLP Pipeline**: Semantic classification of transcripts into the 4-layer model.
- **Outcome Tracking**: Visualizing longitudinal trends in public metrics following specific policy commitments.

---

## プロジェクト概要（日本語）
本プロジェクトは、日本の公共政策における「論理的整合性」と「実効性」を可視化するためのオープンソース・シビックテックです。

### 解決したい課題
1. **議論の解像度不足**: 議事録を解析し、発言が「現象(L1)」「仕組み(L2)」「構造(L3)」「哲学(L4)」のどの階層にあるかを可視化します。
2. **効果測定の不在**: 過去の政策提言（議事録）と、その後の公的統計データ（e-Stat等）を時系列で照合し、政策の実行結果を客観的に評価できるダッシュボードを提供します。

### 開発者より
「馬鹿のふりしてガチを仕込む」。
感情的な批判ではなく、公開された「事実」と「論理」を突き合わせることで、国家というシステムのパフォーマンスをデバッグしましょう。

腕に覚えのあるエンジニア、データサイエンティストの参加を待っています。
