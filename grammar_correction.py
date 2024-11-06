import openai

TOGETHER_API_KEY = "4e64b86828fc1a78f80a608642df389339ca93eb7b503afd7ad1e4e4ef4ecde7"

client = openai.OpenAI(
    api_key=TOGETHER_API_KEY,
    base_url="https://api.together.xyz/v1",
)

def get_code_completion(messages, max_tokens=512, model="meta-llama/Llama-3-70b-chat-hf"):
    chat_completion = client.chat.completions.create(
        messages=messages,
        model=model,
        max_tokens=max_tokens,
        stop=[
            "<step>"
        ],
        frequency_penalty=1,
        presence_penalty=1,
        top_p=0.7,
        n=10,
        temperature=0.7,
    )

    return chat_completion

def grammar_correction(text):
    messages = [
        {
            "role": "system",
            "content": "Từ các từ trên, hãy chuyển thành câu hoàn chỉnh, có ý nghĩa, tự nhiên nhất",
        },
        {
            "role": "user",
            "content": text,
        }
    ]
    chat_completion = get_code_completion(messages)
    return chat_completion.choices[0].message['content']
