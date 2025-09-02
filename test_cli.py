import logging
import os

# pastikan folder logs ada
os.makedirs("logs", exist_ok=True)

# setup logging
logging.basicConfig(
    filename="logs/bot.log",
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s"
)

from ssh import chatbot_response

user_id = "123"

print("Start CLI Chatbot (tanpa Discord)")

while True:
    msg = input("You: ")
    if msg.lower() in ["exit", "quit"]:
        break
    res = chatbot_response(user_id, msg)
    print("Bot:", res)

    # simpan ke log
    logging.info(f"[User: {user_id}] Input: {msg}")
    logging.info(f"Response: {res}")
