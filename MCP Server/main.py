from mcp.server.fastmcp import FastMCP
from mcp.server.transport_security import TransportSecuritySettings
from tools import (
    web_search_tool,
    fetch_sofr_rates,
    fetch_benchmark_rates,
    policies_rag_tool,
    fetch_loan_details
)

mcp = FastMCP(
    "StatefulServer",
    stateless_http=True,
    transport_security=TransportSecuritySettings(enable_dns_rebinding_protection=False),
)
mcp.settings.host = "0.0.0.0"
mcp.settings.port = 8351

# Register all tools with the MCP server
mcp.tool()(web_search_tool)
mcp.tool()(fetch_sofr_rates)
mcp.tool()(fetch_benchmark_rates)
mcp.tool()(policies_rag_tool)
mcp.tool()(fetch_loan_details)


if __name__ == "__main__":
    print("Starting MCP server on http://0.0.0.0:8351")
    mcp.run(transport="streamable-http")
