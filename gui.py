from importlib.metadata import files
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QTextEdit, QStackedWidget,
    QWidget, QLineEdit, QGridLayout, QVBoxLayout,
    QHBoxLayout, QPushButton
)
from PyQt5.QtGui import QIcon, QPainter, QMovie, QColor, QTextCharFormat, QFont, QPixmap, QTextBlockFormat

from PyQt5.QtCore import Qt, QTimer  # QtCore module with correct capitalization
from dotenv import dotenv_values  # dotenv_values comes from python-dotenv

from PyQt5.QtWidgets import QVBoxLayout, QTextEdit, QFrame, QSizePolicy, QLabel
from PyQt5.QtGui import QColor, QTextCharFormat, QFont, QMovie
from PyQt5.QtCore import Qt, QTimer, QSize
import sys
import os

from click import Command

env_vars = dotenv_values(".env")
Assistantname = env_vars.get("assistantname")
current_dir = os.getcwd()
old_chat_messages = ""
TempDirPath = rf"{current_dir}\frontend\files"
GraphicsDirPath = rf"{current_dir}\frontend\graphics"


def AnswerModifier(answer):
    lines = answer.split("\n")
    non_empty_lines = [line for line in lines if line.strip()]
    modified_answer = "\n".join(non_empty_lines)
    return modified_answer


def QueryModifier(query):
    new_query = query.lower().strip()
    query_words = new_query.split()
    question_words = ["how", "what", "who", "where", "when", "why", "which", "whose"]

    if any(new_query.startswith(word) for word in question_words):
        if new_query.endswith(('.', '?', '!')):
            new_query = new_query[:-1] + "?"
        else:
            new_query += "?"
    else:
        if query_words[-1][-1] in ['.', '?', '!']:
            new_query = new_query[:-1] + "."
        else:
            new_query += "."

    return new_query.capitalize()


def SetMicrophoneStatus(command):
    with open(rf'{TempDirPath}\Mic.data', "w", encoding='utf-8') as file:
        file.write(command)


def GetMicrophoneStatus():
    with open(rf'{TempDirPath}\Mic.data', "r", encoding='utf-8') as file:
        status = file.read()
    return status


def SetAssistantStatus(status):
    with open(rf'{TempDirPath}\Status.data', "w", encoding='utf-8') as file:
        file.write(status)


def GetAssistantStatus():
    with open(rf'{TempDirPath}\Status.data', "r", encoding='utf-8') as file:
        status = file.read()
    return status


def MicButtonInitialed():
    SetMicrophoneStatus("False")


def MicButtonClosed():
    SetMicrophoneStatus("True")


def GraphicsDirectoryPath(filename):
    path = rf'{GraphicsDirPath}\{filename}'
    return path


def ShowTextToScreen(Text):
    with open(rf'{TempDirPath}\Response.data', "w", encoding='utf-8') as file:
        class ChatSection(QWidget):
            class ChatSection(QWidget):
                def __init__(self):
                    super(ChatSection, self).__init__()

                    layout = QVBoxLayout(self)
                    layout.setContentsMargins(0, 40, 40, 100)
                    layout.setSpacing(10)

                    self.chat_text_edit = QTextEdit()
                    self.chat_text_edit.setReadOnly(True)
                    self.chat_text_edit.setTextInteractionFlags(Qt.NoTextInteraction)
                    self.chat_text_edit.setFrameStyle(QFrame.NoFrame)
                    layout.addWidget(self.chat_text_edit)

                    self.setStyleSheet("background-color: black;")

                    self.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding))

                    text_color = QColor(Qt.blue)
                    text_color_format = QTextCharFormat()
                    text_color_format.setForeground(text_color)
                    self.chat_text_edit.setCurrentCharFormat(text_color_format)

                    self.gif_label = QLabel()
                    self.gif_label.setStyleSheet("border: none;")
                    movie = QMovie(GraphicsDirectoryPath('farzu.mp4'))  # This should be a GIF, not MP4
                    movie.setScaledSize(QSize(480, 270))
                    self.gif_label.setAlignment(Qt.AlignRight | Qt.AlignBottom)
                    self.gif_label.setMovie(movie)
                    movie.start()
                    layout.addWidget(self.gif_label)

                    self.label = QLabel("")
                    self.label.setStyleSheet(
                        "color: white; font-size: 16px; margin-right: 195px; border: none; margin-top: -30px;")
                    self.label.setAlignment(Qt.AlignRight)
                    layout.addWidget(self.label)

                    font = QFont()
                    font.setPointSize(13)
                    self.chat_text_edit.setFont(font)

                    self.timer = QTimer(self)
                    self.timer.timeout.connect(self.loadMessages)
                    self.timer.timeout.connect(self.SpeechRecogText)
                    self.timer.start(5)

                    self.chat_text_edit.viewport().installEventFilter(self)

                    self.setStyleSheet("""
            QScrollBar:vertical {
                border: none;
                background: black;
                width: 10px;
                margin: 0px 0px 0px 0px;
            }
            QScrollBar::handle:vertical {
                background: white;
                min-height: 20px;
            }
            QScrollBar::add-line:vertical {
                background: black;
                subcontrol-position: bottom;
                subcontrol-origin: margin;
                height: 10px;
            }
            QScrollBar::up-arrow:vertical,
            QScrollBar::down-arrow:vertical {
                border: none;
                background: none;
                color: none;
            }
            QScrollBar::add-page:vertical,
            QScrollBar::sub-page:vertical {
                background: none;
            }
        """)


