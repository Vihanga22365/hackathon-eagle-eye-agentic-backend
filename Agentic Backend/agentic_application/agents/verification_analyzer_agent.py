from google.adk.agents import LlmAgent
from google.adk.agents.sequential_agent import SequentialAgent
from ..config import OPENAI_GPT_MODEL, GENERATE_CONTENT_CONFIG, VERIFICATION_ANALYZER_TOOLS
from ..prompts.verification_analyzer_prompt import VERIFICATION_ANALYZER_INSTRUCTION, VERIFICATION_ANALYZER_DESCRIPTION
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, StreamableHTTPConnectionParams
from ..config import MCP_SERVER_URL

# Verification Analyzer Agent Definition
verification_analyzer_agent = LlmAgent(
    name="VerificationAnalyzerAgent",
    model=OPENAI_GPT_MODEL,
    instruction=VERIFICATION_ANALYZER_INSTRUCTION,
    description=VERIFICATION_ANALYZER_DESCRIPTION,
    tools=[
        MCPToolset(
            connection_params=StreamableHTTPConnectionParams(
                url=MCP_SERVER_URL
            ),
            tool_filter=VERIFICATION_ANALYZER_TOOLS
        )
    ] if VERIFICATION_ANALYZER_TOOLS else [],
    generate_content_config=GENERATE_CONTENT_CONFIG,
)
