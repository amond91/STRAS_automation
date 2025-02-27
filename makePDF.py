from reportlab.lib.pagesizes import A4, landscape
from reportlab.pdfgen import canvas

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Image, Spacer, PageBreak
from reportlab.lib import colors

import os
from io import BytesIO

from reportlab.lib.utils import ImageReader
import pandas as pd


def create_pdf(common_info, selected_products):
    buffer = BytesIO()

    # font 설정
    font_path = "font/NotoSansKR-Regular.ttf"
    pdfmetrics.registerFont(TTFont("NotoSansKR", font_path))

    doc = SimpleDocTemplate(buffer, pagesize=landscape(A4), topMargin=0, bottomMargin=0)
    elements = []

    for _, row in selected_products.iterrows():
        elements += create_single_PDF(common_info, dict(row))
        elements.append(PageBreak())

    doc.build(elements)
    buffer.seek(0)
    return buffer


def create_single_PDF(common_info, prd_info):
    width, height = landscape(A4)

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

    common_data = [
        ["거래처", f"{prd_info['주문자']}", f"{len(prd_info)}", "STRAS 생산 의뢰서", "발주", "갑피", "저부", "출고"],
        ["소비자", f"{prd_info['적요']}", img, "", f"{common_info['po_no']}", "", "", ""],
        ["디자인 NO", f"{prd_info['CODE']}", "", "", "", "", "", ""],
        ["", f"{prd_info['순번']}", "", "", "", "", "", ""]
    ]

    # ✅ 테이블 스타일 설정
    style1 = TableStyle([
        ('SPAN', (2, 1), (3, 3)),
        ('ALIGN', (2, 1), (3, 3), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, -1), 'NotoSansKR'),  # 폰트 설정
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),  # 테두리 설정
    ])

    # ✅ A4 가로 너비를 8개의 열로 균등 분배 (여백 50 유지)
    table_width = width - 50  # 좌우 여백 50씩 제외
    colWidths = [93, 93, 40, 240, 60, 60, 60, 60]

    # ✅ 테이블 생성
    common_table = Table(common_data, colWidths=colWidths)
    common_table.setStyle(style1)

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

    style2 = TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'NotoSansKR'),  # 폰트 설정
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),  # 테두리 설정
    ])

    table_width = (width)/2  # 좌우 여백 50씩 제외
    col_width = table_width / 4  # 각 열의 너비 계산
    colWidths = [col_width/2, col_width, col_width]

    prd_table1 = Table(prd_data1, colWidths=colWidths)
    prd_table1.setStyle(style2)

    prd_table2 = Table(prd_data2, colWidths=colWidths)
    prd_table2.setStyle(style2)


    prd_image_path = f"images/products/{prd_info['CODE']}.jpg"
    if not os.path.exists((prd_image_path)):
        prd_image_path = "images/products/no_product.jpg"

    prd_img = Image(prd_image_path, width=750/3, height=500/3)

    left_table = Table([[prd_table1], [prd_table2]])
    layout = Table([[left_table, prd_img]])

    if prd_info["타입"] == "실외용":
        requirements = "실외용 - 선심 길게"
    else:
        requirements = ""

    bottom_data1 = [
        ["특이사항", f"{prd_info['추가요청사항']}"],
        ["", requirements],
        ["", f"{prd_info['규격']}({prd_info['수량(단위포함)']})"]
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
    size_index = (int(prd_info['규격'])-215)//5
    bottom_data3[1][size_index] = 1

    style3 = TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'NotoSansKR'),  # 폰트 설정
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),  # 테두리 설정
    ])

    bottom_table1 = Table(bottom_data1)
    bottom_table1.setStyle((style3))
    bottom_table2 = Table(bottom_data2)
    bottom_table2.setStyle((style3))
    bottom_table3 = Table(bottom_data3)
    bottom_table3.setStyle((style3))

    bottom_table = Table([[bottom_table1], [bottom_table2, bottom_table3]])

    # ✅ 테이블을 Story에 추가하여 PDF 생성
    elements = [common_table, layout, bottom_table]


    # table_x = width - table_width  # 우측 정렬 (여백 고려)
    # table_y = height  # 상단에서 50만큼 내려서 배치
    # doc.build(elements,
    #           onFirstPage=lambda c, _: table.wrapOn(c, width, height) or table.drawOn(c, table_x, table_y))

    return elements


if __name__ == "__main__":
    print("Hello World!")