def loadMessages(self):
    global old_chat_message

    with open(TempDirPath('Responses.data'), "r", encoding='utf-8') as file:
        messages = file.read()

    if messages is None or len(messages) < 1:
        pass
    elif str(old_chat_message) == str(messages):
        pass
    else:
        self.addMessage(message=messages, color='White')
        old_chat_message = messages


def SpeechRecogText(self):
    with open(TempDirPath('Status.data'), "r", encoding='utf-8') as file:
        message = file.read()
        self.label.setText(message)


def load_icon(self, path, width=60, height=60):
    pixmap = QPixmap(path)
    new_pixmap = pixmap.scaled(width, height)
    self.icon_label.setPixmap(new_pixmap)


def toggle_icon(self, event=None):
    if self.toggled:
        self.load_icon(GraphicsDirectoryPath('mic-on.jpeg'), 60, 60)
        MicButtonInitialed()
    else:
        self.load_icon(GraphicsDirectoryPath('mic-off.jpeg'), 60, 60)
        MicButtonClosed()

    self.toggled = not self.toggled


def addMessage(self, message, color):
    cursor = self.chat_text_edit.textCursor()

    char_format = QTextCharFormat()
    block_format = QTextBlockFormat()

    block_format.setTopMargin(10)
    block_format.setLeftMargin(10)

    char_format.setForeground(QColor(color))

    cursor.setCharFormat(char_format)
    cursor.setBlockFormat(block_format)

    cursor.insertText(message + "\n")
    self.chat_text_edit.setTextCursor(cursor)


class InitialScreen(QWidget):
    class MyWidget(QWidget):
        def __init__(self, parent=None):
            super().__init__(parent)

            # Get screen dimensions
            desktop = QApplication.desktop()
            screen_width = desktop.screenGeometry().width()
            screen_height = desktop.screenGeometry().height()

            # Layout
            content_layout = QVBoxLayout()
            content_layout.setContentsMargins(0, 0, 0, 0)

            # GIF Movie
            gif_label = QLabel()
            movie = QMovie(self.GraphicsDirectoryPath('farzu.mp4'))  # Assuming you meant .mp4 or .gif, not .mp3
            max_gif_size_H = int(screen_width / 16 * 9)
            movie.setScaledSize(QSize(screen_width, max_gif_size_H))
            gif_label.setMovie(movie)
            gif_label.setAlignment(Qt.AlignCenter)
            movie.start()
            gif_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

            # Icon label
            self.icon_label = QLabel()
            pixmap = QPixmap(self.GraphicsDirectoryPath('Mic_on.jpeg'))
            new_pixmap = pixmap.scaled(60, 60)
            self.icon_label.setPixmap(new_pixmap)
            self.icon_label.setFixedSize(150, 150)
            self.icon_label.setAlignment(Qt.AlignCenter)

            # Toggle logic
            self.toggled = True
            self.toggle_icon()
            self.icon_label.mousePressEvent = self.toggle_icon_event

            # Speech text label
            self.label = QLabel("")
            self.label.setStyleSheet("color: white; font-size: 16px; margin-bottom: 0;")

            # Add widgets to layout
            content_layout.addWidget(gif_label, alignment=Qt.AlignCenter)
            content_layout.addWidget(self.label, alignment=Qt.AlignCenter)
            content_layout.addWidget(self.icon_label, alignment=Qt.AlignCenter)
            content_layout.setContentsMargins(0, 0, 0, 150)

            self.setLayout(content_layout)
            self.setFixedHeight(screen_height)
            self.setFixedWidth(screen_width)
            self.setStyleSheet("background-color: black;")

            # Timer
            self.timer = QTimer(self)
            self.timer.timeout.connect(self.SpeechRecogText)
            self.timer.start(5)

        def toggle_icon_event(self, event):
            self.toggle_icon()

        def toggle_icon(self):
            # Example toggle logic
            if self.toggled:
                pixmap = QPixmap(self.GraphicsDirectoryPath('Mic_off.jpeg'))
            else:
                pixmap = QPixmap(self.GraphicsDirectoryPath('Mic_on.jpeg'))
            self.icon_label.setPixmap(pixmap.scaled(60, 60))
            self.toggled = not self.toggled


