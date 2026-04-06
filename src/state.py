import operator
from typing import Annotated, Sequence, TypedDict

from langchain_core.messages import BaseMessage


class Member360State(TypedDict):
    """
    State for the Healthcare Member 360 multi-agent system.
    """
    messages: Annotated[Sequence[BaseMessage], operator.add]
    # The 'next' field indicates which node the supervisor will route to next
    next: str
    # Member context: holds arbitrary info that can be shared across agents
    member_context: dict