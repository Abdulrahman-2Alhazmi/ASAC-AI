import cohere

co = cohere.ClientV2("55jJ5MENJymIlXYJQghwA6kozSSZ6Azwi6q3pNPw")

response = co.chat(
    model="command-a-03-2025",
    messages=[
        {
            "role": "user",
            "content": "كيف حالك"
        }
    ]
)

print(response.message.content[0].text)