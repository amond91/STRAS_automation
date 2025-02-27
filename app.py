import streamlit as st
import pandas as pd
from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from POM import *

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
    st.dataframe(product_info)

    # PDF 생성 함수
    def create_pdf(dataframe):
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4)
        elements = []

        # 테이블 데이터 준비
        data = [["번호", "품목코드", "품목명", "수량", "규격(사이즈)", "굽높이", "발볼", "추가요청사항"]]  # 헤더 추가
        for _, row in dataframe.iterrows():
            data.append([row["번호"], row["품목코드"], row["품목명"], row["수량"], row["규격(사이즈)"], row["굽높이"], row["발볼"], row["추가요청사항"]])

        # 테이블 스타일 적용
        table = Table(data, colWidths=[30, 80, 150, 50, 60, 60, 60, 80])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))

        # PDF 문서에 테이블 추가
        elements.append(table)
        doc.build(elements)
        buffer.seek(0)
        return buffer

    # 버튼 클릭 시 PDF 생성
    if st.button("📄 작업지시서 PDF 생성"):
        pdf_buffer = create_pdf(df_work_order)
        st.download_button(label="📥 PDF 다운로드", data=pdf_buffer, file_name="작업지시서.pdf", mime="application/pdf")
