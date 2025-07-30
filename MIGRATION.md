# Talk to the City - Migration Guide

## 🚨 重要な更新

このプロジェクトは最新のLangChain v0.3およびOpenAI API v1との互換性を確保するために更新されました。

## 🔄 主な変更点

### ライブラリバージョン更新
- `openai`: 0.28.1 → 1.30.0+
- `langchain`: 0.0.308 → 0.3.0+
- 新しい依存関係: `langchain-openai`, `langchain-core`, `langchain-community`

### コード変更
- **インポートパス更新**:
  - `from langchain.chat_models import ChatOpenAI` → `from langchain_openai import ChatOpenAI`
  - `from langchain.embeddings import OpenAIEmbeddings` → `from langchain_openai import OpenAIEmbeddings`
  - `from langchain.schema import AIMessage` → `from langchain_core.messages import AIMessage`

- **API変更**:
  - `ChatOpenAI(model_name=...)` → `ChatOpenAI(model=...)`
  - `llm(messages=...)` → `llm.invoke(...)`

## 🛠️ 移行手順

### 自動移行（推奨）

1. **移行スクリプトの実行**:
   ```bash
   cd talk-to-the-city-reports/scatter/pipeline
   python ../migrate_to_latest.py
   ```

2. **環境変数の設定**:
   ```bash
   export OPENAI_API_KEY=your_api_key_here
   ```

3. **テスト実行**:
   ```bash
   python main.py configs/example-polis.json
   ```

### 手動移行

1. **仮想環境の作成（推奨）**:
   ```bash
   python -m venv venv_new
   source venv_new/bin/activate  # Linux/Mac
   # または
   venv_new\Scripts\activate  # Windows
   ```

2. **依存関係の更新**:
   ```bash
   pip install -U pip
   pip install -r requirements.txt
   ```

3. **NLTK データのダウンロード**:
   ```bash
   python -c "import nltk; nltk.download('stopwords')"
   ```

## 🧪 動作確認

### 基本テスト
```bash
# 移行スクリプトでテスト
python migrate_to_latest.py

# 実際のパイプライン実行
python main.py configs/example-polis.json
```

### 期待される結果
- エラーなしでパイプラインが開始される
- `outputs/example-polis/` ディレクトリにファイルが生成される
- 最終的に `report/` フォルダが作成される

## 🐛 トラブルシューティング

### よくある問題

#### 1. インポートエラー
```
ImportError: cannot import name 'ChatOpenAI' from 'langchain.chat_models'
```
**解決方法**: 新しいライブラリがインストールされていません
```bash
pip install -r requirements.txt
```

#### 2. API仕様エラー
```
TypeError: ChatOpenAI() got an unexpected keyword argument 'model_name'
```
**解決方法**: コードが更新されていません。移行スクリプトを再実行してください。

#### 3. OpenAI API エラー
```
openai.AuthenticationError: No API key provided
```
**解決方法**: 環境変数を設定してください
```bash
export OPENAI_API_KEY=your_api_key_here
```

#### 4. バージョン競合
```
ERROR: pip's dependency resolver does not currently have a way to resolve this conflict
```
**解決方法**: 新しい仮想環境で再インストール
```bash
python -m venv venv_clean
source venv_clean/bin/activate
pip install -r requirements.txt
```

## 📋 更新されたファイル一覧

- `requirements.txt` - 依存関係の更新
- `pipeline/utils.py` - メッセージインポートの更新
- `pipeline/steps/extraction.py` - ChatOpenAI API更新
- `pipeline/steps/embedding.py` - OpenAIEmbeddings インポート更新
- `pipeline/steps/labelling.py` - ChatOpenAI API更新
- `pipeline/steps/takeaways.py` - ChatOpenAI API更新
- `pipeline/steps/overview.py` - ChatOpenAI API更新
- `pipeline/steps/translation.py` - 完全書き直し
- `pipeline/steps/aggregation.py` - 不要なインポート削除

## 💡 新機能の活用

### より安定したAPI
- OpenAI API v1の安定性向上
- LangChain v0.3の新機能

### 改善されたエラーハンドリング
- より詳細なエラーメッセージ
- 自動リトライ機能の改善

### パフォーマンス向上
- 最適化されたライブラリバージョン
- メモリ使用量の改善

## 🆘 サポート

問題が発生した場合：

1. **ログの確認**: エラーメッセージを詳しく確認
2. **環境の確認**: Python バージョン、依存関係の確認
3. **クリーンインストール**: 新しい仮想環境での再インストール

## ✅ 移行完了チェックリスト

- [ ] 新しい依存関係のインストール完了
- [ ] `migrate_to_latest.py` の実行成功
- [ ] OPENAI_API_KEY の設定完了
- [ ] `python main.py configs/example-polis.json` の実行成功
- [ ] 出力ファイルの生成確認
- [ ] レポートの表示確認

移行が完了したら、通常通りプロジェクトを使用できます！ 