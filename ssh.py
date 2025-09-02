import os
import discord
import re
import datetime
from dotenv import load_dotenv
import logging

# Setup logging
logging.basicConfig(
    filename="logs/bot.log",
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)

# Load token dari .env
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
print("TOKEN Loaded:", TOKEN[:10], "...")

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

client = discord.Client(intents=intents)

context = {}

def get_time_of_day():
    now = datetime.datetime.now().hour
    if 5 <= now < 12:
        return "pagi"
    elif 12 <= now < 18:
        return "siang"
    elif 18 <= now < 22:
        return "malam"
    return "larut malam"

def chatbot_response(user_id, user_input):
    global context
    time_of_day = get_time_of_day()

    # Inisialisasi konteks
    if user_id not in context:
        context[user_id] = {"state": None}

    state = context[user_id]["state"]

    # ===== RULE 1: Sapaan =====
    if re.search(r'\b(halo|hai|hi|selamat)\b', user_input, re.IGNORECASE):
        context[user_id]["state"] = "offer_tips"
        return (
            f"Halo, selamat {time_of_day} 👋 \n"
            "Senang bisa ngobrol denganmu.\n"
            "Aku bisa kasih tips seputar *Diet*, *Latihan*, atau *Relaksasi*.\n"
            "Mau mulai dari mana?"
        )

    # ===== RULE 2: Pilihan Diet/Latihan/Relaksasi =====
    if state == "offer_tips":
        if re.search(r'\bdiet\b', user_input, re.IGNORECASE):
            context[user_id]["state"] = "diet_menu"
            return (
                "Oke, kita bahas diet yaa 🥗.\n"
                "Ini contoh menu harian sehat:\n\n"
                "- Sarapan: Oatmeal + buah\n"
                "- Siang: Nasi merah + dada ayam\n"
                "- Snack: Yogurt tanpa gula\n"
                "- Malam: Ikan panggang + salad\n\n"
                "Mau aku tambahkan *tips minuman sehat* juga?"
            )
        elif re.search(r'\blatihan\b', user_input, re.IGNORECASE):
            context[user_id]["state"] = "workout_plan"
            return (
                "Baik, ini jadwal latihan mingguan yang bisa kamu lakukan. Usahakan minimal 3 kali seminggu yaa! 💪\n\n"
                "- Senin: Lari santai 30 menit\n"
                "- Rabu: Latihan beban (upper body)\n"
                "- Jumat: Bersepeda 45 menit\n\n"
                "Mau aku kasih *tips pemanasan* sebelum latihan?"
            )
        elif re.search(r'\b(relaksasi|stres|stress)\b', user_input, re.IGNORECASE):
            context[user_id]["state"] = "relaxation"
            return (
                "Kalau lagi penat 🌿 coba tarik napas dalam 5 detik lalu hembuskan perlahan.\n"
                "Mau aku bagikan *teknik relaksasi lainnya*?"
            )
        elif re.search(r'\bya|boleh|oke\b', user_input, re.IGNORECASE):
            return "Sip, tinggal pilih aja: *Diet*, *Latihan*, atau *Relaksasi*."
        else:
            return "Hmm, coba pilih salah satu: *Diet*, *Latihan*, atau *Relaksasi* 🙂"

    # ===== RULE 3: Diet lanjutan =====
    if state == "diet_menu":
        if re.search(r'\b(ya|boleh|oke|lanjut)\b', user_input, re.IGNORECASE):
            context[user_id]["state"] = "offer_tips"
            return (
                "Tips minuman sehat 💧:\n"
                "- Minum air putih minimal 8 gelas sehari\n"
                "- Infused water (lemon + mint) bisa dicoba\n"
                "- Teh hijau tanpa gula bagus buat relaksasi\n\n"
                "Pola minum yang baik sama pentingnya dengan pola makan."
            )
        else:
            return "Kalau mau aku kasih tips minuman sehat, tinggal bilang *ya*."

    # ===== RULE 4: Latihan lanjutan =====
    if state == "workout_plan":
        if re.search(r'\b(ya|boleh|oke|lanjut)\b', user_input, re.IGNORECASE):
            context[user_id]["state"] = "offer_tips"
            return (
                "Tips pemanasan 🔥:\n"
                "- Peregangan dinamis 5 menit\n"
                "- Contoh: arm circle, lunges, jogging ringan\n\n"
                "Dengan pemanasan, risiko cedera bisa berkurang."
            )
        else:
            return "Kalau mau tips pemanasan, bilang aja *ya*."

    # ===== RULE 5: Relaksasi lanjutan =====
    if state == "relaxation":
        if re.search(r'\b(ya|boleh|oke|lanjut)\b', user_input, re.IGNORECASE):
            context[user_id]["state"] = "offer_tips"
            return (
                "Beberapa teknik relaksasi lain 🌸:\n"
                "- Dengarkan musik menenangkan\n"
                "- Meditasi 5 menit\n"
                "- Jalan santai sebentar di luar rumah\n\n"
                "Hal sederhana bisa bikin pikiran lebih segar."
            )
        else:
            return "Kalau mau aku kasih teknik relaksasi tambahan, tinggal bilang *ya*."

    # ===== Fallback =====
    if state:
        # user lagi di state tertentu → jangan reset
        return "Aku kurang paham maksudmu. Coba jawab lagi sesuai pertanyaan sebelumnya 🙂"
    else:
        # user nggak ada di state → arahkan ke menu awal
        return (
            "Halo, aku bisa bantu dengan tips seputar *Diet*, *Latihan*, atau *Relaksasi*.\n"
            "Kamu mau pilih yang mana?"
        )

@client.event
async def on_ready():
    print(f'✅ Bot login sebagai {client.user}')
    logging.info(f"Bot login sebagai {client.user}")

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    user_id = str(message.author.id)
    user_input = message.content    

    response = chatbot_response(user_id, user_input)

    # catat ke log
    logging.info(f"[User: {user_id}] Input: {user_input}")
    logging.info(f"Response: {response}")

    # kirim balasan ke Discord
    await message.channel.send(response)

# Run bot
if __name__ == "__main__":
    client.run(TOKEN)
