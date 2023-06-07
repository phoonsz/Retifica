from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QTableWidget, QTableWidgetItem, QVBoxLayout

class ClientList(QWidget):
    def __init__(self, df):
        super().__init__()
        self.setWindowTitle('Lista de Clientes')
        self.setWindowIcon(QIcon('icon.ico'))
        self.df = df
        self.table = QTableWidget()
        self.table.setColumnCount(len(df.columns))
        self.table.setHorizontalHeaderLabels(df.columns)
        self.table.setRowCount(len(df))
        self.fill_table()
        layout = QVBoxLayout()
        layout.addWidget(self.table)
        self.setLayout(layout)

    def fill_table(self):
        for i in range(len(self.df)):
            for j in range(len(self.df.columns)):
                item = QTableWidgetItem(str(self.df.iloc[i, j]))
                self.table.setItem(i, j, item)