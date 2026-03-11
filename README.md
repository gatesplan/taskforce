# taskforce

AI agent-oriented multi-LLM roundtable library.

Multiple top-tier LLMs (GPT, Grok, Claude, Gemini) are queried in parallel with the same agenda, and the collected opinions are classified into **common / divergent / unique** perspectives, returned as a structured `IdeaPool`.

**This package is designed for AI agents, not for direct human use.**
The primary interface is the MCP wrapper (`roundtable_discuss` tool), which allows agents to invoke a roundtable discussion as a tool call. A Python API is also available for programmatic integration.

## Quick Start

### 1. Install

```bash
pip install taskforce
```

For MCP server support:

```bash
pip install taskforce[mcp]
```

### 2. Set environment variables

At least two provider API keys are required (one will be excluded as the caller).
`XAI_API_KEY` is always required (used by the summarizer).

```
OPENAI_API_KEY=sk-...
XAI_API_KEY=xai-...
ANTHROPIC_API_KEY=sk-ant-...
GEMINI_API_KEY=AI...
```

### 3. Use as MCP tool (recommended for agents)

Add to your MCP server config:

`TASKFORCE_CALLER_PROVIDER` is the provider of the agent that will call this tool.
The matching provider's model is excluded from the panel -- querying the same model that is already reasoning adds no diversity.
For example, if Claude Code is the caller, set it to `"anthropic"` so Claude is excluded from the panel.

```json
{
  "mcpServers": {
    "taskforce": {
      "command": "python",
      "args": ["-m", "taskforce.mcp_wrapper"],
      "env": {
        "TASKFORCE_CALLER_PROVIDER": "anthropic"
      }
    }
  }
}
```

The agent can then call the `roundtable_discuss` tool with `agenda` and `context` parameters.

### 4. Use as Python library

```python
from taskforce import Taskforce

tf = Taskforce(caller_provider="anthropic")
pool = tf.discuss(
    agenda="Evaluate the trade-offs of approach A vs B",
    context="<detailed context here>"
)

# pool.common    -- list[str]: points most models agree on
# pool.divergent -- list[DivergentPoint]: topics with differing positions
# pool.unique    -- list[UniquePoint]: points raised by only one model
```

## Important Notes

- **Paid API calls.** Every `discuss()` invocation calls multiple LLM APIs in parallel. Agents should confirm with the user before calling.
- **caller_provider exclusion.** The model from the same provider as the calling agent is excluded from the panel to maximize perspective diversity.
- **XAI_API_KEY is mandatory.** The summarizer (grok-4-1-fast-non-reasoning) always uses the XAI key.
- **Rich context matters.** Input tokens are cheap. Provide as much context as possible -- specifications, constraints, background, decisions already made -- so the panel can give concrete, actionable opinions instead of generic advice.

## API

### `Taskforce(caller_provider, dotenv_path=None)`

- `caller_provider` (`str`): The LLM provider of the calling agent (e.g. `"anthropic"`, `"openai"`). That provider's model is excluded from the panel.
- `dotenv_path` (`str | None`): Path to `.env` file. Defaults to auto-discovery.

### `Taskforce.discuss(agenda, context="") -> IdeaPool`

Synchronous wrapper. Queries the panel, summarizes, and returns an `IdeaPool`.

### `Taskforce.discuss_async(agenda, context="") -> IdeaPool`

Async version for use in async contexts.

### `IdeaPool`

| Field | Type | Description |
|-------|------|-------------|
| `agenda` | `str` | The original agenda |
| `common` | `list[str]` | Points most models agree on |
| `divergent` | `list[DivergentPoint]` | Topics with differing positions (`topic`, `positions: dict[model, position]`) |
| `unique` | `list[UniquePoint]` | Points from a single model (`point`, `source_model`) |
| `total_cost` | `float` | Total API cost (USD) |
| `total_tokens` | `int` | Total tokens consumed |

## License

MIT
