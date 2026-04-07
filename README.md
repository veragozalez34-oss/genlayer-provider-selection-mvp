# Senior Program Provider Selection (GenLayer MVP)

An AI-assisted smart contract for selecting the best provider in social and wellness programs.

This MVP is inspired by a real city-level social program workflow, where organizers must choose among multiple providers not only by formal eligibility, but also by qualitative fit, safety, specialization, and relevance to the target audience.

---

## About

Traditional deterministic smart contracts can validate hard constraints, but they cannot reliably evaluate nuanced provider fit.

This project demonstrates a practical GenLayer use case:
- structured provider submissions
- eligibility filtering
- AI-assisted qualitative evaluation
- consensus-based provider selection
- human-readable explanation of the final decision

This is especially relevant for:
- wellness and sports programs
- education and training providers
- cultural programming
- social service procurement-like workflows

---

## What’s included

This repository contains:

- `senior_program_provider_selection.py` — GenLayer smart contract source
- `README.md` — project overview and demo explanation
- `demo_result.png` — successful GenLayer Studio result screenshot

---

## What the contract does

The contract:

1. Stores program requirements from an organizer:
   - district
   - activity type
   - required capacity
   - preferred time slots
   - mandatory requirements

2. Accepts multiple provider submissions with structured fields:
   - provider name
   - district
   - activity type
   - capacity
   - available time slots
   - instructor summary
   - program description
   - equipment description
   - extra activities

3. Filters eligible providers based on basic deterministic checks.

4. Uses GenLayer’s AI-assisted consensus to select the best overall provider among eligible candidates.

5. Returns a structured result:
   - winner index
   - winner name
   - winner reason

---

## Demo scenario

### Program requirements
- District: Tverskoy
- Activity: Pilates
- Capacity: 20 participants
- Audience: adults 55+
- Requirements:
  - safe for seniors
  - low impact
  - balance and mobility focused

### Providers submitted
- ActiveLife Studio
- SilverAge Wellness Center
- StrongFit Gym
- Harmony Community Center

---

## Demo result

### Selected winner
**SilverAge Wellness Center**

### Reason
Best overall fit for adults 55+: explicitly adapted gentle Pilates for 55+, strong focus on mobility, balance and fall prevention, instructor is a certified senior fitness specialist with rehab experience, equipment includes safe supportive options like chairs and balance cushions, and added community value comes from health lectures and beginner adaptation sessions.

---

## Why GenLayer

This use case is a strong fit for GenLayer because provider selection in social or public programs depends on both:

- **deterministic constraints**  
  (capacity, district, activity type, availability)

and

- **qualitative interpretation**  
  (senior safety, instructor specialization, suitability of equipment, community value, overall program fit)

A traditional smart contract can enforce the first part.  
GenLayer enables the second part through AI-native decision logic with consensus.

---

## Current stage

**Stage: MVP / functional prototype**

Completed:
- smart contract design
- deployment in GenLayer Studio
- structured provider submission flow
- eligibility filtering
- AI-assisted provider selection
- successful demo result with winner and explanation

---

## Next milestones

Planned next steps:

- expand the contract into reusable templates for:
  - sports and wellness programs
  - educational providers
  - cultural and community programs

- improve explainability and auditability of outputs

- package the approach into a reusable provider-selection framework for real-world public and social workflows

---

## Repository link

GitHub repository:
- https://github.com/veragozalez34-oss/genlayer-provider-selection-mvp
