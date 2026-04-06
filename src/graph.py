from langgraph.graph import StateGraph, START, END

from .state import Member360State
from .agents.supervisor import get_supervisor
from .agents.gna_agent import get_gna_agent
from .agents.domain_agents import (
    get_claims_agent, get_benefits_agent, 
    get_clinical_agent, get_customer_service_agent
)

def create_member360_graph(llm):
    # Initialize agents
    supervisor_node_fn = get_supervisor(llm)
    gna_agent_runnable = get_gna_agent(llm)
    claims_agent_runnable = get_claims_agent(llm)
    benefits_agent_runnable = get_benefits_agent(llm)
    clinical_agent_runnable = get_clinical_agent(llm)
    cs_agent_runnable = get_customer_service_agent(llm)

    # Node runner definitions for domain agents
    def gna_node(state: Member360State):
        result = gna_agent_runnable.invoke(state)
        # return newly appended messages
        return {"messages": result["messages"]}

    def claims_node(state: Member360State):
        result = claims_agent_runnable.invoke(state)
        return {"messages": result["messages"]}

    def benefits_node(state: Member360State):
        result = benefits_agent_runnable.invoke(state)
        return {"messages": result["messages"]}

    def clinical_node(state: Member360State):
        result = clinical_agent_runnable.invoke(state)
        return {"messages": result["messages"]}

    def cs_node(state: Member360State):
        result = cs_agent_runnable.invoke(state)
        return {"messages": result["messages"]}
        
    builder = StateGraph(Member360State)
    
    # Add nodes
    builder.add_node("Supervisor", supervisor_node_fn)
    builder.add_node("GNA", gna_node)
    builder.add_node("Claims", claims_node)
    builder.add_node("Benefits", benefits_node)
    builder.add_node("Clinical", clinical_node)
    builder.add_node("CustomerService", cs_node)

    # Define edges: START always goes to Supervisor
    builder.add_edge(START, "Supervisor")

    # Define conditional edges from Supervisor to individual agents
    builder.add_conditional_edges(
        "Supervisor",
        lambda state: state["next"],
        {
            "GNA": "GNA",
            "Claims": "Claims",
            "Benefits": "Benefits",
            "Clinical": "Clinical",
            "CustomerService": "CustomerService",
            "FINISH": END
        }
    )

    # After domain agents reply, they route back to the Supervisor to determine if the query is fulfilled
    builder.add_edge("GNA", "Supervisor")
    builder.add_edge("Claims", "Supervisor")
    builder.add_edge("Benefits", "Supervisor")
    builder.add_edge("Clinical", "Supervisor")
    builder.add_edge("CustomerService", "Supervisor")

    graph = builder.compile()
    return graph