# SARP Linggo Next

[![Build](https://github.com/AzeoLXC/SARP-Linggo-Next/actions/workflows/build.yml/badge.svg)](https://github.com/AzeoLXC/SARP-Linggo-Next/actions/workflows/build.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

English | [Bahasa Indonesia](README-id.md)

---

Real-time contextual translation overlay for GTA SA-MP and CodSMP. Intercepts incoming chat log lines and outbound clipboard or voice input, translating dialogue via Groq API.

## Features

- Real-time chatlog streaming for SA-MP (`chatlog.txt`) and CodSMP (`/logs/*.txt`)
- Inbound translation: foreign dialogue, `/me`, and `/do` translated into Indonesian
- Outbound translation: Indonesian clipboard text translated into English (Standard or Street Slang)
- Push-to-talk voice input via Whisper API
- Transparent HUD overlay with click-through mode and hotkey visibility toggle

## Architecture

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

## Requirements

- Python 3.10 to 3.12 (64-bit)
- Groq API Key

## Setup

```bash
git clone https://github.com/AzeoLXC/SARP-Linggo-Next.git
cd SARP-Linggo-Next
pip install -r requirements.txt
python main.py
```

## Build Binary

```bash
pyinstaller --noconfirm --onefile --windowed --name "SARP-Linggo-Next" --collect-all PyQt6 --hidden-import=sounddevice --hidden-import=_sounddevice --hidden-import=numpy --hidden-import=requests --hidden-import=keyboard --hidden-import=pyperclip main.py
```

## Keybindings

| Key | Action |
| :--- | :--- |
| `F7` | Toggle overlay visibility |
| `F4` | Push-to-talk voice input (hold to record) |
| `CTRL + C` | Copy Indonesian text to trigger outbound translation |
| `CTRL + V` | Paste translated English text in-game |

## Configuration

1. Click **Settings** in the overlay header.
2. Enter your Groq API key.
3. Configure your chatlog path or enable CodSMP tracking.
4. Save and apply.

## License

MIT
