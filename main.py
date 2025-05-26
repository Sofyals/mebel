import sys
from PyQt6.QtWidgets import QApplication
from main2 import Enter

def main():
    app = QApplication(sys.argv)
    main_window = Enter()
    main_window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()