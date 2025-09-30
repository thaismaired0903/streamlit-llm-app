# 専門家AI チャットアプリ

LangChainとStreamlitを使用した専門家AIチャットアプリケーションです。

## 機能

- 4つの専門分野から選択可能：
  - 医療専門家
  - 法律専門家
  - IT専門家
  - 教育専門家
- リアルタイムでAI専門家とチャット
- チャット履歴の表示
- 直感的なUI/UX

## セットアップ

### 必要な環境
- Python 3.11
- OpenAI API キー

### インストール

1. リポジトリをクローン：
```bash
git clone <repository-url>
cd streamlit-llm-app
```

2. 仮想環境の作成と有効化：
```bash
python -m venv env
source env/bin/activate  # macOS/Linux
# or
env\Scripts\activate  # Windows
```

3. 依存関係のインストール：
```bash
pip install -r requirements.txt
```

### 設定

#### ローカル実行の場合
`.streamlit/secrets.toml` ファイルを作成し、OpenAI API キーを設定：

```toml
OPENAI_API_KEY = "your-openai-api-key-here"
```

#### Streamlit Community Cloud デプロイの場合
アプリの設定でシークレットに以下を追加：

```toml
OPENAI_API_KEY = "your-openai-api-key-here"
```

## 実行

```bash
streamlit run app.py
```

## デプロイ

このアプリはStreamlit Community Cloudに対応しています：

1. GitHubにリポジトリをプッシュ
2. Streamlit Community Cloudでアプリを作成
3. シークレット設定でOPENAI_API_KEYを設定
4. デプロイ

## 技術スタック

- **Streamlit**: Webアプリフレームワーク
- **LangChain**: LLMアプリケーション開発フレームワーク
- **OpenAI GPT-3.5-turbo**: 言語モデル
- **Python 3.11**: プログラミング言語