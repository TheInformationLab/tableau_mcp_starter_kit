# Web UI Libraries
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from contextlib import asynccontextmanager

# MCP libraries
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

# LangChain Libraries
from langchain_mcp_adapters.tools import load_mcp_tools
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import HumanMessage
from langgraph.checkpoint.memory import InMemorySaver

# Set Local MCP Logging
from utilities.logging_config import setup_logging
logger = setup_logging("web_app.log")

# Load System Prompt and Message Formatter
from utilities.prompt import AGENT_SYSTEM_PROMPT
from utilities.chat import format_agent_response

# Load Environment and set MCP Filepath
import os
from dotenv import load_dotenv

load_dotenv()
mcp_location = os.environ['TABLEAU_MCP_FILEPATH']

# Set Langfuse Tracing
from langfuse.langchain import CallbackHandler
langfuse_handler = CallbackHandler()

# Global variables for agent and session
agent = None
session_context = None

# Global async context manager for MCP connection
@asynccontextmanager
async def lifespan(app: FastAPI):
    global agent
    logger.info("Starting up application...")
    
    try:
        # Setup MCP connection
        server_params = StdioServerParameters(
            command="node",
            args=[mcp_location],
        )

        # Use proper async context management
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as client_session:
                # Initialize the connection
                await client_session.initialize()

                # Get tools, filter tools using the .env config
                mcp_tools = await load_mcp_tools(client_session)
                
                # Set AI Model
                llm = ChatOpenAI(model="gpt-4.1", temperature=0)

                # Create the agent
                checkpointer = InMemorySaver()
                agent = create_react_agent(model=llm, tools=mcp_tools, prompt=AGENT_SYSTEM_PROMPT, checkpointer=checkpointer)
                
                yield
        
    # Error Handling
    except Exception as e:
        logger.error(f"Failed to initialize agent: {e}")
        raise

# Create FastAPI app with lifespan
app = FastAPI(
    title="Tableau AI Chat", 
    description="Simple AI chat interface for Tableau data",
    lifespan=lifespan
)

# Serve static files (HTML, CSS, JS)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Request/Response models
class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str



@app.get("/")
def home():
    """Serve the main HTML page"""
    return FileResponse('static/index.html')

@app.get("/index.html")
def static_index():
    return FileResponse('static/index.html')

@app.post("/chat")
async def chat(request: ChatRequest) -> ChatResponse:
    """Handle chat messages - this is where the AI magic happens"""
    global agent
    
    if agent is None:
        logger.error("Agent not initialized")
        raise HTTPException(status_code=500, detail="Agent not initialized. Please restart the server.")
    
    try:      
        # Create proper message format for LangGraph
        messages = [HumanMessage(content=request.message)]

        # Get response from agent
        response_text = await format_agent_response(agent, messages, langfuse_handler)
        
        return ChatResponse(response=response_text)
        
    # Error Handling
    except Exception as e:
        logger.error(f"Error processing chat request: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error processing request: {str(e)}")

# Run the app
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)