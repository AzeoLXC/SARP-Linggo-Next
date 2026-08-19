# SA:RP Linggo Next

[![Build & Release](https://github.com/AzeoLXC/SARP-Linggo-Next/actions/workflows/build.yml/badge.svg)](https://github.com/AzeoLXC/SARP-Linggo-Next/actions/workflows/build.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

[English](README.md) | Bahasa Indonesia

---

SA:RP Linggo Next adalah aplikasi overlay penerjemah real-time sumber terbuka (open-source) yang dirancang untuk komunitas roleplay GTA San Andreas Multiplayer (SA-MP) dan CodSMP. Aplikasi ini menangkap percakapan roleplay masuk maupun input keluar (clipboard/suara), menghasilkan terjemahan street slang kontekstual berkecepatan tinggi bertenaga Groq API (`openai/gpt-oss-120b`).

## Fitur Utama

- **Inferensi Sub-detik**: Mesin penerjemah latensi rendah berbasis Groq API.
- **Deteksi Sumber Log Otomatis**: Mendeteksi log aktif pada CodSMP (`/logs/*.txt`) maupun file SA-MP standar (`chatlog.txt`).
- **Penerjemahan Slang Kontekstual**: Menerjemahkan bahasa gaul Indonesia ke gaya percakapan roleplay street slang Amerika tanpa sensor kata.
- **Inbound Stream**: Memfilter dan menampilkan obrolan IC, `/me`, dan `/do` langsung pada HUD transparan di atas game.
- **Outbound Stream**: Menangkap teks bahasa Indonesia yang disalin (`CTRL+C`) dan otomatis menggantinya dengan teks terjemahan bahasa Inggris siap tempel (`CTRL+V`).
- **Integrasi Suara ke Teks**: Menangkap audio mikrofon saat tombol ditekan, mentranskripsikannya melalui Whisper API, lalu menyalin hasil terjemahan ke clipboard.
- **Tampilan HUD Modern**: Overlay Qt glassmorphic frameless dengan mode tembus klik (`ALT+L`) dan tombol sembunyikan cepat (`F7`).
- **Bebas Pembatasan**: 100% open-source di bawah lisensi MIT tanpa pemeriksaan HWID atau sistem lisensi berbayar.

## Struktur Kode

```
SARP-Linggo-Next/
├── core/
│   ├── chat_listener.py      # Thread pemantau chatlog & parsing regex
│   ├── clipboard_listener.py # Pemantau clipboard Windows & worker penerjemah
│   ├── config.py             # Pengelola konfigurasi JSON & deteksi path
│   ├── translator.py         # Klien Groq API & orkestrasi prompt
│   └── voice_listener.py     # Perekam audio mikrofon & transkripsi Whisper
├── ui/
│   ├── icons.py              # Aset ikon vektor SVG
│   ├── overlay.py            # Window overlay utama PyQt6 & dialog pengaturan
│   └── styles.py             # Definisi stylesheet QSS
├── .github/workflows/
│   └── build.yml             # Pipeline otomatis CI/CD GitHub Actions
├── main.py                   # Titik masuk aplikasi & kontrol mutex single-instance
├── requirements.txt          # Dependensi pustaka Python
└── LICENSE                   # Lisensi MIT
```

## Memulai

### Prasyarat

- Python 3.10 hingga 3.12 (disarankan 64-bit)
- Git

### Instalasi

```bash
git clone https://github.com/AzeoLXC/SARP-Linggo-Next.git
cd SARP-Linggo-Next
pip install -r requirements.txt
```

### Menjalankan Aplikasi

```bash
python main.py
```

## Build Executable Mandiri (Single File)

Untuk menghasilkan satu file executable `.exe` menggunakan PyInstaller:

```bash
pyinstaller --noconfirm --onefile --windowed --name "SARP-Linggo-Next" --collect-all PyQt6 --hidden-import=sounddevice --hidden-import=_sounddevice --hidden-import=numpy --hidden-import=requests --hidden-import=keyboard --hidden-import=pyperclip main.py
```

Binary hasil build akan tersimpan di `dist/SARP-Linggo-Next.exe`.

## Pintasan Tombol (Keybindings)

| Tombol | Fungsi |
| :--- | :--- |
| `ALT + L` | Toggle Mode Tembus Klik (mouse tembus langsung ke layar game) |
| `F7` | Toggle Tampilkan / Sembunyikan Overlay (Total Hide) |
| `F4` | Push-to-Talk Input Suara (Tahan untuk merekam, lepas untuk menerjemahkan) |
| `CTRL + C` | Salin teks bahasa Indonesia untuk memicu penerjemahan keluar |
| `CTRL + V` | Tempel teks hasil terjemahan ke dalam kotak obrolan game |

## Konfigurasi

1. Buka aplikasi lalu klik ikon **Settings** (roda gigi) pada header overlay.
2. Masukkan Groq API Key (dapat diperoleh di [console.groq.com](https://console.groq.com/keys)).
3. Periksa atau pilih path `chatlog.txt` SA-MP Anda (atau centang opsi CodSMP).
4. Klik **Save & Apply**.

## Lisensi

Proyek ini didistribusikan di bawah [MIT License](LICENSE).
