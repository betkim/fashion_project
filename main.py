# 필요한 라이브러리
import streamlit as st
from pytrends.request import TrendReq
import pandas as pd
import matplotlib.pyplot as plt

# Google Trends 연결 설정
pytrends = TrendReq(hl='ko', tz=540)

# 연도별 주요 패션 아이템, 트렌드, 브랜드 설정
fashion_trends = {
    2004: {"Item": "Skinny Jeans", "Trend": "Minimalism", "Brand": "Levi's"},
    2005: {"Item": "Boho Chic", "Trend": "Bohemian", "Brand": "Free People"},
    2006: {"Item": "Athleisure", "Trend": "Sporty", "Brand": "Nike"},
    2007: {"Item": "Oversized", "Trend": "Casual", "Brand": "Adidas"},
    2008: {"Item": "Retro Sneakers", "Trend": "Vintage", "Brand": "Vans"},
    2009: {"Item": "Denim Jackets", "Trend": "Classic", "Brand": "Levi's"},
    2010: {"Item": "Minimalism", "Trend": "Simplicity", "Brand": "Uniqlo"},
    2011: {"Item": "Streetwear", "Trend": "Urban", "Brand": "Supreme"},
    2012: {"Item": "Vintage Tees", "Trend": "Retro", "Brand": "Urban Outfitters"},
    2013: {"Item": "Tie-Dye", "Trend": "Boho", "Brand": "Independent Artists"},
    2014: {"Item": "Chunky Sneakers", "Trend": "Athletic", "Brand": "Balenciaga"},
    2015: {"Item": "Y2K Fashion", "Trend": "Throwback", "Brand": "Juicy Couture"},
    2016: {"Item": "Neon Colors", "Trend": "Bold", "Brand": "Louis Vuitton"},
    2017: {"Item": "Grunge Revival", "Trend": "90s Revival", "Brand": "Doc Martens"},
    2018: {"Item": "Baggy Jeans", "Trend": "Loose Fit", "Brand": "Guess"},
    2019: {"Item": "Cottagecore", "Trend": "Nature-Inspired", "Brand": "Zara"},
    2020: {"Item": "Sustainable Fashion", "Trend": "Eco-Friendly", "Brand": "Patagonia"},
    2021: {"Item": "Puff Sleeves", "Trend": "Vintage", "Brand": "H&M"},
    2022: {"Item": "Retro Sunglasses", "Trend": "Retro", "Brand": "Ray-Ban"},
    2023: {"Item": "Eco-Friendly Materials", "Trend": "Sustainable", "Brand": "Everlane"},
    2024: {"Item": "Digital Fashion", "Trend": "Virtual", "Brand": "DressX"}
}

# Streamlit UI 구성
st.title("연도별 패션 트렌드와 주요 브랜드 분석 (2004-2024)")
st.write("각 연도별로 유행했던 패션 아이템, 트렌드, 브랜드의 실제 Google Trends 데이터를 시각화합니다.")

# 연도 선택 슬라이더
selected_year = st.slider("연도 선택", min_value=2004, max_value=2024, step=1, value=2024)

# 선택한 연도의 패션 키워드 가져오기
if selected_year in fashion_trends:
    item = fashion_trends[selected_year]["Item"]
    trend = fashion_trends[selected_year]["Trend"]
    brand = fashion_trends[selected_year]["Brand"]

    st.write(f"### {selected_year}년 패션 정보")
    st.write(f"**아이템:** {item}")
    st.write(f"**패션 트렌드:** {trend}")
    st.write(f"**패션 브랜드:** {brand}")

    # Google Trends 데이터 가져오기
    keywords = [item, trend, brand]
    pytrends.build_payload(keywords, timeframe=f"{selected_year}-01-01 {selected_year}-12-31", geo="KR")
    data = pytrends.interest_over_time()

    # 데이터 시각화
    if not data.empty:
        data = data.drop(columns=['isPartial'])  # 불완전한 데이터 열 제거
        st.write("### 해당 연도 패션 트렌드 검색 인기도")
        
        fig, ax = plt.subplots(figsize=(10, 6))
        for keyword in keywords:
            ax.plot(data.index, data[keyword], label=keyword)
        ax.set_title(f"{selected_year}년 패션 트렌드 인기도")
        ax.set_xlabel("월")
        ax.set_ylabel("인기도")
        ax.legend()
        st.pyplot(fig)
    else:
        st.write("데이터를 가져올 수 없습니다. 다른 연도를 선택해 주세요.")

# 전체 연도별 패션 정보 요약표
st.write("### 전체 연도별 패션 정보 요약")
df = pd.DataFrame(fashion_trends).T
df.index.name = 'Year'
st.dataframe(df)