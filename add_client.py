import datetime
import pandas as pd
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (
    QApplication, QLabel, QComboBox, QVBoxLayout, QHBoxLayout,
    QWidget, QLineEdit, QPushButton, QDateEdit
)
from PyQt5.QtCore import Qt, QDate
from client_list import ClientList
from graph_window import GraphWindow

today = datetime.date.today()

class AddClient(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Novo Pedido')
        self.setWindowIcon(QIcon('icon.ico'))
        self.resize(250, 470)
        # Carregar dados dos clientes
        self.df = self.load_client_data()

        # Widgets
        self.name_label = QLabel('Nome:')
        self.name_input = QLineEdit()

        self.phone_label = QLabel('Telefone:')
        self.phone_input = QLineEdit()
        self.phone_input.setMaxLength(11)  # Define o comprimento máximo do telefone

        self.old_mm_label = QLabel('MM Antigo:')
        self.old_mm_input = QComboBox()
        self.old_mm_input.addItems(['50', '100', '150', '200', '250', '300'])

        self.new_mm_label = QLabel('MM Novo:')
        self.new_mm_input = QComboBox()
        self.new_mm_input.addItems(['50', '100', '150', '200', '250', '300'])

        self.delivery_date_label = QLabel('Data da Entrega:')
        self.delivery_date_input = QDateEdit(calendarPopup=True)
        self.delivery_date_input.setDisplayFormat('dd-MM-yyyy')
        self.delivery_date_input.setDate(QDate.currentDate())  # Define a data padrão como hoje

        self.delivery_state_label = QLabel('MM Antigo:')
        self.delivery_state_input = QComboBox()
        self.delivery_state_input.addItems(['Na fila', 'Em Producao', 'Feito', 'Entregue',])
        
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

    def load_client_data(self):
        # Carregar dados dos clientes a partir do CSV ou inicializar um novo DataFrame
        try:
            return pd.read_csv('clients.csv')
        except FileNotFoundError:
            # Se o arquivo CSV não for encontrado, cria um DataFrame vazio com as colunas necessárias
            return pd.DataFrame(columns=['name', 'phone', 'old_mm', 'new_mm', 'date', 'delivery_date', 'delivery_state'])

    def add_client_to_df(self):
        # Adicionar um novo cliente ao DataFrame e salvar no CSV
        client_data = {
            'name': self.name_input.text(),
            'phone': self.phone_input.text(),
            'old_mm': int(self.old_mm_input.currentText()),
            'new_mm': int(self.new_mm_input.currentText()),
            'date': datetime.date.today().strftime("%d-%m-%Y"),
            'delivery_date': self.delivery_date_input.date().toString(Qt.ISODate),
            'delivery_state': self.delivery_state_input.text()
        }

        # Convert client_data to DataFrame
        new_row = pd.DataFrame([client_data])
    
        # Load the existing data or create a new DataFrame
        self.df = self.load_client_data()
    
        # Concatenate the new row with the existing DataFrame
        self.df = pd.concat([self.df, new_row], ignore_index=True)
    
        # Save the updated DataFrame to CSV
        self.df.to_csv('clients.csv', index=False)

        # Clear the form fields
        self.clear_form()

    def clear_form(self):
        # Limpar os campos do formulário após adicionar um cliente
        self.name_input.clear()
        self.phone_input.clear()
        self.old_mm_input.setCurrentIndex(0)
        self.new_mm_input.setCurrentIndex(0)
        self.delivery_date_input.setDate(QDate.currentDate())
        self.delivery_state_input.clear()

    def open_client_list(self):
        # Abrir a janela da lista de clientes
        self.client_list = ClientList(self.df)
        self.client_list.show()

    def open_graphs(self):
        # Abrir a janela de gráficos
        self.graph_window = GraphWindow(self.df)
        self.graph_window.show()

if __name__ == '__main__':
    app = QApplication([])
    window = AddClient()
    window.show()
    app.exec_()
