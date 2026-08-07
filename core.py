def generate_reply(message: str) -> str:
    message = message.lower()

    if "hello" in message:
        return "Hello. I'm here."

    if "who are you" in message:
        return "I am Aura — a local system running on your machine."

    return f"You said: {message}"