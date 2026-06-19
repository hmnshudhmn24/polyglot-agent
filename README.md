# Polyglot-Agent: MCP Sandbox & Code Generation

An autonomous multi-agent framework that profiles Python scripts, mathematically refactors the logic, and generates highly optimized native C++ using a secure local Model Context Protocol (MCP) server.

## 🚀 Project Overview

In computationally heavy domains, Python 3 is excellent for prototyping but frequently hits performance ceilings due to the GIL and dynamic typing overhead. Translating this logic into optimized native C++ is a tedious manual process.

**Polyglot-Agent** eliminates this friction. It acts as an algorithmic co-pilot that actively profiles original code, applies mathematical reductions (e.g., `O(N²)` to `O(1)`), and autonomously generates, compiles, and verifies performant C++ logic.

---

## 🏗️ Architecture

The system utilizes an agentic orchestration loop to manage state and prevent context drift during language translation.

```text
                       [ Input Python Script ]
                                  │
                       ┌──────────▼──────────┐
                       │  Supervisor Agent   │
                       └────┬───────────┬────┘
                            │           │
           ┌────────────────▼─┐       ┌─▼────────────────┐
           │  Profiler Agent  │       │  Refactor Agent  │
           └────────┬─────────┘       └────────┬─────────┘
      (Measures latency & outputs)    (Generates C++ via Skills)
                    │                          │
                    ▼                          ▼
    ┌────────────────────────────────────────────────────────┐
    │          Model Context Protocol (MCP) Server           │
    │   [ Secure Execution Sandbox & GCC Compiler Loop ]     │
    └────────────────────────────────────────────────────────┘
```

---

## 🛠️ Core Concepts Implemented

This project applies four core technical paradigms:

### Multi-Agent System (ADK)

Coordinated state-machine routing between the Supervisor, Profiler, and Refactor agents using strict data schemas.

### MCP Server

A custom local sandbox exposing:

* `run_profiler`
* `compile_cpp`
* `execute_test_harness`

This active feedback loop prevents the agent from guessing if code works; it must actively compile and parse real-time stderr outputs.

### Agent Skills

Specialized logical bounds defined in `.md` files:

* `math_reduction.md`
* `cpp_memory_safety.md`

These guide generation and prevent structural hallucinations.

### Security Features

Hard limits on:

* Memory usage
* I/O access
* Maximum execution time (2000ms)

This allows safe local execution of LLM-generated native code.

---

## 💻 Local Setup & Execution

### Prerequisites

* Python 3.10+
* GCC/G++ Compiler installed locally and available in system PATH (`g++`)

### Quick Start

Clone the repository:

```bash
git clone https://github.com/yourusername/polyglot-agent.git
cd polyglot-agent
```

Run the orchestrator:

```bash
python main.py
```

---

## ⚙️ Execution Flow

Upon running, the system will:

1. Automatically initialize a secure `./agent_sandbox` directory.
2. Profile the included target Python script to capture reference outputs.
3. Trigger the Refactor Agent to generate C++.
4. Invoke the local MCP server to compile the C++ via `g++`.
5. If compilation fails, stderr is routed back to the agent for autonomous correction.
6. Verify the compiled native binary perfectly matches the original Python output.

---

## 📁 Repository Structure

```text
polyglot-agent/
├── main.py                    # Orchestrator and custom MCP Sandbox implementation
├── requirements.txt           # Core Python dependencies
├── skills/                    # Agent capability isolation
│   ├── math_reduction.md      # Rules for Big-O optimization
│   └── cpp_memory_safety.md   # Strict modern C++20 formatting rules
└── agent_sandbox/             # (Auto-generated) Secure execution environment
```

---

## ⚠️ Security Warning

This framework is designed to execute autonomously generated code.

The local MCP server enforces a strict 2000ms timeout limit, but you should only run this tool inside a trusted environment or Docker container when passing highly unconstrained prompts.

---

## 🎯 Project Goals

* Automated Python profiling
* Mathematical complexity reduction
* Native C++20 code generation
* Autonomous compile-and-fix loops
* Output parity verification
* Secure local execution through MCP sandboxing

Polyglot-Agent demonstrates how modern agentic systems can combine profiling, optimization, code generation, validation, and secure execution into a single autonomous workflow.
