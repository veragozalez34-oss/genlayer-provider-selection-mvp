# genlayer-provider-selection-mvp
GenLayer MVP: AI-assisted provider selection for senior wellness programs

# GenLayer Provider Selection MVP

This MVP demonstrates an AI-assisted smart contract for selecting the best provider for a senior wellness program.

## What it does
- stores program requirements from an organizer
- accepts multiple provider submissions
- filters eligible providers
- uses GenLayer AI consensus to select the best provider
- returns a winner with a human-readable explanation

## Demo scenario
Program:
- District: Tverskoy
- Activity: Pilates
- Capacity: 20 participants
- Audience: adults 55+
- Requirements: safe, low-impact, mobility and balance focused

Providers submitted:
- ActiveLife Studio
- SilverAge Wellness Center
- StrongFit Gym
- Harmony Community Center

## Final result
Winner:
**SilverAge Wellness Center**

Reason:
Best overall fit for adults 55+: explicitly adapted gentle Pilates for 55+, strong focus on mobility, balance and fall prevention, instructor is a certified senior fitness specialist with rehab experience, equipment includes safe supportive options like chairs and balance cushions, and added community value comes from health lectures and beginner adaptation sessions.

## Files
- `senior_program_provider_selection.py` — GenLayer smart contract source
- `demo_result.png` — successful Studio result screenshot
