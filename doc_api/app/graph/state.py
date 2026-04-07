from typing import TypedDict, List, Optional

class GraphState(TypedDict):
    query: str
    history: List[str]
    context: Optional[str]
    intent: Optional[str]
    answer: Optional[str]
    booking: Optional[dict]
