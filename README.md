
#  Factory Maintenance Knowledge Agent

An AI-powered knowledge assistant for factory maintenance teams that combines **OEM machine manuals** with **past maintenance experiences** to help technicians diagnose machine issues faster and make better-informed maintenance decisions.

## Problem

Factory technicians often face recurring machine problems, but the knowledge required to solve them is scattered across:

* OEM manuals and technical documents
* Previous maintenance records
* Senior technician experience
* Different machine-specific troubleshooting procedures

When an issue occurs, technicians may spend significant time searching through manuals or depending on experienced personnel.

This project aims to provide a centralized AI-powered assistant that can retrieve relevant technical information and recall previous solutions to similar problems.

---

##  Solution

The **Factory Maintenance Knowledge Agent** acts as a maintenance assistant.

A technician can provide a machine issue such as:

> "Machine M-102 is showing abnormal vibration and the motor temperature is increasing."

The agent analyzes the issue using:

1. **OEM Knowledge** – information from machine manuals and technical documentation.
2. **Historical Maintenance Knowledge** – previous problems, diagnoses, and solutions stored in long-term memory.
3. **AI Reasoning** – combines the retrieved information to provide relevant troubleshooting guidance.

The goal is to help technicians reach useful information quickly while keeping the recommendations grounded in available maintenance knowledge.

---

## 🔄 Workflow

```text
                Technician
                    │
                    ▼
            Describe Machine Issue
                    │
                    ▼
          ┌─────────────────────┐
          │  Factory Maintenance │
          │   Knowledge Agent    │
          └─────────────────────┘
                    │
          ┌─────────┴─────────┐
          ▼                   ▼
   OEM Machine Manuals    Past Maintenance
   & Technical Data          Knowledge
          │                   │
          └─────────┬─────────┘
                    ▼
             Knowledge Retrieval
                    │
                    ▼
               AI Reasoning
                    │
                    ▼
          Troubleshooting Guidance
                    │
                    ▼
               Technician
```

---

## Role of Hindsight

This project uses **Hindsight** as a long-term memory layer for the maintenance agent.

Instead of treating every technician query as a completely new problem, the system can store and retrieve knowledge from previous maintenance experiences.

For example:

```text
Previous Incident:
Machine → Compressor C-12
Problem → Excessive vibration
Cause → Bearing wear
Solution → Bearing replacement
Result → Vibration returned to normal
```

When a similar issue occurs later, the agent can retrieve this historical knowledge and use it along with the OEM manual information.

This allows the system to preserve **organizational maintenance knowledge** instead of relying only on the current conversation.

---

##  Key Features

### 1. Machine Knowledge

Machine information and maintenance-related data are maintained in structured files.

### 2. OEM Manual Knowledge

The agent can use machine-specific technical documentation to ground troubleshooting information.

### 3. Long-Term Maintenance Memory

Past maintenance incidents and solutions can be stored and recalled using Hindsight.

### 4. Context-Aware Troubleshooting

The agent considers both:

* What the OEM documentation recommends
* What has worked in previous maintenance incidents

### 5. AI-Powered Assistance

The system uses an LLM to interpret the technician's problem and generate a useful response based on retrieved knowledge.

### 6. Centralized Knowledge

Maintenance knowledge that may normally remain with individual technicians can be captured and reused.

---

## Project Structure

```text
factory-maintenance-knowledge-agent/
│
├── .gitignore
├── README.md
├── requirements.txt
│
├── app.py
├── agent.py
├── seed_memory.py
│
└── data/
    └── machines.json
```

### File Description

| File                 | Purpose                                                   |
| -------------------- | --------------------------------------------------------- |
| `app.py`             | Main application/interface                                |
| `agent.py`           | AI agent and knowledge-retrieval logic                    |
| `seed_memory.py`     | Loads previous maintenance knowledge into Hindsight       |
| `data/machines.json` | Machine information and maintenance/OEM-related data      |
| `requirements.txt`   | Python dependencies                                       |
| `.gitignore`         | Prevents sensitive/unnecessary files from being committed |

---

## ⚙️ Technologies Used

* **Python**
* **Large Language Model (LLM)**
* **Hindsight** – long-term memory for the AI agent
* **OEM technical documentation**
* **JSON** – structured machine and maintenance data
* **Git & GitHub** – version control

---

##  Getting Started

### 1. Clone the repository

```bash
git clone <your-repository-url>
cd factory-maintenance-knowledge-agent
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it on macOS/Linux:

```bash
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root:

```text
GROQ_API_KEY=your_groq_api_key
HINDSIGHT_API_KEY=your_hindsight_api_key
```

**Never commit `.env` to GitHub.**

The `.env` file should be included in `.gitignore`.

---

## Running the Project

Depending on the application entry point, run:

```bash
python app.py
```

If memory needs to be initialized first:

```bash
python seed_memory.py
```

Then start the application:

```bash
python app.py
```

---

##  Example

### Input

```text
Machine: M-102

Issue:
The machine is producing abnormal vibration and the motor temperature
has increased significantly.
```

### Agent Process

```text
User Issue
    ↓
Identify Machine
    ↓
Retrieve OEM Information
    ↓
Retrieve Similar Past Incidents
    ↓
Combine Retrieved Knowledge
    ↓
LLM Reasoning
    ↓
Generate Troubleshooting Guidance
```

### Example Output

```text
Possible areas to inspect:

1. Motor bearings
2. Shaft alignment
3. Loose mounting components
4. Cooling system

A previous maintenance incident involving similar vibration was
associated with bearing wear.

Recommended next step:
Inspect the motor bearings and verify shaft alignment against the
OEM maintenance procedure.
```

The response should be treated as **decision-support information**, with technicians following appropriate safety procedures and authorized maintenance processes.

---

##  Future Scope

The system can be extended with:

* Real-time machine sensor data
* Predictive maintenance
* Maintenance ticket integration
* Automatic incident summarization
* Fault-code interpretation
* Technician feedback and learning
* Machine health dashboards
* Voice-based technician interaction
* Multimodal troubleshooting using images
* Automatic maintenance-history generation

---

##  Real-World Impact

The Factory Maintenance Knowledge Agent can help organizations:

* Reduce time spent searching for maintenance information
* Preserve experienced technicians' knowledge
* Improve consistency in troubleshooting
* Make historical maintenance information reusable
* Support faster access to machine-specific information
* Reduce dependence on individual experts for recurring issues

---

## Security

API keys and other sensitive credentials should be stored in environment variables and **must not be committed to GitHub**.

Example:

```text
.env
```

should remain listed in:

```text
.gitignore
```

---

##  Project

**Factory Maintenance Knowledge Agent**

Built as an AI-powered solution for improving access to industrial maintenance knowledge and supporting technicians during machine troubleshooting.
