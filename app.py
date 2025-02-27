import streamlit as st
import pandas as pd
from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from POM import *
from makePDF import create_pdf

# 제목
st.title("📄 작업지시서 생성기")

# 파일 업로드
uploaded_file = st.file_uploader("📂 발주서(엑셀 파일)을 업로드하세요", type=["xlsx"])

if uploaded_file is not None:
    # 엑셀 데이터 불러오기
    df = pd.read_excel(uploaded_file)

    common_info = get_common_info(df)
    n, product_info = get_product_info(df)

    # 데이터 미리보기
    st.subheader("📊 업로드된 데이터")
    st.table(common_info)
    # st.dataframe(product_info)

    # ✅ DataFrame에 체크박스 컬럼 추가
    cols = list(product_info.columns)
    product_info["선택"] = True
    product_info["타입"] = "기본"
    product_info = product_info[["선택", "타입"]+cols]

    # ✅ 전체 선택 기능을 세션 상태에 저장
    if "selected_rows" not in st.session_state:
        st.session_state.selected_rows = product_info.copy()  # 초기값 설정


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

    # 선택된 데이터 표시
    st.subheader("📄 선택된 품목")
    if not selected_products.empty:
        st.dataframe(selected_products.drop(columns=["선택"], axis=1).reset_index(drop=True))
    else:
        st.text("품목이 선택되지 않았습니다.")


    # 버튼 클릭 시 PDF 생성
    if st.button("📄 작업지시서 PDF 생성"):
        pdf_buffer = create_pdf(common_info, selected_products)
        st.download_button(label="📥 PDF 다운로드", data=pdf_buffer, file_name="작업지시서.pdf", mime="application/pdf")
