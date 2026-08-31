import os
import json
import glob
import sys

if getattr(sys, 'frozen', False):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CONFIG_FILE = os.path.join(BASE_DIR, "config.json")

DEFAULT_CONFIG = {
    "api_provider": "Groq",
    "api_endpoint": "https://api.groq.com/openai/v1/chat/completions",
    "api_key": "",
    "model_name": "openai/gpt-oss-120b",
    "custom_headers": {},
    "chatlog_path": "",
    "target_language": "Indonesian",
    "outbound_style": "Standard English",
    "use_codsmp": True,
    "enable_clipboard_outbound": True,
    "enable_voice_input": True,
    "voice_hotkey": "f4",
    "toggle_visibility_hotkey": "f7",
    "font_size": 11,
    "opacity": 0.90,
    "always_on_top": True,
    "click_through": False,
    "auto_translate_ic": True,
    "auto_translate_me_do": True,
    "max_feed_items": 50,
    "overlay_x": 100,
    "overlay_y": 100,
    "overlay_width": 440,
    "overlay_height": 320
}

PRESET_PROVIDERS = {
    "Groq": {
        "endpoint": "https://api.groq.com/openai/v1/chat/completions",
        "models": [
            "openai/gpt-oss-120b",
            "openai/gpt-oss-20b",
            "llama-3.3-70b-versatile",
            "llama-3.1-8b-instant",
            "mixtral-8x7b-32768"
        ],
        "stt_endpoint": "https://api.groq.com/openai/v1/audio/transcriptions",
        "stt_model": "whisper-large-v3-turbo"
    },
    "OpenAI": {
        "endpoint": "https://api.openai.com/v1/chat/completions",
        "models": [
            "gpt-4o-mini",
            "gpt-4o",
            "gpt-4.1-mini",
            "gpt-4.1-turbo"
        ],
        "stt_endpoint": "https://api.openai.com/v1/audio/transcriptions",
        "stt_model": "whisper-1"
    },
    "DeepSeek": {
        "endpoint": "https://api.deepseek.com/chat/completions",
        "models": [
            "deepseek-chat",
            "deepseek-reasoner"
        ],
        "stt_endpoint": "",
        "stt_model": ""
    },
    "OpenRouter": {
        "endpoint": "https://openrouter.ai/api/v1/chat/completions",
        "models": [
            "openai/gpt-4o-mini",
            "meta-llama/llama-3.3-70b-instruct",
            "deepseek/deepseek-chat"
        ],
        "stt_endpoint": "",
        "stt_model": ""
    },
    "Ollama (Local)": {
        "endpoint": "http://localhost:11434/v1/chat/completions",
        "models": [
            "llama3.2",
            "llama3.1",
            "qwen2.5",
            "mistral"
        ],
        "stt_endpoint": "",
        "stt_model": ""
    },
    "Custom (OpenAI Compatible)": {
        "endpoint": "",
        "models": [],
        "stt_endpoint": "",
        "stt_model": ""
    }
}


class ConfigManager:
    """Manages application configuration, persistence, and auto-detection."""

    def __init__(self, config_path=CONFIG_FILE):
        self.config_path = config_path
        self.data = DEFAULT_CONFIG.copy()
        self.load()

    def load(self):
        """Loads configuration from JSON file if it exists."""
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, "r", encoding="utf-8") as f:
                    saved_data = json.load(f)
                    self.data.update(saved_data)
            except Exception as e:
                print(f"[Config] Error loading config file: {e}")

        # Migration from old keys
        if "groq_api_key" in self.data and not self.data.get("api_key"):
            self.data["api_key"] = self.data.pop("groq_api_key")
        if "groq_model" in self.data and not self.data.get("model_name"):
            self.data["model_name"] = self.data.pop("groq_model")

        # Auto-detect missing values
        if not self.data.get("chatlog_path") or not os.path.exists(self.data.get("chatlog_path", "")):
            detected_path = self.detect_chatlog_path()
            if detected_path:
                self.data["chatlog_path"] = detected_path

        if not self.data.get("api_key"):
            detected_key = self.detect_api_key()
            if detected_key:
                self.data["api_key"] = detected_key

        self.save()

    def save(self):
        """Saves current configuration to JSON file."""
        try:
            with open(self.config_path, "w", encoding="utf-8") as f:
                json.dump(self.data, f, indent=4)
        except Exception as e:
            print(f"[Config] Error saving config file: {e}")

    def get(self, key, default=None):
        return self.data.get(key, default)

    def set(self, key, value):
        self.data[key] = value
        self.save()

    @staticmethod
    def detect_chatlog_path():
        """Attempts to auto-detect standard SAMP chatlog.txt locations."""
        user_profile = os.environ.get("USERPROFILE", "")
        possible_paths = [
            os.path.join(user_profile, "Documents", "GTA San Andreas User Files", "SAMP", "chatlog.txt"),
            os.path.join(user_profile, "OneDrive", "Documents", "GTA San Andreas User Files", "SAMP", "chatlog.txt"),
            r"C:\Users\Public\Documents\GTA San Andreas User Files\SAMP\chatlog.txt",
        ]
        for path in possible_paths:
            if os.path.exists(path):
                print(f"[Config] Detected SAMP chatlog path: {path}")
                return path
        return possible_paths[0]

    @staticmethod
    def detect_api_key():
        """Detects API key from environment variable or Downloads directory."""
        env_key = os.environ.get("GROQ_API_KEY", "").strip() or os.environ.get("OPENAI_API_KEY", "").strip()
        if env_key:
            return env_key

        user_profile = os.environ.get("USERPROFILE", "")
        downloads_dir = os.path.join(user_profile, "Downloads")
        if os.path.exists(downloads_dir):
            for pattern in ["gsk_*.txt", "sk_*.txt", "key_*.txt"]:
                key_files = glob.glob(os.path.join(downloads_dir, pattern))
                for key_file in key_files:
                    try:
                        with open(key_file, "r", encoding="utf-8") as f:
                            content = f.read().strip()
                            if content:
                                print(f"[Config] Auto-detected API Key from {key_file}")
                                return content
                    except Exception:
                        pass
        return ""
