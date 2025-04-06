from reportlab.lib import colors
from reportlab.platypus import TableStyle

default_style = [
	('FONTNAME', (0, 0), (-1, -1), 'NotoSansKR'),  # 폰트 설정
	('FONTSIZE', (0, 0), (-1, -1), 13),  # 폰트 사이즈
	('GRID', (0, 0), (-1, -1), 0.5, colors.black),  # 테두리 추가
	('VALIGN', (0, 0), (-1, -1), 'MIDDLE')
]

title_style = [
	('FONTNAME', (0, 0), (-1, -1), 'NotoSansKR_black'),  # 폰트 설정
	('ALIGN', (1, 0), (1, 0), 'RIGHT'),
	('FONTSIZE', (0, 0), (-1, -1), 16),  # 폰트 사이즈
]

table_style_1 = default_style + [
	('SPAN', (0, 0), (0, 1)),
	('SPAN', (1, 0), (1, 1)),
	('FONTSIZE', (1, 0), (1, 1), 18),
	('FONTNAME', (1, 0), (1, 1), 'NotoSansKR_bold'),
	('SPAN', (2, 0), (3, 2)),
	('ALIGN', (2, 0), (3, 2), 'CENTER'),
	('BACKGROUND', (1, 0), (1, -1), colors.white),
	('BACKGROUND', (2, 0), (3, 2), colors.white)

]

prd_style_1 = default_style + [
	('FONTNAME', (1, 0), (1, -1), 'NotoSansKR_bold'),
	('TEXTCOLOR', (1, 2), (1, 2), colors.green),
]

prd_style_2 = default_style + [
	('FONTNAME', (1, 0), (2, 1), 'NotoSansKR_bold'),
	('FONTNAME', (1, 4), (1, 4), 'NotoSansKR_bold'),
	('FONTSIZE', (1, 0), (1, 0), 15),
	('TEXTCOLOR', (1, 0), (1, 0), colors.red),
	('TEXTCOLOR', (2, 1), (2, 1), colors.red)
]

table_style_2 = default_style + [
	('SPAN', (1, 1), (3, 1)),
	('SPAN', (0, 2), (0, 3)),
	('SPAN', (1, 2), (3, 3)),
	('FONTNAME', (3, 0), (3, 0), 'NotoSansKR_bold'),
	('TEXTCOLOR', (1, 0), (1, 0), colors.blue),
	('TEXTCOLOR', (3, 0), (3, 0), colors.red),
	('ALIGN', (3, 0), (3, 0), 'RIGHT'),
	('VALIGN', (0, 2), (0, 3), 'TOP'),
	('VALIGN', (1, 2), (3, 3), 'TOP'),
]

table_style_2_1 = default_style + [
	('TEXTCOLOR', (1, 0), (1, -1), colors.red),
	('ALIGN', (1, 0), (1, -1), 'CENTER'),
]

table_style_3 = default_style + [
	('FONTNAME', (0, 1), (-1, 1), 'NotoSansKR_bold'),
	('ALIGN', (0, 0), (-1, -1), 'CENTER'),
]

no_padding = [
	('LEFTPADDING', (0, 0), (-1, -1), 0),
	('RIGHTPADDING', (0, 0), (-1, -1), 0),
	('TOPPADDING', (0, 0), (-1, -1), 0),
	('BOTTOMPADDING', (0, 0), (-1, -1), 0),
	('ALIGN', (1, 0), (1, 0), 'CENTER'),
	('VALIGN', (1, 0), (1, 0), 'MIDDLE')
]