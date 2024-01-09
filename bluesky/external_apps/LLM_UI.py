# Step 2: Creating the Client Class

from bluesky.network.client import Client

from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QTextEdit
from PyQt5.QtCore import QTimer, Qt


class TextClient(Client):
    def __init__(self):
        super().__init__()
        self.timer = QTimer()
        self.timer.timeout.connect(self.receive)
        self.timer.start(20)

    def event(self, name, data, sender_id):
        if name == b'ECHO':
            text = data['text']
            echobox.echo(text)  # Update the echobox with received text

    def stack(self, text):
        self.send_event(b'STACKCMD', text)

# Step 3: Creating the GUI


class EchoBox(QTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumHeight(150)
        self.setReadOnly(True)
        self.setFocusPolicy(Qt.NoFocus)

    def echo(self, text):
        self.append(text)
        self.verticalScrollBar().setValue(self.verticalScrollBar().maximum())


class CmdLine(QTextEdit):
    def __init__(self, parent=None, client=None):
        super().__init__(parent)
        self.setMaximumHeight(21)
        self.setFocusPolicy(Qt.StrongFocus)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.client = client

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            text = self.toPlainText()
            if self.client:
                self.client.stack(text)
            self.setText('')
        else:
            super().keyPressEvent(event)


# Step 4: Putting It All Together
if __name__ == '__main__':
    app = QApplication([])

    win = QWidget()
    win.setWindowTitle('BlueSky External Application')
    layout = QVBoxLayout()
    win.setLayout(layout)

    echobox = EchoBox(win)
    cmdline = CmdLine(win)
    layout.addWidget(echobox)
    layout.addWidget(cmdline)
    win.show()

    # Create and start BlueSky client
    bsclient = TextClient()
    bsclient.connect(event_port=11000, stream_port=11001)
    cmdline.client = bsclient  # Set the client for the command line

    app.exec_()
