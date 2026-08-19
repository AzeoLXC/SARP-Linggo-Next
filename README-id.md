# SARP Linggo Next

[![Build](https://github.com/AzeoLXC/SARP-Linggo-Next/actions/workflows/build.yml/badge.svg)](https://github.com/AzeoLXC/SARP-Linggo-Next/actions/workflows/build.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

[English](README.md) | Bahasa Indonesia

---

Aplikasi overlay penerjemah real-time untuk GTA SA-MP dan CodSMP. Memantau chatlog masuk serta input clipboard dan suara keluar menggunakan Groq API.

## Fitur

- Pemantauan chatlog real-time untuk SA-MP (`chatlog.txt`) dan CodSMP (`/logs/*.txt`)
- Terjemahan masuk: percakapan asing, `/me`, dan `/do` ke bahasa Indonesia
- Terjemahan keluar: teks clipboard bahasa Indonesia otomatis diterjemahkan ke bahasa Inggris (Standard atau Street Slang)
- Input suara push-to-talk menggunakan Whisper API
- Overlay HUD transparan dengan mode tembus klik dan tombol toggle visibilitas

## Struktur Direktori

```
SARP-Linggo-Next/
├── core/
│   ├── chat_listener.py
│   ├── clipboard_listener.py
│   ├── config.py
│   ├── translator.py
│   └── voice_listener.py
├── ui/
│   ├── icons.py
│   ├── overlay.py
│   └── styles.py
├── .github/workflows/
│   └── build.yml
├── main.py
├── requirements.txt
└── LICENSE
```

## Prasyarat

- Python 3.10 hingga 3.12 (64-bit)
- Groq API Key

## Instalasi & Menjalankan

```bash
git clone https://github.com/AzeoLXC/SARP-Linggo-Next.git
cd SARP-Linggo-Next
pip install -r requirements.txt
python main.py
```

## Build Executable

```bash
pyinstaller --noconfirm --onefile --windowed --name "SARP-Linggo-Next" --collect-all PyQt6 --hidden-import=sounddevice --hidden-import=_sounddevice --hidden-import=numpy --hidden-import=requests --hidden-import=keyboard --hidden-import=pyperclip main.py
```

## Pintasan Tombol

| Tombol | Aksi |
| :--- | :--- |
| `F7` | Toggle visibilitas overlay |
| `F4` | Input suara push-to-talk (tahan untuk rekam) |
| `CTRL + C` | Salin teks bahasa Indonesia untuk memicu terjemahan keluar |
| `CTRL + V` | Tempel teks hasil terjemahan di dalam game |

## Konfigurasi

1. Klik tombol **Settings** pada header overlay.
2. Masukkan Groq API key.
3. Tentukan path chatlog atau aktifkan pelacakan CodSMP.
4. Klik simpan.

## Lisensi

MIT
