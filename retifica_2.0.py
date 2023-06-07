import sys
import pandas as pd
import datetime
import plotly.graph_objs as go
import matplotlib
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (
    QApplication,
    QLabel,
    QSpinBox,
    QVBoxLayout,
    QHBoxLayout,
    QWidget,
    QTableWidget,
    QTableWidgetItem,
    QMessageBox,
    QLineEdit,
)
from PyQt5.QtCore import Qt, QDate
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PyQt5.QtWidgets import QDateEdit, QPushButton, QCalendarWidget

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

semana='Mostrar última semana'
class GraphWindow(QWidget):
    def __init__(self, df):
        super().__init__()
        self.setWindowTitle('Gráficos')
        self.setWindowIcon(QIcon('icon.ico'))
        self.df = df
        self.fig = Figure()
        self.canvas = FigureCanvas(self.fig)
        self.plot_graph()
        
        #botao pra trocar entre mes e semana
        self.btn_switch = QPushButton(semana, self)
        self.btn_switch.clicked.connect(self.switch_graph)
        
        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        layout.addWidget(self.btn_switch)
        self.setLayout(layout)
        
    def plot_graph(self):
        #filtrar pro ultimo mes
        start_date = (datetime.date.today() - datetime.timedelta(days=30)).strftime("%Y-%m-%d")
        end_date = datetime.date.today().strftime("%Y-%m-%d")
        df_last_month = self.df[(self.df['date'] >= start_date) & (self.df['date'] <= end_date)]

        #contar o numero de clientes adicionado por dia
        client_count = df_last_month.groupby('date')['name'].count()

        # criar o grafico de barras
        self.fig.clear()
        ax = self.fig.add_subplot(111)
        ax.bar(client_count.index, client_count.values)
        ax.set_title('Clientes adicionados por dia (último mês)')
        ax.set_xlabel('Data')
        ax.set_ylabel('Número de clientes')
        for tick in ax.get_xticklabels():
            tick.set_rotation(60)
        self.fig.tight_layout()
        self.canvas.draw()
        
    def switch_graph(self):
        if self.btn_switch.text() == semana:
            start_date = (datetime.date.today() - datetime.timedelta(days=7)).strftime("%Y-%m-%d")
            end_date = datetime.date.today().strftime("%Y-%m-%d")
            df_last_week = self.df[(self.df['date'] >= start_date) & (self.df['date'] <= end_date)]
            
            #contar o numero de clientes adicionado por dia
            client_count = df_last_week.groupby('date')['name'].count()
            
            #atualizar o grafico
            ax = self.fig.axes[0]
            ax.clear()
            ax.bar(client_count.index, client_count.values)
            ax.set_title('Clientes adicionados por dia (última semana)')
            ax.set_xlabel('Data')
            ax.set_ylabel('Número de clientes')
            for tick in ax.get_xticklabels():
                tick.set_rotation(60)
            self.fig.tight_layout()
            self.canvas.draw()
            self.btn_switch.setText('Mostrar último mês')
        else:
            #voltar pro grafico mensal
            self.plot_graph()
            self.btn_switch.setText(semana)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = AddClient()
    window.show()
    sys.exit(app.exec_())
