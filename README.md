# SARP-Linggo-Next

Real-time contextual translation overlay for GTA SA-MP and CodSMP client environments. It streams incoming chat log lines and outbound clipboard or audio inputs, processing translation through OpenAI-compatible Chat Completion API endpoints.

## Overview

SARP-Linggo-Next operates as a transparent desktop overlay over game windows. It captures game text streams and player inputs without modifying game memory, providing instantaneous bidirectional translation between Indonesian and English.

## Key Features

- **Multi-Provider AI Engine**: Native support for Groq, OpenAI, DeepSeek, OpenRouter, local Ollama endpoints, and any custom OpenAI-compatible API base URL.
- **Inbound Stream Translation**: Reads `chatlog.txt` (SA-MP) and active log buffers (CodSMP), parses dialogue, `/me`, and `/do` actions, and translates them to Indonesian.
- **Outbound Clipboard Interception**: Intercepts Indonesian text copied to clipboard (`CTRL+C`), converts it into context-appropriate English (`Standard English` or `American Hood`), and replaces clipboard contents for immediate pasting (`CTRL+V`).
- **Push-to-Talk Voice Input**: Captures microphone audio using `sounddevice`, transcribes via Whisper API endpoint, translates to target style, and populates clipboard.
- **Overlay Window Management**: Frameless PyQt6 interface with Win32 click-through (`WS_EX_TRANSPARENT`), topmost persistence (`WS_EX_TOPMOST`), hotkey visibility toggle, opacity adjustments, and edge resizing.
- **API Key Pooling & Rate Limit Handling**: Supports multi-key rotation and parses standard HTTP rate-limit response headers (`x-ratelimit-remaining-requests`, `x-ratelimit-limit-requests`).

## Architecture

```
SARP-Linggo-Next/
├── core/
│   ├── chat_listener.py      # Chatlog tailing and regex parser for SA-MP / CodSMP
│   ├── clipboard_listener.py # Clipboard monitor and outbound worker dispatcher
│   ├── config.py             # Configuration manager with multi-provider presets
│   ├── licensing.py          # Offline HMAC-based licensing validator
│   ├── translator.py         # Universal OpenAI-compatible AI translation & STT client
│   └── voice_listener.py     # Continuous audio buffer and push-to-talk processor
├── ui/
│   ├── icons.py              # Vector SVG icon renderer
│   ├── overlay.py            # Main PyQt6 overlay, settings dialog, and cards
│   └── styles.py             # QSS stylesheet definitions
├── .github/workflows/
│   └── build.yml             # Automated CI build workflow
├── main.py                   # Application bootstrap and IPC single-instance mutex
├── requirements.txt          # Python runtime dependencies
└── LICENSE                   # MIT License
```

## Supported AI Providers & Models

| Provider | Default Endpoint | Supported Models |
| :--- | :--- | :--- |
| **Groq** | `https://api.groq.com/openai/v1/chat/completions` | `openai/gpt-oss-120b`, `llama-3.3-70b-versatile`, `llama-3.1-8b-instant` |
| **OpenAI** | `https://api.openai.com/v1/chat/completions` | `gpt-4o-mini`, `gpt-4o`, `gpt-4.1-mini`, `gpt-4.1-turbo` |
| **DeepSeek** | `https://api.deepseek.com/chat/completions` | `deepseek-chat`, `deepseek-reasoner` |
| **OpenRouter** | `https://openrouter.ai/api/v1/chat/completions` | `openai/gpt-4o-mini`, `meta-llama/llama-3.3-70b-instruct` |
| **Ollama (Local)** | `http://localhost:11434/v1/chat/completions` | `llama3.2`, `llama3.1`, `qwen2.5`, `mistral` |
| **Custom** | User-defined URL | Any model identifier supported by the endpoint |

## System Requirements

- Windows 10 / Windows 11 (64-bit)
- Python 3.10 to 3.12 (64-bit)
- AI API Key (Groq, OpenAI, DeepSeek, OpenRouter, or Local Ollama)

## Installation and Execution

Clone the repository and install the dependencies:

```bash
git clone git@github.com:AzeoLXC/SARP-Linggo-Next.git
cd SARP-Linggo-Next
pip install -r requirements.txt
python main.py
```

## Packaging

Build a standalone executable using PyInstaller:

```bash
pyinstaller --noconfirm --onefile --windowed \
  --name "SARP-Linggo-Next" \
  --collect-all PyQt6 \
  --hidden-import=sounddevice \
  --hidden-import=_sounddevice \
  --hidden-import=numpy \
  --hidden-import=requests \
  --hidden-import=keyboard \
  --hidden-import=pyperclip \
  main.py
```

## Default Keybindings

| Key | Function |
| :--- | :--- |
| `F7` | Toggle overlay visibility (Show / Hide) |
| `F4` | Push-to-talk voice recording (Hold to record, release to process) |
| `CTRL + C` | Copy Indonesian text to trigger outbound translation |
| `CTRL + V` | Paste translated text in-game |

## Configuration Reference

Configuration parameters stored in `config.json`:

| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `api_provider` | string | `"Groq"` | Active provider preset (`Groq`, `OpenAI`, `DeepSeek`, `OpenRouter`, `Ollama (Local)`, `Custom`) |
| `api_endpoint` | string | `""` | Full URL to Chat Completion endpoint |
| `api_key` | string | `""` | API key (or multiple keys separated by commas/newlines) |
| `model_name` | string | `"openai/gpt-oss-120b"` | Target model ID for translation |
| `chatlog_path` | string | `""` | Absolute path to `chatlog.txt` |
| `use_codsmp` | boolean | `true` | Automatically track newest log in `logs/` directory |
| `target_language` | string | `"Indonesian"` | Inbound translation target language |
| `outbound_style` | string | `"Standard English"` | Outbound style: `Standard English` or `American Hood` |
| `enable_voice_input`| boolean | `true` | Enable voice recording worker |
| `voice_hotkey` | string | `"f4"` | Hotkey for voice input |
| `toggle_visibility_hotkey` | string | `"f7"` | Global hotkey to hide/show overlay |
| `opacity` | float | `0.90` | Window opacity factor (`0.20` - `1.00`) |
| `font_size` | integer | `11` | Font point size in chat feed |

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.
