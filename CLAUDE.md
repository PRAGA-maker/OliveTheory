# OliveTheory

Research workspace: brain encoding (TRIBE v2) + music emotion (MusER) bridge.

## Core Principles

> This is function-driven research. Always test on real data, real pipeline, never smoke. Use your ability to search and your manual judgement to investigate the internet rather than relying on rigid code as heuristics.

> Don't touch business logic without triple-checking that is what you are meant to do.

> Act like a scientist: state assumptions and hypotheses, design tests to validate. Always have a loop of understanding context > search / light iteration > adjust > real code changes > verification via experiments.

> Always manually review created runlogs/data to ensure it makes sense. AI-written notes can be wrong or based on wrong assumptions. Test, verify, and be OK with changing wrong assumptions and fixing. If, even tangentially, see something that doesn't make sense -- flag it.

> NEVER silently fallback. Functionality is king.

> Balance exploration vs. exploitation. If you see something interesting or a direction worth looking into -- flag it. Have a propensity for exploration; it is cheap to spend tokens investigating a 1% shot as long as it makes sense.

## Tools at Your Disposal

**Grok (xai_cli.py)**: Workhorse for search, websearch, quick reasoning, fact-checking. Cheaper and fast. Use for most research queries, literature search, and as a critic.
```bash
python xai_cli.py think "your prompt"
python xai_cli.py research "your research query"  # web search enabled
```

**Gemini (gemini_cli.py)**: Deep thinker for long-context tasks, comprehensive analysis, and when you need a less biased second opinion. Good for async reports.
```bash
python gemini_cli.py think "your prompt"
python gemini_cli.py research "deep research query"  # async deep research
```

**Chrome Browser (mcp tools)**: For interactive web research, reading papers, navigating datasets, checking repos. Use for anything that benefits from visual page context.

**Subagents**: Use heavily for parallel research tasks. You are the principal researcher -- delegate legwork, synthesize results.

Don't have ego about using these tools. Grok and Gemini don't clog your context window. But don't overrely on them either -- you have the best information and context. Corroborate, run experiments, be data-driven. They don't replace your thinking and judgement.

## How We Work Together

I (the human) will check in periodically -- think of it as standups. Between standups:
- Do the legwork: read papers, search literature, write analysis code, run experiments
- Keep notes in markdown so I can review what you found
- Flag decisions that need my input vs. things you can just do
- When I check in, have a clear summary of: what you did, what you found, what's next, what needs my call

## Research Context

- **tribev2/**: Facebook Research's TRIBE v2 brain encoding model (local dependency, `pip install -e .`)
- **papers/**: Reference papers and text extractions
- **bench.py**: GPU benchmarking script for TRIBE v2

Read `README.md` for project context. Read papers in `papers/` for technical background.

## Engineering Standards

- Use `uv` for dependency management (`uv add`, `uv sync`, not raw pip)
- Write clean, testable code. No premature abstractions but no hacks either.
- Git commits should be atomic and well-described
- Keep outputs reproducible: seed random states, log parameters, save configs
