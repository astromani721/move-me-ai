# move-me-ai
> **A Multi-Agent Orchestration Framework for Autonomous Relocation Planning.**

`move-me-ai` is an advanced AI system built to solve the "messy," high-stakes problem of relocating. Instead of a simple chatbot, this project uses a **Hierarchical Multi-Agent Architecture** to coordinate specialized "Worker" agents. By leveraging Hugging Face's `smolagents` and **CodeAgents**, the system doesn't just talk—it writes and executes Python code to find homes, evaluate school districts, calculate insurance risks, and map out local lifestyle amenities in a single autonomous pass.



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
├── src/
│   ├── manager.py          # The CodeAgent orchestrator (The "Brain")
│   ├── agents/             # Child agent definitions (Specialists)
│   │   ├── housing.py      # Property search logic
│   │   ├── school.py       # Education & district analysis
│   │   ├── insurance.py    # Risk & premium estimation
│   │   └── lifestyle.py    # Grocery, park, & library scouting
│   ├── tools/              # Custom @tool definitions (API wrappers)
│   └── models.py           # Pydantic schemas for cross-agent data consistency
├── README.md               # Architecture & Project Documentation
└── requirements.txt        # Dependencies (smolagents, pydantic, etc.)
