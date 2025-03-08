from reportlab.lib import colors
from reportlab.platypus import TableStyle

default_style = [
	('FONTNAME', (0, 0), (-1, -1), 'NotoSansKR'),  # 폰트 설정
	('GRID', (0, 0), (-1, -1), 0.5, colors.black),  # 테두리 추가
]

table_style_1 = [
	('SPAN', (2, 0), (3, 0)),
	('SPAN', (2, 0), (3, 3)),
	('ALIGN', (2, 0), (3, 3), 'CENTER'),
	('VALIGN', (2, 0), (3, 3), 'MIDDLE'),
] + default_style

no_padding = [
	('LEFTPADDING', (0, 0), (-1, -1), 0),
	('RIGHTPADDING', (0, 0), (-1, -1), 0),
	('TOPPADDING', (0, 0), (-1, -1), 0),
	('BOTTOMPADDING', (0, 0), (-1, -1), 0),
	('ALIGN', (1, 0), (1, 0), 'CENTER'),
	('VALIGN', (1, 0), (1, 0), 'MIDDLE')
]