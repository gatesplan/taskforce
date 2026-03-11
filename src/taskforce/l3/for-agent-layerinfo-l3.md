# l3

## roundtable
Roundtable.__init__(panelists: list[Panelist], summarizer: Panelist)
Roundtable.gather(agenda: str, context: str = "") -> list[Opinion]
Roundtable.summarize(agenda: str, opinions: list[Opinion]) -> IdeaPool
Roundtable.discuss(agenda: str, context: str = "") -> IdeaPool
