# taskforce

## l1
- schema: 데이터 모델 (ModelEntry, Opinion, IdeaPool)

## l2
- config: .env 로드, 모델 레지스트리, caller 제외 로직
- panelist: LiteLLM 래퍼, 개별 모델 async 호출
- session_logger: 세션 전문 로그 (~/.taskforce/logs/)
- cost_logger: 비용 요약 로그 (~/.taskforce/cost_logs/)

## l3
- roundtable: 병렬 질의 + summarizer 분류 취합

## l4
- taskforce_facade: 최상위 퍼사드, 초기화/discuss/로그 기록
