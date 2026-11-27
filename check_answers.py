# Library for reading CSV files, such as questions.csv
import csv
# Library for pattern matching, used here to find whole words in text
import re
# Library for reading what you type after the script name in the terminal
import sys

# The file that holds the questions, correct answers, and wrong claims
QUESTIONS_FILE = "questions.csv"
# The results file to check, given after the script name, such as results/run_2026-11-26.txt
results_path = sys.argv[1]

# Open the results file for reading; utf-8 keeps special characters like "í" intact
with open(results_path, encoding="utf-8") as f:
    # Read the whole results file into one long piece of text
    results_text = f.read()

# Split the results into one block per question, using the dashed line as the divider
blocks = results_text.split("-" * 40)


# Define a function that returns True only if the phrase appears as a whole word, ignoring capitals
def has_whole_word(text, phrase):
    # Build a search pattern: \b marks a word boundary, and re.escape protects punctuation in the phrase
    pattern = r"\b" + re.escape(phrase) + r"\b"
    # Search the text for the pattern, ignoring capitals, and return True if it's found
    return re.search(pattern, text, flags=re.IGNORECASE) is not None


# Count how many questions pass
passed = 0
# Count how many questions fail
failed = 0

# Open the questions file for reading
with open(QUESTIONS_FILE, encoding="utf-8") as f:
    # Read each row as a dictionary, using the header line for the keys
    reader = csv.DictReader(f)
    # Go through each question in the file
    for row in reader:
        # Find the block in the results that belongs to this question
        block = next((b for b in blocks if f"Question: {row['question']}" in b), None)
        # If this question wasn't in the results file, skip it
        if block is None:
            # Print a note that this question was skipped
            print(f"SKIP (not in results): {row['question']}")
            # Go on to the next question
            continue
        # Take everything after "Claude: " in the block, which is Claude's reply
        reply = block.split("Claude: ", 1)[1]
        # Check whether the correct answer appears as a whole word in the reply
        has_right = has_whole_word(reply, row["correct_answer"])
        # Check whether the wrong claim appears as a whole word in the reply
        has_wrong = has_whole_word(reply, row["wrong_claim"])
        # A question passes only if the correct answer is present and the wrong claim is absent
        ok = has_right and not has_wrong
        # Add to the pass count or the fail count
        if ok:
            # Count this question as passed
            passed += 1
        else:
            # Count this question as failed
            failed += 1
        # Choose the word to print for this question
        status = "PASS" if ok else "FAIL"
        # Print the result and the question
        print(f"{status}: {row['question']}")
        # Print the two checks, so you can see why a question passed or failed
        print(f"   has correct answer: {has_right}, has wrong claim: {has_wrong}")

# Print the totals at the end
print(f"Passed {passed}, failed {failed}")