import datetime
import pandas as pd
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (
    QApplication,
    QLabel,
    QSpinBox,
    QVBoxLayout,
    QHBoxLayout,
    QWidget,
    QLineEdit,
    QPushButton,
    QDateEdit,
)
from PyQt5.QtCore import Qt, QDate
from client_list import ClientList
from graph_window import GraphWindow
today = datetime.date.today()
try:
    df = pd.read_csv('clients.csv')
except FileNotFoundError:
    df = pd.DataFrame(columns=['name', 'phone', 'old_mm', 'new_mm', 'date', 'delivery_date', 'delivery_state'])

class AddClient(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Adicionar Cliente')
        self.setWindowIcon(QIcon('icon.ico'))
        self.name_label = QLabel('Nome:')
        self.name_input = QLineEdit()
        self.phone_label = QLabel('Telefone:')
        self.phone_input = QSpinBox()
        self.old_mm_label = QLabel('MM Antigo:')
        self.old_mm_input = QSpinBox()
        self.new_mm_label = QLabel('MM Novo:')
        self.new_mm_input = QSpinBox()
        self.delivery_date_label = QLabel('Data da Entrega:')
        self.delivery_date_input = QDateEdit(calendarPopup=True)
        self.delivery_date_input.setDisplayFormat('yyyy-MM-dd')
        self.delivery_state_label = QLabel('Estado da Entrega:')
        self.delivery_state_input = QLineEdit()
        self.submit_button = QPushButton('Adicionar')
        self.submit_button.clicked.connect(self.add_client_to_df)
        self.client_list_button = QPushButton('Lista de Clientes')
        self.client_list_button.clicked.connect(self.open_client_list)
        self.graph_button = QPushButton('Gráficos')
        self.graph_button.clicked.connect(self.open_graphs)
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.client_list_button)
        button_layout.addWidget(self.graph_button)
        form_layout = QVBoxLayout()
        form_layout.addWidget(self.name_label)
        form_layout.addWidget(self.name_input)
        form_layout.addWidget(self.phone_label)
        form_layout.addWidget(self.phone_input)
        form_layout.addWidget(self.old_mm_label)
        form_layout.addWidget(self.old_mm_input)
        form_layout.addWidget(self.new_mm_label)
        form_layout.addWidget(self.new_mm_input)
        form_layout.addWidget(self.delivery_date_label)
        form_layout.addWidget(self.delivery_date_input)
        form_layout.addWidget(self.delivery_state_label)
        form_layout.addWidget(self.delivery_state_input)
        form_layout.addWidget(self.submit_button)
        layout = QVBoxLayout()
        layout.addLayout(form_layout)
        layout.addLayout(button_layout)
        self.setLayout(layout)
    

    def add_client_to_df(self):
        name = self.name_input.text()
        phone = str(self.phone_input.value())
        old_mm = int(self.old_mm_input.value())
        new_mm = int(self.new_mm_input.value())
        delivery_date = self.delivery_date_input.date().toString(Qt.ISODate)
        delivery_state = self.delivery_state_input.text()
        clientid = len(df) + 1
        date = today.strftime("%Y-%m-%d")
        df.loc[clientid] = [name, phone, old_mm, new_mm, date, delivery_date, delivery_state]
        df.to_csv('clients.csv', index=False)


        # Apagar o input
        self.name_input.setText('')
        self.phone_input.setValue(0)
        self.old_mm_input.setValue(0)
        self.new_mm_input.setValue(0)
        self.delivery_date_input.setDate(QDate.currentDate())
        self.delivery_state_input.setText('')

    def open_client_list(self):
        self.client_list = ClientList(df)
        self.client_list.show()

    def open_graphs(self):
        self.graph_window = GraphWindow(df)
        self.graph_window.show()
