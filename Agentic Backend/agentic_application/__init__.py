# Load environment configuration first
from . import config

from .agents import (
    supervisor_agent,
    verification_analyzer_agent,
    policy_reviewer_agent,
    market_analyzer_agent,
)
from .prompts import (
    SUPERVISOR_AGENT_INSTRUCTION,
    SUPERVISOR_AGENT_DESCRIPTION,
    VERIFICATION_ANALYZER_INSTRUCTION,
    VERIFICATION_ANALYZER_DESCRIPTION,
    POLICY_REVIEWER_INSTRUCTION,
    POLICY_REVIEWER_DESCRIPTION,
    MARKET_ANALYZER_INSTRUCTION,
    MARKET_ANALYZER_DESCRIPTION,
)

# Expose supervisor_agent as root_agent for Google ADK
root_agent = supervisor_agent
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or specify your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

__all__ = [
    'root_agent',
    'supervisor_agent',
    'verification_analyzer_agent',
    'policy_reviewer_agent',
    'market_analyzer_agent',
    'app',
    'SUPERVISOR_AGENT_INSTRUCTION',
    'SUPERVISOR_AGENT_DESCRIPTION',
    'VERIFICATION_ANALYZER_INSTRUCTION',
    'VERIFICATION_ANALYZER_DESCRIPTION',
    'POLICY_REVIEWER_INSTRUCTION',
    'POLICY_REVIEWER_DESCRIPTION',
    'MARKET_ANALYZER_INSTRUCTION',
    'MARKET_ANALYZER_DESCRIPTION',
]
