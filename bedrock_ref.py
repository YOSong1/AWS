# import boto3


# bedrock = boto3.client("bedrock-runtime", verify=False)

# def ask_bedrock(prompt: str) -> str:

#     response = bedrock.converse(
#         modelId="aanthropic.claude-3-haiku-20240307-v1:0", 
#         messages=[
#             {
#                 "role": "user",
#                 "content": [{"text": prompt}],
#             }
#         ],
#         inferenceConfig={
#             "maxTokens": 100,        
#         },
#     )

#     # 출력 텍스트 추출
#     output_message = response["output"]["message"]
#     text = output_message["content"][0]["text"]
#     return text


# if __name__ == "__main__":
#     user_prompt = "VS Code에서 Bedrock를 설명해주세요."
#     answer = ask_bedrock(user_prompt)
#     print("Bedrock 응답:", answer)




import boto3
import json
from dotenv import load_dotenv
import os
from botocore.config import Config
import warnings
from urllib3.exceptions import InsecureRequestWarning

# SSL 경고 무시
warnings.filterwarnings('ignore', category=InsecureRequestWarning)

load_dotenv()  # .env 읽기 (.env가 없어도 무시됨)

# 1) 모델/리전 설정
MODEL_ID = os.getenv("BEDROCK_CHAT_MODEL_ID", "amazon.titan-text-express-v1")
REGION = os.getenv("AWS_DEFAULT_REGION") or os.getenv("AWS_REGION", "us-east-1")

# 2) 프록시 무시 설정
config = Config(
    proxies={},  # 프록시 사용 안 함
    proxies_config={'proxy_use_forwarding_for_https': False}
)

# 3) Bedrock Runtime 클라이언트 생성
bedrock = boto3.client("bedrock-runtime", verify=False, region_name=REGION, config=config)



response = bedrock.invoke_model(
    modelId="anthropic.claude-3-haiku-20240307-v1:0",
    body=json.dumps({
        "anthropic_version": "bedrock-2023-05-31",
        "messages": [
            {"role": "user", "content": "안녕, 자기소개해줘"}
        ],
        "max_tokens": 256,
    }),
    contentType="application/json",
    accept="application/json",
)

# 응답 파싱 및 출력
result = json.loads(response["body"].read().decode("utf-8"))
print("\n=== Claude 응답 ===")
if "content" in result and len(result["content"]) > 0:
    print(result["content"][0]["text"])
else:
    print(json.dumps(result, indent=2, ensure_ascii=False))
