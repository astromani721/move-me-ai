# move-me-ai
> **A Multi-Agent Orchestration Framework for Autonomous Relocation Planning.**

`move-me-ai` is an advanced AI system built to solve the "messy," high-stakes problem of relocating. Instead of a simple chatbot, this project uses a **Hierarchical Multi-Agent Architecture** to coordinate specialized "Worker" agents. By leveraging Hugging Face's `smolagents` and **CodeAgents**, the system doesn't just talk—it writes and executes Python code to find homes, evaluate school districts, calculate insurance risks, and map out local lifestyle amenities in a single autonomous pass.

## 📌 Current Status

The repository includes a working **CLI and orchestration scaffold**:

* Typed Pydantic models for cross-agent data contracts
* A manager entrypoint that orchestrates specialist modules
* Housing search CLI with zip, bedrooms, bathrooms, and max-rent filters
* Structured JSON logging
* 24 tests covering housing filters, CLI args, and render output

`smolagents` `CodeAgent` orchestration and live provider integrations are planned next.

---

## 🏗 System Architecture

The project follows the **Manager-Worker (Orchestrator)** pattern, ensuring strict separation of concerns and modularity.

* **The Orchestrator (Manager Agent):** A `CodeAgent` that acts as the "Engineering Lead." It receives high-level requirements, generates execution plans, handles data handoffs between specialists, and synthesizes the final report.
* **The Housing Expert:** Specialized in real-time real estate data retrieval and market analysis.
* **The School Liaison:** Evaluates education metrics, ratings, and school district boundaries.
* **The Insurance Specialist:** Analyzes risk factors and provides estimated quotes for auto and renter's insurance.
* **The Lifestyle Scout:** Maps out neighborhood "livability," focusing on groceries (Indian/Asian specialists), parks, and libraries.

---

## 🚀 Key Features

* **Autonomous Logic:** Uses `CodeAgents` that write their own Python loops to process multiple property listings simultaneously.
* **Stateful Orchestration:** Ensures that the specific address found by the Housing agent is correctly passed to the Insurance, School, and Lifestyle specialists.
* **Resource Efficiency:** Uses `ManagedAgent` memory isolation to prevent context window bloat during long-running research tasks.
* **Extensible Tooling:** Custom Python-based tools for Zillow, Google Places, and GreatSchools API integrations.

---

## 📂 Repository Structure

```text
move-me-ai/
├── src/                    # Sources root
│   ├── manager.py          # The CodeAgent orchestrator (The "Brain")
│   ├── models.py           # Pydantic schemas for cross-agent data consistency
│   ├── cli.py              # Command-line interface (argparse + rich)
│   ├── logging_config.py   # Structured JSON logging
│   ├── agents/             # Child agent definitions (Specialists)
│   │   ├── housing.py      # Property search logic
│   │   ├── school.py       # Education & district analysis
│   │   ├── insurance.py    # Risk & premium estimation
│   │   └── lifestyle.py    # Grocery, park, & library scouting
│   └── tools/              # Custom @tool definitions (API wrappers)
│       └── providers.py
├── tests/                  # Test suite (24 tests)
├── .env.example            # Environment variable template
├── requirements.txt        # Runtime dependencies
├── requirements-dev.txt    # Dev tools (lint, typecheck, test)
├── pyproject.toml          # Build, ruff, mypy, and pytest configuration
└── Makefile                # Common developer commands
```

---

## 🛠 Getting Started

### Prerequisites
* **Python 3.10+**
* **Hugging Face API Token** (Read/Write access required)
* **API Keys** (Optional for full functionality: Google Places, Zillow/RentCast, or GreatSchools)

