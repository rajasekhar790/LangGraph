import os
from langchain_core.messages import HumanMessage
from src.graph import create_member360_graph
from src.models import CustomChatModel

def main():
    print("Initializing Healthcare Member 360 Multi-Agent System...")
    
    # We will use the custom LLM here. To get real reasoning, you can swap this with ChatOpenAI later.
    llm = CustomChatModel()
    
    app = create_member360_graph(llm)
    
    # Test query 1
    query_1 = "I need to check the status of my recent appeal and understand why my claim was denied."
    print(f"\n[User Query]: {query_1}")
    
    state = {
        "messages": [HumanMessage(content=query_1)],
        "member_context": {"member_id": "MEM12345"}
    }
    
    # Run graph
    for output in app.stream(state):
        # The output comes back as a dict with the name of the node that just executed
        for node_name, result in output.items():
            print(f"---\n(Node: {node_name}):")
            if "messages" in result:
                # Print the latest message
                latest = result["messages"][-1].content
                print(f"  {latest}")
            elif "next" in result:
                print(f"  Routing to: {result['next']}")

if __name__ == "__main__":
    main()