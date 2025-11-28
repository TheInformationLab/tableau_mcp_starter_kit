from langgraph.graph.state import CompiledStateGraph
from langchain_core.messages import HumanMessage
from typing import List
from langfuse.langchain import CallbackHandler

async def format_agent_response(agent: CompiledStateGraph, messages: List[HumanMessage], langfuse_handler: CallbackHandler):
    """Stream response from agent and return the final content"""
    
    response_text = ""
    async for chunk in agent.astream(
        {"messages": messages}, 
        config={"configurable": {"thread_id": "main_session"}, "callbacks": [langfuse_handler]}, 
        stream_mode="values"
    ):
        if 'messages' in chunk and chunk['messages']:
            latest_message = chunk['messages'][-1]
            if hasattr(latest_message, 'content'):
                response_text = latest_message.content
    
    return response_text