### Installation

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/your-username/move-me-ai.git](https://github.com/your-username/move-me-ai.git)
    cd move-me-ai
    ```

2.  **Set up a virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use: venv\Scripts\activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -e . -r requirements.txt
    ```

4.  **Configure environment variables:**
    ```bash
    cp .env.example .env
    ```
    Then edit `.env` with the tokens/keys you plan to use.

### Developer Workflow

For local development (linting, formatting, type checks, and tests):

```bash
make install-dev
```

Common commands:

```bash
make help
make lint
make fix
make format
make typecheck
make test
make check
```

### Running a Housing Search

```bash
make search                                  # defaults: zip=10583, 3BR, 1BA
make search ZIP=10583 BED=3 BATH=2
make search ZIP=10583 BED=3 RENT=5000 LIMIT=3
```

Or directly:

```bash
PYTHONPATH=src python -m cli --zip 10583 --bedrooms 3 --bathrooms 2 --max-rent 5500
```

## 🗺 Roadmap

* Integrate `smolagents` manager + managed child agents
* Replace provider stubs with real API-backed tools (housing, schools, insurance, places)
* Add integration tests for multi-agent orchestration and external tool behavior

---

## 📊 Sample Output: Relocation Dossier

Once the **Relocation Manager** completes its autonomous research loop, it synthesizes the findings into a structured report. Below is a representation of the output generated for a search in **Scarsdale, NY (10583)**:

### **Relocation Summary: Scarsdale, NY**
> **Request:** 3-bedroom rentals, top-tier schools, auto/renter's insurance estimates, and proximity to Indian/Asian groceries.

| Feature | Option 1: Weaver St. | Option 2: Post Rd. | Option 3: Mamaroneck Rd. |
| :--- | :--- | :--- | :--- |
| **Monthly Rent** | $5,200 | $4,800 | $6,000 |
| **School Assigned** | Scarsdale High School | Edgemont Junior-Senior | Heathcote School |
| **School Rating** | 10/10 | 9/10 | 10/10 |
| **Insurance (Est.)** | $215/mo (Combined) | $195/mo (Combined) | $240/mo (Combined) |
| **Nearest Grocery** | 1.1 mi (Patel Brothers) | 0.8 mi (H-Mart) | 1.5 mi (Trader Joe's) |
| **Green Space** | 0.3 mi (Boulder Brook) | 0.6 mi (Chase Park) | 0.2 mi (Saxon Woods) |
| **Commute (NYC)** | 32 mins (Metro-North) | 35 mins (Metro-North) | 38 mins (Metro-North) |

### **Agent Reasoning Log (Internal Logic)**
* **Housing Expert:** Identified 3 verified listings on Zillow within the requested budget.
* **School Liaison:** Cross-referenced addresses with the Scarsdale Union Free School District map; verified current Niche ratings.

---

## 💡 Why `smolagents`?

Traditional agent frameworks often rely on complex JSON parsing (the ReAct pattern), which can be brittle and prone to "hallucinations" when the LLM fails to follow a strict schema. `move-me-ai` utilizes Hugging Face's **`smolagents`** because it introduces a paradigm shift: **The Agent Thinks in Code.**

### **The "Code-First" Advantage**

* **Zero Logic Brittleness:** By allowing the LLM to write its own Python snippets, we bypass the need for a "middle-man" parser. If the agent needs to loop through 5 houses, it writes a native `for` loop rather than hoping a JSON blob is formatted correctly.
* **Deterministic Reasoning:** Mathematical calculations (like calculating total monthly relocation costs) and data filtering are performed by the Python interpreter, not the LLM's "guesswork."
* **Minimalist & Lightweight:** With a core codebase of ~1,000 lines, `smolagents` provides a transparent abstraction layer that is easy to debug and extend—ideal for high-reliability engineering projects.
* **Secure Sandboxing:** All generated code is executed in a secure environment (or via E2B integration), ensuring that the agent's autonomy does not compromise the host system.

### **Orchestration vs. Chat**

Unlike a standard chatbot that might "forget" an address halfway through a conversation, the **`CodeAgent`** maintains a strict execution state. In `move-me-ai`, this means:
1.  **Stateful Handoffs:** The Manager ensures the specific address from the *Housing Expert* is passed as a typed variable to the *School* and *Insurance* specialists.
2.  **Parallel Execution:** The library enables the manager to treat child agents as callable functions, allowing for complex, nested workflows that mimic human decision-making.
