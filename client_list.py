from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QTableWidget, QTableWidgetItem, QVBoxLayout

class ClientList(QWidget):
    def __init__(self, df):
        super().__init__()
        self.setWindowTitle('Lista de Clientes')
        self.setWindowIcon(QIcon('icon.ico'))
        self.df = df
        self.init_ui()

    def init_ui(self):
        """Initialize the UI layout and table structure."""
        self.table = QTableWidget(len(self.df), len(self.df.columns))
        self.table.setHorizontalHeaderLabels(self.df.columns)

        # Fill the table
        self.fill_table()

        layout = QVBoxLayout()
        layout.addWidget(self.table)
        self.setLayout(layout)

    def fill_table(self):
        """Fill the table with data from the DataFrame."""
        for i, row in enumerate(self.df.itertuples(index=False)):
            for j, value in enumerate(row):
                self.table.setItem(i, j, QTableWidgetItem(str(value)))
