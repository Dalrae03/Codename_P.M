from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base  #이동시 models/base.py내부

URL_DATABASE = 'mysql+pymysql://root:yejinmysql151303%40@localhost:3306/codename_pm'

# engine 객체를 생성하면 SQLAlchemy가 해당 데이터베이스와 연결을 설정하고 SQL 명령을 실행할 수 있도록 한다.
# 데이터베이스 연결 설정
engine = create_engine(URL_DATABASE)

# 세션 생성
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# ORM 모델 베이스 생성성
Base = declarative_base()  #이동시 models/base.py내부