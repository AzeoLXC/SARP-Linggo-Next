MAIN_STYLE = """
QWidget#CentralWidget {
    background-color: rgba(15, 23, 42, 0.94);
    border: 1px solid rgba(51, 65, 85, 0.8);
    border-radius: 6px;
}

QFrame#HeaderFrame {
    background-color: rgba(30, 41, 59, 0.95);
    border-top-left-radius: 6px;
    border-top-right-radius: 6px;
    border-bottom: 1px solid rgba(51, 65, 85, 0.8);
    padding: 3px 6px;
}

QLabel#AppTitle {
    color: #F8FAFC;
    font-weight: 600;
    font-size: 11px;
    letter-spacing: 0.5px;
    font-family: 'Segoe UI', system-ui, sans-serif;
}

QLabel#StatusLabel {
    color: #38BDF8;
    font-size: 10px;
    font-weight: 500;
}

QPushButton.HeaderBtn {
    background-color: rgba(255, 255, 255, 0.04);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 4px;
    color: #94A3B8;
    font-size: 10px;
    font-weight: 500;
    padding: 2px 6px;
    min-height: 22px;
}

QPushButton.HeaderBtn:hover {
    background-color: rgba(56, 189, 248, 0.12);
    border-color: rgba(56, 189, 248, 0.4);
    color: #F8FAFC;
}

QPushButton.HeaderBtn:pressed {
    background-color: rgba(56, 189, 248, 0.2);
}

QPushButton.HeaderBtn[active="true"] {
    background-color: rgba(56, 189, 248, 0.16);
    border-color: #38BDF8;
    color: #38BDF8;
}

QPushButton.HeaderIconBtn {
    background-color: transparent;
    border: 1px solid transparent;
    border-radius: 4px;
    padding: 2px;
    min-width: 22px;
    min-height: 22px;
    max-width: 22px;
    max-height: 22px;
}

QPushButton.HeaderIconBtn:hover {
    background-color: rgba(255, 255, 255, 0.06);
    border-color: rgba(255, 255, 255, 0.12);
}

QPushButton.HeaderIconBtn:pressed {
    background-color: rgba(255, 255, 255, 0.1);
}

QPushButton.HeaderIconBtn#CloseBtn:hover {
    background-color: rgba(239, 68, 68, 0.18);
    border-color: rgba(239, 68, 68, 0.4);
}

QPushButton#LockBtn[locked="true"] {
    background-color: rgba(239, 68, 68, 0.15);
    border-color: #EF4444;
    color: #EF4444;
}

QScrollArea {
    background: transparent;
    border: none;
}

QScrollArea > QWidget > QWidget {
    background: transparent;
}

QScrollBar:vertical {
    border: none;
    background: rgba(15, 23, 42, 0.4);
    width: 4px;
    margin: 0px;
    border-radius: 2px;
}

QScrollBar::handle:vertical {
    background: rgba(148, 163, 184, 0.3);
    min-height: 20px;
    border-radius: 2px;
}

QScrollBar::handle:vertical:hover {
    background: rgba(56, 189, 248, 0.6);
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0px;
}

QFrame.ChatItemCard {
    background-color: rgba(30, 41, 59, 0.6);
    border: 1px solid rgba(51, 65, 85, 0.5);
    border-left: 2px solid #64748B;
    border-radius: 4px;
    margin-bottom: 3px;
    padding: 4px 6px;
}

QFrame.ChatItemCard:hover {
    background-color: rgba(30, 41, 59, 0.85);
    border-color: rgba(71, 85, 105, 0.8);
}

QFrame.ChatItemCard[chat_type="SAYS"] {
    border-left: 2px solid #38BDF8;
}

QFrame.ChatItemCard[chat_type="ME"] {
    border-left: 2px solid #C084FC;
}

QFrame.ChatItemCard[chat_type="DO"] {
    border-left: 2px solid #A855F7;
}

QFrame.ChatItemCard[chat_type="OUTBOUND"] {
    border-left: 2px solid #2DD4BF;
    background-color: rgba(45, 212, 191, 0.08);
}

QFrame.ChatItemCard[chat_type="OUTBOUND_VOICE"] {
    border-left: 2px solid #818CF8;
    background-color: rgba(129, 140, 248, 0.08);
}

QLabel.OrigLine {
    color: #94A3B8;
    font-size: 10px;
    font-family: 'Segoe UI', Arial, sans-serif;
}

QLabel.TransLine {
    font-size: 11px;
    font-weight: 500;
    font-family: 'Segoe UI', Arial, sans-serif;
    color: #F1F5F9;
}

QLabel.TransLine[chat_type="SAYS"] {
    color: #E2E8F0;
}

QLabel.TransLine[chat_type="ME"] {
    color: #F3E8FF;
}

QLabel.TransLine[chat_type="DO"] {
    color: #F5D0FE;
}

QLabel.TransLine[chat_type="OUTBOUND"] {
    color: #CCFBF1;
}

QLabel.TransLine[chat_type="OUTBOUND_VOICE"] {
    color: #E0E7FF;
}

QDialog {
    background-color: #0F172A;
    color: #F8FAFC;
    border: 1px solid #334155;
    border-radius: 6px;
}

QLineEdit, QComboBox, QSpinBox {
    background-color: #1E293B;
    color: #F8FAFC;
    border: 1px solid #334155;
    border-radius: 4px;
    padding: 5px 8px;
    font-size: 11px;
}

QLineEdit:focus, QComboBox:focus, QSpinBox:focus {
    border-color: #38BDF8;
}

QComboBox QAbstractItemView {
    background-color: #1E293B;
    color: #F8FAFC;
    selection-background-color: #334155;
    border: 1px solid #334155;
}

QCheckBox {
    color: #CBD5E1;
    font-size: 11px;
    spacing: 6px;
}

QCheckBox::indicator {
    width: 14px;
    height: 14px;
    border-radius: 3px;
    border: 1px solid #475569;
    background-color: #1E293B;
}

QCheckBox::indicator:checked {
    background-color: #38BDF8;
    border-color: #38BDF8;
}

QLabel {
    color: #CBD5E1;
    font-size: 11px;
}

QSizeGrip {
    width: 10px;
    height: 10px;
    background: transparent;
}
"""
