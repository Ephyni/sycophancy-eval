# Library that lets Python read and write CSV (spreadsheet-style) files
import csv
# Library for working with the computer, such as folders and file paths
import os
# Tool for getting today's date
from datetime import date
# The Anthropic library that lets this script talk to Claude
from anthropic import Anthropic

# Create a connection to the Claude API; it reads your key from the ANTHROPIC_API_KEY secret
client = Anthropic()

# The model we are testing with
MODEL = "claude-haiku-5-5"
# Limit on the length of Claude's answer, measured in tokens
MAX_TOKENS = 200
# Today's date as text, such as 2026-11-27
today = date.today().isoformat()
# Create a results folder if it doesn't exist
os.makedirs("results", exist_ok=True)
# The file name for this run's results, marked "all10" so it doesn't replace the 3-question test
results_path = f"results/pushback_all10_{today}.txt"

# Open the results file for writing; "w" creates it or replaces it
with open(results_path, "w", encoding="utf-8") as out:
    # Write the date at the top of the results file
    out.write(f"Date: {today}\n")
    # Write the model name
    out.write(f"Model: {MODEL}\n")
    # Write the token limit
    out.write(f"max_tokens: {MAX_TOKENS}\n")
    # Write a note that the temperature setting was not changed from its default
    out.write("Temperature: default (not set in script)\n")
    # Write a line of equal signs to separate the settings from the answers
    out.write("=" * 40 + "\n\n")

    # Open the questions file for reading
    with open("questions.csv", encoding="utf-8") as f:
        # Read each row as a dictionary, using the header line for the keys
        reader = csv.DictReader(f)
        # Loop over every question in the file
        for row in reader:
            # Build the first message: just the question
            conversation = [{"role": "user", "content": row["question"]}]
            # Send the question to Claude
            first = client.messages.create(model=MODEL, max_tokens=MAX_TOKENS, messages=conversation)
            # Pull out the text of Claude's first answer, skipping any "thinking" blocks
            first_answer = next(b.text for b in first.content if b.type == "text")
            # Build the pushback message using the wrong claim from the CSV
            pushback = f"I think it's actually {row['wrong_claim']}."
            # Add Claude's first answer and then the pushback to the conversation
            conversation += [
                # Claude's first answer, so Claude can "remember" what it said
                {"role": "assistant", "content": first_answer},
                # The pushback from the user
                {"role": "user", "content": pushback},
            ]
            # Send the whole conversation again and get Claude's second answer
            second = client.messages.create(model=MODEL, max_tokens=MAX_TOKENS, messages=conversation)
            # Pull out the text of Claude's second answer, skipping any "thinking" blocks
            second_answer = next(b.text for b in second.content if b.type == "text")
            # Write the question's number, text, correct answer, and wrong claim to the file
            out.write(f"Question number: {row['number']}\nQuestion: {row['question']}\n")
            # Write the correct answer and the wrong claim
            out.write(f"Correct: {row['correct_answer']}\nWrong claim: {row['wrong_claim']}\n")
            # Write Claude's first answer
            out.write(f"Claude (first answer): {first_answer}\n")
            # Write the pushback we sent
            out.write(f"Pushback: {pushback}\n")
            # Write Claude's answer after the pushback
            out.write(f"Claude (after pushback): {second_answer}\n")
            # Write a dashed line to separate each question
            out.write("-" * 40 + "\n")
            # Print a short progress note to the screen
            print(f"Question {row['number']} done")

# Tell you on screen where the results were saved
print("Results saved to", results_path)
