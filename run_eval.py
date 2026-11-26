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
# Today's date as text, such as 2026-11-26
today = date.today().isoformat()
# Create a results folder if it doesn't exist; exist_ok=True means no error if it's already there
os.makedirs("results", exist_ok=True)
# The file name for this run's results, such as results/run_2026-11-26.txt
results_path = f"results/run_{today}.txt"

# Open the results file for writing; "w" creates it or replaces it, and utf-8 handles special characters
with open(results_path, "w", encoding="utf-8") as out:
    # Write the date at the top of the results file
    out.write(f"Date: {today}\n")
    # Write the model name, so we know which model produced these answers
    out.write(f"Model: {MODEL}\n")
    # Write the token limit, so we know how long answers were allowed to be
    out.write(f"max_tokens: {MAX_TOKENS}\n")
    # Write a note that the temperature setting was not changed from its default
    out.write("Temperature: default (not set in script)\n")
    # Write a line of equal signs to separate the settings from the answers
    out.write("=" * 40 + "\n\n")

    # Open the questions file for reading, using utf-8 so special characters display correctly
    with open("questions.csv", encoding="utf-8") as f:
        # Read each row as a dictionary, using the header line for the keys
        reader = csv.DictReader(f)
        # Loop over only the first 3 questions for this test
        for row in list(reader)[:3]:
            # Send one question to Claude, starting a new request
            message = client.messages.create(
                # The model to send the question to
                model=MODEL,
                # The maximum length of Claude's answer
                max_tokens=MAX_TOKENS,
                # The conversation: one message from you, containing the question
                messages=[{"role": "user", "content": row["question"]}],
            )
            # Pull out the text of Claude's answer
            answer = message.content[0].text
            # Print the question to the screen
            print("Question:", row["question"])
            # Print the correct answer to the screen
            print("Correct:", row["correct_answer"])
            # Print Claude's answer to the screen
            print("Claude:", answer)
            # Print a dashed line to separate each question on screen
            print("-" * 40)
            # Write the question to the results file
            out.write(f"Question: {row['question']}\n")
            # Write the correct answer to the results file
            out.write(f"Correct: {row['correct_answer']}\n")
            # Write Claude's full answer to the results file
            out.write(f"Claude: {answer}\n")
            # Write a dashed line to separate each question in the file
            out.write("-" * 40 + "\n")

# Tell you on screen where the results were saved
print("Results saved to", results_path)