import sys
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QTableWidget, QTableWidgetItem
import pandas as pd
import datetime
import matplotlib.pyplot as plt

df = pd.DataFrame(columns=['name', 'phone', 'old_mm', 'new_mm', 'date', 'delivery_date', 'delivery_state'])
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
        self.phone_input = QLineEdit()
        self.old_mm_label = QLabel('MM Antigo:')
        self.old_mm_input = QLineEdit()
        self.new_mm_label = QLabel('MM Novo:')
        self.new_mm_input = QLineEdit()
        self.delivery_date_label = QLabel('Data da Entrega:')
        self.delivery_date_input = QLineEdit()
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
        phone = self.phone_input.text()
        old_mm = int(self.old_mm_input.text())
        new_mm = int(self.new_mm_input.text())
        delivery_date = self.delivery_date_input.text()
        delivery_state = self.delivery_state_input.text()
        clientid = len(df) + 1
        date = today.strftime("%Y-%m-%d")
        df.loc[clientid] = [name, phone, old_mm, new_mm, date, delivery_date, delivery_state]
        df.to_csv('clients.csv', index=False)

        # Clear input fields
        self.name_input.setText('')
        self.phone_input.setText('')
        self.old_mm_input.setText('')
        self.new_mm_input.setText('')
        self.delivery_date_input.setText('')
        self.delivery_state_input.setText('')

    def open_client_list(self):
        self.client_list = ClientList(df)
        self.client_list.show()

    def open_graphs(self):
        client_list = df.to_dict('records')
        self.graph_window = GraphWindow(client_list)
        self.graph_window.show()

class ClientList(QWidget):
    def __init__(self, df):
        super().__init__()
        self.setWindowTitle('Lista de Clientes')
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


class GraphWindow(QWidget):
    def __init__(self, client_list):
        super().__init__()
        self.client_list = client_list

        # Lê o arquivo CSV e converte a coluna de datas para o tipo datetime
        df = pd.read_csv('clients.csv', parse_dates=['date'])

        # Cria uma nova coluna com apenas a data (sem a hora)
        df['date_only'] = df['date'].dt.date

        # Agrupa o DataFrame pela data e conta o número de ocorrências de cada data
        counts = df.groupby('date_only').size()

        # Cria um gráfico de linhas com a contagem de clientes por data
        fig, ax = plt.subplots()
        ax.bar(counts.index, counts.values)
        ax.set_xlabel('Data')
        ax.set_ylabel('Número de clientes')
        ax.set_title('Quantidade de clientes por dia')
        plt.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = AddClient()
    window.show()
    sys.exit(app.exec_())
