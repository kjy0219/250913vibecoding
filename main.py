import streamlit as st
import pandas as pd
import altair as alt
import os

# 1. 스트림릿 페이지 설정
st.set_page_config(
    page_title="국가별 MBTI 유형 분포 분석",
    layout="wide"
)

st.title("🌏 국가별 MBTI 유형 분석")
st.write("사용자가 업로드한 CSV 파일을 바탕으로 각 MBTI 유형별 비율이 가장 높은 국가 TOP 10을 시각화합니다.")

# 2. 데이터 불러오기 (로컬 파일 우선, 없을 경우 업로더 사용)
DEFAULT_FILE_PATH = "countriesMBTI_16types.csv"
df = None

@st.cache_data
def load_data(file):
    return pd.read_csv(file)

# 로컬 파일이 있는지 확인하고 불러오기
if os.path.exists(DEFAULT_FILE_PATH):
    try:
        df = load_data(DEFAULT_FILE_PATH)
        st.success(f"로컬 파일 '{DEFAULT_FILE_PATH}'을(를) 성공적으로 불러왔습니다.")
    except Exception as e:
        st.error(f"로컬 파일을 읽는 중 오류가 발생했습니다: {e}")
        
# 로컬 파일을 불러오지 못했거나 없는 경우, 파일 업로더 사용
if df is None:
    uploaded_file = st.file_uploader("CSV 파일을 업로드해주세요", type=['csv'])
    if uploaded_file is not None:
        try:
            df = load_data(uploaded_file)
            st.success("파일 업로드 완료!")
        except Exception as e:
            st.error(f"업로드한 파일을 읽는 중 오류가 발생했습니다: {e}")

# 3. 데이터가 성공적으로 로드된 경우에만 분석 및 시각화 진행
if df is not None:
    # 3. MBTI 유형 선택 및 TOP 10 데이터 생성
    mbti_types = df.columns.tolist()[1:]
    
    selected_mbti = st.selectbox(
        '**어떤 MBTI 유형의 TOP 10 국가를 보시겠어요?**',
        mbti_types
    )
    
    if selected_mbti:
        # 선택된 MBTI 유형의 비율이 가장 높은 TOP 10 국가 정렬
        top_10_countries = df.sort_values(by=selected_mbti, ascending=False).head(10)
        
        # 4. Altair를 활용한 인터랙티브 막대 그래프 그리기
        st.subheader(f"✨ **{selected_mbti}** 유형 비율 TOP 10 국가")
        
        # 100% 비율로 변환
        top_10_countries['Percentage'] = top_10_countries[selected_mbti] * 100
        
        chart = alt.Chart(top_10_countries).mark_bar().encode(
            x=alt.X('Country:N', sort='-y', title="국가"),
            y=alt.Y('Percentage:Q', title="비율 (%)"),
            tooltip=['Country', alt.Tooltip('Percentage', format='.2f')]
        ).properties(
            title=f'{selected_mbti} 유형 비율이 가장 높은 국가'
        ).interactive() # 인터랙티브 기능 추가
        
        st.altair_chart(chart, use_container_width=True)
        
        # 5. 데이터 테이블 표시 (선택 사항)
        st.subheader("데이터 미리보기")
        st.dataframe(top_10_countries[['Country', selected_mbti]])
