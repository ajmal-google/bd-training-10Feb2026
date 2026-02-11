# Wesfarmers BD Demo Agent (Google ADK + Google Slides/Drive)

This repo contains a very simple but realistic demo agent for the Wesfarmers Business Development team.

The agent can:
1. Show review modes:
   - `IC Hard Mode` (skeptical, pressure-tests assumptions)
   - `Style Police` (strict precedent + formatting discipline)
   - `CEO-friendly` (tone + narrative clarity)
2. Add predetermined Drive comments to a Google Slides deck based on selected mode.
3. Insert an **Issues Register** slide at the start of the deck.
4. Write verbose, per-slide speaker notes aligned to the style guide.

## 1) Prerequisites

- Python 3.11+
- [`uv`](https://docs.astral.sh/uv/)
- A Google Cloud project with APIs enabled:
  - Google Slides API
  - Google Drive API
- Credentials for both:
  - Recommended: Service account JSON key
  - Alternative: Application Default Credentials (ADC)

## 2) Setup (uv)

From `/Users/ajmal/Projects/bd_demo/wesfarmers-slide-reviewer`:

```bash
uv sync
cp .env.example .env
```

Then update `.env` with:
- `GOOGLE_API_KEY` (for ADK/Gemini model)
- `GOOGLE_SERVICE_ACCOUNT_JSON` (absolute path to service account key)

If using a service account, share the target Google Slides deck with the service account email as `Editor`.

## 3) Quick smoke tests

List modes:

```bash
uv run wesfarmers-slide-reviewer modes
```

Run workflow directly (no chat):

```bash
uv run wesfarmers-slide-reviewer run \
  --presentation-id "YOUR_PRESENTATION_ID" \
  --review-mode "ic_hard_mode"
```

`presentation_id` is the string between `/d/` and `/edit` in the deck URL.

## 4) Run with ADK (chat demo)

### ADK web UI

```bash
uv run adk web
```

Open the URL shown by ADK and choose agent: `wesfarmers_slide_reviewer`.

### ADK terminal mode

```bash
uv run adk run wesfarmers_slide_reviewer
```

Suggested demo prompts:
- `Show me the available review modes for this deck review.`
- `Use review_mode=ic_hard_mode presentation_id=YOUR_PRESENTATION_ID and run the review.`
- `Now rerun with review_mode=ceo_friendly on the same presentation.`

## 5) What the workflow changes in the deck

- Inserts (or updates) a first slide:
  - `Issues Register | <mode>`
- Adds a mode-specific set of Drive comments against the presentation file.
- Rewrites speaker notes for each existing slide with:
  - mode-specific feedback lens
  - style guide checks
  - recommended talk track

## 6) Project structure

- `/Users/ajmal/Projects/bd_demo/wesfarmers-slide-reviewer/wesfarmers_slide_reviewer/agent.py`: ADK `root_agent`
- `/Users/ajmal/Projects/bd_demo/wesfarmers-slide-reviewer/wesfarmers_slide_reviewer/tools.py`: ADK tool functions
- `/Users/ajmal/Projects/bd_demo/wesfarmers-slide-reviewer/wesfarmers_slide_reviewer/review_workflow.py`: Google API workflow logic
- `/Users/ajmal/Projects/bd_demo/wesfarmers-slide-reviewer/wesfarmers_slide_reviewer/demo_content.py`: predefined comments and review-mode behavior
- `/Users/ajmal/Projects/bd_demo/wesfarmers-slide-reviewer/wesfarmers_slide_reviewer/wesfarmers_style_guide.md`: style guide benchmark text

## 7) Troubleshooting

- `No Google credentials found`:
  - Set `GOOGLE_SERVICE_ACCOUNT_JSON`, or
  - Run ADC login:

```bash
gcloud auth application-default login \
  --scopes=https://www.googleapis.com/auth/presentations,https://www.googleapis.com/auth/drive
```

- `403 insufficient permissions`:
  - Ensure Slides + Drive APIs are enabled.
  - Ensure the deck is shared with credential identity.
  - Ensure credentials include both `presentations` and `drive` scopes.
