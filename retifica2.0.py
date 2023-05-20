import sys
import pandas as pd
import datetime
from plotly.subplots import make_subplots
import plotly.graph_objs as go
import matplotlib
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PyQt5.QtCore import Qt
from PyQt5.QtGui import (
    QIcon,
    QIntValidator,
    QFont,
    QPalette,
    QColor,
)
from PyQt5.QtWidgets import (
    QApplication,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QWidget,
    QTableWidget,
    QTableWidgetItem,
    QComboBox,
    QMessageBox,
)

semana='Mostrar última semana'
icon='icon.ico'
ttt="%Y-%m-%d"
today = datetime.date.today()
palette = QPalette()
discord_background_color = QColor(200, 200, 200)  # Tom de Cinza Claro
discord_text_color = QColor(40, 40, 40)  # Tom de Cinza Escuro
discord_button_color = QColor(160, 160, 160)  # Tom de Cinza Médio
palette.setColor(QPalette.Window, discord_background_color)
palette.setColor(QPalette.WindowText, discord_text_color)
palette.setColor(QPalette.Button, discord_button_color)
try:
    df = pd.read_csv('clients.csv')
except FileNotFoundError:
    df = pd.DataFrame(columns=['name', 'phone', 'old_mm', 'new_mm', 'date', 'delivery_date', 'delivery_state'])



class AddClient(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Adicionar Cliente')
        self.setWindowIcon(QIcon(icon))
        self.widgets = {
            'name': {'label': QLabel('Nome:'), 'input': QLineEdit()},
            'phone': {'label': QLabel('Telefone:'), 'input': QLineEdit()},
            'old_mm': {'label': QLabel('MM Antigo:'), 'input': QLineEdit()},
            'new_mm': {'label': QLabel('MM Novo:'), 'input': QLineEdit()},
            'delivery_date': {'label': QLabel('Data da Entrega:'), 'input': QLineEdit()},
            'delivery_state': {'label': QLabel('Estado da Entrega:'), 'input': QLineEdit()}
        }
        for field in ['old_mm', 'new_mm']: self.widgets[field]['input'].setValidator(QIntValidator())
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
        for widget_group in self.widgets.values():
            form_layout.addWidget(widget_group['label'])
            form_layout.addWidget(widget_group['input'])
        form_layout.addWidget(self.submit_button)
        layout = QVBoxLayout()
        layout.addLayout(form_layout)
        layout.addLayout(button_layout)
        self.setLayout(layout)

    def add_client_to_df(self):
        inputs = {key: widget_group['input'].text() for key, widget_group in self.widgets.items()}

        if not inputs['old_mm'] or not inputs['new_mm']:
            QMessageBox.warning(self, 'Campos Vazios', 'Por favor, preencha todos os campos.')
            return

        try:
            old_mm = int(inputs['old_mm'])
            new_mm = int(inputs['new_mm'])
        except ValueError:
            QMessageBox.warning(self, 'Valor Inválido', 'Por favor, insira apenas números inteiros nos campos MM Antigo e MM Novo.')
            return

        # Resto do seu código a partir daqui
        clientid = len(df) + 1
        date = today.strftime(ttt)
        df.loc[clientid] = [inputs['name'], inputs['phone'], old_mm, new_mm, date, inputs['delivery_date'], inputs['delivery_state']]
        df.to_csv('clients.csv', index=False)

        # Limpar os campos de entrada
        for widget_group in self.widgets.values():
            widget_group['input'].setText('')
                    
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
        self.setWindowIcon(QIcon(icon))
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
    def __init__(self, df):
        super().__init__()
        self.setWindowTitle('Gráficos')
        self.setWindowIcon(QIcon(icon))
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
        start_date = (datetime.date.today() - datetime.timedelta(days=30)).strftime(ttt)
        end_date = datetime.date.today().strftime(ttt)
        df_last_month = self.df[(self.df['date'] >= start_date) & (self.df['date'] <= end_date)]

        #contar o numero de clientes adicionado por dia
        client_count = df_last_month.groupby('date')['name'].count()

        # criar o grafico de barras
               # ...
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
            start_date = (datetime.date.today() - datetime.timedelta(days=7)).strftime(ttt)
            end_date = datetime.date.today().strftime(ttt)
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
    font = QFont("Helvetica")
    app.setFont(font)
    app.setPalette(palette)
    window = AddClient()
    window.show()
    sys.exit(app.exec_())
