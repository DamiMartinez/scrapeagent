import os
import pathlib
from dotenv import load_dotenv
from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm
from google.adk.skills import load_skill_from_dir
from google.adk.tools import skill_toolset
from google.adk.tools.mcp_tool.mcp_toolset import McpToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StdioConnectionParams
from mcp import StdioServerParameters
from scrapeagent.prompt import PROMPT
from scrapeagent.tools.file_tools import save_output, create_skill

load_dotenv()

# --- Load skills from the skills directory ---
# Architecture note: Skills use progressive disclosure to keep the context window lean.
# At startup, only L1 metadata (~100 tokens per skill) is loaded for every skill.
# The full SKILL.md body (L2) is loaded only when the agent decides the skill is relevant.
# L3 resources (references/ and assets/) are loaded only when the skill instructions reference them.
# A library of 50 skills costs ~5000 tokens at startup vs. blowing the context window with
# a monolithic system prompt. See README.md for the full architecture explanation.
_skills_dir = pathlib.Path(__file__).parent / "skills"
_skills = [
    load_skill_from_dir(d) for d in sorted(_skills_dir.iterdir()) if d.is_dir()
]

# SkillToolset exposes all skills to the agent with progressive loading.
# See the comment above — only skill descriptions are in context at startup.
skill_tools = skill_toolset.SkillToolset(skills=_skills)

# --- MCP toolsets ---
# mcp-server-fetch: lightweight HTTP fetcher for static sites (no JS rendering)
# timeout=120.0: covers both MCP connection init and per-request fetch time;
# 30s was too short after ADK 1.28.0 started applying it to each tool call.
fetch_toolset = McpToolset(
    connection_params=StdioConnectionParams(
        server_params=StdioServerParameters(
            command="uvx",
            args=["mcp-server-fetch"],
        ),
        timeout=120.0,
    )
)

# @playwright/mcp: full browser automation for JS-heavy sites
# -y flag required: auto-accepts npx package download in non-interactive environments
playwright_toolset = McpToolset(
    connection_params=StdioConnectionParams(
        server_params=StdioServerParameters(
            command="npx",
            args=["-y", "@playwright/mcp", "--headless"],
        ),
        timeout=120.0,
    )
)

# --- Root agent ---
root_agent = LlmAgent(
    model=LiteLlm(model=os.getenv("LITELLM_MODEL", "gemini/gemini-2.5-flash")),
    name="scrapeagent",
    description=(
        "An open-source web scraping agent. "
        "Scrapes any website and saves results as CSV, JSON, or Markdown."
    ),
    instruction=PROMPT,
    tools=[
        skill_tools,
        fetch_toolset,
        playwright_toolset,
        save_output,
        create_skill,
    ],
)
