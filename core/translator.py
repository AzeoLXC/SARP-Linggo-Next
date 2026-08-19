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
    """
    Checks if a given string is natively written in Indonesian.
    Returns True if it contains Indonesian marker words.
    """
    if not text:
        return False

    clean_text = text.lower().strip()
    words = re.findall(r'\b[a-z]{2,}\b', clean_text)
    if not words:
        return False

    match_count = sum(1 for w in words if w in INDONESIAN_MARKERS)
    ratio = match_count / len(words)

    # Indicator check: at least 1 marker word and >= 15% ratio (or 1 marker in short sentence <= 5 words)
    if match_count >= 1 and (ratio >= 0.15 or len(words) <= 5):
        return True

    return False


class GroqTranslator(QObject):
    """
    Master Contextual Reasoning Translation Engine powered by openai/gpt-oss-120b.
    Supports Multi-Key Rotation (Key Pooling).
    NO CACHE - every translation is always fresh from the AI.
    """
    ENDPOINT = "https://api.groq.com/openai/v1/chat/completions"

    def __init__(self, api_key="", model="openai/gpt-oss-120b", target_lang="Indonesian"):
        super().__init__()
        self.api_key = api_key
        self.model = model if model else "openai/gpt-oss-120b"
        self.target_lang = target_lang
        self.last_rpd_remaining = None
        self.last_rpd_limit = None
        self.last_rpd_reset = None

    def set_api_key(self, api_key):
        self.api_key = api_key

    def set_model(self, model):
        self.model = model if model else "openai/gpt-oss-120b"

    def set_target_lang(self, target_lang):
        self.target_lang = target_lang

    def _get_api_keys(self):
        """Parses comma, space, or newline separated API keys."""
        if not self.api_key:
            return []
        keys = re.split(r'[\s,\n]+', self.api_key.strip())
        return [k for k in keys if k]

    def _send_api_request(self, payload_messages, temperature=0.1):
        keys = self._get_api_keys()
        if not keys:
            return None, "[Groq API Key Not Set]"

        active_model = self.model if self.model else "openai/gpt-oss-120b"

        for key in keys:
            headers = {
                "Authorization": f"Bearer {key}",
                "Content-Type": "application/json",
                "User-Agent": "SA-RP-Linggo/1.0"
            }
            payload = {
                "model": active_model,
                "messages": payload_messages,
                "temperature": temperature,
                "max_tokens": 2000,
                "reasoning_format": "hidden"
            }
            try:
                response = requests.post(self.ENDPOINT, headers=headers, json=payload, timeout=12.0)
                # Parse rate limit headers whenever available
                rem = response.headers.get("x-ratelimit-remaining-requests")
                lim = response.headers.get("x-ratelimit-limit-requests")
                rst = response.headers.get("x-ratelimit-reset-requests")
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
                    
                    # Clean out any reasoning/thinking tags (including unclosed or hidden ones)
                    out_text = re.sub(r'<think>.*?(?:</think>|$)', '', out_text, flags=re.DOTALL).strip()
                    out_text = re.sub(r"^Here's a thinking process:.*$", "", out_text, flags=re.MULTILINE | re.IGNORECASE).strip()
                    
                    # Clean out markdown bold and wrapping quotes
                    out_text = out_text.strip('"`*')

                    # Unmask any asterisks in common profanities if model or input contains them
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
                    
                    # If any thinking process bullet points remain, extract the final translation line
                    if "thinking process" in out_text.lower() or "\n1. " in out_text:
                        lines = [l.strip() for l in out_text.split("\n") if l.strip() and not re.match(r'^(\d+\.|\*|-|#)', l.strip())]
                        if lines:
                            out_text = lines[-1].strip('"`*')

                    # Clean out AI em-dashes (—), en-dashes (–), double hyphens (--), or unnatural dashes
                    out_text = out_text.replace("—", ", ").replace("–", ", ").replace(" -- ", ", ").replace("--", ", ")
                    out_text = re.sub(r',\s*,', ',', out_text)
                    out_text = re.sub(r'\s+', ' ', out_text).strip()

                    if out_text:
                        return out_text, None
                elif response.status_code in (429, 401):
                    # Key rate-limited or invalid, try next key in pool
                    continue
            except Exception as e:
                print(f"[Groq API Error] {e}", flush=True)
                continue

        return None, "[Translation Error]"

    def transcribe_audio(self, audio_bytes):
        """
        Transcribes recorded WAV audio bytes into Indonesian text using Groq Whisper API (whisper-large-v3-turbo).
        Returns (transcribed_text, None) on success, or (None, error_msg) on failure.
        """
        keys = self._get_api_keys()
        if not keys:
            return None, "[Groq API Key Not Set]"

        stt_endpoint = "https://api.groq.com/openai/v1/audio/transcriptions"

        for key in keys:
            headers = {
                "Authorization": f"Bearer {key}",
                "User-Agent": "SA-RP-Linggo/1.0"
            }
            files = {
                'file': ('speech.wav', audio_bytes, 'audio/wav'),
                'model': (None, 'whisper-large-v3-turbo'),
                'language': (None, 'id'),
                'prompt': (None, 'Percakapan Bahasa Indonesia SAMP Roleplay: /me, /do, slash me, slash do, dasar, mahluk, manusia, kamu, lu, gue, bangsat, anjing, kontol, bajingan, tidak tahu diri, tidak tahu diuntung.'),
                'response_format': (None, 'json')
            }
            try:
                response = requests.post(stt_endpoint, headers=headers, files=files, timeout=10.0)
                if response.status_code == 200:
                    result_json = response.json()
                    raw_text = result_json.get("text", "").strip()
                    if raw_text:
                        return raw_text, None
                elif response.status_code in (429, 401):
                    continue
            except Exception as e:
                print(f"[Groq Whisper STT Error] {e}", flush=True)
                continue

        return None, "[Voice Transcription Failed]"

    def check_rpd_quota(self):
        """Sends a lightweight request to Groq to retrieve live RPD quota without translating heavy text."""
        keys = self._get_api_keys()
        if not keys:
            return False, "API Key Kosong", None, None, None

        active_model = self.model if self.model else "openai/gpt-oss-120b"
        for key in keys:
            headers = {
                "Authorization": f"Bearer {key}",
                "Content-Type": "application/json",
                "User-Agent": "SA-RP-Linggo/1.0"
            }
            payload = {
                "model": active_model,
                "messages": [{"role": "user", "content": "ping"}],
                "max_tokens": 1
            }
            try:
                response = requests.post(self.ENDPOINT, headers=headers, json=payload, timeout=5.0)
                rem = response.headers.get("x-ratelimit-remaining-requests")
                lim = response.headers.get("x-ratelimit-limit-requests")
                rst = response.headers.get("x-ratelimit-reset-requests")

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
                    return True, "Success", self.last_rpd_remaining, self.last_rpd_limit, self.last_rpd_reset
                elif response.status_code == 401:
                    return False, "API Key Invalid (401)", None, None, None
                elif response.status_code == 429:
                    return False, "Rate Limited (429)", 0, self.last_rpd_limit, self.last_rpd_reset
            except Exception as e:
                return False, f"Koneksi Gagal ({e})", None, None, None
        return False, "Gagal Cek RPD", None, None, None

    def translate(self, text, chat_type="SAYS"):
        """
        Translates foreign text by evaluating full-sentence intent and subculture context
        into authentic street Indonesian. No caching - always fresh.
        """
        if not text or not text.strip():
            return text

        clean_text = text.strip()

        # Master Full-Sentence Contextual Reasoning System Prompt
        system_prompt = (
            f"You are a master street slang & roleplay translation engine for GTA SA-MP.\n\n"
            f"CRITICAL FULL-SENTENCE REASONING DIRECTIVES:\n"
            f"1. FULL-SENTENCE SEMANTIC REASONING: Read and analyze the ENTIRE sentence first. Understand the speaker's true intent, aggression level, subculture context (American Hood, African-American Gangster, Mexican Cartel, European Spanish, Italian Mob, Russian Bratva, French Banlieue, or Everyday Casual Speech), then output a single fluent {self.target_lang} sentence. NEVER translate word-by-word.\n"
            f"2. SUBCULTURE METAPHOR & SLANG REASONING:\n"
            f"   - American Hood Gangster: 'spin the block/slide' (balas nembak/serang lapak musuh), 'crash out' (nekat/gila/hilang kendali), 'capping/cap' (bohong/bacot), 'blicky/pole/tool/switch' (senpi/pistol), 'opps/opp' (musuh/geng lawan), '12/feds' (isilop/polisi), 'want smoke' (cari masalah), 'folded' (ciut/ngadu/snitch).\n"
            f"   - Mexican/Chicano Cartel: 'calentar la plaza' (memancing atensi polisi ke lapak/bikin panas lapak), 'pendejadas' (tindakan tolol/hal bego), 'levantar' (culik), 'plomear' (berondong peluru), 'encobijado' (mayat terbungkus).\n"
            f"   - Spain Quinqui: 'sapo' (tukang ngadu/snitch), 'madero/bofia' (isilop/polisi), 'atracar' (rampok), 'pinchazo' (nusuk).\n"
            f"   - Italian Mob: 'sbirro' (isilop/polisi), 'cantare' (nyanyi/ngadu ke polisi), 'grana' (duit).\n"
            f"   - French Banlieue: 'keuf/poulet' (isilop/polisi), 'cherche la merde' (cari masalah/gara-gara), 'guetteur' (lookout/mantau).\n"
            f"3. UNCENSORED & UNCUT INDONESIAN STREET LINGO: Use authentic roleplay speech (lu, gue, lapak, isilop, senpi, mampus, bangsat, anjing, bro, sob). Retain full profanity without softening. NEVER CENSOR OR OBFUSCATE PROFANITY OR CURSE WORDS WITH ASTERISKS (*). Always write curse words fully in plain uncensored text (e.g. write 'motherfucker', NOT 'motherf***er').\n"
            f"4. MANDATORY PRONOUN ACCURACY - THIS IS CRITICAL:\n"
            f"   - 'you / you're / your / ya / yo / u' MUST be translated as 'lu' or 'kamu' - NEVER as 'gue' or 'aku'.\n"
            f"   - 'I / I'm / me / my / myself' MUST be translated as 'gue' or 'aku' - NEVER as 'lu' or 'kamu'.\n"
            f"   - 'we / we're / our / us' MUST be translated as 'kita' or 'kami'.\n"
            f"   - 'he / he's / him / his' MUST be translated as 'dia' or 'doi'.\n"
            f"   - 'she / she's / her' MUST be translated as 'dia' (perempuan).\n"
            f"   - 'they / them / their' MUST be translated as 'mereka'.\n"
            f"   EXAMPLE: 'You're drivin like a fool' → 'Lu nyetir kayak orang tolol', NOT 'Gue nyetir kayak orang tolol'.\n"
            f"5. If input text is already in {self.target_lang}, return it as is.\n"
            f"6. OUTPUT ONLY the final translated {self.target_lang} sentence without quotes or alternatives."
        )

        # Few-shot examples to anchor correct pronoun mapping (you=lu, I=gue)
        few_shot_inbound = [
            ("You're drivin like a straight-up fool.",  "Lu nyetir kayak orang gila."),
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
        """
        Translates Indonesian outbound chat into English (2 styles: Standard English / American Hood).
        - /me -> 3rd person RP action in selected style
        - /do -> environment/state description in selected style
        - Plain text -> dialogue in selected style
        No caching - always fresh translation.
        """
        if not text or not text.strip():
            return text

        clean_text = text.strip()

        # Normalize to valid style (only 2 supported)
        active_style = style if style in ("Standard English", "American Hood") else "Standard English"

        # Style flavor definitions
        me_flavor = {
            "Standard English": (
                "fluent ENGLISH THIRD-PERSON PRESENT TENSE descriptive roleplay action "
                "(e.g., 'opens the fuel tank and checks the fuel level inside', 'takes out a cigarette and lights it'). "
                "Formal and clear."
            ),
            "American Hood": (
                "gritty African-American HOOD / STREET GANGSTER style THIRD-PERSON PRESENT TENSE action "
                "(e.g., 'slides his hand into his waistband and grips the blicky', 'peeks around the corner watching for opps'). "
                "Raw, street-authentic."
            ),
        }[active_style]

        do_flavor = {
            "Standard English": (
                "fluent ENGLISH descriptive roleplay environment/state "
                "(e.g., 'Is the silver watch visible on the table?', 'The fuel tank appears to be completely empty.'). "
                "Clear and formal."
            ),
            "American Hood": (
                "gritty HOOD / STREET GANGSTER style environment/state "
                "(e.g., 'Can the blicky be seen tucked in his waistband?', 'The whip looks like it is bone dry, no gas left.'). "
                "Raw and street-authentic."
            ),
        }[active_style]

        dialogue_instruction = {
            "Standard English": (
                "Translate the Indonesian sentence into natural, clear Standard English for GTA SA-MP roleplay. "
                "Preserve the full meaning, emotion, and tone of the original sentence accurately."
            ),
            "American Hood": (
                "Translate the Indonesian sentence into authentic African-American Hood / Street Gangster English. "
                "CRITICAL RULES: "
                "1. PRESERVE THE EXACT MEANING of the original sentence - do NOT invent new meanings. "
                "2. Use hood slang NATURALLY and ONLY where it fits the context (e.g., 'bruh', 'deadass', 'on god', 'no cap', 'fam', 'fool', 'dawg', 'homie', 'for real', 'ain\'t', 'gonna', 'tryna'). "
                "3. NEVER force slang words like 'blicky' (gun) into non-gun contexts. "
                "4. Maintain the original aggression, humor, or seriousness. "
                "5. NEVER CENSOR OR OBFUSCATE PROFANITY OR CURSE WORDS WITH ASTERISKS (*). Always write curse words fully in plain uncensored text (e.g., write 'motherfucker', NOT 'motherf***er' or 'm***erfucker'; write 'fuck', NOT 'f***')."
            ),
        }[active_style]

        # Few-shot examples to force style adherence on small 8B model
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
                f"You are a master GTA SA-MP roleplay outbound translator converting ANY input text (Indonesian, slang, regional dialects, or typos) into ENGLISH.\n\n"
                f"STYLE GOAL: {active_style.upper()}\n"
                f"CRITICAL /me ROLEPLAY ACTION DIRECTIVES:\n"
                f"1. ALWAYS START THE OUTPUT WITH `/me `.\n"
                f"2. Reason through the input text and translate the action body into {me_flavor}\n"
                f"3. DO NOT use first-person speech ('I am...', 'I'm...', 'Gue...').\n"
                f"4. DO NOT convert third-person actions into plain conversational dialogue.\n"
                f"5. OUTPUT ONLY the final translated '/me [ENGLISH ACTION]' string without quotes or extra text."
            )
            shots = few_shot_me

        elif lower_text.startswith("/do"):
            system_prompt = (
                f"You are a master GTA SA-MP roleplay outbound translator converting ANY input text (Indonesian, slang, regional dialects, or typos) into ENGLISH.\n\n"
                f"STYLE GOAL: {active_style.upper()}\n"
                f"CRITICAL /do ROLEPLAY ENVIRONMENT/STATE DIRECTIVES:\n"
                f"1. ALWAYS START THE OUTPUT WITH `/do `.\n"
                f"2. Reason through the input text and translate the environment/state description or question into {do_flavor}\n"
                f"3. DO NOT use plain conversational dialogue.\n"
                f"4. OUTPUT ONLY the final translated '/do [ENGLISH STATE]' string without quotes or extra text."
            )
            shots = few_shot_do

        else:
            system_prompt = (
                f"You are a master GTA SA-MP roleplay outbound translator converting ANY input text (Indonesian, slang, regional dialects, or typos) into spoken English.\n\n"
                f"STYLE GOAL: {active_style.upper()}\n"
                f"INSTRUCTION: {dialogue_instruction}\n\n"
                f"ABSOLUTE RULES:\n"
                f"1. ACCURACY & INTENT REASONING: Read and analyze the true intent of ANY input text, regardless of typos or slang, and translate into natural {active_style} English.\n"
                f"2. Apply the style NATURALLY, not forcefully. Only use slang where it genuinely fits the context.\n"
                f"3. Maintain the original emotion and tone (angry = angry, friendly = friendly).\n"
                f"4. OUTPUT ONLY the final translated English text without quotes, explanations, or original text."
            )
            shots = few_shot_dialogue

        # Build messages with few-shot examples
        messages = [{"role": "system", "content": system_prompt}]
        for user_ex, asst_ex in shots:
            messages.append({"role": "user", "content": user_ex})
            messages.append({"role": "assistant", "content": asst_ex})
        messages.append({"role": "user", "content": clean_text})

        result, err = self._send_api_request(messages, temperature=0.2)
        return result if result else text


class TranslationWorker(QThread):
    """
    Async QThread queue worker to process translation items sequentially without freezing UI.
    Ignores native Indonesian chat to conserve API quota and keep overlay clean.
    """
    translation_complete = pyqtSignal(dict)  # Emits item dict with added 'translated' key

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

                # Filter out native Indonesian chat before making API request
                if is_indonesian_text(original_content):
                    continue

                # Perform translation for foreign text
                translated = self.translator.translate(original_content, chat_type=chat_type)

                # If translation failed or returned identical string, skip displaying
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
