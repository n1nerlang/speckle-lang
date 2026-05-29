# <img src="md-assets/logo.png" align="right" width="120" alt="Speckle Logo"/> Speckle (.spk)

> A clean, lightweight, visual programming language built for speed, simplicity, and geometric creation.

[![Language](https://img.shields.io/badge/Language-Speckle-89b4fa?style=for-the-badge)](https://github.com/n1nerlang/speckle-lang)
[![Core Engine](https://img.shields.io/badge/Engine-Python_3-f9e2af?style=for-the-badge&logo=python)](https://www.python.org)
[![Syntax Style](https://img.shields.io/badge/Syntax-Lua_Inspired-a6e3a1?style=for-the-badge&logo=lua)](https://www.lua.org)
[![License](https://img.shields.io/badge/License-MIT-f38ba8?style=for-the-badge)](LICENSE)

---

Speckle is an interpreted, expressions-first language designed to bridge mathematical computation with native turtle graphics rendering. Its syntax is heavily inspired by Lua—featuring elegant function calls and lightweight block structures—making it highly accessible for developers.

## 🌟 Key Features

* **Native Geometric Runtime:** Move objects, paint canvases, and render vectors natively using built-in engine commands.
* **Flexible Extensions:** Supports multiple recognized file formats: `.spk`, `.speckle`, `.sp`, and `.pk`.
* **Isolated Environments:** A sandbox-safe global execution context mimicking classic registry paradigms.
* **TextMate Native Syntax:** Custom token mappings ready for GitHub Linguist integration.

---

## 🏗️ Architecture Pipeline

The Speckle compilation pipeline steps through three key phases to take your code from plain text to raw execution output:

```text
  [ Raw Source Code ] (.spk / .sp / .pk)
           │
           ▼
   ┌───────────────┐
   │  1. Lexer     │ ──► Regular Expression Tokenizer
   └───────────────┘
           │
           ▼
   ┌───────────────┐
   │  2. Parser    │ ──► Top-Down Recursive Descent State Machine
   └───────────────┘
           │
           ▼
  [ Abstract Syntax Tree (AST) ] (Structural Data Object Branches)
           │
           ▼
   ┌───────────────┐
   │3. Interpreter │ ──► Dynamic Execution Sandbox & Runtime Loops
   └───────────────┘
           │
           ▼
  [ Screen Output / Visual Graphic Rendering Canvas ]
