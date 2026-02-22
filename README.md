# 🏛️ C-LOD: Civic Logic Dashboard

**C-LOD** は、政治家の発言（国会会議録）と、現実に起きている社会の統計データ（e-Stat）を直結させ、政治の**「論理的深度（Logical Depth）」**と**「Reality Gap（言行不一致）」**を可視化するダッシュボードです。

## ✨ 特徴 (Features)

1. **Instant Gratification (デモモード内蔵)**
   APIキーなしで即座に価値を体験できるように、事前に取得した「少子化」「防衛費」「DX」などのデータ（Starter Pack）を内蔵しています。
2. **Metadata-First Hybrid Search**
   高速にメタデータをリスト表示し、ユーザーがクリックした発言のみ、L1（トピック）からL4（論理的深度）までの重いスコアリング解析を遅延実行します。
3. **Causality Visualization (因果の可視化)**
   「発言が行われたタイミング（年）」と「その後の実際の統計データの推移」を同一グラフ上でオーバーレイすることで、公約と結果のギャップを直感的に気づかせます。

---

## 🚀 セットアップと起動方法

本プロジェクトは Python >= 3.11 環境を推奨します。

### 1. リポジトリのクローンと依存関係のインストール
```sh
git clone https://github.com/tma0206/civic-logic-dashboard.git
cd civic-logic-dashboard
pip install -r requirements.txt
```

### 2. 環境変数の設定 (Live APIモードをご利用の場合)
e-Stat (政府統計API) から最新の実データを取得するには、App IDが必要です。取得したApp IDを環境変数として設定します。

`.env.example` をコピーして `.env` ファイルを作成し、ご自身のIDを貼り付けてください。
```sh
# .env ファイルの例
ESTAT_APP_ID=your_actual_app_id_here
```
*(※ .env ファイルがない、またはApp IDが未設定の場合は、システムが自動的にフェールセーフのダミー統計データを使用してダッシュボードの表示を維持します。)*

### 3. アプリケーションの起動
```sh
streamlit run dashboard/app.py
```
ブラウザが起動し、`http://localhost:8501` 等でダッシュボードが表示されます。

---

## 🏗️ 4-Layer 分析モデルについて
裏側の `analysis/classifier.py` では、以下の4つのレイヤーで発言の「深さ」を評価しています。

- **Layer 1 (トピック)**: 発言が対象としている政策課題。
- **Layer 2 (コミットメント)**: 発言の中での行動への約束度（「検討する」vs「XXまでに達成する」）。
- **Layer 3 (エビデンス)**: 発言の裏付けとなる具体的なデータや基準（「％」「兆円」等の有無）。
- **Layer 4 (論理的深度)**: L1〜L3を総合し、発言がLevel 1(ポピュリズム)〜Level 4(データに基づく公策)のどれに該当するかをスコアリング。
