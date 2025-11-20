import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

endpoint = "database-1.cbuaymeeggmf.ap-northeast-2.rds.amazonaws.com"
username = "xxx"
password = "xxx"
database = "bxxxx"

QUERIES = [
    ("1. 스키마 확인", "SELECT schema_name FROM information_schema.schemata WHERE schema_name = 'bedrock_integration';"),
    ("2. 테이블 확인 (bedrock_integration)", "SELECT table_name FROM information_schema.tables WHERE table_schema = 'bedrock_integration';"),
    ("3. 테이블 구조 확인 (bedrock_kb)", "SELECT column_name, data_type FROM information_schema.columns WHERE table_schema = 'bedrock_integration' AND table_name = 'bedrock_kb' ORDER BY ordinal_position;"),
    ("4. 현재 데이터 개수 (bedrock_kb)", "SELECT COUNT(*) as count FROM bedrock_integration.bedrock_kb;"),
    ("5. 샘플 데이터 조회 (최대 5개)", "SELECT id, chunks, metadata FROM bedrock_integration.bedrock_kb LIMIT 5;"),
    ("6. pgvector 확장 확인", "SELECT extname, extversion FROM pg_extension WHERE extname = 'vector';"),
    ("7. LangChain 컬렉션 목록 (langchain_pg_collection)", "SELECT * FROM langchain_pg_collection LIMIT 20;"),
    ("8.a LangChain 임베딩 - 컬럼 확인 (langchain_pg_embedding)", "SELECT column_name FROM information_schema.columns WHERE table_name = 'langchain_pg_embedding';"),
    ("8.b LangChain 임베딩 샘플 (langchain_pg_embedding)", "SELECT * FROM langchain_pg_embedding LIMIT 10;")
]


def run_queries():
    try:
        print("데이터 조회를 시작합니다...\n")
        # 데이터베이스 연결
        conn = psycopg2.connect(
            host=endpoint,
            database=database,
            user=username,
            password=password,
            port=5432
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

        cur = conn.cursor()

        print(f"연결된 데이터베이스: {database} @ {endpoint}\n")

        for title, q in QUERIES:
            print("===", title, "===")
            try:
                cur.execute(q)
                rows = cur.fetchall()
                if not rows:
                    print("  (결과 없음)")
                else:
                    # 컬럼 이름 가져오기
                    colnames = [desc[0] for desc in cur.description] if cur.description else []
                    for r in rows:
                        if colnames:
                            # 매핑 형태로 보기 좋게 출력
                            print("  -", {col: val for col, val in zip(colnames, r)})
                        else:
                            print("  -", r)
            except Exception as e:
                print(f"  쿼리 실행 오류: {e}")
            print()

        cur.close()
        conn.close()

    except Exception as e:
        print(f"오류 발생: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    run_queries()
