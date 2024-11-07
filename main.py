# 필요한 라이브러리
import streamlit as st
from pytrends.request import TrendReq
import pandas as pd
import matplotlib.pyplot as plt

# 한글 폰트 설정
plt.rc('font', family='Malgun Gothic')  # Windows 사용자는 'Malgun Gothic'으로 설정
# plt.rc('font', family='AppleGothic')  # macOS 사용자는 'AppleGothic'으로 설정
plt.rcParams['axes.unicode_minus'] = False  # 마이너스 기호 깨짐 방지

# Google Trends 연결 설정
pytrends = TrendReq(hl='ko', tz=540)

# 연도별 주요 패션 아이템, 트렌드, 브랜드, 철학 설정
fashion_trends = {
    2004: {"Item": "Skinny Jeans", "Trend": "Minimalism", "Brand": "Levi's", "Philosophy": "개인의 스타일을 중시하는 자기 표현의 자유"},
    2005: {"Item": "Boho Chic", "Trend": "Bohemian", "Brand": "Free People", "Philosophy": "자연과 조화를 이루는 자유로운 삶의 방식"},
    2006: {"Item": "Athleisure", "Trend": "Sporty", "Brand": "Nike", "Philosophy": "건강과 자기 관리를 중요시하는 라이프스타일"},
    2007: {"Item": "Oversized", "Trend": "Casual", "Brand": "Adidas", "Philosophy": "편안함과 실용성을 중시하는 가치관"},
    2008: {"Item": "Retro Sneakers", "Trend": "Vintage", "Brand": "Vans", "Philosophy": "과거의 아름다움과 추억을 존중하는 레트로 문화"},
    2009: {"Item": "Denim Jackets", "Trend": "Classic", "Brand": "Levi's", "Philosophy": "시간을 초월하는 스타일과 품질에 대한 가치"},
    2010: {"Item": "Minimalism", "Trend": "Simplicity", "Brand": "Uniqlo", "Philosophy": "필요 없는 것은 버리고 본질에 집중하는 삶"},
    2011: {"Item": "Streetwear", "Trend": "Urban", "Brand": "Supreme", "Philosophy": "도시 문화와 스트리트 감성을 중시하는 개성 표현"},
    2012: {"Item": "Vintage Tees", "Trend": "Retro", "Brand": "Urban Outfitters", "Philosophy": "옛 것에 대한 존중과 재활용을 중시"},
    2013: {"Item": "Tie-Dye", "Trend": "Boho", "Brand": "Independent Artists", "Philosophy": "자유롭고 개성 있는 표현을 중요시"},
    2014: {"Item": "Chunky Sneakers", "Trend": "Athletic", "Brand": "Balenciaga", "Philosophy": "스타일과 편안함을 동시에 추구"},
    2015: {"Item": "Y2K Fashion", "Trend": "Throwback", "Brand": "Juicy Couture", "Philosophy": "2000년대 초반의 무드와 낙관주의"},
    2016: {"Item": "Neon Colors", "Trend": "Bold", "Brand": "Louis Vuitton", "Philosophy": "대담하고 눈에 띄는 자기 표현"},
    2017: {"Item": "Grunge Revival", "Trend": "90s Revival", "Brand": "Doc Martens", "Philosophy": "기성 가치에 대한 저항과 자아 탐색"},
    2018: {"Item": "Baggy Jeans", "Trend": "Loose Fit", "Brand": "Guess", "Philosophy": "편안함과 자유로운 라이프스타일"},
    2019: {"Item": "Cottagecore", "Trend": "Nature-Inspired", "Brand": "Zara", "Philosophy": "자연과 조화를 이루는 삶과 환경 보호"},
    2020: {"Item": "Sustainable Fashion", "Trend": "Eco-Friendly", "Brand": "Patagonia", "Philosophy": "지속 가능성과 환경 보호에 대한 책임 의식"},
    2021: {"Item": "Puff Sleeves", "Trend": "Vintage", "Brand": "H&M", "Philosophy": "전통적인 아름다움에 대한 향수"},
    2022: {"Item": "Retro Sunglasses", "Trend": "Retro", "Brand": "Ray-Ban", "Philosophy": "과거의 스타일을 현대에 재해석"},
    2023: {"Item": "Eco-Friendly Materials", "Trend": "Sustainable", "Brand": "Everlane", "Philosophy": "환경에 미치는 영향을 최소화하는 의식적인 선택"},
    2024: {"Item": "Digital Fashion", "Trend": "Virtual", "Brand": "DressX", "Philosophy": "가상 세계와 디지털 정체성을 중시하는 시대"}
}

# Streamlit UI 구성
st.title("연도별 패션 트렌드와 주요 브랜드, 철학 분석 (2004-2024)")
st.write("각 연도별로 유행했던 패션 아이템, 트렌드, 브랜드 및 철학을 Google Trends 데이터를 통해 분석합니다.")

# 연도 선택 슬라이더
selected_year = st.slider("연도 선택", min_value=2004, max_value=2024, step=1, value=2024)

# 선택한 연도의 패션 키워드 및 철학 가져오기
if selected_year in fashion_trends:
    item = fashion_trends[selected_year]["Item"]
    trend = fashion_trends[selected_year]["Trend"]
    brand = fashion_trends[selected_year]["Brand"]
    philosophy = fashion_trends[selected_year]["Philosophy"]

    st.write(f"### {selected_year}년 패션 정보")
    st.write(f"**아이템:** {item}")
    st.write(f"**패션 트렌드:** {trend}")
    st.write(f"**패션 브랜드:** {brand}")
    st.write(f"**철학:** {philosophy}")

    # Google Trends 데이터 가져오기
    keywords = [item, trend, brand]
    pytrends.build_payload(keywords, timeframe=f"{selected_year}-01-01 {selected_year}-12-31", geo="KR")
    data = pytrends.interest_over_time()

    # 데이터 시각화
    if not data.empty and all(keyword in data.columns for keyword in keywords):
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
        st.write("데이터를 가져올 수 없습니다. 해당 연도에 대한 트렌드 데이터가 부족합니다.")
else:
    st.write("선택한 연도의 데이터를 찾을 수 없습니다.")

# 전체 연도별 패션 정보 요약표
st.write("### 전체 연도별 패션 정보 및 철학 요약")
df = pd.DataFrame(fashion_trends).T
df.index.name = 'Year'
st.dataframe(df)
