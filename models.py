from sqlalchemy import Column, Integer, String, Float, Text, ForeignKey
from database import Base

# 따로 models파일에 넣으려면 relationship import해야함 하단에도 relationship 선언 필요요

# 분석용 DB
class AnalyzeList(Base):
    __tablename__ = "analyze_list"

    scenario_name = Column(String(255), ForeignKey("scenario_list.scenario_name", ondelete="CASCADE"), primary_key=True)
    scenario_summary = Column(Text)
    example_answer_A = Column(Text)
    example_answer_B = Column(Text)
    example_answer_C = Column(Text)
    example_answer_D = Column(Text)


# 분석결과 DB
class AnalyzeResult(Base):
    __tablename__ = "analyze_result"

    # String 쓸거면 항상 뒤에 길이를 반드시 명시해야한다.
    scenario_name = Column(String(255), ForeignKey("scenario_list.scenario_name", ondelete="CASCADE"), primary_key=True)
    summary_accuracy = Column(Float)
    answer_result_A = Column(Float)
    answer_result_B = Column(Float)
    answer_result_C = Column(Float)
    answer_result_D = Column(Float)
    total_analysis_results = Column(Text)


# NPC 데이터
class CharacterInfo(Base):
    __tablename__ = "character_info"

    NPC_name = Column(String(100), primary_key=True)
    personality = Column(Text)
    speech = Column(Text)




# 시나리오 리스트
class ScenarioList(Base):  # 시나리오 리스트가 먼저 메인. info가 이것을 참조
    __tablename__ = "scenario_list"

    #autoincrement=True - 새로운 행이 추가될 때마다 자동으로 값이 증가
    primary_key = Column(Integer, primary_key=True, autoincrement=True)
    scenario_name = Column(String(255), unique=True, nullable=False)
    NPC_name1 = Column(String(100), ForeignKey("character_info.NPC_name", ondelete="SET NULL"))
    NPC_name2 = Column(String(100), ForeignKey("character_info.NPC_name", ondelete="SET NULL"))




# 대사 출력
class ScenarioInfo(Base):
    __tablename__ = "scenario_info"
    
    # "CASCADE" - 부모 테이블(참조되는 테이블)의 데이터가 삭제될 때, 자식 테이블(참조하는 테이블)의 관련 데이터도 함께 삭제되도록 설정
    scenario_name = Column(String(255), ForeignKey("scenario_list.scenario_name", ondelete="CASCADE"), primary_key=True)
    script_list = Column(Text)
    script_order_list = Column(Text)  #변경된 컬럼 추가
