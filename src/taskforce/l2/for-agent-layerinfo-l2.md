# l2

## config
EnvConfig.__init__(caller_provider: str, dotenv_path: str | None = None)
EnvConfig.get_active_panels() -> list[ModelEntry]

## panelist
Panelist.__init__(model_entry: ModelEntry)
Panelist.ask_async(prompt: str, system_msg: str = "") -> Opinion

## session_logger
SessionLogger.__init__(log_dir: Path | None = None)
SessionLogger.log(agenda: str, context: str, opinions: list[Opinion], summarizer_output: str = "") -> Path

## cost_logger
CostLogger.__init__(log_dir: Path | None = None)
CostLogger.log(agenda: str, opinions: list[Opinion], summarizer_cost: float = 0.0, summarizer_tokens: int = 0) -> None
