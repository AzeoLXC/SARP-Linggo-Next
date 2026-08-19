# SA:RP Linggo Next

[![Build & Release](https://github.com/AzeoLXC/SARP-Linggo-Next/actions/workflows/build.yml/badge.svg)](https://github.com/AzeoLXC/SARP-Linggo-Next/actions/workflows/build.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

English | [Bahasa Indonesia](README-id.md)

---

SA:RP Linggo Next is an open-source real-time translation overlay designed for GTA San Andreas Multiplayer (SA-MP) and CodSMP roleplay environments. It intercepts incoming roleplay dialogues and outbound clipboard/voice inputs, providing low-latency contextual street slang translation powered by Groq API (`openai/gpt-oss-120b`).

## Features

- **Sub-second Inference**: High-throughput translation engine powered by Groq API.
- **Log Source Detection**: Automatically monitors active logs across CodSMP (`/logs/*.txt`) and standard SA-MP (`chatlog.txt`).
- **Contextual Slang Handling**: Translates Indonesian colloquialisms into natural American roleplay slang without word filtering.
- **Inbound Stream**: Filters and renders IC chat, `/me`, and `/do` actions onto a transparent HUD overlay.
- **Outbound Stream**: Intercepts Indonesian clipboard entries (`CTRL+C`) and replaces them with English translations ready for in-game input (`CTRL+V`).
- **Voice-to-Text Pipeline**: Captures push-to-talk microphone audio, transcribes via Whisper API, and injects translations into the clipboard.
- **HUD Interface**: Frameless glassmorphic Qt overlay with click-through lock mode (`ALT+L`) and global toggle hotkey (`F7`).
- **Zero Lock-in**: Fully open source under MIT; no HWID checks or licensing restrictions.

## Architecture

```
SARP-Linggo-Next/
├── core/
│   ├── chat_listener.py      # Chatlog file monitoring & regex parsing thread
│   ├── clipboard_listener.py # Windows clipboard polling & translation worker
│   ├── config.py             # JSON configuration manager & path resolver
│   ├── translator.py         # Groq API client & prompt orchestration
│   └── voice_listener.py     # Continuous audio capture & Whisper transcription
├── ui/
│   ├── icons.py              # SVG vector icon assets
│   ├── overlay.py            # Main PyQt6 transparent HUD & settings dialog
│   └── styles.py             # QSS stylesheet definitions
├── .github/workflows/
│   └── build.yml             # GitHub Actions standalone CI/CD pipeline
├── main.py                   # Entry point & single-instance mutex controller
├── requirements.txt          # Python runtime dependencies
└── LICENSE                   # MIT License
```

## Getting Started

### Prerequisites

- Python 3.10 to 3.12 (64-bit recommended)
- Git

### Installation

```bash
git clone https://github.com/AzeoLXC/SARP-Linggo-Next.git
cd SARP-Linggo-Next
pip install -r requirements.txt
```

### Running Locally

```bash
python main.py
```

## Build Standalone Binary

To produce a single-file executable using PyInstaller:

```bash
pyinstaller --noconfirm --onefile --windowed --name "SARP-Linggo-Next" --collect-all PyQt6 --hidden-import=sounddevice --hidden-import=_sounddevice --hidden-import=numpy --hidden-import=requests --hidden-import=keyboard --hidden-import=pyperclip main.py
```

The output binary will be generated at `dist/SARP-Linggo-Next.exe`.

## Keybindings

| Keybinding | Action |
| :--- | :--- |
| `ALT + L` | Toggle Click-Through Mode (pass mouse clicks directly to the game) |
| `F7` | Toggle Overlay Visibility (Total Hide / Show) |
| `F4` | Push-to-Talk Voice Input (Hold to record, release to translate) |
| `CTRL + C` | Copy Indonesian text to trigger outbound translation |
| `CTRL + V` | Paste translated English text into game chatbox |

## Configuration

1. Launch the application and click the **Settings** (gear icon) on the overlay header.
2. Enter your Groq API Key (obtainable at [console.groq.com](https://console.groq.com/keys)).
3. Verify or manually set your SA-MP `chatlog.txt` path (or enable the CodSMP option).
4. Click **Save & Apply**.

## License

This project is licensed under the [MIT License](LICENSE).
