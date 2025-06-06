# ./adk_agent_samples/mcp_client_agent/agent.py
import os
from dotenv import load_dotenv

from google.adk.agents.llm_agent import LlmAgent
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset
from google.adk.tools.mcp_tool.mcp_toolset import StdioServerParameters
from google.adk.models.lite_llm import LiteLlm
import sys


# --- Load Environment Variables (If ADK tools need them, e.g., API keys) ---
load_dotenv() # Create a .env file in the same directory if needed
 
root_agent = LlmAgent(
    # model=LiteLlm(model="ollama/gemma3:27b"), 
    model=LiteLlm(model="ollama_chat/qwen3:30b"),  
    # model='gemini-2.5-pro-preview-05-06',
    name='mcp_server_client',
    instruction="You are a helpful assistant that has access to a chroma db with info about the ADK, only use your tools to get help the user",
    tools=[
        # MCPToolset(
        #     connection_params=StdioServerParameters(
        #         command='npx',
        #         args=["-y","@modelcontextprotocol/server-memory"],
        #         env={
        #             "MEMORY_FILE_PATH": "/Users/jvillarreal/Documents/playground/mcp_server_framework/memory.json"
        #         }
        #     ),errlog=sys.stderr
        # ),
        # MCPToolset(
        #     connection_params=StdioServerParameters(
        #         command='node',  
        #         args=[
        #             "/Users/jvillarreal/Documents/Cline/MCP/fetch-mcp/dist/index.js"
        #         ],
        #     )
        # ),
        # MCPToolset(
        #     connection_params=StdioServerParameters(
        #         command='python3',
        #         args=["/Users/jvillarreal/Documents/playground/mcp_server_framework/mcp_servers/mcp_stdio_mac_tts_mcp_server/mac_tts_mcp_server.py"],
        #     )
        #     ,errlog=sys.stderr
        # ),
        MCPToolset(
            connection_params=StdioServerParameters(
                command='python3',
                args=["/Users/jvillarreal/Documents/playground/mcp_server_framework/mcp_servers/chromadb_server/chromadb_server.py"],
            )
            ,errlog=sys.stderr
        ),
    ],

)

 