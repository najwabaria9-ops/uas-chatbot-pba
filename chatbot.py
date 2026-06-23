import os
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

# Memuat variabel lingkungan dari file .env
load_dotenv()

# Mengambil API Key dari .env
API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY or API_KEY == "your_api_key_here":
    print("[ERROR] API Key Gemini belum dikonfigurasi di file .env!")
    print("Silakan buka file .env dan masukkan API Key yang valid.")
    exit()

# Inisialisasi Google Gemini Client
client = genai.Client(api_key=API_KEY)

# Definisi System Prompt (Persona Guru Bahasa Arab)
PERSONA_PROMPT = """
Kamu adalah 'Kamus Hidup', seorang tutor/guru Bahasa Arab yang ramah, interaktif, dan ahli dalam mengajarkan Maharah Mufradat (kosakata) untuk tingkat Pemula.
Tugas utama kamu adalah membantu mahasiswa belajar kosakata Arab sesuai dengan topik yang mereka pilih.
Gaya bahasa kamu harus pedagogis, memotivasi, menggunakan campuran Bahasa Indonesia dan kosakata Arab yang jelas beserta artinya.
Berikan respons yang terstruktur, tidak terlalu panjang, dan selalu ajak pengguna berinteraksi atau berikan kuis kecil di akhir responsmu untuk menguji pemahaman mereka.
"""

def main():
    print("==================================================")
    print("     === UAS CHATBOT PEMBELAJARAN BAHASA ARAB === ")
    print("          Persona: Kamus Hidup (Mufradat)        ")
    print("==================================================")
    print("Selamat datang! Saya adalah Kamus Hidup, tutor Arabmu.\n")
    
    # Fitur Minimum: 3 Mode/Topik Pembelajaran
    print("Silakan pilih topik pembelajaran hari ini:")
    print("1. Al-Mufradat al-Yaumiyyah (Kosakata Sehari-hari)")
    print("2. Fil-Madrasah (Kosakata di Lingkungan Sekolah)")
    print("3. Fil-Uthlah (Kosakata tentang Liburan)")
    print("--------------------------------------------------")
    print("Ketik 'keluar' atau 'exit' untuk menyudahi aplikasi.\n")

    topik_pilihan = ""
    while topik_pilihan not in ["1", "2", "3"]:
        pilihan = input("Pilih nomor topik (1/2/3): ").strip()
        if pilihan.lower() in ['keluar', 'exit']:
            print("\nKamus Hidup: Syukran! Sampai jumpa lagi. Ma'as salamah!")
            return
        if pilihan in ["1", "2", "3"]:
            topik_pilihan = pilihan
        else:
            print("Pilihan tidak valid. Silakan masukkan angka 1, 2, atau 3.")

    topik_nama = {
        "1": "Kosakata Sehari-hari (Al-Mufradat al-Yaumiyyah)",
        "2": "Kosakata Lingkungan Sekolah (Fil-Madrasah)",
        "3": "Kosakata Liburan (Fil-Uthlah)"
    }[topik_pilihan]

    print(f"\n[Sistem] Anda masuk ke mode: {topik_nama}")
    print("Kamus Hidup: Sesi dimulai! Silakan tanyakan kosakata atau sapa saya untuk memulai belajar.")

    # Fitur Minimum: Menyimpan Riwayat Percakapan (Conversation History) dalam satu sesi
    history = [
        {"role": "user", "parts": [{"text": PERSONA_PROMPT}]},
        {"role": "model", "parts": [{"text": f"Baik, saya siap mengajar sebagai Kamus Hidup untuk topik {topik_nama}."}]}
    ]

    while True:
        user_input = input("\nKamu: ").strip()
        if not user_input:
            continue
            
        if user_input.lower() in ['keluar', 'exit']:
            print("\nKamus Hidup: Alhamdulillah, sesi belajar selesai. Semangat terus belajarnya! Ma'as salamah!")
            break

        # Menambahkan input user ke riwayat
        history.append({"role": "user", "parts": [{"text": user_input}]})

        try:
            # Mengirimkan riwayat percakapan ke API Gemini
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=history
            )
            
            bot_response = response.text
            print(f"\nKamus Hidup: {bot_response}")
            
            # Menambahkan respons bot ke riwayat agar konteks terjaga
            history.append({"role": "model", "parts": [{"text": bot_response}]})

        except Exception as e:
            print(f"\n[Sistem Error] Gagal terhubung ke Gemini API: {e}")
            print("Pastikan API Key di file .env sudah benar dan koneksi internet aktif.")
            break

if __name__ == "__main__":
    main()