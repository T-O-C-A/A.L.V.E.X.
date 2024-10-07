from PyQt5.QtWidgets import QApplication, QPushButton, QLabel, QVBoxLayout, QWidget
from PyQt5.QtCore import Qt, QRect
import sys

from backend.hand_tracking import check_for_hand_hover

class ALVEXScreen(QWidget):
    def __init__(self):
        super().__init__()

        # Setup window
        self.setWindowTitle("A.L.V.E.X. - External Display")
        self.setGeometry(100, 100, 800, 600)

        # Setup layout
        self.layout = QVBoxLayout()

        # Add a label to display dynamic text
        self.dynamic_label = QLabel("Welcome to A.L.V.E.X.", self)
        self.dynamic_label.setAlignment(Qt.AlignCenter)
        self.dynamic_label.setStyleSheet("font-size: 24px;")
        self.layout.addWidget(self.dynamic_label)

        # Add a placeholder for dynamic buttons
        self.buttons = []
        self.button_positions = {}  # Store button positions

        # Set the layout
        self.setLayout(self.layout)

    def update_text(self, text):
        """Update the projected text."""
        self.dynamic_label.setText(text)

    def add_button(self, label, callback, button_name):
        """Dynamically add buttons and store their positions."""
        button = QPushButton(label, self)
        button.setStyleSheet("font-size: 20px;")
        button.clicked.connect(callback)  # Connect to a function
        self.layout.addWidget(button)
        self.buttons.append(button)

        # Store button's geometry for hand tracking
        self.button_positions[button_name] = button.geometry()

    def clear_buttons(self):
        """Remove all buttons from the layout."""
        for button in self.buttons:
            self.layout.removeWidget(button)
            button.deleteLater()
        self.buttons = []
        self.button_positions = {}

    def handle_hand_gesture(self, hand_landmarks):
        """Handle hand gestures for button interaction."""
        for button_name, button_rect in self.button_positions.items():
            if check_for_hand_hover(hand_landmarks, button_rect):
                print(f"Button '{button_name}' pressed!")
                self.dynamic_label.setText(f"Button '{button_name}' pressed")
