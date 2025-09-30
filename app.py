import streamlit as st
import os
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage

# アプリのタイトルと説明
st.title("🤖 専門家AI チャットアプリ")
st.markdown("""
## 概要
このアプリでは、異なる専門分野のAI専門家とチャットすることができます。
ラジオボタンで専門家の種類を選択し、質問を入力してください。

## 操作方法
1. **専門家の種類を選択**: ラジオボタンから相談したい専門家を選択してください
2. **質問を入力**: テキストフィールドに質問や相談内容を入力してください
3. **送信**: 「送信」ボタンをクリックして回答を取得してください

## 利用可能な専門家
- **医療専門家**: 健康や医療に関する質問にお答えします
- **法律専門家**: 法律や権利に関する相談に対応します
- **IT専門家**: プログラミングや技術的な問題を解決します
- **教育専門家**: 学習方法や教育に関するアドバイスを提供します
""")

st.divider()

def get_expert_response(input_text: str, expert_type: str) -> str:
    """
    専門家の種類と入力テキストに基づいてLLMからの回答を取得する関数
    
    Args:
        input_text (str): ユーザーからの入力テキスト
        expert_type (str): 選択された専門家の種類
    
    Returns:
        str: LLMからの回答
    """
    # OpenAI API キーの確認
    if "OPENAI_API_KEY" not in st.secrets:
        return "⚠️ OpenAI API キーが設定されていません。Streamlit Community Cloudのシークレット設定でOPENAI_API_KEYを設定してください。"
    
    try:
        # ChatOpenAI インスタンスの作成
        llm = ChatOpenAI(
            model="gpt-3.5-turbo",
            temperature=0.7,
            openai_api_key=st.secrets["OPENAI_API_KEY"]
        )
        
        # 専門家の種類に応じたシステムメッセージの定義
        expert_prompts = {
            "医療専門家": """あなたは経験豊富な医療専門家です。
医学的知識と臨床経験に基づいて、患者の健康や医療に関する質問に丁寧かつ正確にお答えします。
ただし、具体的な診断や治療の決定については必ず医療機関での相談を勧めてください。
専門用語を使う際は、一般の方にも理解しやすいよう説明を添えてください。""",
            
            "法律専門家": """あなたは経験豊富な法律専門家です。
法律知識と実務経験に基づいて、法的な問題や権利に関する質問に正確かつ分かりやすくお答えします。
複雑な法的概念については、具体例を交えて説明してください。
重要な法的判断については、必ず専門の弁護士への相談を勧めてください。""",
            
            "IT専門家": """あなたは経験豊富なIT専門家です。
プログラミング、システム設計、技術的な問題解決に関する深い知識を持っています。
技術的な質問に対して、実践的で具体的なソリューションを提供してください。
コードサンプルや手順を示す際は、初心者にも理解しやすいよう説明を添えてください。""",
            
            "教育専門家": """あなたは経験豊富な教育専門家です。
学習理論と教育実践に基づいて、学習方法や教育に関する質問に建設的なアドバイスを提供します。
個人の学習スタイルや状況に配慮した、実践的な学習戦略を提案してください。
年齢や学習レベルに応じて、適切な説明をしてください。"""
        }
        
        # システムメッセージの設定
        system_message = SystemMessage(content=expert_prompts[expert_type])
        human_message = HumanMessage(content=input_text)
        
        # LLMに質問を送信
        messages = [system_message, human_message]
        response = llm.invoke(messages)
        
        return response.content
        
    except Exception as e:
        return f"エラーが発生しました: {str(e)}"

# メインのUI
col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("専門家選択")
    expert_type = st.radio(
        "相談したい専門家を選択してください:",
        ["医療専門家", "法律専門家", "IT専門家", "教育専門家"],
        help="質問の内容に応じて適切な専門家を選択してください"
    )

with col2:
    st.subheader("質問入力")
    input_text = st.text_area(
        "質問や相談内容を入力してください:",
        height=150,
        placeholder=f"{expert_type}に相談したい内容を詳しく入力してください...",
        help="具体的で詳細な質問をいただくと、より適切な回答を提供できます"
    )

# 送信ボタン
if st.button("送信", type="primary", use_container_width=True):
    if input_text.strip():
        with st.spinner(f"{expert_type}が回答を準備中..."):
            # 専門家からの回答を取得
            response = get_expert_response(input_text, expert_type)
            
            # 回答の表示
            st.subheader(f"💡 {expert_type}からの回答")
            st.write(response)
            
            # セッション状態に履歴を保存（オプション）
            if "chat_history" not in st.session_state:
                st.session_state.chat_history = []
            
            st.session_state.chat_history.append({
                "expert": expert_type,
                "question": input_text,
                "answer": response
            })
    else:
        st.warning("質問を入力してください。")

# チャット履歴の表示（オプション）
if "chat_history" in st.session_state and st.session_state.chat_history:
    st.divider()
    st.subheader("📝 チャット履歴")
    
    # 最新の履歴のみ表示（最大5件）
    recent_history = st.session_state.chat_history[-5:]
    
    for i, chat in enumerate(reversed(recent_history)):
        with st.expander(f"{chat['expert']} - {chat['question'][:50]}..." if len(chat['question']) > 50 else f"{chat['expert']} - {chat['question']}"):
            st.write("**質問:**")
            st.write(chat['question'])
            st.write("**回答:**")
            st.write(chat['answer'])

# フッター
st.divider()
st.markdown("""
### 注意事項
- このアプリはAIによる回答を提供しますが、最終的な判断は専門家にご相談ください
- 医療や法律に関する重要な決定については、必ず資格を持った専門家にご相談ください
- 個人情報や機密情報の入力は避けてください

### Python バージョン
- このアプリはPython 3.11で動作します
""")
