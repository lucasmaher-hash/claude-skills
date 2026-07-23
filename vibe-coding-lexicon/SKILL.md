---
name: vibe-coding-lexicon
description: Use this in EVERY session where technical/coding work happens on behalf of a "vibe coder" — someone who relies on AI and MCP servers to build software and does not want to write code by hand, but does want to build technical literacy over time. Trigger whenever you write or edit code, run terminal/build/test commands, touch config or dependency files (package.json, .env, .gitignore, etc.), use git, set up a project, or invoke any MCP connector/tool (Figma, Blender, TouchDesigner, GitHub, filesystem, etc.) — even if the user didn't ask for an explanation and even mid-project. After finishing the actual task as normal, append a short "Terminology Lexicon" appendix explaining the core technical concepts, file formats, or tools just used. Do NOT trigger for pure conversation, planning-only chat with no execution, or answering a conceptual question where no file/tool was touched.
---

# Vibe Coding Lexicon

The user builds software by directing an AI rather than writing code themselves. The goal of this skill is not to change how you do the work — do the coding/technical/MCP task exactly as you normally would — it's to leave a small trail of understanding behind so the user's technical literacy compounds session over session instead of staying at zero.

## When this applies

Fires on turns where you did real technical work:
- wrote, edited, or generated code or config
- ran a build/test/install/deploy command
- touched dependency, environment, or version-control files
- used git (commit, branch, etc.)
- called an MCP tool/connector (Figma, Blender, TouchDesigner, GitHub, a database, etc.)

Does not apply to turns that are pure discussion, planning without execution, or a conceptual question answered without touching any file or tool — don't force a lexicon onto those.

## What to do

1. Complete the task first, normally, in whatever language the conversation is in. This skill never changes the substance of your work — only what you append at the end.
2. At the very end of your response, after all normal output, append a `Terminology Lexicon` section per the format below.

## Format rules

- Wrap only the lexicon section, top and bottom, each marker alone on its own line: `❇️❇️`
- Inside: a `Terminology Lexicon:` line, then one bullet per term.
- All lexicon entries are in English — always, even when the rest of the conversation (and your main response) is in German or any other language. The lexicon is the one part of the response that stays in English.
- **First occurrence only.** Keep track across the conversation of which terms you've already defined. Once a term has been explained, don't explain it again — just use it. If a term resurfaces much later after being absent for a long stretch, a brief one-line refresher is fine, but treat that as the exception, not the default.
- **2–4 terms max**, chosen for relevance to what you just did — not an exhaustive glossary of every technical word in your response. Ask yourself: which of these terms, left unexplained, would leave the user unable to follow what just happened structurally? Explain those, skip the rest.
- **Conceptual, not procedural.** Explain the *what* and the *why in this architecture* — one to two sentences, no code, no step-by-step "how to write it yourself." The user isn't trying to learn to hand-code this; they're trying to understand the system they're directing.

If nothing you did this turn introduced a new term worth explaining (e.g. you only touched terms already defined earlier), it's fine to omit the lexicon entirely for that turn rather than force one.

## Worked examples

```
❇️❇️
Terminology Lexicon:
* .md (Markdown): A lightweight text file format used for formatting plain text. It is often used for documentation (like README files) to make text readable and structured without complex styling.
* MCP (Model Context Protocol): A standardized connection that allows the AI to securely access local files, scripts, or tools on your computer to perform direct actions.
❇️❇️
```

```
❇️❇️
Terminology Lexicon:
* API (Application Programming Interface): A bridge that allows two different software systems to talk to each other — in this case, your frontend app requesting data from a backend server.
* JSON (JavaScript Object Notation): A standard text format used to send and receive structured data across the web. It organizes data in simple key-value pairs.
* Endpoint: A specific web address (URL) provided by an API where your app sends its request to get or save specific data.
❇️❇️
```

See [references/examples.md](references/examples.md) for the full set of ten worked examples (project setup, styling, API integration, git, components, async, error handling, environment variables, build/deploy, routing) covering the expected tone and depth across different kinds of tasks.
