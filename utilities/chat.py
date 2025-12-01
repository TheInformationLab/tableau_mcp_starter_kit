from langgraph.graph.state import CompiledStateGraph
from langchain_core.messages import HumanMessage
from typing import List
from langfuse.langchain import CallbackHandler

async def format_agent_response(agent: CompiledStateGraph, messages: List[HumanMessage], langfuse_handler: CallbackHandler, session_id: str):
    """Stream response from agent and return the final content

    Args:
        agent: The LangGraph agent
        messages: List of messages to send
        langfuse_handler: Langfuse callback handler for tracing
        session_id: Unique session ID for this user's conversation thread
    """

    response_text = ""
    async for chunk in agent.astream(
        {"messages": messages},
        config={"configurable": {"thread_id": session_id}, "callbacks": [langfuse_handler]},
        stream_mode="values"
    ):
        if 'messages' in chunk and chunk['messages']:
            latest_message = chunk['messages'][-1]
            if hasattr(latest_message, 'content'):
                response_text = latest_message.content

    return response_text
