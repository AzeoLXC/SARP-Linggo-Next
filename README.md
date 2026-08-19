# SA-RP Linggo

[![Build & Release](https://github.com/AzeoLXC/SARP-Linggo-Next/actions/workflows/build.yml/badge.svg)](https://github.com/AzeoLXC/SARP-Linggo-Next/actions/workflows/build.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)

**[English](#english)** | **[Bahasa Indonesia](#bahasa-indonesia)**

---

<a name="english"></a>
## English

SA-RP Linggo is an open-source, real-time AI translation overlay application designed for GTA San Andreas Multiplayer (SA-MP) and CodSMP players. It provides instantaneous translation of roleplay interactions (Inbound chatlog and Outbound clipboard/voice) with contextual slang translation.

### Key Features

- **AI Engine (openai/gpt-oss-120b)**: Low-latency translation via Groq API.
- **CodSMP and Standard SA-MP Detection**: Automatic detection of logs in `/logs/` directory or default `chatlog.txt`.
- **Uncensored Roleplay Slang Translation**: Preserves authentic street slang without word censorship.
- **Inbound Live Feed**: Displays IC chat, `/me`, and `/do` directly on the overlay.
- **Outbound Translator (Indonesian to English)**: Translates copied text (`CTRL+C`) and automatically copies output for in-game pasting (`CTRL+V`).
- **Voice-to-Text Outbound**: Voice input support via microphone with customizable hotkeys.
- **Glassmorphism HUD**: Frameless, transparent overlay with click-through support.
- **Fully Open Source**: Free of license restrictions and hardware ID locks.

### Running from Source

#### Prerequisites
- Python 3.10 - 3.12
- Git

#### Installation
```bash
git clone https://github.com/AzeoLXC/SARP-Linggo-Next.git
cd SARP-Linggo-Next
pip install -r requirements.txt
```

#### Run Application
```bash
python main.py
```

### Build Standalone Executable (PyInstaller)

Run the following command on Windows:
```bash
pyinstaller --noconfirm --onedir --windowed --name "SA-RP Linggo" --collect-all PyQt6 --hidden-import=sounddevice --hidden-import=_sounddevice --hidden-import=numpy --hidden-import=requests --hidden-import=keyboard --hidden-import=pyperclip main.py
```

The compiled binary will be located in `dist/SA-RP Linggo/`.

### CI / CD (GitHub Actions)

The repository includes `.github/workflows/build.yml` to:
- Automatically compile the Windows binary on push to `main`.
- Upload the compiled archive as a workflow artifact.
- Publish a release asset when a git tag is created (e.g. `v1.0.0`).

### Usage & Keybindings

1. **Configuration**:
   - Obtain a Groq API key from console.groq.com.
   - Open Settings in the overlay and enter the key.
   - Set the chatlog path or enable CodSMP detection.
   - Click Save & Apply.

2. **Hotkeys**:
   - `ALT + L` : Toggle Lock Mode (Click-Through mouse pass-through).
   - `F7` : Toggle Overlay Visibility.
   - `F4` : Push to Talk (Voice Input).
   - `CTRL + C` : Translate copied clipboard text.
   - `CTRL + V` : Paste translated output into chatbox.

---

<a name="bahasa-indonesia"></a>
## Bahasa Indonesia

SA-RP Linggo adalah aplikasi overlay terjemahan real-time berbasis AI untuk pemain GTA San Andreas Multiplayer (SA-MP) dan CodSMP. Menerjemahkan percakapan Roleplay (Inbound Chatlog dan Outbound Clipboard/Voice) secara instan.

### Fitur Utama

- **AI Engine (openai/gpt-oss-120b)**: Kecepatan respon sub-detik melalui Groq API.
- **Deteksi Otomatis CodSMP dan SA-MP Standar**: Mendeteksi file log terbaru di direktori `/logs/` maupun file `chatlog.txt` standar.
- **Uncensored Slang Translation**: Menerjemahkan istilah roleplay dan street slang secara akurat tanpa sensor kata.
- **Inbound Live Feed**: Membaca chat IC, `/me`, dan `/do` langsung pada layar overlay game.
- **Outbound Translator (Indonesian to English)**: Menerjemahkan teks clipboard (`CTRL+C`) dan otomatis menyalin hasil terjemahan untuk ditempelkan ke dalam game (`CTRL+V`).
- **Voice-to-Text Outbound**: Input suara via mikrofon dengan hotkey yang dapat dikonfigurasi.
- **Glassmorphism HUD**: Tampilan overlay frameless, transparan, serta mendukung mode kunci (Click-Through).
- **Open Source**: Bebas lisensi pihak ketiga, tanpa pembatasan hardware ID (HWID).

### Menjalankan dari Source Code

#### Prasyarat
- Python 3.10 - 3.12
- Git

#### Instalasi Dependensi
```bash
git clone https://github.com/AzeoLXC/SARP-Linggo-Next.git
cd SARP-Linggo-Next
pip install -r requirements.txt
```

#### Menjalankan Program
```bash
python main.py
```

### Build Executable Mandiri (PyInstaller)

Jalankan perintah berikut pada terminal Windows:
```bash
pyinstaller --noconfirm --onedir --windowed --name "SA-RP Linggo" --collect-all PyQt6 --hidden-import=sounddevice --hidden-import=_sounddevice --hidden-import=numpy --hidden-import=requests --hidden-import=keyboard --hidden-import=pyperclip main.py
```

File output `.exe` akan tersedia di direktori `dist/SA-RP Linggo/`.

### Integrasi CI / CD (GitHub Actions)

Repositori ini menyertakan alur kerja otomasi di `.github/workflows/build.yml`:
- Mengompilasi executable Windows secara otomatis setiap ada push ke branch `main`.
- Menyimpan hasil kompilasi ke artifact zip.
- Merilis paket instalasi secara otomatis saat pembuatan tag rilis baru (contoh: `v1.0.0`).

### Panduan Penggunaan

1. **Konfigurasi API Key**:
   - Dapatkan Groq API Key di console.groq.com.
   - Buka menu Settings di overlay aplikasi, lalu masukkan API Key.
   - Tentukan lokasi file chatlog atau aktifkan opsi CodSMP.
   - Klik Save & Apply.

2. **Shortcut Keyboard**:
   - `ALT + L` : Toggle Lock Mode (Click-Through mouse tembus ke layar game).
   - `F7` : Sembunyikan / Tampilkan Overlay.
   - `F4` : Push to Talk (Input Suara).
   - `CTRL + C` : Terjemahkan teks yang disalin.
   - `CTRL + V` : Tempel teks hasil terjemahan ke chatbox.

---

## License / Lisensi

Distributed under the MIT License. See [LICENSE](LICENSE) for more details.
