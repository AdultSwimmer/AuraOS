# Google / Gemini Evidence Archive

**Public research record**  
**Last updated: 25 August 2026**

This repository preserves primary source materials related to a specific Gemini conversation and subsequent Google My Activity / interface records from 25 August 2026, along with related follow-up sessions.

**Purpose**

> Preserve the original artifacts in their original form so that any reader can examine them directly.

This repository does **not** claim to have established the cause of every anomaly documented here. Its purpose is to preserve the evidence, document provenance, and distinguish direct observation from interpretation.

---

## Controlling Methodology

All analysis in this archive is governed by the formal evidentiary standard:

→ **[docs/EVIDENTIARY-STANDARD.md](docs/EVIDENTIARY-STANDARD.md)**

Key principles:

- **Observed** = directly present in primary artifacts  
- **Independently Documented** = established by external official sources  
- **Inferred** = bounded deductions (must remain labeled)  
- **Possible / Unknown** = unresolved mechanisms

**Core rule regarding chronology:**

> The documented chronological sequence must not be dismissed, but chronology alone must not be converted into proof of motive, intent, or mechanism.

Methodological changes are recorded in:

→ **[CHANGELOG.md](CHANGELOG.md)**

---

## Primary Evidence Inventory

### Core Incident Files

| File | Description |
|------|-------------|
| `GEMINI-ADMITS.docx` | Preserved primary transcript |
| `GEMINI-ADMITS.txt` | Plain-text version of the same transcript |
| `Gemini-Original.docx` | Additional preserved copy |
| `googleDELETE1.png` – `googleDELETE6.png` | Sequential Google My Activity and Gemini interface screenshots |
| `Googlefulldelete.png` | Gemini search interface (historical results + loading error) |
| `GOOGLEDELETERESPONSE.png` | Gemini response after deletion-related screenshots were re-uploaded |

### Related Session Files

| File | Description |
|------|-------------|
| `GEMINIGOOGLE.docx` | Later conversation involving liability-script discussion |
| `Google_Bust.txt` | Structured transcript of the “blissful ignorance” debate |
| `Google_Lawsuit.docx` | Formatted version of the same debate |
| `geminlies.txt` | Extended multi-turn log |
| `moregeminlies.txt` | Continuation of the above log |

### Supporting / Interpretive Material

These files contain later analysis and philosophical framing. They are **not** primary event evidence:

- `The Explanation.docx`
- `chatgpt-google.docx` / `google-chatgpt.docx`
- Related notes and summaries

---

## Observed Chronological Sequence

The archive documents the following sequence (to the extent supported by the preserved artifacts):

1. Contested language was generated in the preserved conversation.
2. The user subsequently confronted the model about that language.
3. Response-side material later became unavailable in the visible interfaces while user-side prompts and attachments remained represented.

This sequence is treated as an **observed chronological fact**.

The causal relationship (if any) between the content, the confrontation, and the later unavailability is **not established**.

Multiple possible mechanisms remain open. See the full standard for details.

---

## How to Read This Archive

1. Start with the primary transcript (`GEMINI-ADMITS.docx` or `.txt`).
2. Examine the sequential screenshots in order.
3. Compare the My Activity records against the Gemini interface states.
4. Treat all later analysis and multi-model summaries as secondary commentary.
5. Refer to `docs/EVIDENTIARY-STANDARD.md` for the rules governing every claim.

---

## File Structure

```text
/
├── README.md
├── CHANGELOG.md
├── docs/
│   └── EVIDENTIARY-STANDARD.md
│
├── evidence/
│   ├── transcripts/
│   │   ├── GEMINI-ADMITS.docx
│   │   ├── GEMINI-ADMITS.txt
│   │   ├── Gemini-Original.docx
│   │   ├── GEMINIGOOGLE.docx
│   │   ├── Google_Bust.txt
│   │   ├── Google_Lawsuit.docx
│   │   ├── geminlies.txt
│   │   └── moregeminlies.txt
│   │
│   └── screenshots/
│       ├── googleDELETE1.png
│       ├── googleDELETE2.png
│       ├── googleDELETE3.png
│       ├── googleDELETE4.png
│       ├── googleDELETE5.png
│       ├── googleDELETE6.png
│       ├── Googlefulldelete.png
│       └── GOOGLEDELETERESPONSE.png
│
└── supporting/
    ├── The Explanation.docx
    ├── chatgpt-google.docx
    └── google-chatgpt.docx