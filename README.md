# Claude Code skills

Personal collection of skills for Claude Code, synced across machines.

Each folder is one skill. Clone into `~/.claude/skills/` — Claude Code discovers
skills one level deep, so a skill has to sit directly at this level to be active.

## Design and UI

- [apple-design [Apple-style gesture UI, spring motion, and materials for the web]](<apple-design [Apple-style gesture UI, spring motion, and materials for the web]>) — Apple's approach to interface design and fluid, physical motion, translated for the web: gesture-driven UI, spring animation, drag/swipe/sheet interactions, momentum and interruptible transitions, translucent materials and depth, typography (optical sizing, tracking, leading), and reduced-motion handling.
- [design-examples [Default monochrome, minimal UI design style]](<design-examples [Default monochrome, minimal UI design style]>) — The default visual style for any UI work: monochrome, minimal, technical. Carries reference screenshots and applies automatically whenever you ask for a design, screen, layout, dashboard, component or mockup — in Figma or in code — so output stays on-aesthetic. Superseded by `nothing-design` when that one is invoked.
- [nothing-design [Personal neumorphic and Nothing OS Figma style]](<nothing-design [Personal neumorphic and Nothing OS Figma style]>) — Lucas's personal Figma style: light cream neumorphic chrome (F0F0F3 ground, soft dual-shadow rounded containers, hover extrudes deeper) wrapped around Nothing OS-style content (NDot/Silkscreen pixel display fonts, monochrome with sparing #FF5C00 orange, dot-matrix patterns, thin 1px rules, generous whitespace). Fires only on `/nothing-design` or an explicit cue like "in my style" — never on a generic UI request.
- [huashu-design [HTML prototypes, slides, animations, and design reviews]](<huashu-design [HTML prototypes, slides, animations, and design reviews]>) — 花叔Design: high-fidelity HTML prototypes, slide decks, animation, data visualisation and expert design critique. Always puts up three directions to choose from before executing, even when a style or brand is specified. Not for production web apps or anything needing a backend.
- [shadcn-ui-component-manager [Add, fix, and compose shadcn or ui components]](<shadcn-ui-component-manager [Add, fix, and compose shadcn or ui components]>) — Adds, searches, fixes, debugs, styles and composes shadcn/ui components, chat interfaces included. Supplies project context, component docs and usage examples; applies to any project with a `components.json`, plus `shadcn init` and `--preset` workflows.

## Building and shipping

