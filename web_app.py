# Web UI Libraries
from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from contextlib import asynccontextmanager
from starlette.middleware.sessions import SessionMiddleware
import uuid

# MCP libraries
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

# LangChain Libraries
from langchain_mcp_adapters.tools import load_mcp_tools
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_anthropic import ChatAnthropic
from langchain.agents import create_agent
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
        # Setup MCP connection with environment variables
        server_params = StdioServerParameters(
            command="node",
            args=[mcp_location],
            env=dict(os.environ)  # Pass all environment variables to MCP server
        )

        # Use proper async context management
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as client_session:
                # Initialize the connection
                await client_session.initialize()

                # Get tools, filter tools using the .env config
                mcp_tools = await load_mcp_tools(client_session)
                
                # Set AI Model
                match os.environ['MODEL_PROVIDER']:
                    case 'OpenAI':
                        llm = ChatOpenAI(model=os.environ["OPENAI_MODEL"], temperature=0)
                    case 'Google':
                        llm = ChatGoogleGenerativeAI(model=os.environ["GEMINI_MODEL"], temperature=0)
                    case 'Anthropic':
                        llm = ChatAnthropic(model=os.environ["ANTHROPIC_MODEL"], temperature=0, max_retries=7)
                    case _:
                        raise RuntimeError("Could not initialise llm")

                # Create the agent with checkpointer for conversation memory
                checkpointer = InMemorySaver()
                agent = create_agent(model=llm, tools=mcp_tools, system_prompt=AGENT_SYSTEM_PROMPT, checkpointer=checkpointer)
                
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

# Add session middleware for user session management
# Secret key should be random and kept secret in production
SESSION_SECRET_KEY = os.environ.get("SESSION_SECRET_KEY", str(uuid.uuid4()))
app.add_middleware(SessionMiddleware, secret_key=SESSION_SECRET_KEY)

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

@app.get("/session")
async def get_session(request: Request):
    """Get the current session ID"""
    if "session_id" not in request.session:
        request.session["session_id"] = str(uuid.uuid4())
    return {"session_id": request.session["session_id"]}

@app.post("/chat")
async def chat(chat_request: ChatRequest, request: Request) -> ChatResponse:
    """Handle chat messages - this is where the AI magic happens"""
    global agent

    if agent is None:
        logger.error("Agent not initialized")
        raise HTTPException(status_code=500, detail="Agent not initialized. Please restart the server.")

    try:
        # Get or create session ID for this user
        if "session_id" not in request.session:
            request.session["session_id"] = str(uuid.uuid4())

        session_id = request.session["session_id"]
        logger.info(f"Processing chat request for session: {session_id}")

        # Create proper message format for LangGraph
        messages = [HumanMessage(content=chat_request.message)]

        # Get response from agent with session-specific thread_id
        response_text = await format_agent_response(agent, messages, langfuse_handler, session_id)

        return ChatResponse(response=response_text)

    # Error Handling
    except Exception as e:
        logger.error(f"Error processing chat request: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error processing request: {str(e)}")

# Run the app
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)