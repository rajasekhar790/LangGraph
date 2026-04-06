from typing import Any, List, Optional
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import BaseMessage, SystemMessage, HumanMessage, AIMessage
from langchain_core.outputs import ChatResult, ChatGeneration

class CustomChatModel(BaseChatModel):
    """
    A custom chat model modified to support basic routing and conversational completion tasks.
    """
    model_name: str = "custom-healthcare-model"
    
    def _generate(
        self, 
        messages: List[BaseMessage], 
        stop: Optional[List[str]] = None, 
        **kwargs: Any
    ) -> ChatResult:
        
        formatted_messages = []
        for msg in messages:
            if isinstance(msg, SystemMessage):
                formatted_messages.append({"role": "system", "content": msg.content})
            elif isinstance(msg, HumanMessage):
                formatted_messages.append({"role": "user", "content": cast_content(msg.content)})
            elif isinstance(msg, AIMessage):
                formatted_messages.append({"role": "assistant", "content": cast_content(msg.content)})
            
        print(f"[Model Integration] Sending payload to internal proxy API for processing.")
        
        # Here we mock the result to provide standard text outputs since we are not connecting to a real OpenAI API.
        user_message_text = formatted_messages[-1]['content'].lower() if formatted_messages else ""
        
        # Super rudimentary logic for mock tool binding and routing behaviors for demonstration purposes.
        response_content = f"The mock model received your query: {user_message_text}"
        
        message = AIMessage(content=response_content)
        generation = ChatGeneration(message=message)
        
        return ChatResult(generations=[generation])

    @property
    def _llm_type(self) -> str:
        return "custom_chat_model"

def cast_content(content: Any) -> str:
    if isinstance(content, str):
        return content
    elif isinstance(content, list):
        return " ".join([str(c) for c in content])
    return str(content)