import requests
import json
import re
from PyQt6.QtCore import QThread, pyqtSignal, QObject

INDONESIAN_MARKERS = {
    "apa", "apakah", "siapa", "dimana", "kapan", "mengapa", "kenapa", "bagaimana",
    "gimana", "kamu", "saya", "aku", "dia", "mereka", "kita", "kami", "anda", "ini",
    "itu", "yang", "dan", "atau", "tidak", "gak", "nggak", "ngga", "ga", "tak", "bukan",
    "ada", "bisa", "bila", "jika", "kalau", "sudah", "udah", "belum", "akan", "mau",
    "ingin", "harus", "adalah", "lagi", "sedang", "dapat", "sama", "dengan", "ke",
    "di", "dari", "untuk", "pada", "kabar", "baik", "tolong", "makasih", "terima",
    "kasih", "mas", "mbak", "gan", "min", "halo", "selamat", "pagi", "siang", "malam",
    "sore", "iya", "ya", "enggak", "gua", "gue", "lu", "sampe", "sampai", "bener",
    "benar", "sih", "dong", "kan", "lah", "deh", "kok", "noh", "tuh", "nih", "nanti",
    "kemarin", "besok", "mana", "sini", "situ", "sana", "brapa", "berapa", "bang",
    "orang", "kerja", "jalan", "makan", "minum", "beli", "jual", "rumah", "mobil", "motor",
    "sepertinya", "kehabisan", "bensin", "kayaknya", "rasanya", "pasti", "bikin", "buat",
    "lihat", "pergi", "datang", "naik", "turun", "bawa", "polisi", "senjata", "peluru",
    "buka", "tutup", "mati", "hidup", "rusak", "bakar", "hilang", "cari", "temu", "tarik",
    "dorong", "pukul", "tendang", "lari", "duduk", "tidur", "bangun", "serang", "kabur",
    "kelakuan", "mu", "sungguh", "memalukan", "parah", "banget", "parahbanget", "anjir",
    "anjg", "jir", "jirrr", "panteq", "pantek", "goblok", "tolol", "bego", "kontol",
    "memek", "peler", "bgst", "asli", "wkwk", "wkwkwk", "woi", "woii", "bro", "bray"
}

def is_indonesian_text(text):
    if not text:
        return False

    clean_text = text.lower().strip()
    words = re.findall(r'\b[a-z]{2,}\b', clean_text)
    if not words:
        return False

    match_count = sum(1 for w in words if w in INDONESIAN_MARKERS)
    ratio = match_count / len(words)

    if match_count >= 1 and (ratio >= 0.15 or len(words) <= 5):
        return True

    return False


