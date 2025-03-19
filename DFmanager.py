import pandas as pd
from R2api import read_file_r2

def get_common_info(n, df):
	po_no = list(df.iloc[0])[0].split(":")[1].strip()
	customer = list(df.iloc[1])[0].split(":")[1].strip()
	warehouse = list(df.iloc[2])[0].split(":")[1].strip()

	result = {
		"po_no":po_no,
		"customer":customer,
		"warehouse":warehouse,
		"num_of_prd": n
	}

	return result

def get_product_info(df):
	# 데이터 정리 (컬럼명 추출 및 필요 없는 행 제거)
	df_cleaned = df.iloc[4:].reset_index(drop=True)
	df_cleaned.columns = df_cleaned.iloc[0]  # 첫 번째 행을 컬럼명으로 지정
	df_product = df_cleaned[1:-2].reset_index(drop=True)

	num = list(df_cleaned.iloc[-2])[5]
	df_product = manage_product_info(df_product)
	df_product = update_last(df_product)

	return num, df_product


def manage_product_info(df):
	expanded_data = []
	df["CAT"] = df["품목명"].map(lambda x: x.split("/")[0].strip())
	df["CODE"] = df["품목명"].map(lambda x: x.split("/")[1].strip())
	# for id, row in df.iterrows():
	# 	duplicated_row = row.copy()
	# 	duplicated_row["순번"] = id + 1
	# 	sizes = str(row["규격"]).split(",")
	# 	size_list = []
	# 	for size in sizes:
	# 		if "-" not in size:
	# 			size_list.append((size, 1))
	# 		else:
	# 			siz, num = size.split("-")
	# 			size_list.append((siz, num))
	#
	# 	print(size_list)
	# 	duplicated_row["SIZE"] = str(size_list)
	# 	expanded_data.append(duplicated_row)
	#
	# result = pd.DataFrame(expanded_data)
	df["순번"] = range(1, len(df) + 1)

	return df


def update_last(df):
	index_df = pd.read_excel(read_file_r2("data/라스트_굽_중창.xlsx"))
	index_df = index_df.set_index(index_df["인덱스"])

	new_data = []

	for _, row in df.iterrows():
		prd_index = f"{row['품목그룹1명']}@{row['발볼']}@{row['굽높이']}"
		row["라스트"] = index_df.loc[prd_index]["라스트"]
		row["사용굽"] = index_df.loc[prd_index]["사용굽"]
		row["중창"] = index_df.loc[prd_index]["중창"]
		new_data.append(row)

	return pd.DataFrame(new_data)


if __name__ == "__main__":
	df = pd.read_excel("test_data/Ecount.xlsx")
	print(get_common_info(df))
	n, df = get_product_info(df)
	df = manage_product_info(df)

	df.to_csv("test.csv")


