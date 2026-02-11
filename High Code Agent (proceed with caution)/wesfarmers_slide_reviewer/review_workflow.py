"""Core workflow that mutates a Google Slides deck for demo review output."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any
from uuid import uuid4

from googleapiclient.errors import HttpError

from .demo_content import (
    STYLE_GUIDE_FILE,
    ModeContent,
    get_mode_or_raise,
    load_slide_ai_comments,
    load_style_guide_rules,
)
from .google_clients import (
    build_drive_service,
    build_slides_service,
    load_credentials,
)

WESFARMERS_RED = {"red": 0.8, "green": 0.0, "blue": 0.15}
WESFARMERS_CHARCOAL = {"red": 0.14, "green": 0.16, "blue": 0.19}
WESFARMERS_MUTED = {"red": 0.34, "green": 0.37, "blue": 0.41}


def _new_object_id(prefix: str) -> str:
    return f"{prefix}_{uuid4().hex[:10]}"


def _truncate(value: str, limit: int = 220) -> str:
    if len(value) <= limit:
        return value
    return value[: limit - 3].rstrip() + "..."


def _extract_issue_category_and_text(comment: str) -> tuple[str, str]:
    stripped = comment.strip()
    if stripped.startswith("[") and "]" in stripped:
        end_idx = stripped.find("]")
        category = stripped[1:end_idx].strip() or "ISSUE"
        message = stripped[end_idx + 1 :].strip()
        return category, message
    return "ISSUE", stripped


def _issues_register_rows(mode: ModeContent, max_rows: int = 8) -> list[tuple[str, str, str, str]]:
    rows: list[tuple[str, str, str, str]] = []
    for idx, (slide_ref, comment) in enumerate(mode.drive_comments[:max_rows], start=1):
        category, text = _extract_issue_category_and_text(comment)
        rows.append(
            (
                str(idx),
                slide_ref,
                _truncate(f"[{category}] {text}", 125),
                "BD lead | Open",
            )
        )
    return rows


def _issues_register_content_requests(
    slide_id: str,
    mode: ModeContent,
) -> list[dict[str, Any]]:
    generated = datetime.now(timezone.utc).strftime("%d %b %Y %H:%M UTC")
    rows = _issues_register_rows(mode)
    row_count = len(rows) + 1

    top_bar_id = _new_object_id("issues_top_bar")
    title_id = _new_object_id("issues_title")
    subtitle_id = _new_object_id("issues_subtitle")
    meta_id = _new_object_id("issues_meta")
    table_id = _new_object_id("issues_table")
    footer_id = _new_object_id("issues_footer")

    requests: list[dict[str, Any]] = [
        {
            "createShape": {
                "objectId": top_bar_id,
                "shapeType": "RECTANGLE",
                "elementProperties": {
                    "pageObjectId": slide_id,
                    "size": {
                        "height": {"magnitude": 54, "unit": "PT"},
                        "width": {"magnitude": 720, "unit": "PT"},
                    },
                    "transform": {
                        "scaleX": 1,
                        "scaleY": 1,
                        "translateX": 0,
                        "translateY": 0,
                        "unit": "PT",
                    },
                },
            }
        },
        {
            "updateShapeProperties": {
                "objectId": top_bar_id,
                "shapeProperties": {
                    "shapeBackgroundFill": {
                        "solidFill": {
                            "color": {"rgbColor": WESFARMERS_RED},
                            "alpha": 1,
                        }
                    },
                    "outline": {"propertyState": "NOT_RENDERED"},
                },
                "fields": (
                    "shapeBackgroundFill.solidFill.color,"
                    "shapeBackgroundFill.solidFill.alpha,"
                    "outline.propertyState"
                ),
            }
        },
        {
            "createShape": {
                "objectId": title_id,
                "shapeType": "TEXT_BOX",
                "elementProperties": {
                    "pageObjectId": slide_id,
                    "size": {
                        "height": {"magnitude": 30, "unit": "PT"},
                        "width": {"magnitude": 640, "unit": "PT"},
                    },
                    "transform": {
                        "scaleX": 1,
                        "scaleY": 1,
                        "translateX": 24,
                        "translateY": 12,
                        "unit": "PT",
                    },
                },
            }
        },
        {
            "insertText": {
                "objectId": title_id,
                "insertionIndex": 0,
                "text": "Wesfarmers Issues Register",
            }
        },
        {
            "updateTextStyle": {
                "objectId": title_id,
                "textRange": {"type": "ALL"},
                "style": {
                    "bold": True,
                    "fontSize": {"magnitude": 20, "unit": "PT"},
                    "foregroundColor": {"opaqueColor": {"rgbColor": {"red": 1, "green": 1, "blue": 1}}},
                },
                "fields": "bold,fontSize,foregroundColor",
            }
        },
        {
            "createShape": {
                "objectId": subtitle_id,
                "shapeType": "TEXT_BOX",
                "elementProperties": {
                    "pageObjectId": slide_id,
                    "size": {
                        "height": {"magnitude": 20, "unit": "PT"},
                        "width": {"magnitude": 672, "unit": "PT"},
                    },
                    "transform": {
                        "scaleX": 1,
                        "scaleY": 1,
                        "translateX": 24,
                        "translateY": 62,
                        "unit": "PT",
                    },
                },
            }
        },
        {
            "insertText": {
                "objectId": subtitle_id,
                "insertionIndex": 0,
                "text": f"Focus: {mode.issues_register_summary}",
            }
        },
        {
            "updateTextStyle": {
                "objectId": subtitle_id,
                "textRange": {"type": "ALL"},
                "style": {
                    "bold": True,
                    "fontSize": {"magnitude": 11, "unit": "PT"},
                    "foregroundColor": {"opaqueColor": {"rgbColor": WESFARMERS_CHARCOAL}},
                },
                "fields": "bold,fontSize,foregroundColor",
            }
        },
        {
            "createShape": {
                "objectId": meta_id,
                "shapeType": "TEXT_BOX",
                "elementProperties": {
                    "pageObjectId": slide_id,
                    "size": {
                        "height": {"magnitude": 16, "unit": "PT"},
                        "width": {"magnitude": 672, "unit": "PT"},
                    },
                    "transform": {
                        "scaleX": 1,
                        "scaleY": 1,
                        "translateX": 24,
                        "translateY": 80,
                        "unit": "PT",
                    },
                },
            }
        },
        {
            "insertText": {
                "objectId": meta_id,
                "insertionIndex": 0,
                "text": (
                    f"Generated: {generated} | Showing {len(rows)} of {len(mode.drive_comments)} issues | "
                    "Source: ADK demo comments"
                ),
            }
        },
        {
            "updateTextStyle": {
                "objectId": meta_id,
                "textRange": {"type": "ALL"},
                "style": {
                    "fontSize": {"magnitude": 9, "unit": "PT"},
                    "foregroundColor": {"opaqueColor": {"rgbColor": WESFARMERS_MUTED}},
                },
                "fields": "fontSize,foregroundColor",
            }
        },
        {
            "createTable": {
                "objectId": table_id,
                "rows": row_count,
                "columns": 4,
                "elementProperties": {
                    "pageObjectId": slide_id,
                    "size": {
                        "height": {"magnitude": 242, "unit": "PT"},
                        "width": {"magnitude": 700, "unit": "PT"},
                    },
                    "transform": {
                        "scaleX": 1,
                        "scaleY": 1,
                        "translateX": 10,
                        "translateY": 104,
                        "unit": "PT",
                    },
                },
            }
        },
        {
            "updateTableColumnProperties": {
                "objectId": table_id,
                "columnIndices": [0],
                "tableColumnProperties": {
                    "columnWidth": {"magnitude": 32, "unit": "PT"},
                },
                "fields": "columnWidth",
            }
        },
        {
            "updateTableColumnProperties": {
                "objectId": table_id,
                "columnIndices": [1],
                "tableColumnProperties": {
                    "columnWidth": {"magnitude": 82, "unit": "PT"},
                },
                "fields": "columnWidth",
            }
        },
        {
            "updateTableColumnProperties": {
                "objectId": table_id,
                "columnIndices": [2],
                "tableColumnProperties": {
                    "columnWidth": {"magnitude": 470, "unit": "PT"},
                },
                "fields": "columnWidth",
            }
        },
        {
            "updateTableColumnProperties": {
                "objectId": table_id,
                "columnIndices": [3],
                "tableColumnProperties": {
                    "columnWidth": {"magnitude": 116, "unit": "PT"},
                },
                "fields": "columnWidth",
            }
        },
    ]

    headers = ("#", "Slide", "Issue Register Entry", "Owner / Status")
    for col, header in enumerate(headers):
        requests.extend(
            [
                {
                    "insertText": {
                        "objectId": table_id,
                        "cellLocation": {"rowIndex": 0, "columnIndex": col},
                        "insertionIndex": 0,
                        "text": header,
                    }
                },
                {
                    "updateTextStyle": {
                        "objectId": table_id,
                        "cellLocation": {"rowIndex": 0, "columnIndex": col},
                        "textRange": {"type": "ALL"},
                        "style": {
                            "bold": True,
                            "fontSize": {"magnitude": 9, "unit": "PT"},
                            "foregroundColor": {"opaqueColor": {"rgbColor": WESFARMERS_RED}},
                        },
                        "fields": "bold,fontSize,foregroundColor",
                    }
                },
            ]
        )

    for row_index, row in enumerate(rows, start=1):
        for col_index, value in enumerate(row):
            requests.append(
                {
                    "insertText": {
                        "objectId": table_id,
                        "cellLocation": {"rowIndex": row_index, "columnIndex": col_index},
                        "insertionIndex": 0,
                        "text": value,
                    }
                }
            )
            requests.append(
                {
                    "updateTextStyle": {
                        "objectId": table_id,
                        "cellLocation": {"rowIndex": row_index, "columnIndex": col_index},
                        "textRange": {"type": "ALL"},
                        "style": {
                            "fontSize": {"magnitude": 8, "unit": "PT"},
                            "foregroundColor": {"opaqueColor": {"rgbColor": WESFARMERS_CHARCOAL}},
                        },
                        "fields": "fontSize,foregroundColor",
                    }
                }
            )

    requests.extend(
        [
            {
                "createShape": {
                    "objectId": footer_id,
                    "shapeType": "TEXT_BOX",
                    "elementProperties": {
                        "pageObjectId": slide_id,
                        "size": {
                            "height": {"magnitude": 22, "unit": "PT"},
                            "width": {"magnitude": 672, "unit": "PT"},
                        },
                        "transform": {
                            "scaleX": 1,
                            "scaleY": 1,
                            "translateX": 24,
                            "translateY": 356,
                            "unit": "PT",
                        },
                    },
                }
            },
            {
                "insertText": {
                    "objectId": footer_id,
                    "insertionIndex": 0,
                    "text": "Status cadence: Open -> In progress -> Ready for re-review | Owner recommendation: BD workstream lead",
                }
            },
            {
                "updateTextStyle": {
                    "objectId": footer_id,
                    "textRange": {"type": "ALL"},
                    "style": {
                        "fontSize": {"magnitude": 9, "unit": "PT"},
                        "foregroundColor": {"opaqueColor": {"rgbColor": WESFARMERS_MUTED}},
                    },
                    "fields": "fontSize,foregroundColor",
                }
            },
        ]
    )

    return requests


def _extract_text_from_shape(shape: dict[str, Any]) -> str:
    text_content = shape.get("text", {}).get("textElements", [])
    chunks: list[str] = []
    for element in text_content:
        run = element.get("textRun")
        if run and run.get("content"):
            chunks.append(run["content"])
    return "".join(chunks).strip()


def _slide_title(slide: dict[str, Any], fallback: str) -> str:
    for page_element in slide.get("pageElements", []):
        shape = page_element.get("shape")
        if not shape:
            continue
        placeholder = shape.get("placeholder", {})
        if placeholder.get("type") in {"TITLE", "CENTERED_TITLE"}:
            title = _extract_text_from_shape(shape)
            if title:
                return title

    for page_element in slide.get("pageElements", []):
        shape = page_element.get("shape")
        if not shape:
            continue
        text = _extract_text_from_shape(shape)
        if text:
            return text.splitlines()[0].strip()

    return fallback


def _has_text_in_page_elements(
    page_elements: list[dict[str, Any]],
    object_id: str,
) -> bool:
    for page_element in page_elements:
        if page_element.get("objectId") != object_id:
            continue
        shape = page_element.get("shape")
        if not shape:
            return False
        return bool(_extract_text_from_shape(shape))
    return False


def _speaker_note_text(
    mode: ModeContent,
    content_slide_number: int,
    absolute_slide_number: int,
    slide_title: str,
    style_guide_rules: tuple[str, ...],
) -> str:
    slide_ref, mode_comment = mode.drive_comments[
        (content_slide_number - 1) % len(mode.drive_comments)
    ]
    ai_comment_lines = load_slide_ai_comments(content_slide_number)
    style_checks = "\n".join(f"- {rule}" for rule in style_guide_rules)
    mode_focus = "\n".join(f"- {line}" for line in mode.speaker_focus)
    ai_comment_block = (
        "\n".join(f"- {line}" for line in ai_comment_lines)
        if ai_comment_lines
        else "- No explicit AI comment provided for this slide number."
    )

    return (
        f"Slide under review: Slide {content_slide_number} - {slide_title}\n"
        f"Deck position (including Issues Register if present): {absolute_slide_number}\n\n"
        "AI Comment (requested deck guidance):\n"
        f"{ai_comment_block}\n\n"
        "Per-slide feedback summary:\n"
        f"- Benchmark reference: {slide_ref}\n"
        f"- Priority concern: {mode_comment}\n"
        "- Practical edit: tighten the headline so it states one clear decision implication.\n"
        "- Presenter cue: explain evidence quality first, then recommendation confidence.\n\n"
        "Review lens to apply while presenting:\n"
        f"{mode_focus}\n\n"
        "Wesfarmers style guide checks:\n"
        f"{style_checks}\n\n"
        "Suggested talk track (demo narrative):\n"
        "1) Open with the decision statement in one sentence.\n"
        "2) Confirm evidence basis and key assumptions.\n"
        "3) State commercial implication and risk owner.\n"
        "4) Close with ask, owner, and due date for follow-up.\n"
    )


def _insert_issues_register_slide(
    slides_service: Any,
    presentation_id: str,
    mode: ModeContent,
) -> dict[str, str]:
    slide_id = _new_object_id("issues_register")
    requests = [{"createSlide": {"objectId": slide_id, "insertionIndex": 0}}]
    requests.extend(_issues_register_content_requests(slide_id=slide_id, mode=mode))

    slides_service.presentations().batchUpdate(
        presentationId=presentation_id,
        body={"requests": requests},
    ).execute()

    return {
        "slide_id": slide_id,
        "action": "created",
    }


def _add_drive_comments(
    drive_service: Any,
    presentation_id: str,
    mode: ModeContent,
) -> list[dict[str, str]]:
    created: list[dict[str, str]] = []

    for slide_ref, content in mode.drive_comments:
        response = (
            drive_service.comments()
            .create(
                fileId=presentation_id,
                fields="id,content,createdTime",
                body={
                    "content": f"{slide_ref}: {content}",
                },
            )
            .execute()
        )

        created.append(
            {
                "comment_id": response.get("id", "unknown"),
                "slide_ref": slide_ref,
                "content": response.get("content", ""),
                "created_time": response.get("createdTime", ""),
            }
        )

    return created


def _update_speaker_notes(
    slides_service: Any,
    presentation_id: str,
    mode: ModeContent,
    issues_slide_id: str,
) -> list[dict[str, str]]:
    deck = slides_service.presentations().get(presentationId=presentation_id).execute()
    style_guide_rules = load_style_guide_rules()
    requests: list[dict[str, Any]] = []
    updated_slides: list[dict[str, str]] = []
    content_slide_number = 0

    for absolute_slide_number, slide in enumerate(deck.get("slides", []), start=1):
        if slide.get("objectId") == issues_slide_id:
            continue

        content_slide_number += 1
        notes_page = slide.get("slideProperties", {}).get("notesPage", {})
        notes_page_elements = notes_page.get("pageElements", [])
        notes_object_id = (
            notes_page
            .get("notesProperties", {})
            .get("speakerNotesObjectId")
        )
        if not notes_object_id:
            continue

        title = _slide_title(slide, fallback=f"Untitled slide {content_slide_number}")
        text = _speaker_note_text(
            mode,
            content_slide_number=content_slide_number,
            absolute_slide_number=absolute_slide_number,
            slide_title=title,
            style_guide_rules=style_guide_rules,
        )

        if _has_text_in_page_elements(notes_page_elements, notes_object_id):
            requests.append(
                {
                    "deleteText": {
                        "objectId": notes_object_id,
                        "textRange": {"type": "ALL"},
                    }
                }
            )
        requests.append(
            {
                "insertText": {
                    "objectId": notes_object_id,
                    "insertionIndex": 0,
                    "text": text,
                }
            }
        )

        updated_slides.append(
            {
                "slide_object_id": slide.get("objectId", "unknown"),
                "slide_number": str(content_slide_number),
                "slide_title": title,
            }
        )

    if requests:
        slides_service.presentations().batchUpdate(
            presentationId=presentation_id,
            body={"requests": requests},
        ).execute()

    return updated_slides


def run_review_workflow(
    presentation_id: str,
    review_mode: str,
    reviewer_name: str = "Wesfarmers BD Demo Agent",
) -> dict[str, Any]:
    """Execute the full demo workflow against a Google Slides presentation."""

    mode = get_mode_or_raise(review_mode)
    credentials = load_credentials()
    slides_service = build_slides_service(credentials)
    drive_service = build_drive_service(credentials)

    try:
        presentation = (
            slides_service.presentations()
            .get(presentationId=presentation_id)
            .execute()
        )
        deck_title = presentation.get("title", "Untitled presentation")

        issues_slide = _insert_issues_register_slide(
            slides_service=slides_service,
            presentation_id=presentation_id,
            mode=mode,
        )

        created_comments = _add_drive_comments(
            drive_service=drive_service,
            presentation_id=presentation_id,
            mode=mode,
        )

        updated_notes = _update_speaker_notes(
            slides_service=slides_service,
            presentation_id=presentation_id,
            mode=mode,
            issues_slide_id=issues_slide["slide_id"],
        )

    except HttpError as exc:
        message = getattr(exc, "_get_reason", lambda: str(exc))()
        raise RuntimeError(f"Google API request failed: {message}") from exc

    return {
        "status": "ok",
        "presentation_id": presentation_id,
        "presentation_title": deck_title,
        "review_mode": mode.key,
        "review_mode_label": mode.label,
        "reviewer_name": reviewer_name,
        "issues_register_slide_id": issues_slide["slide_id"],
        "issues_register_action": issues_slide["action"],
        "drive_comments_created": len(created_comments),
        "speaker_notes_updated": len(updated_notes),
        "created_comment_sample": created_comments[:3],
        "updated_slides_sample": updated_notes[:5],
        "style_guide_file": str(STYLE_GUIDE_FILE),
        "next_step": (
            "Open the deck and validate comments, the first slide Issues Register, and speaker notes. "
            "Then ask the agent to rerun in a different mode for comparison."
        ),
    }
