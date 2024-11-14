from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QTextEdit, QPushButton, QListWidget, QHBoxLayout, QMessageBox
from PySide6.QtCore import Qt
import os

# Directory to store note files
NOTES_DIR = "notes"

class NoteTakingApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Note Taking App")
        self.setGeometry(100, 100, 600, 500)

        if not os.path.exists(NOTES_DIR):
            os.makedirs(NOTES_DIR)

        self.setStyleSheet("""
            QWidget {
                background-color: #fafafa;
                font-family: Arial, sans-serif;
            }
            QLineEdit, QTextEdit {
                border-radius: 5px;
                border: 1px solid #ccc;
                padding: 10px;
                background-color: #fff;
                font-size: 14px;
            }
            QTextEdit {
                min-height: 100px;
            }
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border-radius: 5px;
                padding: 10px 20px;
                font-size: 16px;
                border: none;
                transition: background-color 0.3s;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #388E3C;
            }
            QListWidget {
                background-color: #f4f4f4;
                border: 1px solid #ddd;
                border-radius: 5px;
                padding: 10px;
                font-size: 14px;
            }
            QListWidget::item {
                padding: 8px;
                border-bottom: 1px solid #ddd;
            }
            QListWidget::item:hover {
                background-color: #e8f5e9;
                cursor: pointer;
            }
            QLineEdit {
                font-size: 16px;
            }
            QLabel {
                font-weight: bold;
                font-size: 18px;
                margin-bottom: 5px;
            }
        """)

        self.layout = QVBoxLayout(self)

        # Search bar for searching notes
        self.search_bar = QLineEdit(self)
        self.search_bar.setPlaceholderText("Search notes...")
        self.layout.addWidget(self.search_bar)

        self.title_input = QLineEdit(self)
        self.title_input.setPlaceholderText("Enter note title...")
        self.layout.addWidget(self.title_input)

        self.note_input = QTextEdit(self)
        self.note_input.setPlaceholderText("Enter note content...")
        self.layout.addWidget(self.note_input)

        button_layout = QHBoxLayout()

        self.save_button = QPushButton("Save Note", self)
        self.cancel_button = QPushButton("Cancel", self)
        self.delete_button = QPushButton("Delete Note", self)

        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.cancel_button)
        button_layout.addWidget(self.delete_button)

        self.layout.addLayout(button_layout)

        # List to display notes
        self.note_list = QListWidget(self)
        self.layout.addWidget(self.note_list)

        self.notes = self.load_notes()
        self.update_note_list()

        self.save_button.clicked.connect(self.save_note)
        self.cancel_button.clicked.connect(self.cancel_edit)
        self.delete_button.clicked.connect(self.delete_note)
        self.note_list.itemClicked.connect(self.load_note)
        self.search_bar.textChanged.connect(self.search_notes)

    def save_note(self):
        title = self.title_input.text().strip()
        content = self.note_input.toPlainText().strip()

        if not title or not content:
            QMessageBox.warning(self, "Input Error", "Both title and content are required!")
            return
        file_path = os.path.join(NOTES_DIR, f"{title}.txt")
        with open(file_path, "w") as file:
            file.write(content)

        self.notes = self.load_notes()  # Reload notes from the directory
        self.update_note_list()

        self.title_input.clear()
        self.note_input.clear()

    def delete_note(self):
        selected_item = self.note_list.currentItem()
        if selected_item:
            note_title = selected_item.text()
            file_path = os.path.join(NOTES_DIR, f"{note_title}.txt")
            if os.path.exists(file_path):
                os.remove(file_path)

            self.notes = self.load_notes()  # Reload notes after deletion
            self.update_note_list()

    def cancel_edit(self):
        self.title_input.clear()
        self.note_input.clear()

    def load_note(self, item):
        title = item.text()
        file_path = os.path.join(NOTES_DIR, f"{title}.txt")
        try:
            with open(file_path, "r") as file:
                content = file.read()
                self.title_input.setText(title)
                self.note_input.setPlainText(content)
        except FileNotFoundError:
            QMessageBox.warning(self, "File Error", f"Failed to load {title}.txt.")

    def load_notes(self):
        notes = {}
        try:
            # List all files in the NOTES_DIR directory
            for filename in os.listdir(NOTES_DIR):
                if filename.endswith(".txt"):
                    title = filename.replace(".txt", "")
                    notes[title] = filename
        except FileNotFoundError:
            pass  # If the directory doesn't exist, just return an empty dictionary
        return notes

    def update_note_list(self):
        self.note_list.clear()
        self.note_list.addItems(self.notes.keys())

    def search_notes(self):
        search_term = self.search_bar.text().lower()
        filtered_notes = [title for title in self.notes if search_term in title.lower()]

        self.note_list.clear()
        self.note_list.addItems(filtered_notes)

if __name__ == "__main__":
    app = QApplication([])
    window = NoteTakingApp()
    window.show()
    app.exec()
