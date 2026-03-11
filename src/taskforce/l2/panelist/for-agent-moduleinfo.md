# Panelist

LiteLLM 래퍼. 개별 LLM 모델에 async 질의.

## Panelist

ModelEntry를 받아 LiteLLM acompletion으로 호출.

### Properties
model_entry: ModelEntry    # 모델 정보

### __init__
__init__(model_entry: ModelEntry)
    ModelEntry 기반으로 LiteLLM 모델 ID 해석.
    OpenAI는 model_id만, 나머지는 provider/model_id 형식.

### Methods

ask_async(prompt: str, system_msg: str = "") -> Opinion
    raise Exception
    LiteLLM acompletion으로 모델 호출.
    system_msg가 있으면 system role로 전달.
    실패 시 원본 예외 전파.
