from google.adk.agents import LlmAgent
from ..config import OPENAI_GPT_MODEL, GENERATE_CONTENT_CONFIG
from ..prompts.summary_generator_prompt import SUMMARY_GENERATOR_INSTRUCTION, SUMMARY_GENERATOR_DESCRIPTION


summary_generator_agent = LlmAgent(
    name="SummaryGeneratorAgent",
    model=OPENAI_GPT_MODEL,
    instruction=SUMMARY_GENERATOR_INSTRUCTION,
    description=SUMMARY_GENERATOR_DESCRIPTION,
    tools=[],
    generate_content_config=GENERATE_CONTENT_CONFIG,
)