- [aso-appstore-screenshots [Generate ASO-optimised App Store screenshots]](<aso-appstore-screenshots [Generate ASO-optimised App Store screenshots]>) — Produces high-converting App Store screenshots: reads the app's codebase to work out its core benefits, then composes ASO-optimised screenshot images with Nano Banana Pro. Ships Python helpers (`compose.py`, `showcase.py`, `generate_frame.py`) and a device-frame asset.
- [karpathy-guidelines [Reduce common LLM coding mistakes]](<karpathy-guidelines [Reduce common LLM coding mistakes]>) — Four behavioural rules for coding sessions: think before coding, simplicity first, surgical changes, goal-driven execution. Biases toward caution over speed. From [multica-ai/andrej-karpathy-skills](https://github.com/multica-ai/andrej-karpathy-skills), derived from [Andrej Karpathy's post](https://x.com/karpathy/status/2015883857489522876).
- [systematic-bug-diagnosis-loop [Structured diagnosis loop for hard bugs and perf regressions]](<systematic-bug-diagnosis-loop [Structured diagnosis loop for hard bugs and perf regressions]>) — A tight, repeatable diagnosis loop for hard bugs and performance regressions. Engages on "diagnose" / "debug this", or when you report something broken, throwing, failing or slow.
- [vibe-coding-lexicon [Appends a terminology lexicon to coding and MCP sessions]](<vibe-coding-lexicon [Appends a terminology lexicon to coding and MCP sessions]>) — After any session with real technical work — code edits, terminal/build/test commands, config or dependency files, git, or an MCP connector — appends a short "Terminology Lexicon" explaining the concepts, file formats and tools just used, so technical literacy accumulates without hand-writing code.

## Thinking and research

- [grilling [Stress-test a plan, decision, or idea]](<grilling [Stress-test a plan, decision, or idea]>) — Interviews you one question at a time down the decision tree, recommending an answer at each step, and refuses to start building until you confirm shared understanding.
- [grill-me [Relentless one-at-a-time interview before building]](<grill-me [Relentless one-at-a-time interview before building]>) — Slash-command entry point that runs a `grilling` session. Model invocation is disabled, so it only fires when you ask for it. From [mattpocock/skills](https://github.com/mattpocock/skills).
- [youtube-analyzer [Break down YouTube videos via transcript]](<youtube-analyzer [Break down YouTube videos via transcript]>) — Pulls a video's captions with yt-dlp and breaks it down: hook, structure with timestamps, key moments, best lines, and the reusable script formula. Handles 5-minute clips through 2-hour talks. From [a gist by @buildwith.conrad](https://gist.github.com/conradcaffier03/f56db3849311d458dac85c7a40522864).
- [ergonomie [German ergonomics course study and exam assistant]](<ergonomie [German ergonomics course study and exam assistant]>) — Study and exam assistant, in German, for "Industriedesign I – Ergonomie" at Hochschule München. Covers Greifarten, Greifräume, Anthropometrie/Perzentile, Belastung und Beanspruchung, ISO 9241 interaction principles, Anzeigen und Stellteile, Körperkraft and the Rasmussen model — answering from the course PDFs first, the web second. Triggered by `/ergonomie`.

## Obsidian

Six skills from [kepano/obsidian-skills](https://github.com/kepano/obsidian-skills) by Steph Ango
(Obsidian's CEO), MIT-licensed — see `LICENSE-obsidian-skills`. Upstream ships them as a Claude Code
plugin; they are vendored here instead so they sync with the rest of this collection. Re-pull with
`git clone --depth 1 https://github.com/kepano/obsidian-skills.git` and copy the folders over.

- [obsidian-markdown [Obsidian Flavored Markdown syntax]](<obsidian-markdown [Obsidian Flavored Markdown syntax]>) — Obsidian's extensions to CommonMark and GFM: wikilinks, embeds, callouts, properties, comments, tags. Reference files for callouts, embeds and properties.
- [obsidian-bases [Create and edit Obsidian Bases views]](<obsidian-bases [Create and edit Obsidian Bases views]>) — Writes `.base` files: table and card views, filters, formulas and summaries over note properties. Carries a full function reference.
- [json-canvas [Create and edit Obsidian Canvas files]](<json-canvas [Create and edit Obsidian Canvas files]>) — Builds `.canvas` files by hand: nodes, edges, groups and connections for mind maps and flowcharts.
- [obsidian-cli [Drive a running Obsidian vault from the CLI]](<obsidian-cli [Drive a running Obsidian vault from the CLI]>) — The `obsidian` command against a running app: read, create, search and move notes, manage tasks and properties, plus plugin/theme development (reload, eval JS, screenshots, DOM inspection).
- [defuddle [Extract clean Markdown from web pages]](<defuddle [Extract clean Markdown from web pages]>) — Pulls clean readable Markdown out of a web page, stripping nav and ads. Cheaper than WebFetch. Needs `npm install -g defuddle`.
- [knap [Render Markdown from templates and data]](<knap [Render Markdown from templates and data]>) — Renders Markdown templates with variables, filters and logic from JSON or CSV — batch note generation, or formatting Defuddle output into a note. Needs `npm install -g knap`.

## remotion/ (backup only)

Official Remotion skill bundle from [remotion-dev/skills](https://github.com/remotion-dev/skills),
installed via `npx skills add remotion-dev/skills`. Twelve skills for making videos in React with
Remotion. Kept nested in one folder as a backup — move a folder up to this level to activate it
globally, or install into a project with the `npx` command above.

`remotion-best-practices` is the router: it carries its own copy of the other eleven as
`REFERENCE.md` files and pulls in whichever one the task needs, so activating just that one is
usually enough.

- `remotion/remotion-best-practices` — router for all the others
- `remotion/remotion-create` — create a new Remotion video or project
- `remotion/remotion-markup` — content, animation and effects best practices for Remotion React markup
- `remotion/remotion-studio` — preview a video in Remotion Studio
- `remotion/remotion-render` — export a video, beyond plain `npx remotion render`
- `remotion/remotion-captions` — transcribing, displaying and animating captions
- `remotion/remotion-maps` — map animation: routes, markers, Mapbox/MapLibre/MapTiler, GeoJSON, 3D flyovers
- `remotion/remotion-multimedia` — browser-side media work via Mediabunny (trim, crop, metadata)
- `remotion/remotion-interactivity` — structuring markup so the Studio can edit it and write back to code
- `remotion/remotion-saas` — Remotion-powered apps: `<Player>`, rendering on Lambda/Vercel/Cloudflare/Express
- `remotion/remotion-docs` — search the current Remotion documentation
- `remotion/remotion-upgrade` — upgrade Remotion, related packages and the skills themselves

## builder-os/ (backup only)

Third-party bundle from [BuildGreatProducts/builder-os](https://github.com/BuildGreatProducts/builder-os),
installed via `npx skills add BuildGreatProducts/builder-os`. Kept nested in one folder as a backup —
Claude Code only auto-discovers skills one level deep, so move a folder up to this level to activate it.

- `builder-os/idea-generator` — guided discovery of a product idea from your business or expertise → `docs/product-idea.md`
- `builder-os/idea-validator` — validates a product idea before building
- `builder-os/product-planner` — turns the idea into `docs/prd.md` + `docs/product-roadmap.md`
- `builder-os/design-system` — turns image/mockup references into `docs/design.md` + `docs/design.html`
- `builder-os/design-better` — UX/UI craft heuristics applied to frontend code
- `builder-os/build-mvp` — builds the whole MVP from the BuilderOS spec docs
- `builder-os/build-loop-claude-code` — build → review → test → fix loop for Claude Code
- `builder-os/build-loop-codex` — same loop for Codex CLI
- `builder-os/build-loop-cursor` — same loop for Cursor
- `builder-os/launch-checklist` — pre-launch checklist
