# SickSuckHealth - Rule-based Chatbot 🗨️

Hello! Kami membuat SickSuckHealth Chatbot untuk memenuhi tugas mata kuliah NLP^^

SickSuckHealth adalah chatbot berbasis aturan (regex) dengan konteks percakapan sederhana dan reflection kata ganti.  
Chatbot ini dikembangkan untuk memberikan tips kesehatan seputar **diet, latihan, dan relaksasi** dengan cara yang natural dan ramah.  

- Integrasi dilakukan menggunakan **Discord API** melalui library [`discord.py`](https://discordpy.readthedocs.io/).
- Output akhir kami adalah Chatbot interaktif yang bisa diakses via Discord [`https://discord.gg/X88wTgkX`](https://discord.gg/X88wTgkX).
- Untuk penjelasan lebih lengkapnya, silakan kunjungi [`bit.ly/PPTSickSuckHealth`](https://bit.ly/PPTSickSuckHealth).

---

## 🧑‍💻 Tim NLP
- Rani Nirmala Prakoso (22/493982/TK/54153)
- Barbara Neanake Ajiesti (22/494495/TK/54238)

---

## Fitur
- Chatbot rule-based dengan regex dan state sederhana.
- Reflection kata ganti (contoh: "saya" → "kamu").
- Topik tips: **Diet**, **Latihan**, dan **Relaksasi**.
- Konteks percakapan multi-turn (bot ingat state user).
- Bisa dijalankan via **CLI (Command Line)** untuk testing tanpa Discord.
- Integrasi dengan **Discord bot** untuk deployment nyata.

---

## Struktur Proyek
```plaintext
sick-suck-health-chat-bot/
├── ssh.py          # Core chatbot + integrasi Discord
├── test_cli.py     # CLI testing tanpa Discord
├── test/           # Unit tests
│   ├── __init__.py
│   └── test_chatbot.py
├── logs/           # Folder log
│   └── bot.log
├── .env.example    # Contoh konfigurasi token
└── README.md       # Dokumentasi
```
---

## ⚙️ Setup & Run 

### 1. Clone Repo
```bash
git clone https://github.com/<username>/sick-suck-health-chat-bot.git
cd sick-suck-health-chat-bot
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```
Minimal requirements:
- discord.py
- python-dotenv

### 3. Konfigurasi Token
Buat file .env di root folder:
```bash
DISCORD_TOKEN=your_discord_bot_token_here
```
Jangan pernah commit .env.
Gunakan .env.example sebagai template.

### 4. Run di CLI (tanpa Discord)
```bash
python test_cli.py
```

### 5. Run di Discord
```bash
python ssh.py
```
Jika berhasil, bot akan login dan siap menerima pesan:
- Mention bot → @SickSuckHealth hai
- Atau gunakan prefix → !tanya diet

---

## Testing
Unit tests tersedia di folder tests/.

Jalankan dengan:
```bash
python -m unittest discover -s tests -p "test_*.py" -v
```
---

## 📸 Demo
<img width="1080" height="690" alt="image" src="https://github.com/user-attachments/assets/38c26b35-bfa8-4edd-b4f7-89d8640c8871" />
<img width="1080" height="690" alt="image" src="https://github.com/user-attachments/assets/ec361d9c-0aed-4810-85ae-507952bfe70e" />

---

## 📖 Notes
- Bot ini hanya prototipe berbasis aturan (rule-based), bukan NLP canggih.
- Fokus utama: regex, reflection, dan integrasi platform.
- Token dan kredensial jangan pernah dipush ke repo publik.

