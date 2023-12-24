import sys
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

from receive import start_receiving
from send import configure_server_socket, start_sending

class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("the-socket-thing")
        self.setGeometry(10, 10, 600, 800)

        send_button = QPushButton("Send a file...")
        send_button.clicked.connect(self.handle_send_click)

        receive_button = QPushButton("Receive a file..")
        receive_button.clicked.connect(self.handle_receive_click)

        self.main_layout = QVBoxLayout()

        self.main_layout.addWidget(send_button)
        self.main_layout.addWidget(receive_button)

        main_widget = QWidget()
        main_widget.setLayout(self.main_layout)
        self.setCentralWidget(main_widget)

    def clear_layout(self):
        while self.main_layout.count():
            self.main_layout.takeAt(0).widget().deleteLater()

    def handle_send_click(self, event):
        file_path = QFileDialog().getOpenFileName(self)[0]
        sever_socket, share_code = configure_server_socket()
        self.clear_layout()
        label = QLabel(f"Share code: {share_code}")
        font = label.font()
        font.setPointSize(50)
        label.setFont(font)
        self.main_layout.addWidget(label)
        start_sending(sever_socket, file_path)

    def handle_receive_click(self, event):
        self.clear_layout()
        share_code_input = QLineEdit(self)
        font = share_code_input.font()
        font.setPointSize(30)
        share_code_input.setFont(font)
        share_code_input.setPlaceholderText("Enter the share code from sender here...")

        def handle_enter_click():
            share_code = share_code_input.text()
            if share_code:
                try:
                    server_ip, server_port = share_code.strip().split(":")
                except:
                    print('Invalid value')
                    return
                dir_path = QFileDialog(self, "Choose where to store the file").getExistingDirectory(self)
                start_receiving(server_ip, int(server_port), dir_path)

        share_code_input.returnPressed.connect(handle_enter_click)
        self.main_layout.addWidget(share_code_input)
        

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    app.exec()
