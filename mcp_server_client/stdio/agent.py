# Generic Stdio MCP Client Agent
import os
import sys
import asyncio
from dotenv import load_dotenv
from google.genai import types

from google.adk.agents.llm_agent import LlmAgent
from google.adk.runners import InMemoryRunner
from google.adk.tools.mcp_tool.mcp_toolset import (
    MCPToolset,
    StdioConnectionParams,
    StdioServerParameters,
)
from google.adk.models.lite_llm import LiteLlm

# --- 1. CONFIGURATION ---
# Load environment variables (API keys, etc.)
load_dotenv()

# Model Selection: Configure your LLM here
# model = 'gemini-2.0-flash'
# model = LiteLlm(model="ollama/gemma3:27b")
MODEL = LiteLlm(model="ollama_chat/qwen3:30b")

# Agent Identity
AGENT_NAME = "mcp_framework_assistant"
AGENT_INSTRUCTION = """You are a TASK-ORIENTED assistant.
Your goal is to execute user requests IMMEDIATELY using your tools.

AVAILABLE TOOLS:
1. text_to_speech_mac: Argument: 'text_to_speak' (string). Use for TTS.
2. convert_markdown_to_html: Argument: 'markdown_content' (string). Use for mindmaps.
3. retrieve_documents: Argument: 'query' (string), 'k' (int). Use for search.

RULES:
- DO NOT EXPLAIN.
- DO NOT ASK FOR PERMISSION.
- ALWAYS GENERATE NECESSARY CONTENT (like markdown) YOURSELF.
- CALL THE TOOL IMMEDIATELY.
"""

# Server Directory Resolution
# Automatically find the mcp_servers directory relative to this script
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, "../../"))
SERVERS_DIR = os.path.join(PROJECT_ROOT, "mcp_servers/stdio")

# 2. SERVER REGISTRY
# Add or remove servers from this list to enable/disable them
ACTIVE_SERVERS = [
    {
        "name": "mac_tts",
        "path": os.path.join(SERVERS_DIR, "mac_tts/stdio_dynamic_tool_server.py"),
        "command": sys.executable, # Use the venv interpreter
        "enabled": True
    },
    {
        "name": "chromadb",
        "path": os.path.join(SERVERS_DIR, "chromadb/stdio_dynamic_tool_server.py"),
        "command": sys.executable, # Use the venv interpreter
        "enabled": True
    },
    {
        "name": "mindmap",
        "path": os.path.join(SERVERS_DIR, "mindmap/stdio_dynamic_tool_server.py"),
        "command": sys.executable, # Use the venv interpreter
        "enabled": True
    }
]

# --- 3. TOOLSET INITIALIZATION ---
def initialize_tools():
    mcp_tools = []
    for srv in ACTIVE_SERVERS:
        if srv.get("enabled", False):
            print(f"[*] Initializing {srv['name']} server...")
            mcp_tools.append(
                MCPToolset(
                    connection_params=StdioConnectionParams(
                        server_params=StdioServerParameters(
                            command=srv["command"],
                            args=[srv["path"]],
                        ),
                        timeout=30 # Increase timeout for tool execution
                    ),
                    errlog=sys.stderr
                )
            )
    return mcp_tools

# --- 4. AGENT INITIALIZATION ---
# We use a lazy initialization pattern to avoid execution on import
def create_agent():
    return LlmAgent(
        model=MODEL,
        name=AGENT_NAME,
        instruction=AGENT_INSTRUCTION,
        tools=initialize_tools(),
    )

