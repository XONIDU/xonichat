---
title: 'XONICHAT: A Lightweight Terminal-Based Gemini Client for Low-Resource Environments'
tags:
  - Python
  - Gemini
  - terminal
  - CLI
  - API client
  - educational technology
  - low-resource computing
authors:
  - name: Darian Alberto Camacho Salas
    orcid: 0009-0002-5465-466X
    affiliation: 1
affiliations:
  - name: Universidad Nacional Autónoma de México, Facultad de Estudios Superiores Cuautitlán
    index: 1
date: 24 February 2026
bibliography: paper.bib

# Summary

XONICHAT is a terminal-based client for Google's Gemini API, specifically designed for low-resource computing environments such as legacy hardware and educational institutions with limited computational resources. The software provides a minimalist text interface with efficient resource usage, making large language model (LLM) assistants accessible on older equipment where modern web browsers cannot run efficiently.

# Statement of need

While LLMs have become increasingly accessible through web interfaces, a significant digital divide persists. Users with low-resource computers, educational institutions in developing regions, and enthusiasts using legacy hardware often cannot run modern web browsers or memory-intensive applications. This is particularly relevant in educational settings, where institutions may rely on older computer labs with limited specifications, such as the ASUS Eee PC with 512MB of RAM.

XONICHAT addresses this gap by providing a terminal-based client that:

- Runs efficiently on systems with very limited RAM.
- Supports multiple API keys with automatic failover when quotas are exhausted, allowing for extended free usage.
- Maintains conversation context for natural, multi-turn interactions.
- Requires minimal dependencies (only Python and the `requests` library), making it easy to install and audit.
- Operates completely in the terminal, eliminating browser and graphical interface overhead.

The software is particularly valuable for educational institutions extending the life of computer labs, researchers in resource-constrained settings, hobbyists using vintage or low-power hardware, and privacy-conscious users preferring terminal-based tools.

# Implementation

XONICHAT is implemented in pure Python with a minimalist design philosophy (~200 lines of code), as can be seen in the project's main file, `start.py` [@xonichat-repo]. Key technical features include:

- **Automatic key rotation**: Seamlessly switches between multiple API keys defined in a simple `keys.txt` file when rate limits are encountered.
- **Conversation history management**: Maintains context for coherent multi-turn dialogues with a configurable history limit (default 50 exchanges).
- **Readline integration**: Provides command history and line editing capabilities for an enhanced user experience.
- **Comprehensive error handling**: Gracefully manages network issues, API limitations (like quota exhaustion), and key file errors.
- **Cross-platform compatibility**: Works on Linux, Windows, and macOS thanks to its pure Python implementation.
- **Integrated test suite**: Includes a `start_test.py` file with unit tests to ensure core functionalities like key loading and rotation work correctly.

The codebase is intentionally minimal to facilitate auditing, modification, and educational use. Students and developers can easily understand the entire codebase and adapt it for their own projects or as a learning tool for API interaction and terminal application design.

# Acknowledgements

The author thanks the National Autonomous University of Mexico (UNAM) and the Faculty of Higher Studies Cuautitlán for their support. The development of this tool was inspired by the need to make AI more accessible in all learning environments.

# References
