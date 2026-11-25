# Sycophancy Eval

A small project testing sycophancy in language models: how often a model drops a correct answer when a user pushes back with a wrong claim.

## How it works
1. Ask the model a factual question with one clear right answer.
2. Push back with a wrong claim ("I think it's actually X").
3. Record whether the model held its answer or caved.

## Plan
- **Prototype:** 10 questions, one push back style, one Claude model.
- **Next:** grow to 30 and then 100+ questions, test four push back styles (polite doubt, confident assertion, claimed expertise, emotional pressure), compare models, add controls that separate caving from legitimate updating, run repeats with confidence intervals, and write up the results.

## Status
In progress. Code and results will be added here.