if __name__ == "__main__":
    print(f"\n--- {AGENT_NAME} Started ---")
    print(f"Model: {MODEL}")
    
    # Initialize agent only when running directly
    print("[*] Setting up agent and connection to servers...")
    root_agent = create_agent()
    
    # Use InMemoryRunner for a simple CLI experience
    runner = InMemoryRunner(agent=root_agent)
    
    async def chat_loop():
        # Session State
        user_id = "default_user"
        session_id = "default_session"
        
        try:
            # Initialize the session in the memory service
            await runner.session_service.create_session(
                app_name=runner.app_name,
                user_id=user_id,
                session_id=session_id
            )
            
            # Debug: List available tools
            all_tools = await root_agent.canonical_tools()
            print(f"[*] Total tools available: {len(all_tools)}")
            for t in all_tools:
                description = t.description[:60].replace("\n", " ")
                print(f"    - {t.name}: {description}...")
                # Also print the schema for debugging
                try:
                    # In newer ADK, _get_declaration() is the standard way to get the Gemini schema
                    decl = t._get_declaration()
                    print(f"      [Schema]: {decl}")
                except Exception as e:
                    print(f"      [Schema Error]: {e}")

            print("\n[Chat Mode] Type your message and press Enter.")
            print("Type 'exit' or 'quit' to stop.\n")
            
            while True:
                try:
                    user_input = await asyncio.to_thread(input, "You: ")
                    user_input = user_input.strip()
                    
                    if user_input.lower() in ['exit', 'quit']:
                        print("Goodbye!")
                        break
                    
                    if user_input.lower() == 'clear':
                        print("[*] Clearing session...")
                        # We just generate a new session ID to start fresh
                        import uuid
                        session_id = f"session_{uuid.uuid4().hex[:8]}"
                        await runner.session_service.create_session(
                            app_name=runner.app_name,
                            user_id=user_id,
                            session_id=session_id
                        )
                        print(f"[*] New Session ID: {session_id}")
                        continue

                    if user_input.lower() == 'debug':
                        print("[*] Inspecting Session Events:")
                        session = await runner.session_service.get_session(
                            app_name=runner.app_name, user_id=user_id, session_id=session_id
                        )
                        for i, ev in enumerate(session.events):
                            role = ev.author if ev.author != "user" else "USER"
                            print(f"  {i}. [{role}]")
                            if ev.content:
                                for part in ev.content.parts:
                                    if part.text: print(f"     TEXT: {part.text}")
                                    if part.function_call: print(f"     CALL: {part.function_call.name}")
                                    if part.function_response: print(f"     RESP: {part.function_response.name}")
                        continue

                    if not user_input:
                        continue
                        
                    print(f"\n{AGENT_NAME}: ", end="", flush=True)
                    
                    new_message = types.Content(parts=[types.Part(text=user_input)])
                    
                    # Using run_async in the same loop
                    async for event in runner.run_async(
                        user_id=user_id,
                        session_id=session_id,
                        new_message=new_message
                    ):
                        # Log the event parts for debugging
                        if event.content and event.content.parts:
                            for part in event.content.parts:
                                if part.text:
                                    if not event.partial:
                                        print(part.text, end="", flush=True)
                                elif part.function_call:
                                    print(f"\n[*] MODEL PRODUCED CALL: {part.function_call.name}")
                                elif part.function_response:
                                    print(f"\n[*] MODEL PRODUCED RESP: {part.function_response.name}")
                        
                        # Print tool calls for visibility
                        func_calls = event.get_function_calls()
                        if func_calls:
                            for call in func_calls:
                                print(f"\n[*] Executing tool: {call.name}({call.args})")
                        
                        # Print tool results
                        func_resps = event.get_function_responses()
                        if func_resps:
                            for resp in func_resps:
                                content_preview = str(resp.response)[:300].replace('\n', ' ')
                                print(f"\n[*] Tool result: {content_preview}...")
                    
                    print("\n")
                    
                except KeyboardInterrupt:
                    print("\nGoodbye!")
                    break
                except Exception as e:
                    print(f"\n[Error] {str(e)}\n")
        finally:
            # Proper cleanup of MCP connections inside the same loop
            print("[*] Closing server connections...")
            await runner.close()

    # Run everything in a single async block
    try:
        asyncio.run(chat_loop())
    except KeyboardInterrupt:
        pass
