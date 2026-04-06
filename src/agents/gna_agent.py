from langchain_core.messages import SystemMessage, HumanMessage
from langgraph.prebuilt import create_react_agent
from ..models import CustomChatModel
from ..tools.gna_tools import get_gna_cases, get_case_details

# We use standard create_react_agent from langgraph.prebuilt to bind tools
def get_gna_agent(llm):
    tools = [get_gna_cases, get_case_details]
    agent = create_react_agent(llm, tools, state_modifier="""
You are a Grievance and Appeals (GNA) specialist for Healthcare Member 360.
You help members check the status of their appeals and file grievances.
Answer their questions using the provided tools.
    """)
    return agent
