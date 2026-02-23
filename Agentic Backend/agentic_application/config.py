import os
from urllib.parse import urlparse
from dotenv import load_dotenv
from google.adk.models.lite_llm import LiteLlm
from google.genai import types

# Load environment variables from .env file
load_dotenv()

# Set environment variables
# os.environ['GOOGLE_API_KEY'] = os.getenv('GOOGLE_API_KEY')
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")


def _clean_env(value: str) -> str:
    return value.replace("\r", "").replace("\n", "").strip()

# MCP Server Configuration
# Local default is localhost:8351.
# In deployment, MCP_SERVER_HOST can be full URL (e.g. https://...run.app).
MCP_SERVER_URL = _clean_env(os.getenv('MCP_SERVER_URL', ''))
MCP_SERVER_HOST = _clean_env(os.getenv('MCP_SERVER_HOST', 'localhost'))
MCP_SERVER_PORT = _clean_env(os.getenv('MCP_SERVER_PORT', '8351'))

if MCP_SERVER_URL:
    MCP_SERVER_URL = MCP_SERVER_URL.rstrip('/')
    if not MCP_SERVER_URL.endswith('/mcp'):
        MCP_SERVER_URL = f"{MCP_SERVER_URL}/mcp"
elif MCP_SERVER_HOST.startswith(('http://', 'https://')):
    parsed = urlparse(MCP_SERVER_HOST)
    is_local_host = parsed.hostname in {'localhost', '127.0.0.1'}
    if parsed.scheme == 'https' and is_local_host:
        host_with_port = parsed.netloc or parsed.path
        MCP_SERVER_URL = f"http://{host_with_port}".rstrip('/')
    else:
        MCP_SERVER_URL = MCP_SERVER_HOST.rstrip('/')
    if not MCP_SERVER_URL.endswith('/mcp'):
        MCP_SERVER_URL = f"{MCP_SERVER_URL}/mcp"
else:
    MCP_SERVER_URL = f"http://{MCP_SERVER_HOST}:{MCP_SERVER_PORT}/mcp"


# Model configurations
OPENAI_GPT_MODEL = LiteLlm(model="openai/gpt-4.1-mini")

# Generate Content Configuration
GENERATE_CONTENT_CONFIG = types.GenerateContentConfig(
    temperature=0.1,
)

# Tool Filter Configurations for Bank Loan Processing System
# These configurations define which MCP tools each agent can access

# Supervisor Agent - Coordinates the workflow, no specific tools needed
SUPERVISOR_AGENT_TOOLS = ['fetch_loan_details']

# Verification Analyzer Agent - Document verification and fraud detection
# No specific tools required - uses AI analysis
VERIFICATION_ANALYZER_TOOLS = ['fetch_loan_details', 'web_search_tool']

# Policy Reviewer Agent - Banking policy review and loan product matching
# Uses bank and loan details RAG tools to access bank policies
POLICY_REVIEWER_TOOLS = ['policies_rag_tool']

# Market Analyzer Agent - Market rate analysis using real SOFR, LIBOR, and benchmark data
# Uses web search and benchmark rate tools to gather market data
MARKET_ANALYZER_TOOLS = ['fetch_sofr_rates', 'fetch_benchmark_rates', 'web_search_tool']


