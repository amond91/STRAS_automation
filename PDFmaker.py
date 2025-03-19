from reportlab.lib.pagesizes import A4, landscape

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Image, Spacer, PageBreak, Paragraph
from reportlab.lib import colors, styles, units

import os
from io import BytesIO

import pandas as pd

from PDFtablestyle import *
from R2api import read_file_r2


def create_pdf(common_info, selected_products):
    common_info["len"] = len(selected_products)
    buffer = BytesIO()

    # font 설정
    font_path = "font/NotoSansKR-Regular.ttf"
    pdfmetrics.registerFont(TTFont("NotoSansKR", font_path))

    # PDF 문서 설정
    doc = SimpleDocTemplate(buffer, pagesize=landscape(A4),
                            topMargin=15, bottomMargin=15, leftMargin=50, rightMargin=50)
    elements = []

    # 각 PDF 페이지별 설정
    for _, row in selected_products.iterrows():
        elements += create_single_PDF(common_info, dict(row))
        elements.append(PageBreak())

    doc.build(elements)
    buffer.seek(0)
    return buffer


def create_single_PDF(common_info, prd_info):
    title_style = styles.ParagraphStyle(
        name="TitleStyle",
        fontName="NotoSansKR",
        fontSize=13,
        leading=22,  # ✅ 줄 간격 조절
        alignment=0,  # ✅ 가운데 정렬 (0=왼쪽, 1=가운데, 2=오른쪽)
        spaceAfter=0.3 * units.cm  # ✅ 제목 아래 여백 추가
    )

    title_text = f"STRAS 생산 의뢰서 - {prd_info['주문자']} ({prd_info['순번']} / {common_info['len']})"
    title = Paragraph(title_text, title_style)

    # Nan 값 공백으로 대체
    for k in prd_info.keys():
        if pd.isna(prd_info[k]):
            prd_info[k] = ""

    # 로고 업데이트
    if prd_info["타입"] == "Withus":
        image_path = "images/withus_logo.jpg"
        img = Image(image_path, width=125, height=50)
    else:
        image_path = "images/stras_logo.jpg"
        img = Image(image_path, width=167, height=50)

    order_data = [["거래처", f"{prd_info['주문자']}"],
                  ["소비자", f"{prd_info['적요']}"]]
    order_table = Table(order_data, colWidths=[70, 630])
    order_table.setStyle(default_style)

    top_top_table = Table([[order_table]])


    common_data = [
        ["디자인 NO", f"{prd_info['CODE']}", img, "",  "발주", "갑피", "저부", "출고"],
        ["순번", f"{prd_info['순번']}", "", "", f"{common_info['po_no']}", "", "", ""],
        ["전체 수량", f"{common_info['num_of_prd']}", "", "", "", "", "", ""],
        ["작업 수량", f"{prd_info['수량(단위포함)']}", "", "", "", "", "", ""]
    ]

    # ✅ 전체 너비 : 700
    col_widths = [70, 110, 40, 200, 70, 70, 70, 70]

    # ✅ 테이블 생성

    common_table = Table(common_data, colWidths=col_widths)
    common_table.setStyle(table_style_1)

    top_table = Table([[common_table]])

    if prd_info["타입"] == "지퍼 안쪽":
        zipper = "<-- 안쪽 지퍼"
    else:
        zipper = ""
    prd_data1 = [
        ["외피", f"{prd_info['외피']}", ""],
        ["내피", f"{prd_info['내피']}", ""],
        ["실색(자수)", f"{prd_info['실색']}", ""],
        ["장식", f"{prd_info['장식']}", zipper]
    ]

    heel_hights = prd_info["굽높이"].split("cm")[0]

    prd_data2 = [
        ["라스트", f"{prd_info['라스트']}", ""],
        ["굽", f"{prd_info['사용굽']}", f"{heel_hights}"],
        ["중창", f"{prd_info['중창']}", ""],
        ["중창싸개", f"{prd_info['중창싸게']}", ""],
        ["창", f"{prd_info['창']}", ""],
        ["까래", f"{prd_info['까래']}", ""]
    ]

    col_widths = [70, 180, 80]

    prd_table1 = Table(prd_data1, colWidths=col_widths)
    prd_table1.setStyle(default_style)

    prd_table2 = Table(prd_data2, colWidths=col_widths)
    prd_table2.setStyle(default_style)

    prd_image_path = f"images/products/{prd_info['CODE']}.jpg"
    res = read_file_r2(prd_image_path)
    if not res:
        prd_image_path = "images/products/no_product.jpg"

    # 이미지 설정
    scale = 2.7
    if isinstance(res, BytesIO):  # R2에서 받은 이미지가 BytesIO인지 확인
        prd_img = Image(res, width=750 / scale, height=500 / scale)
    else:
        prd_img = Image("images/products/no_product.jpg", width=750/scale, height=500/scale)

    left_table = Table([[prd_table1], [prd_table2]])
    layout = Table([[left_table, prd_img]])
    layout.setStyle(no_padding)

    if prd_info["타입"] == "실외용":
        requirements = "실외용 - 선심 길게"
    else:
        requirements = ""

    bottom_data1 = [
        ["특이사항", f"{prd_info['추가요청사항']}"],
        ["옵션", f"{prd_info['가보시/밑창']}"],
        ["", requirements],
    ]

    bottom_data2 = [
        ["부츠 통", ""],
        ["종아리 둘레", f"{prd_info['종아리둘레']}"],
        ["종아리 높이", f"{prd_info['종아리높이']}"],
        ["추가 기장", f"(+) {prd_info['추가기장']}cm"],
        ["총 기장", f"{prd_info['높이']}cm"],
    ]

    bottom_data3 = [
        ["215", "220", "225", "230", "235", "240", "245", "250", "255", "260", "265", "계"],
        ["", "", "", "", "", "", "", "", "", "", "", "", ],
        ["", "", "", "", "", "", "", "", "", "", "", "", ],
        ["", "", "", "", "", "", "", "", "", "", "", "", ],
        ["", "", "", "", "", "", "", "", "", "", "", "", ],
    ]

    sizes = str(prd_info["규격"]).split(",")
    for size in sizes:
        if "-" not in size:
            size_index = (int(size) - 215) // 5
            bottom_data3[1][size_index] = 1
        else:
            s, n = size.split("-")
            size_index = (int(s) - 215) // 5
            bottom_data3[1][size_index] = n

    bottom_data3[1][-1] = prd_info['수량(단위포함)']

    bottom_table1 = Table(bottom_data1, colWidths=[70, 630])
    bottom_table1.setStyle(default_style)
    bottom_table_upper = Table([[bottom_table1]])

    bottom_table2 = Table(bottom_data2, colWidths=[70, 130])
    bottom_table2.setStyle(default_style)
    bottom_table3 = Table(bottom_data3)
    bottom_table3.setStyle(default_style)

    bottom_table = Table([[bottom_table2, bottom_table3]])


    # ✅ 테이블을 Story에 추가하여 PDF 생성
    elements = [title, top_table, top_top_table, layout, bottom_table_upper, bottom_table]

    return elements


if __name__ == "__main__":
    print("Hello World!")
