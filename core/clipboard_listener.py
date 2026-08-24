from PyQt6.QtCore import QObject, pyqtSignal, QThread, QTimer
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QClipboard
from core.translator import is_indonesian_text


class OutboundWorker(QThread):
    finished_translation = pyqtSignal(str, str, str)  # original, translated, style

    def __init__(self, translator, text, style):
        super().__init__()
        self.translator = translator
        self.text = text
        self.style = style

    def run(self):
        try:
            translated = self.translator.translate_outbound(self.text, style=self.style)
            self.finished_translation.emit(self.text, translated, self.style)
        except Exception as e:
            print(f"[ClipboardListener] Translation error: {e}", flush=True)


class ClipboardListener(QObject):
    """
    Monitors Windows Clipboard for copied Indonesian text.
    Translates outbound Indonesian text into English (Standard or Slang)
    and updates clipboard with anti-looping safeguards.
    Supports high-reliability background polling for Windows 10/11.
    """
    outbound_translated = pyqtSignal(dict)  # Emits {'type': 'OUTBOUND', 'original': str, 'translated': str, 'style': str}

    def __init__(self, translator, config_manager, license_manager=None):
        super().__init__()
        self.translator = translator
        self.config = config_manager
        self.license_manager = license_manager
        self.enabled = self.config.get("enable_clipboard_outbound", True)
        self.last_processed_text = ""
        self.last_translated_text = ""
        self.active_workers = []

        # Connect to QApplication clipboard
        self.clipboard = QApplication.clipboard()
        self.clipboard.dataChanged.connect(self.check_clipboard)

        # High-reliability background timer (300ms) for Windows 10/11 non-focused applications
        self.poll_timer = QTimer(self)
        self.poll_timer.setInterval(300)
        self.poll_timer.timeout.connect(self.check_clipboard)
        self.poll_timer.start()

    def set_enabled(self, enabled):
        self.enabled = enabled
        if enabled:
            self.poll_timer.start()
        else:
            self.poll_timer.stop()

    def check_clipboard(self):
        if not self.enabled:
            return

        if self.license_manager and not self.license_manager.is_active():
            return

        try:
            text = self.clipboard.text().strip()
        except Exception:
            return

        if not text or len(text) < 2:
            return

        # Skip if text is already processed or translated
        if text == self.last_processed_text or text == self.last_translated_text:
            return

        lower_text = text.lower()
        # Skip pure system slash commands (except /me and /do roleplay commands)
        if text.startswith("/") and not (lower_text.startswith("/me ") or lower_text.startswith("/do ") or lower_text == "/me" or lower_text == "/do"):
            return

        # Strict Indonesian Language Validation (Prevents translating English back to English)
        if not is_indonesian_text(text):
            return

        self.last_processed_text = text
        style = self.config.get("outbound_style", "Standard English")

        # Run in background QThread to keep UI & Clipboard instant
        worker = OutboundWorker(self.translator, text, style)
        worker.finished_translation.connect(self.on_worker_finished)
        self.active_workers.append(worker)
        worker.start()

    def on_worker_finished(self, original, translated, style):
        # Clean up worker thread
        sender = self.sender()
        if sender in self.active_workers:
            self.active_workers.remove(sender)

        if translated and translated != original:
            self.last_translated_text = translated

            # Set Qt Clipboard directly with explicit Mode.Clipboard
            self.clipboard.setText(translated, QClipboard.Mode.Clipboard)

            # Emit signal for Overlay UI notification
            self.outbound_translated.emit({
                "type": "OUTBOUND",
                "original": original,
                "translated": translated,
                "style": style,
                "rpd_remaining": self.translator.last_rpd_remaining,
                "rpd_limit": self.translator.last_rpd_limit,
                "rpd_reset": self.translator.last_rpd_reset
            })
