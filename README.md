# 🌌 Speckle Programming Language

[![Version](https://img.shields.io/badge/version-1.5.0b--beta-pink?style=plastic)](https://github.com/n1nerlang/speckle-lang)
[![License](https://img.shields.io/badge/license-MIT-blue?style=plastic)](./LICENSE)
[![Organization](https://img.shields.io/badge/Org-n1nerlang-89b4fa?style=plastic)](https://github.com/n1nerlang)

A fast, lightweight, and visual language framework built for structural matrix parsing, geometric rendering, and byte-level text obfuscation processing routines. Developed natively by **Speckle LLC** under the **n1nerlang** organization umbrella.

---

## 📖 Table of Contents
1. [Core Architecture Overview](#-core-architecture-overview)
2. [Version 1.5.0b Changelog](#%EF%B8%8F-version-150b-changelog)
3. [Language API Reference](#-language-api-reference)
4. [Installation & Operational Usage](#-installation--operational-usage)
5. [Complete Verification Script](#-complete-verification-script)

---

## 🔬 Core Architecture Overview

Speckle operates via a strict linear compilation stack compiled entirely from scratch, optimizing standard AST transformations without relying on heavy external dependencies.

> 💡 **System Design Note:** Speckle treats statements as independent execution streams. Variables are bound to a global dynamic memory environment table during runtime, allowing loops and geometric functions to access mutable state instantaneously.

### The Compilation Pipeline
```text
  [ Source Code (.spk) ]
            │
            ▼
     [ Lexer Engine ]  ───────► Token Stream (Identifiers, Strings, Numbers)
            │
            ▼
    [ Parser Engine ]  ───────► Abstract Syntax Tree (AST Nodes)
            │
            ▼
 [ Interpreter Runtime ] ─────► Environment Execution Memory Space
```

---

## 🛠️ Version 1.5.0b Changelog

| Feature Matrix | Status | Execution Tier | Description |
| :--- | :---: | :---: | :--- |
| **`ascii_textify()`** | `RELEASED` | Byte Decoder | Reconstructs plain-text strings from backslash decimal arrays. |
| **`jumble_string()`** | `RELEASED` | Obfuscator Core | Converts regular strings into secure, raw decimal sequences. |
| **`inject_junk()`** | `RELEASED` | Metamorphic Engine | Spams dead calculations to disrupt external parsers. |
| **Interactive REPL** | `RELEASED` | System Prompt | Allows users to test code directly line-by-line without saving a file. |
| **Turtle Matrix** | `STABLE` | Graphics Vector | Maximum rendering speed acceleration for geometric workspaces. |

---

## ⚡ Language API Reference

### 1. Cryptographic & Core Byte Utilities
* `ascii_textify(string)`: Takes an obfuscated array of character decimal numbers separated by backslashes and converts them back to plain-text string formatting variables.
* `jumble_string(string)`: Reverses text strings into numeric backslash arrays.
* `inject_junk(integer)`: Injects a stream of completely random dead operational functions to mask clean code behavior.

### 2. Mathematics Vector Engine
* `add(x, y)`, `sub(x, y)`, `mul(x, y)`, `div(x, y)`: Standalone mathematical calculation parameters.
* `sin(degrees)`, `cos(degrees)`: High-level trigonometric alignment functions.
* `random_int(low, high)`: Generates a completely randomized absolute integer between boundaries.

### 3. Native Canvas Vector Drawing
```lua
init_canvas()                       (( Configures dark visual matrix window ))
set_background_color("#0f0f17")     (( Modifies backdrop workspace canvas ))
set_line_color("#89b4fa")           (( Sets trajectory brush hex color ))
move_forward(100)                   (( Displaces cursor ahead linearly ))
turn_left(90)                       (( Aligns vector heading angle ))
```

---

## 🚀 Installation & Operational Usage

Ensure you have **Python 3.8+** installed locally in your environment. Clone the module structure and run the compiler entry point:

### Running the Live Interactive Shell (REPL)
To drop into the command prompt framework immediately for fast, zero-file execution verification, run the script with **no arguments**:
```bash
python main.py
```

### Executing an Extracted File Payload
To pass a complete compiled script containing multi-variable execution states, target the tracking extension:
```bash
python main.py test.spk
```

---

## 📝 Complete Verification Script

Save this production code array inside your local repository as **`test.spk`** to execute a full integration test checking all features added in version `1.5.0b`:

```lua
(( Speckle Complete Integration Framework Verification ))

(( Phase 1: Verify Header Banners ))
ascii_banner("SPECKLE ENGINE V1.5.0b")
ascii_brick(24, 2)

(( Phase 2: Decrypt Stream Strings Natively ))
scrambled_key = "110\101\111\98\101\51"
decrypted_handle = ascii_textify(scrambled_key)

print("Decrypted System Target Handle Identity:")
print(decrypted_handle)

(( Phase 3: Deploy Security Smokescreens ))
jumble_string("SecurePayloadString")
inject_junk(3)

(( Phase 4: Compute Matrix Orientations ))
target_angle = random_int(45, 135)
amplitude = sin(target_angle)
warn("Dynamic waveform projection initialized successfully.")

(( Phase 5: Initialize Visual Display Architecture ))
init_canvas()
set_background_color("#0b0b12")
set_line_color("#f38ba8")
move_forward(120)
turn_right(target_angle)
move_forward(80)
```

---

Built with 💻 by [lupsup39](https://tenringsofdoom1x.github.io) under the [n1nerlang](https://github.com/n1nerlang) organization for Speckle LLC. Licensed under the [MIT License](./LICENSE).
