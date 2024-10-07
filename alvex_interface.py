import sys
import pyttsx3
import psutil
from backend.system_monitor import get_system_status  # Import the system monitor
import speech_recognition as sr
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QLineEdit, 
                             QTextEdit, QProgressBar, QComboBox, QMessageBox, QCheckBox)
from PyQt5.QtCore import Qt

class ALVEXInterface(QWidget):
    def __init__(self):
        super().__init__()

        # Initialize TTS engine
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 150)  # Speed of speech
        self.engine.setProperty('volume', 1)  # Volume level (0.0 to 1.0)
        
        # Initialize Speech Recognition
        self.recognizer = sr.Recognizer()
        self.listening = False  # State of the listen toggle

        # Set up the UI
        self.initUI()

    def initUI(self):
        # Main layout
        layout = QVBoxLayout()

        # Title
        self.title_label = QLabel("A.L.V.E.X. - Adaptive Learning Virtual EXecutive", self)
        self.title_label.setStyleSheet("font-size: 18px; font-weight: bold; color: cyan;")
        layout.addWidget(self.title_label)

        # Toggle Listen On/Off
        self.listen_checkbox = QCheckBox("Listen (Voice Commands)", self)
        self.listen_checkbox.setChecked(False)
        self.listen_checkbox.stateChanged.connect(self.toggle_listen)
        self.listen_checkbox.setStyleSheet("color: yellow;")
        layout.addWidget(self.listen_checkbox)

        # Command Input
        self.command_input = QLineEdit(self)
        self.command_input.setPlaceholderText("Enter command...")
        self.command_input.setStyleSheet("background-color: #333333; color: white; border: 1px solid cyan;")
        layout.addWidget(self.command_input)

        # Execute Command Button
        self.execute_button = QPushButton("Execute Command", self)
        self.execute_button.clicked.connect(self.execute_command)
        self.execute_button.setStyleSheet("background-color: #555555; color: white; border: 1px solid cyan;")
        layout.addWidget(self.execute_button)

        # Workflow Selection
        self.workflow_label = QLabel("Select Workflow", self)
        self.workflow_label.setStyleSheet("color: yellow;")
        layout.addWidget(self.workflow_label)

        self.workflow_combo = QComboBox(self)
        self.workflow_combo.addItem("Morning Routine")
        self.workflow_combo.addItem("End of Day Routine")
        self.workflow_combo.setStyleSheet("background-color: #333333; color: white; border: 1px solid cyan;")
        layout.addWidget(self.workflow_combo)

        # Execute Workflow Button
        self.workflow_button = QPushButton("Execute Workflow", self)
        self.workflow_button.clicked.connect(self.execute_workflow)
        self.workflow_button.setStyleSheet("background-color: #555555; color: white; border: 1px solid cyan;")
        layout.addWidget(self.workflow_button)

        # System Monitoring
        self.monitor_label = QLabel("System Monitoring", self)
        self.monitor_label.setStyleSheet("color: cyan;")
        layout.addWidget(self.monitor_label)
        
        self.cpu_label = QLabel("CPU Usage: 0%", self)
        self.cpu_label.setStyleSheet("color: white;")
        self.memory_label = QLabel("Memory Usage: 0%", self)
        self.memory_label.setStyleSheet("color: white;")
        self.disk_label = QLabel("Disk Usage: 0%", self)
        self.disk_label.setStyleSheet("color: white;")
        layout.addWidget(self.cpu_label)
        layout.addWidget(self.memory_label)
        layout.addWidget(self.disk_label)
        
        # Progress Bars for Monitoring
        self.cpu_bar = QProgressBar(self)
        self.cpu_bar.setStyleSheet("QProgressBar { background-color: #333333; color: white; border: 1px solid cyan; }"
                                   "QProgressBar::chunk { background-color: cyan; }")
        self.cpu_bar.setValue(0)
        layout.addWidget(self.cpu_bar)
        
        self.memory_bar = QProgressBar(self)
        self.memory_bar.setStyleSheet("QProgressBar { background-color: #333333; color: white; border: 1px solid yellow; }"
                                      "QProgressBar::chunk { background-color: yellow; }")
        self.memory_bar.setValue(0)
        layout.addWidget(self.memory_bar)
        
        self.disk_bar = QProgressBar(self)
        self.disk_bar.setStyleSheet("QProgressBar { background-color: #333333; color: white; border: 1px solid magenta; }"
                                    "QProgressBar::chunk { background-color: magenta; }")
        self.disk_bar.setValue(0)
        layout.addWidget(self.disk_bar)
        
        # Refresh System Status Button
        self.refresh_button = QPushButton("Refresh System Status", self)
        self.refresh_button.clicked.connect(self.refresh_system_status)
        self.refresh_button.setStyleSheet("background-color: #555555; color: white; border: 1px solid cyan;")
        layout.addWidget(self.refresh_button)

        # Feedback Section
        self.feedback_label = QLabel("Feedback", self)
        self.feedback_label.setStyleSheet("color: yellow;")
        layout.addWidget(self.feedback_label)

        self.feedback_input = QTextEdit(self)
        self.feedback_input.setPlaceholderText("Provide feedback...")
        self.feedback_input.setStyleSheet("background-color: #333333; color: white; border: 1px solid cyan;")
        layout.addWidget(self.feedback_input)

        self.feedback_button = QPushButton("Submit Feedback", self)
        self.feedback_button.clicked.connect(self.submit_feedback)
        self.feedback_button.setStyleSheet("background-color: #555555; color: white; border: 1px solid cyan;")
        layout.addWidget(self.feedback_button)
        
        # Set the main layout
        self.setLayout(layout)
        self.setWindowTitle("A.L.V.E.X.")
        self.setGeometry(300, 300, 400, 600)
        self.setStyleSheet("background-color: black;")
        self.show()

    # Talk function: Text-to-Speech
    def talk(self, text):
        """Speaks the provided text."""
        self.engine.say(text)
        self.engine.runAndWait()

    # Toggle the listen state
    def toggle_listen(self, state):
        """Toggles the speech recognition listening mode."""
        if state == Qt.Checked:
            self.listening = True
            self.talk("Listening enabled. Please say a command.")
            self.start_listening()
        else:
            self.listening = False
            self.talk("Listening disabled.")

    # Start listening for voice commands
    def start_listening(self):
        """Starts the speech recognition loop when listening is enabled."""
        if self.listening:
            with sr.Microphone() as source:
                self.talk("I'm listening for a command...")
                try:
                    # Adjust for ambient noise and capture audio
                    self.recognizer.adjust_for_ambient_noise(source)
                    audio = self.recognizer.listen(source, timeout=5)
                    command = self.recognizer.recognize_google(audio)
                    self.talk(f"You said: {command}")
                    self.command_input.setText(command)  # Display recognized command in input field
                    self.execute_command()  # Automatically execute recognized command
                except sr.UnknownValueError:
                    self.talk("Sorry, I didn't understand that.")
                except sr.RequestError:
                    self.talk("Error in recognizing your voice.")
                except sr.WaitTimeoutError:
                    self.talk("Listening timed out.")
            if self.listening:  # Keep listening if toggle is on
                self.start_listening()

    # Execute a command and provide a spoken response
    def execute_command(self):
        command = self.command_input.text()
        if command:
            message = f"Executing command: {command}"
            QMessageBox.information(self, "Command Execution", message)
            self.talk(message)  # Speak out the message
            # Here you would call the backend function to execute the command
            # Example: execute_command('user1', command)
        else:
            warning_message = "Please enter a command to execute."
            QMessageBox.warning(self, "Input Error", warning_message)
            self.talk(warning_message)

    # Execute a workflow and provide a spoken response
    def execute_workflow(self):
        workflow = self.workflow_combo.currentText()
        message = f"Executing workflow: {workflow}"
        QMessageBox.information(self, "Workflow Execution", message)
        self.talk(message)  # Speak out the workflow execution
        # Here you would call the backend function to execute the selected workflow
        # Example: execute_workflow('user1', workflow)

    # Refresh system status and speak the updated status
    def refresh_system_status(self):
        # Refresh the system monitoring status using psutil
        cpu_usage = psutil.cpu_percent()
        memory_info = psutil.virtual_memory()
        disk_info = psutil.disk_usage('/')
        
        self.cpu_label.setText(f"CPU Usage: {cpu_usage}%")
        self.cpu_bar.setValue(cpu_usage)

        memory_usage = memory_info.percent
        self.memory_label.setText(f"Memory Usage: {memory_usage}%")
        self.memory_bar.setValue(memory_usage)

        disk_usage = disk_info.percent
        self.disk_label.setText(f"Disk Usage: {disk_usage}%")
        self.disk_bar.setValue(disk_usage)

        # Speak the system status
        status_message = (f"Current CPU usage is {cpu_usage} percent. "
                          f"Memory usage is {memory_usage} percent. "
                          f"Disk usage is {disk_usage} percent.")
        self.talk(status_message)

    # Submit feedback and provide a spoken confirmation
    def submit_feedback(self):
        feedback = self.feedback_input.toPlainText()
        if feedback:
            message = "Thank you for your feedback!"
            QMessageBox.information(self, "Feedback Submitted", message)
            self.talk(message)  # Speak out the confirmation
            # Here you would call the backend function to submit the feedback
            # Example: submit_feedback('user1', 'command_or_workflow', feedback, is_positive=True/False)
        else:
            warning_message = "Please enter your feedback."
            QMessageBox.warning(self, "Input Error", warning_message)
            self.talk(warning_message)

# Inside the ALVEXInterface class in alvex_interface.py
def refresh_system_status(self):
    status = get_system_status()  # Get system status from the backend
    cpu_usage = status['cpu_usage']
    memory_usage = status['memory_usage']
    disk_usage = status['disk_usage']

    self.cpu_label.setText(f"CPU Usage: {cpu_usage}%")
    self.cpu_bar.setValue(cpu_usage)

    self.memory_label.setText(f"Memory Usage: {memory_usage}%")
    self.memory_bar.setValue(memory_usage)

    self.disk_label.setText(f"Disk Usage: {disk_usage}%")
    self.disk_bar.setValue(disk_usage)

    # Speak the system status
    status_message = (f"Current CPU usage is {cpu_usage} percent. "
                      f"Memory usage is {memory_usage} percent. "
                      f"Disk usage is {disk_usage} percent.")
    self.talk(status_message)
