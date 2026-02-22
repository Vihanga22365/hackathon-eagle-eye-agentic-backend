from google.adk.agents import LlmAgent
from google.adk.agents.sequential_agent import SequentialAgent
from ..config import OPENAI_GPT_MODEL, GENERATE_CONTENT_CONFIG, POLICY_REVIEWER_TOOLS
from ..prompts.policy_reviewer_prompt import POLICY_REVIEWER_INSTRUCTION, POLICY_REVIEWER_DESCRIPTION
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, StreamableHTTPConnectionParams
from ..config import MCP_SERVER_URL

# Policy Reviewer Agent Definition
policy_reviewer_agent = LlmAgent(
    name="PolicyReviewerAgent",
    model=OPENAI_GPT_MODEL,
    instruction=POLICY_REVIEWER_INSTRUCTION,
    description=POLICY_REVIEWER_DESCRIPTION,
    tools=[
        MCPToolset(
            connection_params=StreamableHTTPConnectionParams(
                url=MCP_SERVER_URL
            ),
            tool_filter=POLICY_REVIEWER_TOOLS
        )
    ],
    generate_content_config=GENERATE_CONTENT_CONFIG,
)
