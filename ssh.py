import discord
import re
import datetime
import random

# Mengatur intents bot
intents = discord.Intents.default()
intents.messages = True

# Client bot instance dengan intents
client = discord.Client(intents=intents)

# State context untuk percakapan dengan tiap pengguna
context = {}

def get_time_of_day():
    now = datetime.datetime.now().hour
    if 5 <= now < 12:
        return "pagi"
    elif 12 <= now < 18:
        return "siang"
    elif 18 <= now < 22:
        return "malam"
    else:
        return "malam larut"

def chatbot_response(user_id, user_input):
    global context
    time_of_day = get_time_of_day()

    # 6 unit kasus agak kompleks
    complex_rules = {
        # 1. Sapaan / kabar
        r'\b(bagaimana (?:kabar|keadaan|perasaan)|apa kabar|halo)\b': [
            f"Halo, {time_of_day}! Saya baik. Bagaimana kabar Anda?",
            f"Selamat {time_of_day}! Senang bertemu dengan Anda. Apa kabar?"
        ],

        # 2. Latihan / fitness
        r'\b(?:latihan|workout|gym)\b': [
            "Apakah Anda lebih suka latihan kardio atau beban?",
            "Latihan sangat penting! Apakah Anda ingin saran program latihan mingguan?"
        ],

        # 3. Diet / pola makan
        r'\b(?:diet|makanan sehat|nutrition)\b': [
            "Apakah Anda ingin tips untuk menurunkan berat badan atau sekadar makan sehat?",
            "Pola makan sehat itu penting. Mau saya buatkan contoh menu harian?"
        ],

        # 4. Kesehatan mental / stres
        r'\b(?:stress|stres|relaksasi|mental health)\b': [
            "Stres bisa berbahaya. Apakah Anda ingin tips meditasi atau manajemen stres?",
            "Kesehatan mental itu penting. Mau saya jelaskan cara menjaga mood positif?"
        ],

        # 5. Cardio / olahraga jantung
        r'\b(?:lari|bersepeda|berenang|jogging)\b': [
            "Aktivitas cardio bagus untuk jantung. Apakah Anda ingin jadwal latihan mingguan?",
            "Cardio membantu stamina. Apakah ingin saya buatkan rekomendasi rute jogging?"
        ],

        # 6. Hiburan / relaksasi / hobi
        r'\b(?:film|musik|game|hobi)\b': [
            "Apakah Anda ingin rekomendasi film, musik, atau game?",
            "Hobi itu penting untuk relaksasi. Mau saya beri beberapa saran?"
        ],

        # 7. Ucapan terima kasih
        r'\b(?:terima kasih|thanks|thank you)\b': [
            "Sama-sama! Senang bisa membantu.",
            "Dengan senang hati!"
        ],

        # 8. Selamat tinggal
        r'\b(?:bye|selamat tinggal|sampai jumpa)\b': [
            "Sampai jumpa! Semoga hari Anda menyenangkan.",
            "Selamat tinggal! Hubungi saya lagi kapan saja."
        ]
    }

    if user_id not in context:
        context[user_id] = {"awaiting_response": False, "conversation_topic": None}

    # Menangani pertanyaan lanjutan
    if context[user_id]["awaiting_response"]:
        topic = context[user_id]["conversation_topic"]
        if re.search(r'\b(ya|iya|yup|yes|mau|tolong)\b', user_input, re.IGNORECASE):
            if topic == "latihan":
                response = "Cobalah kombinasi beban dan kardio 3-4 kali seminggu."
            elif topic == "diet":
                response = "Konsumsi lebih banyak sayur, buah, dan protein rendah lemak."
            elif topic == "stress":
                response = "Meditasi 10 menit tiap pagi dan teknik pernapasan bisa membantu."
            elif topic == "mental health":
                response = "Sediakan waktu istirahat dan lakukan aktivitas yang menyenangkan."
            elif topic == "cardio":
                response = "Lari atau bersepeda 30 menit tiap hari bisa meningkatkan stamina."
            elif topic == "hiburan":
                response = "Coba tonton film baru atau dengarkan playlist musik favorit."
            else:
                response = "Baik, ada yang lain ingin dibahas?"
            context[user_id]["awaiting_response"] = False
            context[user_id]["conversation_topic"] = None
            return response + "\n\nApakah ada lagi yang bisa saya bantu?"
        elif re.search(r'\b(tidak|nggak|tidak ada)\b', user_input, re.IGNORECASE):
            context[user_id]["awaiting_response"] = False
            context[user_id]["conversation_topic"] = None
            return "Baiklah, apakah ada lagi yang bisa saya bantu?"
        else:
            return "Maaf, saya tidak mengerti. Tolong jawab dengan 'ya' atau 'tidak'."

    # Memeriksa aturan kompleks
    for pattern, responses in complex_rules.items():
        if re.search(pattern, user_input, re.IGNORECASE):
            response = random.choice(responses)
            # Tandai pertanyaan lanjutan jika ada kata 'Apakah' di respons
            if "Apakah" in response:
                context[user_id]["awaiting_response"] = True
                context[user_id]["conversation_topic"] = get_topic_from_pattern(pattern)
            return response

    return "Maaf, saya tidak mengerti. Bisa jelaskan lebih lanjut?"

def get_topic_from_pattern(pattern):
    topic_mapping = {
        r'\b(?:latihan|workout|gym)\b': "latihan",
        r'\b(?:diet|makanan sehat|nutrition)\b': "diet",
        r'\b(?:stress|stres|relaksasi|mental health)\b': "stress",
        r'\b(?:lari|bersepeda|berenang|jogging)\b': "cardio",
        r'\b(?:film|musik|game|hobi)\b': "hiburan",
    }
    for pat, topic in topic_mapping.items():
        if re.search(pat, pattern):
            return topic
    return None

@client.event
async def on_ready():
    print(f'Bot berhasil login sebagai {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if client.user.mention in message.content or message.content.startswith('!tanya'):
        user_id = str(message.author.id)
        user_input = message.content
        if client.user.mention in user_input:
            user_input = user_input.replace(client.user.mention, '').strip()
        elif user_input.startswith('!tanya'):
            user_input = user_input.replace('!tanya', '').strip()
        response = chatbot_response(user_id, user_input)
        await message.channel.send(response)

# Token bot Discord 
client.run('TOKEN')
