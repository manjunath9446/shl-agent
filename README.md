# SHL Assessment Recommendation Agent

State-aware conversational AI system for recommending SHL assessments through multi-turn hiring consultations.

---




# Project Overview

This project was built for the SHL AI Intern assignment.

The system goes beyond a basic RAG chatbot by supporting:

- strategic clarification
- conversational recommendation workflows
- stack refinement
- HR advisory discussions
- comparison workflows
- hallucination filtering
- multi-turn consultation memory

The goal was to simulate how a real SHL consultant interacts with recruiters during hiring discussions.

---

# Design Choices

## 1. Stateful Consultation Workflow

Instead of a single-shot recommendation system, the architecture was designed around conversational consultation stages:

- clarification
- recommendation
- refinement
- advisory
- comparison

This improved recommendation relevance and conversational realism.

---

## 2. Lightweight Modular Architecture

The system intentionally avoids heavy multi-agent orchestration.

Core modules include:

- retrieval layer
- clarification strategy
- consultation router
- recommendation memory
- hallucination filtering
- recommendation engine

The focus was stability and evaluation reliability over unnecessary complexity.

---

## 3. Hybrid Clarification Strategy

Clarification handling uses hybrid semantic rules rather than fully autonomous memory.

This approach was chosen to:
- reduce hallucinations
- improve reproducibility
- maintain evaluation stability
- support flexible recruiter conversations

---

# Retrieval Setup

## Vector Database

- ChromaDB
- SentenceTransformer embeddings (`all-MiniLM-L6-v2`)

---

## Retrieval Pipeline

1. Query expansion
2. Broad semantic retrieval
3. Candidate filtering
4. Recommendation validation

The system retrieves a broader candidate pool before narrowing recommendations to improve Recall@10 performance.

---

## Hallucination Prevention

Recommendations are validated against retrieved catalog candidates before being returned.

This prevents:
- hallucinated URLs
- hallucinated assessment names
- unsupported recommendations

---

# Prompt Design

Prompts were designed to maintain:

- recruiter-focused tone
- consultative behavior
- hiring strategy awareness
- assessment explainability

Specialized prompts were created for:
- recommendation generation
- refinement workflows
- HR advisory discussions
- assessment comparison

---

# Evaluation Approach

The system was iteratively tested against:

- retrieval relevance
- Recall@10 behavior
- conversational continuity
- refinement consistency
- hallucination prevention
- SHL-style consultation flows

Example evaluation scenarios included:

- contact center hiring
- leadership assessment
- graduate hiring
- sales transformation
- technical hiring

---

# What Didn't Work

Several approaches were attempted and later simplified:

## 1. Large Multi-Agent Orchestration

Early experiments with complex orchestration increased instability and debugging difficulty.

The final architecture intentionally uses a lightweight consultation router instead.

---

## 2. Fully Rule-Based Clarification

Strict phrase matching was too rigid for realistic recruiter conversations.

This was replaced with hybrid semantic clarification detection.

---

## 3. Direct Recommendation Without Clarification

Single-shot recommendations often produced weak retrieval relevance.

Strategic clarification significantly improved recommendation quality.

---

# Improvement Measurement

Improvements were measured through:

- reduction in irrelevant recommendations
- improved conversational continuity
- better recommendation refinement behavior
- lower hallucination frequency
- improved retrieval alignment
- stronger Recall@10 candidate coverage

---

# AI Tools Used

AI-assisted tools were used for:

- iterative architecture exploration
- debugging support
- retrieval optimization ideas
- prompt refinement
- workflow reasoning
- code acceleration

Final architecture decisions, retrieval logic, consultation workflows, and evaluation design were manually refined and integrated.

---

# Tech Stack

- FastAPI
- Streamlit
- ChromaDB
- SentenceTransformers
- Groq/OpenAI APIs
- Python

---

# Key Differentiator

The project evolved from a basic RAG chatbot into a state-aware consultative hiring workflow system focused on realistic recruiter interactions.