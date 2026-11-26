# Import the csv module, which knows how to read comma-separated files
import csv

# Open questions.csv for reading, and use utf-8 so characters like "í" and "°" display correctly
with open("questions.csv", encoding="utf-8") as f:
    # Read each row as a dictionary, using the header line (question, correct_answer, wrong_claim) for the keys
    reader = csv.DictReader(f)
    # Go through the rows one at a time
    for row in reader:
        # Print the question and its correct answer, so we can check the file was read correctly
        print(row["question"], "->", row["correct_answer"])