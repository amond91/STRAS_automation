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
	# ('FONTNAME', (0, 0), (-1, 0), 'NotoSansKR_bold'),
	('FONTSIZE', (1, 0), (1, 1), 18),
	('FONTNAME', (1, 0), (1, 1), 'NotoSansKR_bold'),
	('SPAN', (2, 0), (3, 2)),
	('ALIGN', (2, 0), (3, 2), 'CENTER'),
	# ('BACKGROUND', (0,0), (-1, 0), colors.lightgrey),
	# ('BACKGROUND', (0,0), (0, -1), colors.lightgrey),
	# ('BACKGROUND', (0,0), (-1, 0), colors.lightgrey),
	('BACKGROUND', (1, 0), (1, -1), colors.white),
	('BACKGROUND', (2, 0), (3, 2), colors.white)
	# ('VALIGN', (2, 0), (3, 2), 'MIDDLE'),
]

prd_style_1 = default_style + [
	('FONTNAME', (0, 0), (0, -1), 'NotoSansKR_bold'),
	('FONTNAME', (1, 0), (1, 1), 'NotoSansKR_bold'),
	('FONTSIZE', (1, 0), (1, 0), 15),
	# ('BACKGROUND', (0,0), (0, -1), colors.lightgrey)
]

prd_style_2 = default_style + [
	('FONTNAME', (0, 0), (0, -1), 'NotoSansKR_bold'),
	('FONTNAME', (1, 0), (2, 1), 'NotoSansKR_bold'),
	('FONTNAME', (1, 4), (1, 4), 'NotoSansKR_bold'),
	('FONTSIZE', (1, 0), (1, 0), 15),
	('TEXTCOLOR', (1, 0), (1, 0), colors.red),
	('TEXTCOLOR', (2, 1), (2, 1), colors.red)
	# ('BACKGROUND', (0,0), (0, -1), colors.lightgrey)
]

table_style_2 = default_style + [
	('FONTNAME', (0, 0), (0, -1), 'NotoSansKR_bold'),
	('FONTNAME', (1, 1), (1, 1), 'NotoSansKR_bold'),
	('TEXTCOLOR', (1, 0), (1, 0), colors.blue),
	('TEXTCOLOR', (1, 1), (1, 1), colors.red),
	('ALIGN', (1, 1), (1, 1), 'RIGHT'),
	('SPAN', (0, 3), (0, 4)),
	('SPAN', (1, 3), (1, 4)),
	('VALIGN', (0, 3), (0, 4), 'TOP'),
	('VALIGN', (1, 3), (1, 4), 'TOP'),
	# ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey)
]

table_style_2_1 = default_style + [
	('FONTNAME', (0, 0), (-1, -1), 'NotoSansKR_bold'),
	('TEXTCOLOR', (1, 0), (1, -1), colors.red),
	('ALIGN', (1, 0), (1, -1), 'CENTER'),
	# ('BACKGROUND', (0,0), (0, -1), colors.lightgrey)
]

table_style_3 = default_style + [
	('FONTNAME', (0, 1), (-1, 1), 'NotoSansKR_bold'),
	# ('BACKGROUND', (0,0), (-1, 0), colors.lightgrey),
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