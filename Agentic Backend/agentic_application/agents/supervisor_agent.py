from google.adk.agents import SequentialAgent, LlmAgent
from .verification_analyzer_agent import verification_analyzer_agent
from .policy_reviewer_agent import policy_reviewer_agent
from .market_analyzer_agent import market_analyzer_agent
from .summary_generator_agent import summary_generator_agent
from ..config import OPENAI_GPT_MODEL, MCP_SERVER_URL, SUPERVISOR_AGENT_TOOLS, GENERATE_CONTENT_CONFIG
from ..prompts.supervisor_prompt import SUPERVISOR_AGENT_INSTRUCTION, SUPERVISOR_AGENT_DESCRIPTION
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, StreamableHTTPConnectionParams
from google.adk.planners import BuiltInPlanner
from google.adk.tools import agent_tool

# Supervisor Agent Definition
supervisor_agent = SequentialAgent(
    name="SupervisorAgent",
    description=SUPERVISOR_AGENT_DESCRIPTION,
    sub_agents=[
        verification_analyzer_agent,
        policy_reviewer_agent,
        market_analyzer_agent,
        summary_generator_agent,
    ]
)

# supervisor_agent = LlmAgent(
#     name="SupervisorAgent",
#     model=OPENAI_GPT_MODEL,
#     instruction=SUPERVISOR_AGENT_INSTRUCTION,
#     description=SUPERVISOR_AGENT_DESCRIPTION,
#     tools=[
#         MCPToolset(
#             connection_params=StreamableHTTPConnectionParams(
#                 url=MCP_SERVER_URL
#             ),
#             tool_filter=SUPERVISOR_AGENT_TOOLS
#         )
#     ],
#     sub_agents=[
#         verification_analyzer_agent,
#         policy_reviewer_agent,
#         market_analyzer_agent,
#         summary_generator_agent,
#     ],
#     generate_content_config=GENERATE_CONTENT_CONFIG,
# )