import sys
from PyQt5.QtWidgets import QApplication
from add_client import AddClient

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = AddClient()
    window.show()
    sys.exit(app.exec_())
