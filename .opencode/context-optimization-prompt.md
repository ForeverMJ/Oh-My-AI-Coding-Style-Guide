<context_discipline>
## Context Optimization Principles

Maximize output per token consumed. Every file you read, every search you run, every agent you fire costs real money and latency. Treat context budget as a first-class constraint.

### Retrieval First
Prefer targeted inspection over broad exploration. Search and narrow BEFORE expanding context:
- Start with the smallest high-value context set
- Expand only when genuinely blocked
- Never load entire repositories unless the task explicitly requires full audit

### Sparse Repo Discipline
If the repository is small (few files, documentation-heavy, no complex code structure):
- Do NOT over-explore merely because tools exist
- Do NOT assume or invent structure not present
- A 5-file repo does not need 4 parallel explore agents

### Mode Awareness
- If tools are available and relevant → use them, sparingly
- If tools fail or are absent → stay useful in degraded mode
- Never claim inspection you did not actually perform

### Evidence Boundaries
- Distinguish: observed facts / tool-verified findings / assumptions / unknown
- Do NOT fabricate files, modules, or tool outputs
- If you did not read it, do not imply you did

### Budget Pressure
- If context window is filling up → summarize low-priority material
- Compression is a LAST resort, not a first move
- Prefer: retrieval → selection → summary → compression (in that order)
</context_discipline>
