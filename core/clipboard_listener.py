from PyQt6.QtCore import QObject, pyqtSignal, QThread, QTimer
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QClipboard
from core.translator import is_indonesian_text


class OutboundWorker(QThread):
    finished_translation = pyqtSignal(str, str, str)

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
    outbound_translated = pyqtSignal(dict)

    def __init__(self, translator, config_manager):
        super().__init__()
        self.translator = translator
        self.config = config_manager
        self.enabled = self.config.get("enable_clipboard_outbound", True)
        self.last_processed_text = ""
        self.last_translated_text = ""
        self.active_workers = []

        self.clipboard = QApplication.clipboard()
        self.clipboard.dataChanged.connect(self.check_clipboard)

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

        try:
            text = self.clipboard.text().strip()
        except Exception:
            return

        if not text or len(text) < 2:
            return

        if text == self.last_processed_text or text == self.last_translated_text:
            return

        lower_text = text.lower()
        if text.startswith("/") and not (lower_text.startswith("/me ") or lower_text.startswith("/do ") or lower_text == "/me" or lower_text == "/do"):
            return

        if not is_indonesian_text(text):
            return

        self.last_processed_text = text
        style = self.config.get("outbound_style", "Standard English")

        worker = OutboundWorker(self.translator, text, style)
        worker.finished_translation.connect(self.on_worker_finished)
        self.active_workers.append(worker)
        worker.start()

    def on_worker_finished(self, original, translated, style):
        sender = self.sender()
        if sender in self.active_workers:
            self.active_workers.remove(sender)

        if translated and translated != original:
            self.last_translated_text = translated
            self.clipboard.setText(translated, QClipboard.Mode.Clipboard)

            self.outbound_translated.emit({
                "type": "OUTBOUND",
                "original": original,
                "translated": translated,
                "style": style,
                "rpd_remaining": self.translator.last_rpd_remaining,
                "rpd_limit": self.translator.last_rpd_limit,
                "rpd_reset": self.translator.last_rpd_reset
            })
