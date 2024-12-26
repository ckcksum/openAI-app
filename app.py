import sys
from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QPushButton,
    QTextEdit,
    QRadioButton,
    QButtonGroup,
    QLabel,
    QHBoxLayout
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from openAI import ask
from prompt import Prompt

from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget

import sys

class GrammarGPT(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

        # Loading screen
        self.loading = LoadingWindow(self)

    def initUI(self): 
        central_widget = QWidget(self)
        layout = QVBoxLayout()

        ### Add widgets ###
        #  Select input type
        self.input_type = InputTypeSelection(self)
        layout.addWidget(self.input_type)
        # Input Field
        self.input_field = InputField(self)
        layout.addWidget(self.input_field)
        # Submit Button
        self.submit_button = SubmitButton(self)
        self.submit_button.enter_button.clicked.connect(self.process_input)
        layout.addWidget(self.submit_button)
        # Output Box (Empty)
        self.output_box = OutputBox(self)
        layout.addWidget(self.output_box)

        # UI 
        # layout.addStretch()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)
        self.setWindowTitle('GrammarGPT')
        self.setGeometry(100, 100, 1200, 800)
        self.setStyleSheet("background-color: #0D222F;")
    
        self.show()

    def process_input(self):
        self.loading.show() # Show loading screen
        input_type = self.input_type.get_selected_type() 
        user_input = self.input_field.get_text() 
        # Get prompt
        prompt = Prompt() 
        system_prompt = prompt.get_system_prompt(input_type)
        print("Calling API")
        response = ask(system_prompt, user_input)        
        print("API called")
        self.display_response(response)

    def display_response(self, answer):
        # Hide the loading screen
        self.loading.hide()

        # Display response in the existing OutputBox
        type_map = {
            'e': 'Email',
            'c': 'Chat',
            'g': 'General'
        }
        input_type = self.input_type.get_selected_type()
        display_text = f"[GrammarGPT][{type_map.get(input_type)}]\n{answer}\n\n[End]"
        self.output_box.set_output(display_text)
        print(f"Response displayed: {answer}")

################### Main Components ###################
class InputTypeSelection(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        btns_layout = QHBoxLayout()
        self.type_label = QLabel("Select Input Type:", self)
        btns_layout.addWidget(self.type_label)
        # btns
        self.radio_group = QButtonGroup(self)
        self.radio_general = QRadioButton('General')
        self.radio_email = QRadioButton('Email')
        self.radio_chat = QRadioButton('Chat')
        self.radio_general.setChecked(True)
        self.radio_group.addButton(self.radio_general)
        self.radio_group.addButton(self.radio_email)
        self.radio_group.addButton(self.radio_chat)
        btns_layout.addWidget(self.radio_general)
        btns_layout.addWidget(self.radio_email)
        btns_layout.addWidget(self.radio_chat)
        self.setLayout(btns_layout)

    def get_selected_type(self):
        if self.radio_email.isChecked():
            return 'e'
        elif self.radio_chat.isChecked():
            return 'c'
        else:
            return 'g'


class InputField(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout()
        # Input instruction label
        self.input_label = QLabel("Enter Text:", self)
        layout.addWidget(self.input_label)
        # Text field
        self.input_field = QTextEdit(self)
        layout.addWidget(self.input_field)
        self.setLayout(layout)

    def get_text(self):
        return self.input_field.toPlainText()

# gpt answer output box
class OutputBox(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        output_layout = QVBoxLayout()
        # Text label
        self.output_label = QLabel("", self) # Empty before user input
        output_layout.addWidget(self.output_label)
        # Text box
        self.output_box = QTextEdit(self)
        self.output_box.setReadOnly(True)
        output_layout.addWidget(self.output_box)
        self.setLayout(output_layout)

    def set_output(self, text):
        self.output_label.setText(text.split('\n')[0])  # Set the first line as label
        self.output_box.setText('\n'.join(text.split('\n')[1:]))

############ Buttons ############
class SubmitButton(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QHBoxLayout()
        # btn
        self.enter_button = QPushButton('Submit', self)
        layout.addWidget(self.enter_button)
        self.setLayout(layout)

############ Loading Screen ############
class LoadingWindow(QWidget):
    def __init__(self, parent=None):
        # Set up window
        super().__init__(parent)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        self.setFixedSize(300, 100)
        main_layout = QHBoxLayout()
        self.text = QLabel("Loading, please wait...", self)
        self.text.setStyleSheet("QLabel { color: white; font-size: 16px; }")
        main_layout.addWidget(self.text)
        self.setLayout(main_layout)
        self.setStyleSheet("background-color: #59595e;")

############### Run app ###############
def run():    
    print("App running")
    app = QApplication(sys.argv)
    w = GrammarGPT()
    w.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    run()