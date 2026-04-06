from typing import Literal
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel
from ..state import Member360State

def get_supervisor(llm):
    """
    Creates the Supervisor router.
    Uses Structured Output (or simpler LLM calls) to decide which agent to route to.
    """
    system_prompt = (
        "You are a supervisor for the Healthcare Member 360 multi-agent system. "
        "Your job is to read the user's latest query and route it to the correct specialized agent: "
        "\n1) 'GNA' - For appeals, grievances, or case statuses."
        "\n2) 'Claims' - For billing, payments, or out-of-pocket costs."
        "\n3) 'Benefits' - For plan eligibility, copays, or coverage."
        "\n4) 'Clinical' - For health records, care gaps, or wellness."
        "\n5) 'CustomerService' - For general account support or previous chat history."
        "\n6) 'FINISH' - If the request has been fully answered or is unrelated."
        "\n\nBased on the user query, return EXACTLY ONE of these strings (GNA, Claims, Benefits, Clinical, CustomerService, FINISH)."
    )
    
    # We create a simple router function that injects a mocked structured output behavior for custom llms
    # Or uses standard .with_structured_output for ChatOpenAI / ChatAnthropic
    
    class RouterOut(BaseModel):
        next: Literal["GNA", "Claims", "Benefits", "Clinical", "CustomerService", "FINISH"]

    # If the user uses a standard LLM, this structured routing works gracefully
    if hasattr(llm, "with_structured_output"):
        router = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("messages", "{messages}")
        ]) | llm.with_structured_output(RouterOut)
        
        def run_router(state: Member360State):
            res = router.invoke({"messages": state["messages"]})
            return {"next": res.next}
            
        return run_router
    else:
        # Fallback for custom minimal LLM
        def run_fallback_router(state: Member360State):
            last_msg = state["messages"][-1].content.lower()
            if "appeal" in last_msg or "case" in last_msg or "grievance" in last_msg:
                return {"next": "GNA"}
            elif "claim" in last_msg or "bill" in last_msg:
                return {"next": "Claims"}
            elif "copay" in last_msg or "deductible" in last_msg or "benefit" in last_msg:
                return {"next": "Benefits"}
            elif "gap" in last_msg or "doctor" in last_msg:
                return {"next": "Clinical"}
            else:
                return {"next": "FINISH"}
                
        return run_fallback_router