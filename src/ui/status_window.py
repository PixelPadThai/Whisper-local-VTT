import sys
import os
from PyQt5.QtCore import Qt, pyqtSignal, pyqtSlot, QTimer
from PyQt5.QtGui import QFont, QPixmap, QIcon, QColor
from PyQt5.QtWidgets import QApplication, QLabel, QHBoxLayout, QVBoxLayout

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from ui.base_window import BaseWindow

class StatusWindow(BaseWindow):
    statusSignal = pyqtSignal(str)
    closeSignal = pyqtSignal()

    def __init__(self):
        """
        Initialize the status window.
        """
        super().__init__('WhisperWriter Status', 320, 180)
        self.initStatusUI()
        self.statusSignal.connect(self.updateStatus)

    def initStatusUI(self):
        """
        Initialize the status user interface.
        """
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        
        # Main container
        container = QVBoxLayout()
        container.setContentsMargins(10, 10, 10, 10)
        container.setSpacing(10)
        
        # Status layout (top section)
        status_layout = QHBoxLayout()
        status_layout.setContentsMargins(0, 0, 0, 0)

        self.icon_label = QLabel()
        self.icon_label.setFixedSize(32, 32)
        microphone_path = os.path.join('assets', 'microphone.png')
        pencil_path = os.path.join('assets', 'pencil.png')
        self.microphone_pixmap = QPixmap(microphone_path).scaled(32, 32, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.pencil_pixmap = QPixmap(pencil_path).scaled(32, 32, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.icon_label.setPixmap(self.microphone_pixmap)
        self.icon_label.setAlignment(Qt.AlignCenter)

        self.status_label = QLabel('Recording...')
        self.status_label.setFont(QFont('Segoe UI', 12))

        status_layout.addStretch(1)
        status_layout.addWidget(self.icon_label)
        status_layout.addWidget(self.status_label)
        status_layout.addStretch(1)
        
        # Output status layout (bottom section)
        self.output_status_layout = QVBoxLayout()
        self.output_status_layout.setContentsMargins(5, 0, 5, 0)
        self.output_status_layout.setSpacing(5)
        
        self.output_status_label = QLabel('')
        self.output_status_label.setFont(QFont('Segoe UI', 10))
        self.output_status_label.setWordWrap(True)
        self.output_status_label.setAlignment(Qt.AlignCenter)
        self.output_status_label.hide()  # Initially hidden
        
        self.output_status_layout.addWidget(self.output_status_label)
        
        # Add layouts to container
        container.addLayout(status_layout)
        container.addLayout(self.output_status_layout)

        self.main_layout.addLayout(container)
        
    def show(self):
        """
        Position the window in the bottom center of the screen and show it.
        """
        screen = QApplication.primaryScreen()
        screen_geometry = screen.geometry()
        screen_width = screen_geometry.width()
        screen_height = screen_geometry.height()
        window_width = self.width()
        window_height = self.height()

        x = (screen_width - window_width) // 2
        y = screen_height - window_height - 120

        self.move(x, y)
        super().show()
        
    def closeEvent(self, event):
        """
        Emit the close signal when the window is closed.
        """
        self.closeSignal.emit()
        super().closeEvent(event)

    @pyqtSlot(str)
    def updateStatus(self, status):
        """
        Update the status window based on the given status.
        """
        if status == 'recording':
            self.icon_label.setPixmap(self.microphone_pixmap)
            self.status_label.setText('Recording...')
            self.show()
        elif status == 'transcribing':
            self.icon_label.setPixmap(self.pencil_pixmap)
            self.status_label.setText('Transcribing...')

        if status in ('idle', 'error', 'cancel'):
            self.close()
        
    @pyqtSlot(str, str)
    def updateOutputStatus(self, message, status_type):
        """
        Update the output status section with operation results.
        
        Args:
            message (str): The status message to display
            status_type (str): Type of status ('success' or 'error')
        """
        # Show the output status label if hidden
        self.output_status_label.show()
        
        # Set the message
        self.output_status_label.setText(message)
        
        # Style based on status type
        if status_type == 'success':
            self.output_status_label.setStyleSheet("""
                QLabel {
                    color: #006400;
                    background-color: #E6FFE6;
                    border: 1px solid #C1E1C1;
                    border-radius: 4px;
                    padding: 4px;
                }
            """)
        else:  # error
            self.output_status_label.setStyleSheet("""
                QLabel {
                    color: #8B0000;
                    background-color: #FFE6E6;
                    border: 1px solid #E1C1C1;
                    border-radius: 4px;
                    padding: 4px;
                }
            """)
        
        # Auto-hide the message after 5 seconds
        QTimer.singleShot(5000, self.hideOutputStatus)
    
    def hideOutputStatus(self):
        """Hide the output status message."""
        self.output_status_label.hide()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    status_window = StatusWindow()
    status_window.show()

    # Simulate status updates
    QTimer.singleShot(3000, lambda: status_window.statusSignal.emit('transcribing'))
    QTimer.singleShot(4000, lambda: status_window.updateOutputStatus('Text copied to clipboard', 'success'))
    QTimer.singleShot(6000, lambda: status_window.updateOutputStatus('Text saved to file', 'success'))
    QTimer.singleShot(9000, lambda: status_window.statusSignal.emit('idle'))
    
    sys.exit(app.exec_())
