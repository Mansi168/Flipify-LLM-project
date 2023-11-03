import chainlit as cl
import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")
model_name = "gpt-3.5-turbo"
settings = {
    "temperature": 0.7,
    "max_tokens": 500,
    "top_p": 1,
    "frequency_penalty": 0,
    "presence_penalty": 0,
}

@cl.on_chat_start
def start_chat():
    cl.user_session.set(
        "message_history",
        [{"role": "system", "content": "You are a helpful clothing assistant."}],
    )

@cl.on_chat_start    
async def start():
    # Send the elements globally
    await cl.Image(path="./cat.jpg", name="image1", display="inline").send()
    # await cl.Text(content="Here is a side text document", name="text1", display="side").send()
    # await cl.Text(content="Here is a page text document", name="text2", display="page").send()

    # Send the same message twice
    content = "Here is image1, a nice image of a cat! As well as text1 and text2!"

    await cl.Message(
        content=content,
    ).send()


@cl.on_message
async def main(message: cl.Message):
    message_history = cl.user_session.get("message_history")
    message_history.append({"role": "user", "content": message.content})

    msg = cl.Message(content="")

    async for stream_resp in await openai.ChatCompletion.acreate(
        model=model_name, 
        messages=message_history, 
        stream=True, 
        **settings
    ):
        token = stream_resp.choices[0]["delta"].get("content", "")
        await msg.stream_token(token)

    message_history.append({"role": "assistant", "content": msg.content})
    user_message = message_history[-2].content.lower()
    
    if "clothing" in user_message or "dress" in user_message:
        clothing_suggestions = generate_clothing_suggestions(user_message)
        msg.content = clothing_suggestions
    await msg.send()

def generate_clothing_suggestions(user_message):
    if "summer" in user_message:
        suggestions = [
            "1. Floral sundress",
            "2. Linen shorts and a tank top",
            "3. Beach-ready swimwear",
        ]
