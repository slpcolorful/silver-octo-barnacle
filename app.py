import streamlit as st
from google import genai
client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])
                      
# 페이지 설정
st.set_page_config(page_title="언어 검사 분석기", page_icon="📝", layout="centered")

st.title("🗣️ SELSI & PRES 언어 검사 분석기")
st.write("아동의 언어 검사 정보를 입력하면 제미나이가 전문적인 분석 리포트를 작성해 드립니다.")

# 메인 입력 폼
with st.form("language_test_form"):
    test_type = st.selectbox("검사 도구 선택", ["SELSI (영유아 언어발달검사)", "PRES (취학 전 아동 수용·표현언어 발달척도)"])
    child_age = st.text_input("아동 생활 연령", placeholder="예: 4세 2개월 또는 50개월")
    test_result_text = st.text_area(
        "검사 결과 및 특이사항 입력", 
        placeholder="예시:\n- 수용언어 연령: 3세 6개월 (백분위 20%)\n- 표현언어 연령: 2세 9개월 (백분위 5% 미만)\n- 특이사항: 지시행동은 잘 따르나 문장 표현 시 조사가 누락됨"
    )

    submitted = st.form_submit_button("분석 리포트 생성하기")

# 제출 시 실행되는 로직
if submitted:
    if not child_age or not test_result_text:
        st.warning("생활 연령과 검사 결과를 모두 입력해주세요.")
    else:
        with st.spinner("제미나이가 전문 분석 리포트를 작성 중입니다... 잠시만 기다려주세요!"):
            try:
                # 스트림릿 시크릿 금고에서 API 키 불러오기
                api_key = st.secrets["GEMINI_API_KEY"]

                # 제미나이 클라이언트 초기화
                client = genai.Client(api_key=api_key)

                prompt = f"""
                당신은 전문 언어재활사(Speech-Language Pathologist)입니다. 
                다음 {test_type} 검사 결과를 바탕으로 전문적이면서도 보호자(부모님)가 이해하기 쉬운 종합 언어평가 리포트를 마크다운 형식으로 작성해주세요.

                [아동 기본 정보]
                - 검사 도구: {test_type}
                - 생활 연령: {child_age}

                [검사 결과 데이터]
                {test_result_text}

                [작성 양식]
                1. **종합 발달 요약**: 생활 연령 대비 전반적인 언어 발달 수준 평가
                2. **영역별 세부 분석**: 수용언어 및 표현언어 영역 점수 해석
                3. **수용 vs 표현 격차 분석**: 두 영역 간의 차이가 시사하는 바
                4. **가정 내 추천 중재 방향**: 부모가 일상에서 도울 수 있는 구체적인 팁 3가지
                """

                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=prompt,
                )

                st.success("분석이 완료되었습니다!")
                st.markdown("---")
                st.markdown(response.text)

            except Exception as e:
                st.error(f"오류가 발생했습니다: {e}")
