import os

import streamlit as st

from DFmanager import *
from PDFmaker import create_pdf

# 제목
st.title("📄 STRAS 작업지시서 생성기")

# ✅ 세션 상태를 사용하여 파일 저장
if "uploaded_file" not in st.session_state:
    st.session_state.uploaded_file = None  # 업로드된 파일
    st.session_state.df = None  # 데이터프레임 저장

# 파일 업로드
uploaded_file = st.file_uploader("📂 발주서(엑셀 파일)을 업로드하세요", type=["xlsx"])

if uploaded_file is not None:
    if uploaded_file != st.session_state.uploaded_file:
        st.session_state.uploaded_file = uploaded_file
        st.session_state.df = pd.read_excel(uploaded_file)  # 새로운 데이터 로드
        st.session_state.selected_rows = None  # 기존 선택 데이터 초기화
        st.rerun()  # 페이지 새로고침

df = st.session_state.df

if df is not None:
    n, product_info = get_product_info(df)
    common_info = get_common_info(n, df)

    # 데이터 미리보기
    st.subheader("📊 업로드된 데이터")
    st.text("✔️ 공통 정보")
    st.table(common_info)
    # st.dataframe(product_info)

    # ✅ DataFrame에 체크박스 컬럼 추가
    cols = list(product_info.columns)
    product_info["선택"] = True
    product_info["타입"] = "기본"
    product_info = product_info[["선택", "타입"]+cols]

    st.text("📦 제품 목록")
    # ✅ 전체 선택 기능을 세션 상태에 저장
    if "selected_rows" not in st.session_state or st.session_state.selected_rows is None:
        st.session_state.selected_rows = product_info.copy()


    # ✅ 전체 선택 버튼 기능
    def toggle_all():
        is_selected = not all(st.session_state.selected_rows["선택"])
        st.session_state.selected_rows["선택"] = is_selected  # 전체 선택/해제
        st.rerun()  # 페이지 리프레시


    # 🔘 전체 선택/해제 버튼
    st.button("🔘 전체 선택/해제", on_click=toggle_all)

    # ✅ 사용자 입력 가능한 테이블 생성 (체크박스 포함)
    edited_df = st.data_editor(
        st.session_state.selected_rows,  # 세션 상태의 DataFrame 사용
        column_config={"선택": st.column_config.CheckboxColumn("선택"),
                       "타입": st.column_config.SelectboxColumn("타입", options=["기본", "지퍼 안쪽", "실외용", "Withus"]),
                       },

        use_container_width=True,
        hide_index=True  # ✅ 행번호(인덱스) 숨기기
    )

    # ✅ 체크된 행만 필터링
    selected_products = edited_df[edited_df["선택"] == True]
    selected_products["순번"] = range(1, len(selected_products)+1)

    # 선택된 데이터 표시
    st.subheader("📄 출력 예정 품목")
    if not selected_products.empty:
        st.dataframe(selected_products.drop(columns=["선택"], axis=1).reset_index(drop=True))
    else:
        st.text("품목이 선택되지 않았습니다.")

        # PDF 저장 경로 설정
        pdf_path = "static/작업지시서.pdf"

        # PDF 생성 및 저장
        if st.button("📄 작업지시서 PDF 생성"):
            pdf_buffer = create_pdf(common_info, selected_products)

            # static 디렉토리 생성 (없을 경우)
            os.makedirs("static", exist_ok=True)

            # PDF 파일 저장
            with open(pdf_path, "wb") as f:
                f.write(pdf_buffer.getvalue())

            # JavaScript를 실행하여 새 창에서 PDF 열기
            pdf_url = f"http://localhost:8501/{pdf_path}"  # Streamlit 기본 포트 (8501)
            js_code = f"""
            <script>
                window.open("{pdf_url}", "_blank");
            </script>
            """
            st.components.v1.html(js_code, height=0)  # 실행