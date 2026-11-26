# Import csv for reading the questions file
import csv
# Import anthropic so we can send requests to Claude
import anthropic

# Create the client; it reads your API key from the Codespaces secret automatically
client = anthropic.Anthropic()

# Open the questions file for reading, using utf-8 so special characters display correctly
with open("questions.csv", encoding="utf-8") as f:
    # Read each row as a dictionary, using the header line for the keys
    reader = csv.DictReader(f)
    # Test only the first 3 questions for now, to check the program and the cost
    for row in list(reader)[:3]:
        # Send the question to Claude using the cheapest model
        message = client.messages.create(
            # The model we are testing with
            model="claude-haiku-5-5",
            # Limit the length of Claude's answer to keep costs down
            max_tokens=200,
            # The conversation: one message from you, containing the question
            messages=[{"role": "user", "content": row["question"]}],
        )
        # Pull out the text of Claude's answer
        answer = message.content[0].text
        # Print the question, the correct answer, and Claude's answer
        print("Question:", row["question"])
        print("Correct:", row["correct_answer"])
        print("Claude:", answer)
        # Print a dashed line to separate each question
        print("-" * 40)