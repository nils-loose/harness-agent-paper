# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is an academic research paper about multi-agent driven fuzz-harness generation for Java libraries. The paper is written in LaTeX using the ACM article format (sigconf) and describes a system that uses LLM-powered agents to automatically generate fuzzing harnesses for Java library APIs.

## Document Structure

The paper follows a modular structure:

- `main.tex` - Main document file with abstract, introduction, preliminaries, conclusion
- `sections/main-chapter.tex` - Core approach section describing the multi-agent architecture
- `sections/evaluation.tex` - Evaluation results and metrics
- `sections/related-work.tex` - Related work section
- `main.bib` - Bibliography in BibTeX format
- `figures/` - LaTeX figure files and Python scripts for generating diagrams
- `tables/` - LaTeX table files
- `data/` - Evaluation data including coverage metrics

## Building the Paper

### Compile PDF

The paper uses `pdflatex` with shell-escape enabled (required for SVG figures via Inkscape):

```bash
pdflatex -shell-escape -synctex=1 -interaction=nonstopmode main.tex
```

For a complete build with bibliography:

```bash
pdflatex -shell-escape main.tex
bibtex main
pdflatex -shell-escape main.tex
pdflatex -shell-escape main.tex
```

Or use latexmk for automated building:

```bash
latexmk -pdf -pdflatex="pdflatex -shell-escape" main.tex
```

### Clean Build Artifacts

```bash
rm -f main.aux main.bbl main.blg main.log main.out main.pdf main.synctex.gz main.fls main.fdb_latexmk
```

## Key Technical Components

### LaTeX Packages and Styling

- **Document class**: ACM sigconf format with `review` and `anonymous` options for submission
- **SVG support**: Uses `svg` package with Inkscape for rendering vector graphics
- **Code listings**: Custom YAML and Java syntax highlighting configured in preamble
- **Figure macros**: Custom text styles (`\axtext`, `\ticktext`) for consistent diagram formatting

### Code Listing Styles

Two custom listing styles are defined:

1. **YAML style** (lines 13-23): For configuration/tool schema examples with gray comments
2. **Java style** (lines 26-39): Standard Java highlighting with custom colors

### Architecture Concepts

The paper describes a multi-agent workflow with five specialized agents:

1. **Research Agent** - Explores API documentation and source code to understand target methods
2. **Generation Agent** - Synthesizes initial harness code from research findings
3. **Compilation Agent** - Iteratively fixes build errors
4. **Coverage Analysis Agent** - Interprets coverage gaps and decides on refinement strategy
5. **Refinement Agent** - Modifies harnesses to improve coverage

Key technical innovations:

- **Model Context Protocol (MCP)** - Query-based tool interface for on-demand information retrieval
- **Method-targeted coverage** - JaCoCo instrumentation scoped to target method execution only
- **Coverage-guided refinement** - Iterative improvement using static callgraph + dynamic coverage

## Working with Figures

### Figure Generation

Some figures are generated programmatically:

```bash
cd figures
python generate_research_sequence.py  # Generates sequence diagrams
```

### Figure Files

- `.tex` files - TikZ/PGFPlots figures embedded in the document
- `.svg` files - Vector graphics rendered via Inkscape during compilation
- `.pdf` files - Pre-rendered diagrams

## Bibliography Management

Citations use the ACM Reference Format style. When adding references:

1. Add BibTeX entry to `main.bib` following the existing DBLP format
2. Use the naming convention: `DBLP:venue/AuthorYY:ShortTitle`
3. Reference in text using `\cite{DBLP:...}`

Common citation categories in this paper:
- Harness generation tools (FuzzGen, OGHarn, Rubick, etc.)
- LLM-based approaches (OSS-Fuzz-Gen, PromptFuzz, etc.)
- Tool-augmented reasoning (ReAct, Toolformer)
- Fuzzing frameworks (Jazzer, AFL, libFuzzer)

## Evaluation Data

The `data/coverage/` directory contains coverage metrics for case studies:
- commons-cli, jackson, gson, jsoup, antlr4
- Metrics include token usage, cost, iteration counts, and tool calls per agent

## Common Editing Tasks

### Adding a new section

Sections are modular - create new `.tex` file in `sections/` and include via `\input{sections/filename.tex}`

### Adding a figure

1. Create figure file in `figures/` (TikZ `.tex` or `.svg`)
2. Reference in main text: `\input{figures/filename.tex}` or `\includesvg{filename}`
3. Use `\label{fig:name}` and reference with `\ref{fig:name}`

### Adding a table

1. Create table file in `tables/`
2. Include via `\input{tables/filename.tex}`
3. Follow existing format with `\label{tab:name}` for referencing

## Author Information

The author list (lines 68-131 in main.tex) uses placeholder names from the ACM template. These should be updated before final submission based on conference requirements for anonymity.

## Important Notes

- The `review` and `anonymous` options are enabled for blind review submission
- Shell-escape is required for SVG rendering via Inkscape
- Conference metadata (lines 44-52) needs updating with actual venue information
- Abstract is currently a TODO placeholder (line 136)
- Conclusion section is TODO (line 251)
