"""Static demo content for the Wesfarmers slide-review agent."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class ModeContent:
    key: str
    label: str
    persona: str
    style: str
    issues_register_summary: str
    drive_comments: tuple[tuple[str, str], ...]
    speaker_focus: tuple[str, ...]


DEFAULT_STYLE_GUIDE_RULES: tuple[str, ...] = (
    "Use understated language; avoid superlatives and hype words.",
    "Prefer the Wesfarmers phrase 'satisfactory returns' over promotional claims.",
    "Reconcile every number across slides before publication.",
    "One claim, one source, one timeframe per metric.",
    "Ensure each argument is logically directional, not just numerically true.",
    "Build the narrative as strategy and growth case first, valuation second.",
    "Flag precedent context explicitly when using offshore or non-like-for-like comps.",
    "End with a clear ask, accountable owner, and timing.",
)

STYLE_GUIDE_FILE = Path(__file__).with_name("wesfarmers_style_guide.md")

SLIDE_AI_COMMENTS: dict[int, tuple[str, ...]] = {
    1: (
        "The phrase 'Game-Changing Acquisition Opportunity' may be perceived as promotional for an early-stage IC audience.",
        "Consider a more neutral title (for example: 'Initial Acquisition Opportunity - PetVet Australia') to align with IC tone expectations.",
    ),
    2: (
        "Terms such as 'incredible opportunity' and 'massive strategic opportunity' may benefit from tighter evidentiary support or more neutral phrasing.",
        "Revenue CAGR of 8.1% is described as 'explosive', which may invite scrutiny. Consider aligning descriptive language with the underlying growth profile.",
        "Valuation attractiveness is asserted without explicit downside or sensitivity reference.",
    ),
    3: (
        "Market growth (7.2% CAGR) is presented at an aggregate level. Clarify growth differences between retail, veterinary services, and subscriptions to support the strategic thesis.",
        "Pet ownership is cited as both 'over 70%' and '69%' across the slide. Standardise language for consistency.",
    ),
    4: (
        "The integrated retail + vet model is clearly articulated; however, relative performance versus key competitors is not explicitly quantified.",
        "Consider adding a short comparator benchmark (for example: margins or store economics vs Petbarn / Greencross) to reinforce differentiation.",
    ),
    5: (
        "EBITDA CAGR (14.3%) materially outpaces revenue CAGR (8.1%). Clarify the contribution of mix, pricing, operating leverage, and acquisition activity.",
        "Capex growth appears to outpace revenue growth; explicitly address capital intensity and payback dynamics.",
        "Margin expansion assumptions should be reconciled with integration complexity outlined later in the pack.",
    ),
    6: (
        "Several strategic arguments (Flybuys, OnePass, OneData) overlap conceptually. Consider consolidating into a single 'Data & Loyalty Flywheel' pillar for clarity.",
        "Some synergy benefits described here are repeated in the Synergy Potential slide, creating potential double-counting risk.",
    ),
    7: (
        "Run-rate EBITDA synergies of A$94-126m represent approximately 95-130% of standalone EBITDA, which is high by IC standards.",
        "Revenue synergies are assigned 'Medium' confidence but are still material to the valuation case; consider explicit downside scenarios.",
        "Integration costs and dis-synergies are not quantified and should be highlighted for balance.",
    ),
    8: (
        "Valuation triangulation across methodologies is sound; however, key DCF assumptions (9.5% WACC, 3.0% terminal growth) are not justified elsewhere in the pack.",
        "Consider adding a sensitivity table (for example: +/-100bps WACC, +/-50bps TGR) to demonstrate downside protection.",
        "Precedent transaction multiples exceed trading comps at the high end; rationale for this premium should be articulated.",
    ),
    9: (
        "The roadmap implies significant operational expansion (new states, new verticals, telehealth, private label) within three years.",
        "Execution sequencing and organisational capacity constraints are not explicitly addressed.",
        "Highlight which initiatives are critical-path versus optional.",
    ),
    10: (
        "Risk identification is comprehensive; however, risks are presented qualitatively rather than ranked by potential value impact.",
        "Veterinary talent retention risk may be underweighted given sector-wide shortages and competitive dynamics.",
        "Explicitly link top risks to valuation and synergy sensitivity.",
    ),
    11: (
        "The proposed eight-month timeline appears ambitious given the scale and regulatory complexity of the transaction.",
        "Dependencies between due diligence findings, Board approvals, and regulatory clearance could be made more explicit.",
        "Identify key timetable breakpoints that would trigger reassessment.",
    ),
    12: (
        "The recommendation is decisive but does not explicitly state gating criteria for proceeding beyond Phase 1.",
        "Consider adding key diligence questions, explicit walk-away conditions, and value-based decision thresholds for IC review.",
    ),
}


REVIEW_MODES: dict[str, ModeContent] = {
    "ic_hard_mode": ModeContent(
        key="ic_hard_mode",
        label="IC Hard Mode",
        persona="Skeptical investment-committee reviewer who pressure-tests every claim.",
        style="High skepticism, downside-first framing, and hard evidence standards.",
        issues_register_summary=(
            "Prioritise tone discipline, numeric reconciliation, logical validity, "
            "and precedent realism before asking for any valuation decision."
        ),
        drive_comments=(
            (
                "Slide 1",
                "[TONE] 'Game-Changing', 'transformative', and 'disrupt' are not credible in a Wesfarmers board context. Replace with neutral language and anchor to 'satisfactory returns'.",
            ),
            (
                "Slide 2",
                "[TONE] 'incredible opportunity', 'explosive revenue growth', and 'massive strategic opportunity' read like sell-side hype. Recast in sober, evidence-based terms.",
            ),
            (
                "Slide 12",
                "[TONE] 'outstanding returns' conflicts with Wesfarmers corporate language. Use 'satisfactory returns' unless you can defend a materially different risk profile.",
            ),
            (
                "Slides 2 and 12",
                "[NUMBERS] Flybuys member count is inconsistent: 10.2m vs 9.9m. Use one audited FY25 figure (9.9m) and cascade the correction through every derivative metric.",
            ),
            (
                "Slide 3",
                "[NUMBERS] Subtitle says 'over 70%' while the stat card says 69%. This internal contradiction undermines trust in the entire deck. Pick one number and footnote source/date.",
            ),
            (
                "Slide 5",
                "[NUMBERS] Free Cash Flow 57.8 does not reconcile to EBITDA 97.6 less Capex 36.4 (61.2). Show the missing ~3.4m bridge item explicitly (working capital/other).",
            ),
            (
                "Slides 7 and 12",
                "[NUMBERS] Synergy range conflicts: A$94-126m vs A$95-130m. You cannot ask for approval off two ranges. Align to one base-case interval with scenario notes.",
            ),
            (
                "Slide 6",
                "[LOGIC] '67% of Bunnings customers are pet owners' is presented as a strength, but national household pet ownership is 69%. This is below benchmark, not above.",
            ),
            (
                "Slides 4 and 6",
                "[LOGIC] Recurring revenue claim is 42%, but the pie components shown (Vet 26% + Grooming 10%) total 36%. Either redefine recurring or fix the chart and headline.",
            ),
            (
                "Slides 8 and 9",
                "[STRUCTURE] Valuation appears before the growth roadmap. This inverts the investment narrative. Build strategic thesis and growth confidence before price discussion.",
            ),
            (
                "Location footprint section",
                "[CONSISTENCY] 142 stores + 38 vet clinics implies 180 locations, but state split only totals 142 stores. Add clinic distribution by state or the footprint slide is incomplete.",
            ),
            (
                "Flybuys target section",
                "[CONSISTENCY] 3.5m pet-member target appears undercalled against a 9.9m base with 69% pet ownership (~6.8m addressable). Explain gating logic or revise ambition.",
            ),
            (
                "Slide 6",
                "[PRECEDENT] OnePass integration is cited without acknowledging Catch wind-down. This weakens credibility on ecosystem execution claims. Address what changed in the operating model.",
            ),
            (
                "Slide 8",
                "[PRECEDENT] 12-14x precedent multiple range looks inflated versus the key local anchor (Greencross/TPG 2019 ~10x). If using international comps, label comparability limits clearly.",
            ),
            (
                "Slide 9",
                "[PRECEDENT] Vet clinic-in-Bunnings pilot ignores Homebase precedent and the A$1.96bn loss lesson. Add explicit guardrails and stop-loss criteria before expansion.",
            ),
        ),
        speaker_focus=(
            "Pressure-test every claim against source data and cross-slide consistency.",
            "Translate each contradiction into decision risk and remediation owner.",
            "Require precedent context before accepting valuation assumptions.",
            "Hold approval until tone, numbers, and logic are internally coherent.",
        ),
    ),
    "style_police": ModeContent(
        key="style_police",
        label="Style Police",
        persona="Strict reviewer for precedent, formatting discipline, and standards compliance.",
        style="Rules-based editing, consistency enforcement, and precedent hygiene.",
        issues_register_summary=(
            "Prioritise language standard, numeric reconciliation, sequence discipline, "
            "and explicit precedent annotation."
        ),
        drive_comments=(
            (
                "Slide 1",
                "[TONE] Replace 'Game-Changing', 'transformative', and 'disrupt'. House style requires understated language and avoids superlatives.",
            ),
            (
                "Slide 2",
                "[TONE] Remove 'incredible opportunity', 'explosive revenue growth', and 'massive strategic opportunity'. Rewrite with neutral commercial wording.",
            ),
            (
                "Slide 12",
                "[TONE] Standardise to 'satisfactory returns'. 'Outstanding returns' is not aligned to Wesfarmers precedent language.",
            ),
            (
                "Slides 2 and 12",
                "[NUMBERS] Standardise Flybuys member count to one value. Current mismatch is 10.2m vs 9.9m; set FY25 value to 9.9m and update all linked statements.",
            ),
            (
                "Slide 3",
                "[NUMBERS] Resolve same-slide conflict: subtitle says >70%, stat card says 69%. Keep one figure and cite source date in footnote.",
            ),
            (
                "Slide 5",
                "[NUMBERS] Add a reconciliation line for the 3.4m gap between EBITDA-Capex and FCF. Current table is arithmetically incomplete.",
            ),
            (
                "Slides 7 and 12",
                "[NUMBERS] Synergy band inconsistent (A$94-126m vs A$95-130m). Choose one official range and mirror exactly across summary and valuation pages.",
            ),
            (
                "Slide 6",
                "[LOGIC] Reframe comparator statement: 67% Bunnings customer pet ownership is below national 69%, so it cannot be presented as outperformance.",
            ),
            (
                "Slides 4 and 6",
                "[LOGIC] 42% recurring revenue claim does not match chart composition (26% + 10% = 36%). Align taxonomy and chart labels before publication.",
            ),
            (
                "Slides 8 and 9",
                "[STRUCTURE] Reorder deck so Growth Roadmap precedes Valuation. Standard M&A arc is thesis first, then pricing.",
            ),
            (
                "Location footprint section",
                "[CONSISTENCY] Provide clinic-by-state split for 38 vet clinics. Current state table only reconciles 142 stores.",
            ),
            (
                "Flybuys target section",
                "[CONSISTENCY] 3.5m target requires justification against implied ~6.8m pet-owner base. Add ramp assumptions or adjust target wording.",
            ),
            (
                "Slide 6",
                "[PRECEDENT] Add a short note on Catch wind-down when citing OnePass integration. Omitting that history creates precedent bias.",
            ),
            (
                "Slide 8",
                "[PRECEDENT] Flag local anchor multiple (Greencross/TPG ~10x) and classify 12-14x comps as international/adjusted to avoid misleading like-for-like interpretation.",
            ),
            (
                "Slide 9",
                "[PRECEDENT] Include Homebase lesson and risk controls before proposing vet clinic-in-Bunnings pilot scale-up.",
            ),
        ),
        speaker_focus=(
            "Enforce understated language and house-preferred terminology.",
            "Reconcile every repeated metric across all slides and appendices.",
            "Correct narrative order to strategy and growth before valuation.",
            "Annotate precedent quality and comparability on every comp claim.",
        ),
    ),
    "ceo_friendly": ModeContent(
        key="ceo_friendly",
        label="CEO-friendly",
        persona="Executive narrative reviewer focused on fast, credible decisions.",
        style="Clear storyline, high signal, and action-oriented framing.",
        issues_register_summary=(
            "Prioritise a credible executive narrative: sober language, one truth for numbers, "
            "sound logic, and sequencing that earns the valuation ask."
        ),
        drive_comments=(
            (
                "Slide 1",
                "[TONE] Dial down headline language. 'Game-Changing/transformative/disrupt' reads promotional; use the Wesfarmers norm of disciplined, understated return language.",
            ),
            (
                "Slide 2",
                "[TONE] Executive summary is too hyped ('incredible', 'explosive', 'massive'). Replace with fact-led statements so leadership can trust the baseline.",
            ),
            (
                "Slide 12",
                "[TONE] Close with 'satisfactory returns', not 'outstanding returns'. Tone consistency matters as much as the numbers in senior forums.",
            ),
            (
                "Slides 2 and 12",
                "[NUMBERS] Flybuys base conflicts (10.2m vs 9.9m). Set one number (9.9m FY25) and rebuild all derived claims to avoid credibility leakage.",
            ),
            (
                "Slide 3",
                "[NUMBERS] The deck says both >70% and 69% pet ownership on one page. This is a trust break for executives; fix and footnote.",
            ),
            (
                "Slide 5",
                "[NUMBERS] FCF does not bridge to EBITDA-Capex. Add a simple waterfall with the missing ~3.4m so finance can sign off quickly.",
            ),
            (
                "Slides 7 and 12",
                "[NUMBERS] Two synergy ranges are shown. Decision forums need one official range with explicit upside/downside assumptions.",
            ),
            (
                "Slide 6",
                "[LOGIC] 67% pet-owner mix at Bunnings is below the 69% national context, so this is not evidence of relative strength. Reframe as headroom opportunity.",
            ),
            (
                "Slides 4 and 6",
                "[LOGIC] Recurring revenue story is unclear: 42% claim vs 36% shown in chart components. Clarify definition or adjust the narrative.",
            ),
            (
                "Slides 8 and 9",
                "[STRUCTURE] Move valuation after Growth Roadmap. Leaders should see why this wins before what it costs.",
            ),
            (
                "Location footprint section",
                "[CONSISTENCY] 180 total locations are claimed, but only 142 are geographically allocated. Add clinic distribution to complete the operating picture.",
            ),
            (
                "Flybuys target section",
                "[CONSISTENCY] 3.5m target looks conservative against ~6.8m implied addressable pet members. Explain strategic pacing or reset the ambition statement.",
            ),
            (
                "Slide 6",
                "[PRECEDENT] OnePass narrative needs the Catch wind-down context; otherwise the integration claim appears selective.",
            ),
            (
                "Slide 8",
                "[PRECEDENT] Multiple assumptions look aggressive versus local precedent (~10x Greencross/TPG). Flag this clearly before asking for a valuation stance.",
            ),
            (
                "Slide 9",
                "[PRECEDENT] Vet clinic-in-Bunnings pilot should explicitly reference Homebase lessons and define expansion gates.",
            ),
        ),
        speaker_focus=(
            "Make the story trustworthy first: sober tone and reconciled core numbers.",
            "Explain each logic gap in terms of decision impact and fix owner.",
            "Sequence the narrative so confidence precedes valuation ask.",
            "State precedent caveats plainly before recommending commitment.",
        ),
    ),
}


def normalize_mode(value: str) -> str:
    """Normalize user-provided mode text to internal keys."""

    cleaned = value.strip().lower().replace("-", "_").replace(" ", "_")
    aliases = {
        "ic_hard": "ic_hard_mode",
        "ic": "ic_hard_mode",
        "style": "style_police",
        "style_mode": "style_police",
        "ceo": "ceo_friendly",
        "ceo_mode": "ceo_friendly",
    }
    return aliases.get(cleaned, cleaned)


def get_mode_or_raise(mode: str) -> ModeContent:
    normalized = normalize_mode(mode)
    if normalized not in REVIEW_MODES:
        raise ValueError(
            "Unknown review mode. Expected one of: "
            + ", ".join(sorted(REVIEW_MODES))
        )
    return REVIEW_MODES[normalized]


def load_style_guide_rules() -> tuple[str, ...]:
    """Load style guide bullets from markdown, with safe fallback defaults."""

    if not STYLE_GUIDE_FILE.exists():
        return DEFAULT_STYLE_GUIDE_RULES

    rules: list[str] = []
    for line in STYLE_GUIDE_FILE.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if stripped.startswith("- "):
            rules.append(stripped[2:].strip())

    return tuple(rules) if rules else DEFAULT_STYLE_GUIDE_RULES


def load_slide_ai_comments(slide_number: int) -> tuple[str, ...]:
    """Return explicit AI comments for a specific deck slide, if configured."""

    return SLIDE_AI_COMMENTS.get(slide_number, ())
