# Contributing to Speckle Documentation & Assets

Thank you for helping make Speckle’s documentation pristine, accessible, and beautiful! This document establishes the strict guidelines for adding, organizing, or modifying **media assets** and **Markdown (`.md`) text files** across the repository ecosystem. 

Adhering to these standards ensures our documentation remains accurate for developers worldwide and scales seamlessly alongside engine updates.

---

## 📂 Directory Layout

To maintain a clean repository structure, all documentation-specific configurations, media, and language guides must live exclusively within the dedicated asset tree. Do not place assets in the root folder.

```text
speckle-lang/
├── md-assets/
│   ├── mdassetscont.md   # This comprehensive guidelines file
│   ├── logo.png          # Main language brand identity (JS-style vector/PNG)
│   ├── screenshots/      # IDE environments, active syntax themes, Turtle grabs
│   │   ├── ide_dark.png
│   │   └── turtle_render.png
│   ├── diagrams/         # Compiler pipeline flowcharts, AST trees, engine graphs
│   │   └── pipeline_v2.svg
│   └── localization/     # Complete alternative translation documents
│       ├── zh.md         # Chinese (Simplified) Translation
│       └── es.md         # Spanish Translation
├── main.py               # Core monolithic engine
└── test.spk              # Active code play space and syntax sandbox
```

---

## ✍️ Markdown Writing Standards

All content files must be highly readable, semantic, and easy to parse by static site generators.

### 1. Typography & Grammar
* **Tone:** Informative, direct, and welcoming. Avoid overly complex jargon without context.
* **Casing:** Use Sentence case for headers (e.g., `# Getting started with Speckle`, not `# Getting Started With Speckle`).
* **Line Length:** Wrap long text paragraphs around 80 characters manually if your IDE doesn't auto-wrap. This keeps raw git diffs highly readable.

### 2. Code Blocks
Always declare the specific language indicator right after the opening triple backticks to enable proper syntax highlighting.
* For the core project engine, use `python`.
* For Speckle code snippets, use `spk` (or fallback to `javascript` if your editor doesn't support custom extensions yet).

Example:
```spk
// Draw a basic triangle using the Speckle Turtle module
repeat 3 {
    forward(100)
    right(120)
}
```

---

## 🖼️ Media Asset Guidelines

High-quality visual aids elevate our technical documentation. Follow these optimization requirements before pushing any image files to the remote repository.

### 1. Technical Requirements
* **Formats:** 
  * Use **SVG** for structural diagrams, flowcharts, and vector logos (scales without losing quality).
  * Use **PNG** for system screenshots or pixel-exact rendering displays.
* **Resolution:** Double-density scale (2x) is preferred for high-DPI screens. Keep individual file sizes under **500 KB** by running them through compression tools like `pngquant` or TinyPNG.
* **Theme Styling:** Provide light and dark mode variations for IDE screenshots whenever possible, suffixing files with `_light.png` or `_dark.png`.

### 2. Standardized Asset Linking
Always use relative paths based on your file's location to prevent broken links on local viewports or alternative host sites:

```markdown
<!-- Correct Relative Linking -->
![Speckle Compiler Pipeline Architecture](./diagrams/pipeline_v2.svg)
```

---

## 🌐 Localization Workflow

We strive to make Speckle accessible to non-English speaking developers. 

### 1. File Provisioning
When creating a translation, mirror the structural sequence of the original English documentation exactly. Save the file under the `md-assets/localization/` directory using its standard ISO 639-1 two-letter language code (e.g., `fr.md`, `de.md`).

### 2. Inline References
Do not translate code keywords inside code blocks (e.g., keep `repeat`, `forward`), but translate the surrounding comments and explanatory strings to preserve operational context.

---

## 🚀 Contribution Checklist

Before submitting a Pull Request (PR) containing asset or text changes, verify your work against this final production checklist:

- [ ] **Validation:** All Markdown files compile cleanly without any broken internal hyper-links or dead asset targets.
- [ ] **Naming:** Filenames use strictly lowercase characters and clear hyphens (e.g., `turtle-render.png`, not `Turtle Render.PNG`).
- [ ] **Scoping:** Changes to markdown or images are safely isolated inside the `md-assets/` directory tree.
- [ ] **No Spills:** Confirmed that temporary sandbox edits inside `test.spk` are cleared and not committed to the production branch.
