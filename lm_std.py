from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:1234/v1",
    api_key="lm-studio",
)

response = client.chat.completions.create(
    model="google/gemma-3-1b",
    messages=[
        {
            "role": "user",
            "content": "Say hello in one short sentence.",
        }
    ],
)

print(response.choices[0].message.content)