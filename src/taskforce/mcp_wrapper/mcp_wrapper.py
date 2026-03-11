import os

from mcp.server.fastmcp import FastMCP

from ..l4.taskforce_facade import Taskforce

mcp = FastMCP("taskforce")

_tf = None


def _get_taskforce() -> Taskforce:
    global _tf
    if _tf is None:
        caller = os.getenv("TASKFORCE_CALLER_PROVIDER", "anthropic")
        _tf = Taskforce(caller_provider=caller)
    return _tf


@mcp.tool()
async def roundtable_discuss(agenda: str, context: str = "") -> str:
    """Roundtable: 다수의 최고 성능 LLM(GPT, Grok, Claude, Gemini)에
    동일 의제를 독립적으로 질의하고, 수집된 의견을 common/divergent/unique로
    분류하여 구조화된 JSON을 반환한다.

    유료 API를 호출하는 도구이다. 사용 전 반드시 사용자에게 의견을 묻고,
    사용자가 동의한 경우에만 호출하라.

    서로 다른 방식으로 발달한 모델들의 관점 다양성을 활용하여
    robust한 아이디어 풀을 구축하는 것이 목적이다.
    일회성 외부 의견 수집 도구이므로, 양질의 결과를 위해
    agenda와 context를 최대한 풍부하게 제공해야 한다.

    [agenda 작성 가이드]
    - 분석/검토/비교를 요청하는 명확한 질문 형태로 작성
    - 검토 범위와 판단 기준을 명시
    - 모호한 표현 대신 구체적인 용어 사용

    [context 작성 가이드 - 풍부할수록 좋다]
    input 토큰은 저렴하므로 관련 정보를 아끼지 말고 최대한 제공하라.
    패널이 충분한 맥락 없이 일반론만 답하면 가치가 없다.
    구체적 사양, 수치, 제약 조건, 배경 지식, 도메인 맥락,
    이미 결정된 사항, 실무적 제약 등
    판단에 영향을 줄 수 있는 모든 정보를 포함하라.
    """
    tf = _get_taskforce()
    pool = await tf.discuss_async(agenda, context)
    return pool.model_dump_json(indent=2)
