import openai

openai.api_key = ''

def split_text_gpt3(text, max_tokens=3072):
    tokens = text.split()
    token_chunks = []

    current_chunk = []
    current_length = 0
    for token in tokens:
        current_length += len(token) + 1  # Add 1 for the space
        if current_length < int(max_tokens*(3/4)):
            current_chunk.append(token)
        else:
            token_chunks.append(" ".join(current_chunk))
            current_chunk = [token]
            current_length = len(token) + 1

    if current_chunk:
        token_chunks.append(" ".join(current_chunk))

    return token_chunks
def generate_summary_gpt3(text, model='gpt-3.5-turbo', max_tokens=2048):
    token_chunks = split_text_gpt3(text, max_tokens=max_tokens)

    summarized_text = []
    for chunk in token_chunks:
        response = openai.ChatCompletion.create(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": "You are a summarization AI bot that can summarize effectively with short and easy to understand while still remain the original properties and values.",
                },
                {
                    "role": "user",
                    "content": f"Please summarize the following text in Thai:\n{chunk}\nSummary:",
                },
            ],
            max_tokens=max_tokens,
            temperature=0,
        )

        summary = str(response.choices[0].message.content).strip()
        summarized_text.append(summary)
    return " ".join(summarized_text)