class UniversalAITranslator(QObject):
    """
    Universal Contextual Translation Engine.
    Compatible with OpenAI-compatible Chat Completion API endpoints (Groq, OpenAI, DeepSeek, OpenRouter, Local Ollama, Custom).
    Supports API key rotation and dynamic rate-limit parsing.
    """

    def __init__(self, api_key="", endpoint="https://api.groq.com/openai/v1/chat/completions",
                 model="openai/gpt-oss-120b", target_lang="Indonesian",
                 stt_endpoint="https://api.groq.com/openai/v1/audio/transcriptions",
                 stt_model="whisper-large-v3-turbo"):
        super().__init__()
        self.api_key = api_key
        self.endpoint = endpoint if endpoint else "https://api.groq.com/openai/v1/chat/completions"
        self.model = model if model else "openai/gpt-oss-120b"
        self.target_lang = target_lang
        self.stt_endpoint = stt_endpoint
        self.stt_model = stt_model
        self.last_rpd_remaining = None
        self.last_rpd_limit = None
        self.last_rpd_reset = None

    def set_api_key(self, api_key):
        self.api_key = api_key

    def set_endpoint(self, endpoint):
        self.endpoint = endpoint if endpoint else "https://api.groq.com/openai/v1/chat/completions"

    def set_model(self, model):
        self.model = model if model else "openai/gpt-oss-120b"

    def set_target_lang(self, target_lang):
        self.target_lang = target_lang

    def set_stt_config(self, stt_endpoint, stt_model):
        self.stt_endpoint = stt_endpoint
        self.stt_model = stt_model

    def _get_api_keys(self):
        if not self.api_key:
            return [""] if "localhost" in self.endpoint or "127.0.0.1" in self.endpoint else []
        keys = re.split(r'[\s,\n]+', self.api_key.strip())
        return [k for k in keys if k]

    def _send_api_request(self, payload_messages, temperature=0.1):
        keys = self._get_api_keys()
        if not keys:
            return None, "[API Key Not Set]"

        active_model = self.model if self.model else "openai/gpt-oss-120b"

        for key in keys:
            headers = {
                "Content-Type": "application/json",
                "User-Agent": "SARP-Linggo-Next/1.0"
            }
            if key:
                headers["Authorization"] = f"Bearer {key}"

            payload = {
                "model": active_model,
                "messages": payload_messages,
                "temperature": temperature,
                "max_tokens": 2000
            }
            try:
                response = requests.post(self.endpoint, headers=headers, json=payload, timeout=15.0)

                rem = response.headers.get("x-ratelimit-remaining-requests") or response.headers.get("x-ratelimit-remaining")
                lim = response.headers.get("x-ratelimit-limit-requests") or response.headers.get("x-ratelimit-limit")
                rst = response.headers.get("x-ratelimit-reset-requests") or response.headers.get("x-ratelimit-reset")
                if rem is not None:
                    try:
                        self.last_rpd_remaining = int(rem)
                    except ValueError:
                        self.last_rpd_remaining = rem
                if lim is not None:
                    try:
                        self.last_rpd_limit = int(lim)
                    except ValueError:
                        self.last_rpd_limit = lim
                if rst is not None:
                    self.last_rpd_reset = str(rst)

                if response.status_code == 200:
                    result_json = response.json()
                    out_text = result_json["choices"][0]["message"]["content"].strip()

                    out_text = re.sub(r'<think>.*?(?:</think>|$)', '', out_text, flags=re.DOTALL).strip()
                    out_text = re.sub(r"^Here's a thinking process:.*$", "", out_text, flags=re.MULTILINE | re.IGNORECASE).strip()
                    out_text = out_text.strip('"`*')

                    out_text = re.sub(r'\bmotherf[*#@%]+er\b', 'motherfucker', out_text, flags=re.IGNORECASE)
                    out_text = re.sub(r'\bmotherf[*#@%]+ers\b', 'motherfuckers', out_text, flags=re.IGNORECASE)
                    out_text = re.sub(r'\bf[*#@%]+k\b', 'fuck', out_text, flags=re.IGNORECASE)
                    out_text = re.sub(r'\bf[*#@%]+king\b', 'fucking', out_text, flags=re.IGNORECASE)
                    out_text = re.sub(r'\bf[*#@%]+ker\b', 'fucker', out_text, flags=re.IGNORECASE)
                    out_text = re.sub(r'\bb[*#@%]+ch\b', 'bitch', out_text, flags=re.IGNORECASE)
                    out_text = re.sub(r'\bb[*#@%]+ches\b', 'bitches', out_text, flags=re.IGNORECASE)
                    out_text = re.sub(r'\ba[*#@%]+s\b', 'ass', out_text, flags=re.IGNORECASE)
                    out_text = re.sub(r'\ba[*#@%]+shole\b', 'asshole', out_text, flags=re.IGNORECASE)
                    out_text = re.sub(r'\bn[*#@%]+ga\b', 'nigga', out_text, flags=re.IGNORECASE)
                    out_text = re.sub(r'\bn[*#@%]+gas\b', 'niggas', out_text, flags=re.IGNORECASE)

                    if "thinking process" in out_text.lower() or "\n1. " in out_text:
                        lines = [l.strip() for l in out_text.split("\n") if l.strip() and not re.match(r'^(\d+\.|\*|-|#)', l.strip())]
                        if lines:
                            out_text = lines[-1].strip('"`*')

                    out_text = out_text.replace("—", ", ").replace("–", ", ").replace(" -- ", ", ").replace("--", ", ")
                    out_text = re.sub(r',\s*,', ',', out_text)
                    out_text = re.sub(r'\s+', ' ', out_text).strip()

                    if out_text:
                        return out_text, None
                elif response.status_code in (429, 401):
                    continue
            except Exception as e:
                print(f"[AI Translator Error] {e}", flush=True)
                continue

        return None, "[Translation Error]"

    def transcribe_audio(self, audio_bytes):
        keys = self._get_api_keys()
        if not keys:
            return None, "[API Key Not Set]"

        endpoint = self.stt_endpoint if self.stt_endpoint else "https://api.groq.com/openai/v1/audio/transcriptions"
        stt_model = self.stt_model if self.stt_model else "whisper-large-v3-turbo"

        for key in keys:
            headers = {
                "User-Agent": "SARP-Linggo-Next/1.0"
            }
            if key:
                headers["Authorization"] = f"Bearer {key}"

            files = {
                'file': ('speech.wav', audio_bytes, 'audio/wav'),
                'model': (None, stt_model),
                'language': (None, 'id'),
                'prompt': (None, 'Percakapan Bahasa Indonesia SAMP Roleplay: /me, /do, slash me, slash do, dasar, mahluk, manusia, kamu, lu, gue, bangsat, anjing, kontol, bajingan.'),
                'response_format': (None, 'json')
            }
            try:
                response = requests.post(endpoint, headers=headers, files=files, timeout=12.0)
                if response.status_code == 200:
                    result_json = response.json()
                    raw_text = result_json.get("text", "").strip()
                    if raw_text:
                        return raw_text, None
                elif response.status_code in (429, 401):
                    continue
            except Exception as e:
                print(f"[STT Error] {e}", flush=True)
                continue

        return None, "[Voice Transcription Failed]"

    def check_rpd_quota(self):
        keys = self._get_api_keys()
        if not keys:
            return False, "API Key is empty", None, None, None

        active_model = self.model if self.model else "openai/gpt-oss-120b"
        for key in keys:
            headers = {
                "Content-Type": "application/json",
                "User-Agent": "SARP-Linggo-Next/1.0"
            }
            if key:
                headers["Authorization"] = f"Bearer {key}"

            payload = {
                "model": active_model,
                "messages": [{"role": "user", "content": "ping"}],
                "max_tokens": 1
            }
            try:
                response = requests.post(self.endpoint, headers=headers, json=payload, timeout=6.0)
                rem = response.headers.get("x-ratelimit-remaining-requests") or response.headers.get("x-ratelimit-remaining")
                lim = response.headers.get("x-ratelimit-limit-requests") or response.headers.get("x-ratelimit-limit")
                rst = response.headers.get("x-ratelimit-reset-requests") or response.headers.get("x-ratelimit-reset")

                if rem is not None:
                    try:
                        self.last_rpd_remaining = int(rem)
                    except ValueError:
                        self.last_rpd_remaining = rem
                if lim is not None:
                    try:
                        self.last_rpd_limit = int(lim)
                    except ValueError:
                        self.last_rpd_limit = lim
                if rst is not None:
                    self.last_rpd_reset = str(rst)

                if response.status_code == 200:
                    return True, "Connected", self.last_rpd_remaining, self.last_rpd_limit, self.last_rpd_reset
                elif response.status_code == 401:
                    return False, "Invalid API Key (401)", None, None, None
                elif response.status_code == 429:
                    return False, "Rate Limited (429)", 0, self.last_rpd_limit, self.last_rpd_reset
            except Exception as e:
                return False, f"Connection Failed ({e})", None, None, None
        return False, "Quota Check Failed", None, None, None

    def translate(self, text, chat_type="SAYS"):
        if not text or not text.strip():
            return text

        clean_text = text.strip()

        system_prompt = (
            f"You are a street slang and roleplay translation engine for GTA SA-MP.\n\n"
            f"DIRECTIVES:\n"
            f"1. Analyze the full sentence context and subculture intent, then output fluent {self.target_lang}.\n"
            f"2. Retain authentic conversational tone (e.g. lu, gue, lapak, isilop, senpi, mampus, bangsat, anjing).\n"
            f"3. Do not censor profanities with asterisks.\n"
            f"4. Maintain correct pronoun mapping:\n"
            f"   - 'you / your' -> 'lu' or 'kamu' (never 'gue')\n"
            f"   - 'I / me / my' -> 'gue' or 'aku' (never 'lu')\n"
            f"   - 'we / us' -> 'kita' or 'kami'\n"
            f"   - 'they / them' -> 'mereka'\n"
            f"5. If input is already {self.target_lang}, return as is.\n"
            f"6. Output ONLY the translated sentence without quotes or explanations."
        )

        few_shot_inbound = [
            ("You're drivin like a straight-up fool.", "Lu nyetir kayak orang gila."),
            ("I'm gonna come at you.", "Gue bakal nyamperin lu."),
            ("I told you not to move.", "Gue udah bilang ke lu jangan bergerak."),
            ("You think you can run from me?", "Lu kira lu bisa kabur dari gue?"),
        ]

        messages = [{"role": "system", "content": system_prompt}]
        for user_ex, asst_ex in few_shot_inbound:
            messages.append({"role": "user", "content": user_ex})
            messages.append({"role": "assistant", "content": asst_ex})
        messages.append({"role": "user", "content": clean_text})

        result, err = self._send_api_request(messages, temperature=0.1)
        return result if result else err

    def translate_outbound(self, text, style="Standard English"):
        if not text or not text.strip():
            return text

        clean_text = text.strip()
        active_style = style if style in ("Standard English", "American Hood") else "Standard English"

        me_flavor = {
            "Standard English": "fluent English third-person present tense descriptive roleplay action",
            "American Hood": "gritty African-American hood / street gangster style third-person present tense action"
        }[active_style]

        do_flavor = {
            "Standard English": "fluent English descriptive roleplay environment/state",
            "American Hood": "gritty hood / street gangster style environment/state"
        }[active_style]

        dialogue_instruction = {
            "Standard English": "Translate the Indonesian sentence into natural, clear Standard English for GTA SA-MP roleplay.",
            "American Hood": "Translate the Indonesian sentence into authentic African-American Hood / Street Gangster English without censorship."
        }[active_style]

        few_shot_me = {
            "Standard English": [
                ("/me mengambil pistol dari sakunya", "/me reaches into his pocket and draws his pistol"),
                ("/me menyalakan rokok", "/me lights up a cigarette"),
            ],
            "American Hood": [
                ("/me mengambil pistol dari sakunya", "/me reaches into his waistband and grips his blicky"),
                ("/me menyalakan rokok", "/me sparks up a square and takes a long drag"),
            ],
        }[active_style]

        few_shot_do = {
            "Standard English": [
                ("/do apakah pistolnya terlihat?", "/do Is the pistol visible beneath his jacket?"),
            ],
            "American Hood": [
                ("/do apakah pistolnya terlihat?", "/do Can the blicky be spotted tucked in his waistband?"),
            ],
        }[active_style]

        few_shot_dialogue = {
            "Standard English": [
                ("Dasar bodoh, berkendara yang benar tolol.", "You're an idiot, learn how to drive, fool."),
                ("Hei, kamu mau pergi kemana?", "Hey, where are you headed?"),
                ("Angkat tangan, jangan bergerak!", "Hands up, don't move!"),
            ],
            "American Hood": [
                ("Dasar bodoh, berkendara yang benar tolol.", "Bruh you stupid as hell, learn how to drive, fool."),
                ("Hei, kamu mau pergi kemana?", "Aye, where you finna go, homie?"),
                ("Angkat tangan, jangan bergerak!", "Put ya hands up, don't even think about moving, deadass."),
                ("Aku mau cari masalah sama kamu.", "I'm on yo head, no cap, on god."),
                ("Polisi sedang mendekat, kabur!", "Twelve rollin up, bounce, let's go!"),
            ],
        }[active_style]

        lower_text = clean_text.lower()

        if lower_text.startswith("/me"):
            system_prompt = (
                f"You are a GTA SA-MP roleplay outbound translator converting text into English.\n"
                f"STYLE: {active_style.upper()}\n"
                f"1. Always start output with `/me `.\n"
                f"2. Translate action into {me_flavor}.\n"
                f"3. Do not use first-person pronouns.\n"
                f"4. Output ONLY the translated '/me [ACTION]'."
            )
            shots = few_shot_me

        elif lower_text.startswith("/do"):
            system_prompt = (
                f"You are a GTA SA-MP roleplay outbound translator converting text into English.\n"
                f"STYLE: {active_style.upper()}\n"
                f"1. Always start output with `/do `.\n"
                f"2. Translate environment/state into {do_flavor}.\n"
                f"3. Output ONLY the translated '/do [STATE]'."
            )
            shots = few_shot_do

        else:
            system_prompt = (
                f"You are a GTA SA-MP roleplay outbound translator converting text into English.\n"
                f"STYLE: {active_style.upper()}\n"
                f"INSTRUCTION: {dialogue_instruction}\n"
                f"1. Maintain authentic tone and slang where appropriate.\n"
                f"2. Do not censor profanity with asterisks.\n"
                f"3. Output ONLY the translated English sentence."
            )
            shots = few_shot_dialogue

        messages = [{"role": "system", "content": system_prompt}]
        for user_ex, asst_ex in shots:
            messages.append({"role": "user", "content": user_ex})
            messages.append({"role": "assistant", "content": asst_ex})
        messages.append({"role": "user", "content": clean_text})

        result, err = self._send_api_request(messages, temperature=0.2)
        return result if result else text


# Alias for backward compatibility
GroqTranslator = UniversalAITranslator


class TranslationWorker(QThread):
    """
    Async QThread queue worker to process translation items sequentially.
    """
    translation_complete = pyqtSignal(dict)

    def __init__(self, translator):
        super().__init__()
        self.translator = translator
        self.queue = []
        self.running = True

    def add_job(self, chat_item):
        self.queue.append(chat_item)

    def stop(self):
        self.running = False
        self.wait()

    def run(self):
        import time
        while self.running:
            if self.queue:
                item = self.queue.pop(0)
                original_content = item.get("content", "")
                chat_type = item.get("type", "SAYS")

                if is_indonesian_text(original_content):
                    continue

                translated = self.translator.translate(original_content, chat_type=chat_type)

                clean_orig = original_content.strip().lower()
                clean_trans = translated.strip().lower()
                if clean_orig == clean_trans:
                    continue

                item["translated"] = translated
                item["rpd_remaining"] = self.translator.last_rpd_remaining
                item["rpd_limit"] = self.translator.last_rpd_limit
                item["rpd_reset"] = self.translator.last_rpd_reset
                self.translation_complete.emit(item)
            else:
                time.sleep(0.1)
