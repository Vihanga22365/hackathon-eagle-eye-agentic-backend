from google.adk.agents import LlmAgent
from google.adk.agents.sequential_agent import SequentialAgent
from ..config import OPENAI_GPT_MODEL, GENERATE_CONTENT_CONFIG, MARKET_ANALYZER_TOOLS
from ..prompts.market_analyzer_prompt import MARKET_ANALYZER_INSTRUCTION, MARKET_ANALYZER_DESCRIPTION
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, StreamableHTTPConnectionParams
from ..config import MCP_SERVER_URL

# Market Analyzer Agent Definition
market_analyzer_agent = LlmAgent(
    name="MarketAnalyzerAgent",
    model=OPENAI_GPT_MODEL,
    instruction=MARKET_ANALYZER_INSTRUCTION,
    description=MARKET_ANALYZER_DESCRIPTION,
    tools=[
        MCPToolset(
            connection_params=StreamableHTTPConnectionParams(
                url=MCP_SERVER_URL
            ),
            tool_filter=MARKET_ANALYZER_TOOLS
        )
    ],
    generate_content_config=GENERATE_CONTENT_CONFIG,
)
