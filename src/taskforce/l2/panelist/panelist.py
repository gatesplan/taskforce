import litellm
from loguru import logger

from ...l1.schema import ModelEntry, Opinion


class Panelist:
    def __init__(self, model_entry: ModelEntry):
        self.model_entry = model_entry
        self._litellm_model = self._resolve_model_id()

    def _resolve_model_id(self) -> str:
        # LiteLLM: OpenAI는 model_id만, 나머지는 provider/model_id
        if self.model_entry.provider == "openai":
            return self.model_entry.model_id
        return f"{self.model_entry.provider}/{self.model_entry.model_id}"

    async def ask_async(self, prompt: str, system_msg: str = "") -> Opinion:
        messages = []
        if system_msg:
            messages.append({"role": "system", "content": system_msg})
        messages.append({"role": "user", "content": prompt})

        try:
            response = await litellm.acompletion(
                model=self._litellm_model,
                messages=messages,
                api_key=self.model_entry.api_key,
                **self.model_entry.extra_params,
            )
            content = response.choices[0].message.content

            # 비용/토큰 추출
            cost = 0.0
            tokens = 0
            try:
                cost = litellm.completion_cost(completion_response=response)
            except Exception:
                pass
            if hasattr(response, "usage") and response.usage:
                tokens = getattr(response.usage, "total_tokens", 0)

            logger.debug(f"{self.model_entry.display_name} 응답: {len(content)} chars, {tokens} tokens, ${cost:.4f}")
            return Opinion(
                model_name=self.model_entry.display_name,
                content=content,
                cost=cost,
                tokens=tokens,
            )
        except Exception as e:
            logger.error(f"{self.model_entry.display_name} 호출 실패: {e}")
            raise
