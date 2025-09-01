import discord
import re
import datetime
import random

intents = discord.Intents.default()
intents.messages = True

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

    # RULE: Sapaan → tawarkan tips
    if re.search(r'\b(halo|hai|hi|selamat)\b', user_input, re.IGNORECASE):
        context[user_id]["state"] = "offer_tips"
        return f"Selamat {time_of_day}! 😊 Mau tahu tips apa hari ini?\nPilihan: *Diet*, *Latihan*, atau *Relaksasi*."

    # RULE: Jawab sapaan → kalau state offer_tips
    if context[user_id]["state"] == "offer_tips":
        if re.search(r'\bdiet\b', user_input, re.IGNORECASE):
            context[user_id]["state"] = "diet_menu"
            return "Mantap! Ini menu harian sehat untukmu:\n\n🍳 Sarapan: Oatmeal + buah\n🥗 Siang: Nasi merah + dada ayam\n🥛 Snack: Yogurt tanpa gula\n🥩 Malam: Ikan panggang + salad\n\nMau saya kasih *tips minuman sehat* juga?"
        elif re.search(r'\blatihan\b', user_input, re.IGNORECASE):
            context[user_id]["state"] = "workout_plan"
            return "Gas! Ini jadwal latihan mingguan:\n🏃 Senin: Lari 30 menit\n🏋️ Rabu: Gym upper body\n🚴 Jumat: Sepeda 45 menit\n\nMau saya kasih *tips pemanasan* juga?"
        elif re.search(r'\b(relaksasi|stres|stress)\b', user_input, re.IGNORECASE):
            context[user_id]["state"] = "relax"
            return "Relax dulu! Coba tarik napas 5 detik, buang perlahan. Mau saya kasih *teknik relaksasi lainnya*?"
        elif re.search(r'\bya|boleh|oke\b', user_input, re.IGNORECASE):
            return "Oke, pilih salah satu: *Diet*, *Latihan*, atau *Relaksasi*."
        else:
            return "Hmm, pilihannya Diet, Latihan, atau Relaksasi 😉"

    # RULE: Jika user jawab setelah menu diet
    if context[user_id]["state"] == "diet_menu":
        if re.search(r'\b(ya|boleh|oke|lanjut)\b', user_input, re.IGNORECASE):
            context[user_id]["state"] = None
            return "Tips minuman sehat: 💧 Minum air putih 8 gelas, coba infused water, atau teh hijau tanpa gula!"
        else:
            return "Oke, kalau mau lanjut bilang *ya* 😊"

    # RULE: Jika user jawab setelah jadwal latihan
    if context[user_id]["state"] == "workout_plan":
        if re.search(r'\b(ya|boleh|oke|lanjut)\b', user_input, re.IGNORECASE):
            context[user_id]["state"] = None
            return "Tips pemanasan: 🔥 Lakukan peregangan dinamis 5 menit sebelum latihan!"
        else:
            return "Kalau mau tips pemanasan, bilang *ya* 😊"

    return "Hmm, saya belum paham. Mau pilih *Diet*, *Latihan*, atau *Relaksasi*?"

@client.event
async def on_ready():
    print(f'✅ Bot login sebagai {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if client.user.mention in message.content or message.content.startswith('!tanya'):
        user_id = str(message.author.id)
        user_input = message.content.replace(client.user.mention, '').replace('!tanya', '').strip()
        response = chatbot_response(user_id, user_input)
        await message.channel.send(response)

# Token bot Discord 
client.run('TOKEN')
