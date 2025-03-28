import boto3
from botocore.config import Config
import pandas as pd
from io import BytesIO
import uuid

# R2 설정 정보
R2_ENDPOINT = "https://f2012c5f8226838c9fe9fdd86f17f507.r2.cloudflarestorage.com"
R2_PUBLIC = "https://pub-5bde5532f6fe42c297e5a55d43233d8e.r2.dev"
ACCESS_KEY = "9ad278bc54a792f610c990f3f1fb4fbe"
SECRET_KEY = "6ca3479b0eb8d7482dd4184f5d6cfe0fff903ee6885d282cf44da18d68200a44"
BUCKET_NAME = "stras-automation-data"  # 버킷 이름 입력

# S3 클라이언트 생성 (Cloudflare R2는 S3 API 호환)
session = boto3.session.Session()
s3_client = session.client(
    service_name="s3",
    endpoint_url=R2_ENDPOINT,
    aws_access_key_id=ACCESS_KEY,
    aws_secret_access_key=SECRET_KEY,
    config=Config(signature_version="s3v4")  # Cloudflare R2는 Signature v4 사용
)
# 파일을 메모리로 불러와서 DataFrame으로 변환

def read_file_r2(file_path):
    try:
        response = s3_client.get_object(Bucket=BUCKET_NAME, Key=file_path)
        file_content = response['Body'].read()
        return BytesIO(file_content)
    except Exception as e:
        print(f"❌ 파일 불러오기 실패: {e}")
        return None

def upload_to_r2(buffer, file_path):
    # 환경 변수 또는 설정값 (Cloudflare R2 정보)

    s3_client.put_object(Bucket=BUCKET_NAME, Key=file_path, Body=buffer.getvalue(), ContentType='application/pdf')

    public_url = f"{R2_PUBLIC}/{file_path}"
    return public_url


# 데이터 로드
if __name__ == "__main__":
	res = read_file_r2("data/라스트_굽_중창.xlsx")
	index_df = pd.read_excel(res)

	if index_df is not None:
		print("✅ R2에서 파일 로드 성공!")
		print(index_df.head())  # 데이터 확인