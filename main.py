from fastapi import FastAPI, HTTPException, Depends, status
from pydantic import BaseModel
from typing import Annotated
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from typing import Optional

# from api import npc_router

app = FastAPI()
models.Base.metadata.create_all(bind=engine)

# 의존성 주입(Dependency Injection)을 위한 함수
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]


# API 라우터 등록
# npc.router - npc.py에서 정의한 APIRouter 객체를 등록 (등록해야 FastAPI 앱에서 사용 가능)
# prefix="/npc" - 모든 엔드포인트 앞에 /npc를 자동으로 추가
# tags=["NPC"] - FastAPI 자동 문서 (/docs)에서 이 API 그룹의 태그를 설정
# app.include_router(npc.router, prefix="/npc", tags=["NPC"])





# 데이터 검증 스키마
# 캐릭터 정보
class CharacterInfoBase(BaseModel):
    NPC_name: str
    personality: str #SQLAlchemy에서는 text타입이 존재하지만 Pydantic(BaseModel)에서는 text타입이 존재하지 않는다.
    speech: str #따라서 models에서 text라고 썼어도 여기서는 str로 작성해야한다.

# 시나리오
class ScenarioListBase(BaseModel):
    scenario_name: str
    NPC_name1: Optional[str] = None #원 클래스에서 npc가 삭제되면 그자리를 null로 하도록 세팅되어있음을 고려. (모듈 임포트해야함함)
    NPC_name2: Optional[str] = None

# 대사 
class ScenarioInfoBase(BaseModel):
    scenario_name: str
    script_list: str
    script_order_list: str

# 분석용
class AnalyzeListBase(BaseModel):
    scenario_name: str
    scenario_summary: str
    example_answer_A: str
    example_answer_B: str
    example_answer_C: str
    example_answer_D: str

#분석결과
class AnalyzeResultBase(BaseModel):
    scenario_name: str
    summary_accuracy: str
    answer_result_A: str
    answer_result_B: str
    answer_result_C: str
    answer_result_D: str
    total_analysis_results: str










# api
# 헬스체크 API
@app.get("/ping")
async def ping():
    return {"message": "Server is running"}



# 캐릭터
# 캐릭터 정보 생성 api
@app.post("/characterInfo/", status_code=status.HTTP_201_CREATED)
async def create_character(characterInfo:CharacterInfoBase, db: db_dependency):
    db_characterInfo = models.CharacterInfo(**characterInfo.dict())
    db.add(db_characterInfo)
    db.commit()

# 캐릭터 정보 읽기 api
@app.get("/characterInfo/{NPC_name}", status_code=status.HTTP_200_OK)
async def read_character(NPC_name: str, db: db_dependency):
    characterInfo = db.query(models.CharacterInfo).filter(models.User.id == NPC_name).first()
    if characterInfo is None:
        raise HTTPException(status_code=404, detail='Character not found')
    return characterInfo



# 시나리오
# 시나리오 생성 api
@app.post("/ScenarioList/", status_code=status.HTTP_201_CREATED)
async def create_scenario(scenarioList:ScenarioListBase, db: db_dependency):
    db_scenario = models.ScenarioList(**scenarioList.dict())
    db.add(db_scenario)
    db.commit()

# 시나리오 읽기 api
@app.get("/ScenarioList/{scenario_name}", status_code=status.HTTP_200_OK)
async def read_scenario(scenario_name: str, db: db_dependency):
    scenario = db.query(models.ScenarioList).filter(models.ScenarioList.scenario_name == scenario_name).first()
    if scenario is None:
        raise HTTPException(status_code=404, detail='Scenario not found')
    return scenario



# 대사
# 대사 정보 생성 api
@app.post("/ScenarioInfo/", status_code=status.HTTP_201_CREATED)
async def create_scenarioInfo(scenarioInfo:ScenarioInfoBase, db: db_dependency):
    db_scenarioInfo = models.ScenarioInfo(**scenarioInfo.dict())
    db.add(db_scenarioInfo)
    db.commit()

# 대사 정보 읽기 api (시나리오 이름 뿐만 아니라 뭔가를 하나 더받아야할것같아. 순서 번호같은거... 근데 str임 int가 아닌데?)
@app.get("/ScenarioInfo/{scenario_name}", status_code=status.HTTP_200_OK)
async def read_scenarioInfo(scenario_name: str, db: db_dependency):
    scenarioInfo = db.query(models.ScenarioInfo).filter(models.ScenarioInfo.scenario_name == scenario_name).first()
    if scenarioInfo is None:
        raise HTTPException(status_code=404, detail='ScenarioInfo not found')
    return scenarioInfo



# 분석용
# 분석 리스트 정보 생성 api
@app.post("/AnalyzeList/", status_code=status.HTTP_201_CREATED)
async def create_analyzeList(analyzeList:AnalyzeListBase, db: db_dependency):
    db_analyzeList = models.AnalyzeList(**analyzeList.dict())
    db.add(db_analyzeList)
    db.commit()

# 분석 리스트 정보 읽기 api
@app.get("/AnalyzeList/{scenario_name}", status_code=status.HTTP_200_OK)
async def read_analyzeList(scenario_name: str, db: db_dependency):
    analyzeList = db.query(models.AnalyzeList).filter(models.AnalyzeList.scenario_name == scenario_name).first()
    if analyzeList is None:
        raise HTTPException(status_code=404, detail='AnalyzeList not found')
    return analyzeList



# 분석결과
# 분석 결과 정보 생성 api
@app.post("/AnalyzeResult/", status_code=status.HTTP_201_CREATED)
async def create_analyzeResult(analyzeResult:AnalyzeResultBase, db: db_dependency):
    db_analyzeResult = models.AnalyzeResult(**analyzeResult.dict())
    db.add(db_analyzeResult)
    db.commit()

# 분석 결과 정보 읽기 api
@app.get("/AnalyzeResult/{scenario_name}", status_code=status.HTTP_200_OK)
async def read_analyzeResult(scenario_name: str, db: db_dependency):
    analyzeResult = db.query(models.AnalyzeResult).filter(models.AnalyzeResult.scenario_name == scenario_name).first()
    if analyzeResult is None:
        raise HTTPException(status_code=404, detail='AnalyzeResult not found')
    return analyzeResult