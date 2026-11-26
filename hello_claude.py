import anthropic

client = anthropic.Anthropic()

message = client.messages.create(
    model="claude-haiku-5-5",
    max_tokens=100,
    messages=[{"role": "user", "content": "What is the capital of Australia?"}],
)

print(message.content[0].text)