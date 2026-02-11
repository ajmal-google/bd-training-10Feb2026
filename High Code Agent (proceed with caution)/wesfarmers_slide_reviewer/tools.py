"""ADK tool functions exposed to the review agent."""

from __future__ import annotations

from typing import Any

from .demo_content import REVIEW_MODES, normalize_mode
from .review_workflow import run_review_workflow


def list_review_modes() -> dict[str, Any]:
    """Return available reviewer personas and how they behave."""

    modes = []
    for key, content in REVIEW_MODES.items():
        modes.append(
            {
                "review_mode": key,
                "label": content.label,
                "persona": content.persona,
                "review_style": content.style,
                "focus_areas": list(content.speaker_focus),
            }
        )

    return {
        "review_modes": modes,
        "selection_instruction": (
            "Reply with both `review_mode` and `presentation_id` to execute the review. "
            "Example: review_mode=ic_hard_mode presentation_id=1AbCdEf..."
        ),
    }


def review_presentation(
    presentation_id: str,
    review_mode: str,
    reviewer_name: str = "Wesfarmers BD Demo Agent",
) -> dict[str, Any]:
    """Run the demo review workflow over a Slides presentation."""

    normalized = normalize_mode(review_mode)
    try:
        return run_review_workflow(
            presentation_id=presentation_id,
            review_mode=normalized,
            reviewer_name=reviewer_name,
        )
    except Exception as exc:  # pragma: no cover - surfaced in ADK tool response.
        return {
            "status": "error",
            "presentation_id": presentation_id,
            "review_mode": normalized,
            "error_message": str(exc),
            "remediation": (
                "Check GOOGLE_SERVICE_ACCOUNT_JSON or ADC setup, confirm Slides/Drive API "
                "access, and ensure the deck is shared with the credential identity."
            ),
        }
