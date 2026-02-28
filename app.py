import streamlit as st
import pandas as pd
import random

# --- 1. 頁面設定 ---
st.set_page_config(page_title="539 數據獵人", layout="wide")
st.title("🏆 今彩 539 數據獵人：專業分析版")

# --- 2. 側邊欄設定 ---
st.sidebar.header("🎯 539 實戰設定")
analysis_period = st.sidebar.slider("分析期數", 50, 500, 300)
play_type = st.sidebar.selectbox("選擇投注星數", options=[2, 3, 4, 5], index=1)

# --- 3. 模擬數據生成 (確保畫面不空白，之後可換成你的爬蟲函式) ---
@st.cache_data
def get_mock_539_data(n_periods):
    # 這裡模擬 539 的歷史開獎 (39顆球選5顆)
    data = []
    for _ in range(n_periods):
        draw = random.sample(range(1, 40), 5)
        data.append(draw)
    df = pd.DataFrame(data)
    # 計算各號碼出現次數
    all_nums = [n for sublist in data for n in sublist]
    counts = pd.Series(all_nums).value_counts().sort_index()
    # 模擬遺漏值 (Delta)
    deltas = {i: random.randint(0, 10) for i in range(1, 40)}
    return counts, deltas

counts, last_occurrence = get_mock_539_data(analysis_period)
top_10_idx = counts.nlargest(10).index

# --- 4. 539 獵人精選邏輯 ---
st.divider()
st.subheader(f"🚀 獵人建議：最強 {play_type} 星組合")

# 分類籃子 (539 分界線設為 20)
top_10_list = list(top_10_idx)
baskets = {
    "奇大": [n for n in top_10_list if n % 2 != 0 and n >= 20],
    "奇小": [n for n in top_10_list if n % 2 != 0 and n < 20],
    "偶大": [n for n in top_10_list if n % 2 == 0 and n >= 20],
    "偶小": [n for n in top_10_list if n % 2 == 0 and n < 20]
}

final_539 = []
used_tails = set()
basket_keys = ["奇大", "奇小", "偶大", "偶小"]

for i in range(play_type):
    key = basket_keys[i % 4]
    basket = baskets.get(key, [])
    pick = next((n for n in basket if n % 10 not in used_tails), None)
    if not pick and basket: pick = basket[0]
    if pick:
        final_539.append(pick)
        used_tails.add(pick % 10)

st.success(f"建議執行組合：**{sorted(final_539)}**")

# --- 5. 排行榜顯示 ---
st.divider()
st.write("### 🔥 目前最強勢號碼 (Top 10)")
cols = st.columns(5)
for i, num in enumerate(top_10_idx[:10]):
    with cols[i % 5]:
        st.metric(f"號碼 {num}", f"{counts[num]} 次", f"隔 {last_occurrence[num]} 期")

st.info("💡 539 每日開獎一次，建議著重於『熱門尾數』分析。")
