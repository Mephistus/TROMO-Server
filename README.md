# TROMO-Server (Legacy Showcase)

A high-performance, multithreaded MMORPG backend architecture originally developed in **2010**. This repository serves as a technical showcase for the server-side logic of a fully functional online game.

> **Note:** This is a legacy project provided for code review and architectural demonstration. The client-side application is not included in this repository.

## 🏛 Project Context

Developed during a period of self-managed consultancy, this server powered a live MMORPG environment. It was designed to handle real-time player interactions, persistent world states, and concurrent game logic using a custom-built multithreaded architecture.

## 🛠 Technical Architecture & Concurrency

The core strength of this project lies in its handling of high-concurrency player connections within the Python environment:

* **Task-Based Threading (`taskThread.py`):** Implements a robust threading model to isolate network I/O from heavy game logic (combat, map transitions, and AI).
* **Modular Game Logic:** A clean separation of concerns was maintained across modules like `battle.py`, `monster.py`, and `skill.py` to allow for scalable content updates.
* **State Management:** Detailed handling of player persistence (`paccount.py`, `pcharacter.py`) and world state synchronization.
* **Legacy Performance:** Optimized for the hardware and Python versions of 2010, demonstrating efficient resource management and low-latency packet handling.

## 📂 Key Modules

* **`account_server.py`**: The main entry point for authentication and session management.
* **`map.py` & `fieldFunctions.py`**: Logic for spatial partitioning, grid management, and environmental triggers.
* **`battle.py`**: The combat engine, handling turn-based or real-time calculations and status effects.
* **`pcharacter.py`**: Data structures and methods for player attributes, leveling (`levelUp.py`), and inventories.

## 🚦 Heritage & Insights

This code represents a deep dive into:
* Designing networked systems before the ubiquity of modern async frameworks.
* Managing thread safety and the Python Global Interpreter Lock (GIL) in a gaming context.
* Architecting a scalable backend for an independent MMORPG.

---
**Developer:** [Cassio](https://github.com/Mephistus)  
*Senior Software Engineer & Game Designer*
