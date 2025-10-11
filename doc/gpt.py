import openai
import os
import json
from datetime import datetime

# 🔑 API key setup
openai.api_key = os.getenv("OPENAI_API_KEY") or "YOUR_OPENAI_API_KEY"

# ⚙️ Config
MODEL = "gpt-5"  # can also use gpt-4o or gpt-4o-mini
TEMPERATURE = 0.3
OUTPUT_FILE = "chat_output.txt"
MEMORY_FILE = "memory_log.txt"
MAX_MESSAGES_BEFORE_SUMMARY = 10  # number of turns before summarizing

# 💬 Conversation and memory
conversation = [
    {
        "role": "system",
        "content": (
            "You are a structured assistant that always responds in this JSON format:\n"
            "{\n"
            '  \"summary\": \"short summary of your reply\",\n'
            '  \"details\": \"expanded answer or reasoning\",\n'
            '  \"sources\": [\"if any, list them here\"]\n'
            "}\n\n"
            "Maintain continuity using the conversation summary if provided."
        ),
    }
]

conversation_summary = None  # store condensed memory here


# 🔧 Function: send conversation to GPT
def ask_gpt():
    response = openai.chat.completions.create(
        model=MODEL,
        temperature=TEMPERATURE,
        response_format={"type": "json_object"},
        messages=conversation,
    )
    reply = response.choices[0].message.content
    conversation.append({"role": "assistant", "content": reply})
    return reply


# 🧠 Function: summarize older conversation
def summarize_conversation():
    global conversation_summary, conversation

    if len(conversation) <= 3:
        return

    print("\n🧠 Summarizing older messages to preserve memory...\n")

    summary_prompt = [
        {
            "role": "system",
            "content": (
                "Summarize the following conversation into a short JSON object with keys:\n"
                "{\n"
                '  \"context\": \"summary of what has been discussed so far\",\n'
                '  \"facts\": [\"important details or conclusions\"]\n'
                "}\n"
            ),
        },
        {"role": "user", "content": json.dumps(conversation[-MAX_MESSAGES_BEFORE_SUMMARY:], indent=2)},
    ]

    summary_resp = openai.chat.completions.create(
        model=MODEL,
        temperature=0.2,
        response_format={"type": "json_object"},
        messages=summary_prompt,
    )

    conversation_summary = summary_resp.choices[0].message.content

    # 🧾 Save the summary to a memory log
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(MEMORY_FILE, "a", encoding="utf-8") as mem_file:
        mem_file.write(f"[{timestamp}] Conversation Summary:\n")
        mem_file.write(f"{conversation_summary}\n\n")

    # 🧩 Replace old messages with the summary for compact context
    conversation = [
        {
            "role": "system",
            "content": (
                "You are a structured assistant that always responds in JSON. "
                "Here is a summary of the previous context you must remember:\n"
                f"{conversation_summary}"
            ),
        }
    ]


# 💬 Main chat loop
def main():
    print("🤖 GPT Structured Chat (with summarizing memory log) — type 'exit' to quit\n")

    with open(OUTPUT_FILE, "a", encoding="utf-8") as f:
        while True:
            user_input = input("You: ")
            if user_input.lower() in {"exit", "quit"}:
                print("👋 Goodbye!")
                break

            # Add user input
            conversation.append({"role": "user", "content": user_input})

            # Auto-summarize if conversation is long
            if len(conversation) > MAX_MESSAGES_BEFORE_SUMMARY:
                summarize_conversation()

            # Get GPT reply
            reply = ask_gpt()

            # Display structured JSON
            print("\nAssistant (JSON):")
            print(reply)
            print()

            # Log conversation
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            f.write(f"[{timestamp}] USER: {user_input}\n")
            f.write(f"{reply}\n\n")
            f.flush()


if __name__ == "__main__":
    main()