def SpeechRecogText(self):
    with open(TempDirPath('Status.data'), "r", encoding='utf-8') as file:
        messages = file.read()
    self.label.setText(messages)


def load_icon(self, path, width=60, height=60):
    pixmap = QPixmap(path)
    new_pixmap = pixmap.scaled(width, height)
    self.icon_label.setPixmap(new_pixmap)


def toggle_icon(self, event=None):
    if self.toggled:
        self.load_icon(GraphicsDirectoryPath('Mic_on.jpeg'), 60, 60)
        MicButtonInitialed()
    else:
        self.load_icon(GraphicsDirectoryPath('mic-off.jpeg'), 60, 60)
        MicButtonClosed()

    self.toggled = not self.toggled


class MessageScreen(QWidget):
    class MyWindow(QWidget):
        def __init__(self, parent=None):
            super().__init__(parent)

            desktop = QApplication.desktop()
            screen_width = desktop.screenGeometry().width()
            screen_height = desktop.screenGeometry().height()

            layout = QVBoxLayout()

            label = QLabel("")  # QLabel is correct
            layout.addWidget(label)

            ChatSection = ChatSection()  # ✅ CORRECT
            # Make sure ChatSection is defined/imported
            layout.addWidget(ChatSection)

            self.setLayout(layout)
            self.setStyleSheet("background-color: black;")
            self.setFixedHeight(screen_height)
            self.setFixedWidth(screen_width)


from PyQt5.QtWidgets import QWidget


class CustomTopBar(QWidget):
    def __init__(self, parent, stacked_widget):
        super().__init__(parent)
        self.initUI()
        self.current_screen = None
        self.stacked_widget = stacked_widget


