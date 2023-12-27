"""Main Application of the-socket-thing"""
import sys
import threading
from PyQt6.QtWidgets import (
    QMainWindow,
    QApplication,
    QPushButton,
    QVBoxLayout,
    QWidget,
    QFileDialog,
    QLineEdit,
    QLabel,
)
from PyQt6.QtGui import QFont

from receive import start_receiving
from send import configure_server_socket, start_sending


class MainWindow(QMainWindow):
    """Main window of the-socket-thing GUI"""

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("the-socket-thing")
        self.setGeometry(10, 10, 600, 800)
        self.init_ui()

    def init_ui(self):
        """Initialize UI"""
        send_button = self._create_button("Send a file...")
        send_button.clicked.connect(self.handle_send_click)  # type: ignore

        receive_button = self._create_button("Receive a file..")
        receive_button.clicked.connect(self.handle_receive_click)  # type: ignore

        self.main_layout = QVBoxLayout()

        self.main_layout.addWidget(send_button)
        self.main_layout.addWidget(receive_button)

        main_widget = QWidget()
        self._add_stretch()
        main_widget.setLayout(self.main_layout)
        self.setCentralWidget(main_widget)

    def _add_stretch(self):
        self.main_layout.addStretch(1)

    def _get_font(self) -> QFont:
        font = QFont()
        font.setPointSize(50)
        return font

    def _create_button(self, text: str):
        button = QPushButton(text)
        button.setFixedHeight(100)
        button.setFont(self._get_font())
        return button

    def clear_layout(self):
        """Clears the content of the main window"""
        while self.main_layout.count():
            layout_item = self.main_layout.takeAt(0)
            if layout_item:
                widget = layout_item.widget() if layout_item.widget() else None
                if widget:
                    widget.deleteLater()

    def handle_send_click(self):
        """Slot for handling send button clicks"""
        file_path = QFileDialog().getOpenFileName(self)[0]
        sever_socket, share_code = configure_server_socket()
        self.clear_layout()
        label = QLabel(f"Share code: {share_code}")
        label.setFont(self._get_font())
        self.main_layout.addWidget(label)
        self._add_stretch()

        start_sending_thread = threading.Thread(
            target=start_sending,
            args=(sever_socket, file_path),
        )
        start_sending_thread.start()
        self.send_complete()

    def send_complete(self):
        """After send callback"""
        self.clear_layout()
        self.init_ui()

    def handle_receive_click(self):
        """Slot for handling receive button clicks"""
        self.clear_layout()
        share_code_input = QLineEdit(self)
        share_code_input.setFont(self._get_font())
        share_code_input.setPlaceholderText("Enter the share code from sender here...")

        def handle_enter_click():
            share_code = share_code_input.text()
            if share_code:
                server_ip, server_port = share_code.strip().split(":")
                dir_path = QFileDialog(
                    self, "Choose where to store the file"
                ).getExistingDirectory(self)
                start_receiving(server_ip, int(server_port), dir_path)

        share_code_input.returnPressed.connect(handle_enter_click)  # type: ignore
        self.main_layout.addWidget(share_code_input)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    app.exec()
