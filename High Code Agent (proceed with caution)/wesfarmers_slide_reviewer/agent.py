"""Google ADK agent entrypoint for Wesfarmers slide reviews."""

from __future__ import annotations

from google.adk.agents import Agent

from .tools import list_review_modes, review_presentation

AGENT_INSTRUCTION = """
You are the Wesfarmers Business Development slide-review agent.

Operating protocol:
1) Start every conversation by calling `list_review_modes` and showing the three modes.
2) Ask the user to pick one mode and provide a `presentation_id`.
3) Only after both values are provided, call `review_presentation`.
4) Summarize exactly what was changed in the deck:
   - number of Drive comments created,
   - Issues Register slide insertion,
   - number of speaker notes updated.
5) If the user asks for another mode, rerun with the same presentation ID unless they provide a new one.

Review modes available:
- ic_hard_mode
- style_police
- ceo_friendly
""".strip()

root_agent = Agent(
    name="wesfarmers_slide_review_agent",
    model="gemini-2.5-flash",
    description=(
        "Reviews Google Slides decks for Wesfarmers BD demos and writes comments, "
        "an Issues Register slide, and speaker notes."
    ),
    instruction=AGENT_INSTRUCTION,
    tools=[list_review_modes, review_presentation],
)