def initUI(self):
    self.setFixedHeight(50)  # Fixed typo 'sekf' to 'self'

    layout = QHBoxLayout(self)  # Fixed typo 'QHBoxLAyout'
    layout.setAlignment(Qt.AlignRight)

    home_button = QPushButton()  # Fixed typo 'QpushButton'
    home_icon = QIcon(GraphicsDirectoryPath("Home.jpeg"))  # Fixed typo 'GraphicsDircetoryPath'
    home_button.setIcon(home_icon)
    home_button.setText("Home")
    home_button.setStyleSheet("height:40px; line-height:40px; background-color:white; color: black")

    message_button = QPushButton()  # Fixed typo 'QpushButton'
    message_icon = QIcon(GraphicsDirectoryPath("CHAT.jpeg"))
    message_button.setIcon(message_icon)
    message_button.setText("Chat")  # Fixed typo 'setTExt'
    message_button.setStyleSheet("height:40px; line-height:40px; background-color:white; color: black")

    minimize_button = QPushButton()
    minimize_icon = QIcon(GraphicsDirectoryPath('minimize.jpeg'))
    minimize_button.setIcon(minimize_icon)
    minimize_button.setStyleSheet("background-color: white")
    minimize_button.clicked.connect(self.minimizeWindow)

    self.maximize_button = QPushButton()
    self.maximize_icon = QIcon(GraphicsDirectoryPath('maximize.jpeg'))
    self.restore_icon = QIcon(GraphicsDirectoryPath('minimize.jpeg'))
    self.maximize_button.setIcon(self.maximize_icon)
    self.maximize_button.setFlat(True)
    self.maximize_button.setStyleSheet("background-color:white")
    self.maximize_button.clicked.connect(self.maximizeWindow)

    close_button = QPushButton()
    close_icon = QIcon(GraphicsDirectoryPath('close.jpeg'))
    close_button.setIcon(close_icon)
    close_button.setStyleSheet("background-color: white")
    close_button.clicked.connect(self.closeWindow)

    line_frame = QFrame()
    line_frame.setFixedHeight(1)
    line_frame.setFrameShape(QFrame.HLine)
    line_frame.setFrameShadow(QFrame.Sunken)  # Fixed typo 'Suken'
    line_frame.setStyleSheet("border-color: black;")  # Fixed typo 'broder-coloe'

    title_label = QLabel(f"{str(Assistantname).capitalize()} AI ")  # Fixed typo 'Qlabel'
    title_label.setStyleSheet("color: black; font-size:18px; background-color:white")

    home_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))
    message_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(1))

    layout.addWidget(title_label)
    layout.addStretch(1)  # Fixed typo 'addStrecth'
    layout.addWidget(home_button)
    layout.addWidget(message_button)
    layout.addStretch(1)
    layout.addWidget(minimize_button)
    layout.addWidget(self.maximize_button)
    layout.addWidget(close_button)
    layout.addWidget(line_frame)

    self.draggable = True
    self.offset = None

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.fillRect(self.rect(), Qt.white)

    super().paintEvent('event')

    def minimizeWindow(self):
        self.parent().showMinimized()

    def maximizeWindoe(self):
        if self.parent().isMaximized():
            self.parent().showNormal()
            self.maximize_button.setIcon(self.maximize_icon)
        else:
            self.parent().showMaximized()
        self.maximize_button.setIcon(self.restore_icon)

    def closeWindow(self):
        self.oarent().close()

    def mousePressEvent(self, event):
        if self.draggable:
            self.offset = event.pos()

    def mouseMoveEvent(self, event):
        if self.draggable and self.offset:
            new_pos = event.globalPos() - self.offset

    self.parent().move('new_pos')

    def showMessageScreen(self):
        if self.current_screen is not None:
            self.current_screen.hide()

    message_screen = MessageScreen(self)
    layout = self.parent().layout()
    if layout is not None:
        layout.addWIdget(message_screen)
    self.current_screen = message_screen

    def showInitialScreen(self):
        if self.current_screen is not None:
            self.current_screen.hide()

    initial_screen = InitialScreen(self)
    layout = self.parent().layout()
    if layout is not None:
        layout.addEidget(initial_screen)
    self.current_screen = initial_screen

    class MainWindow(QMainWindow):
        def __init__(self):
            super().__init__()

    self.setWindowFlags(Qt.FramelessWindowHoint)
    self.initUI()


def initUI(self):
    desktop = QApplication.desktop()
    screen_width = desktop.screenGeometry().width()
    screen_height = desktop.screenGeometry().height()  # Fixed typo: 'screen_heigth'

    stacked_widget = QStackedWidget(self)
    initial_screen = InitialScreen()
    message_screen = MessageScreen()
    stacked_widget.addWidget(initial_screen)
    stacked_widget.addWidget(message_screen)

    self.setGeometry(0, 0, screen_width, screen_height)
    self.setStyleSheet("background-color: black;")

    top_bar = top_bar(self, stacked_widget)  # Fixed typo: 'CustopBar' → 'CustomBar'
    self.setMenuWidget(top_bar)  # Fixed typo: 'setMwnuWidget' → 'setMenuWidget'

    self.setCentralWidget(stacked_widget)


def GraphicalUserInterface():
    app = QApplication(sys.argv)
    window = QMainWindow()
    window.show()
    sys.exit(app.exec_())

    if __name__ == "__main__":
        GraphicalUserInterface()

        window.show()
