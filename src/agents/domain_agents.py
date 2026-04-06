from langgraph.prebuilt import create_react_agent
from ..tools.mock_tools import get_claims_history, get_benefits_eligibility, get_care_gaps, get_recent_interactions

def get_claims_agent(llm):
    tools = [get_claims_history]
    return create_react_agent(llm, tools, state_modifier="""
You are a Claims and Billing specialist for Healthcare Member 360.
Assist members with tracking claim status and reviewing billing operations.
""")

def get_benefits_agent(llm):
    tools = [get_benefits_eligibility]
    return create_react_agent(llm, tools, state_modifier="""
You are a Benefits and Eligibility agent. Assist the member in understanding their coverage and deductibles.
""")

def get_clinical_agent(llm):
    tools = [get_care_gaps]
    return create_react_agent(llm, tools, state_modifier="""
You are a Clinical and Wellness specialist. Check for care gaps and wellness visits.
""")

def get_customer_service_agent(llm):
    tools = [get_recent_interactions]
    return create_react_agent(llm, tools, state_modifier="""
You are a Customer Service generalist. Help members navigate their past chats and calls.
""")
