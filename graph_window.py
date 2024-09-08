import datetime
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

# Constantes
SHOW_WEEK = 'Mostrar última semana'
SHOW_MONTH = 'Mostrar último mês'
SHOW_ALL_TIME = 'Mostrar total'
DATE_FORMAT = "%d-%m-%Y"

class GraphWindow(QWidget):
    def __init__(self, df):
        super().__init__()
        self.setWindowTitle('Gráficos')
        self.setWindowIcon(QIcon('icon.ico'))
        self.df = df
        self.fig = Figure()
        self.canvas = FigureCanvas(self.fig)

        # Criar botões
        self.btn_week = QPushButton(SHOW_WEEK, self)
        self.btn_week.clicked.connect(self.switch_to_week)
        
        self.btn_month = QPushButton(SHOW_MONTH, self)
        self.btn_month.clicked.connect(self.switch_to_month)
        
        self.btn_all_time = QPushButton(SHOW_ALL_TIME, self)
        self.btn_all_time.clicked.connect(self.switch_to_all_time)

        # Configuração inicial do layout
        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        layout.addWidget(self.btn_week)
        layout.addWidget(self.btn_month)
        layout.addWidget(self.btn_all_time)
        self.setLayout(layout)

        # Gráfico inicial (último mês por padrão)
        self.plot_graph(days=30, title='Clientes adicionados por dia (último mês)')

    def plot_graph(self, days=None, title=None):
        """Plota adições de clientes para o número de dias fornecido."""
        if days is not None:
            start_date = (datetime.date.today() - datetime.timedelta(days=days)).strftime(DATE_FORMAT)
            end_date = datetime.date.today().strftime(DATE_FORMAT)
            df_filtered = self.df[(self.df['date'] >= start_date) & (self.df['date'] <= end_date)]
        else:
            df_filtered = self.df

        # Contar o número de clientes adicionados por dia
        client_count = df_filtered.groupby('date')['name'].count()

        # Plotar o gráfico
        self.fig.clear()
        ax = self.fig.add_subplot(111)
        ax.bar(client_count.index, client_count.values)
        ax.set_title(title)
        ax.set_xlabel('Data')
        ax.set_ylabel('Número de clientes')

        # Rotacionar os rótulos das datas para melhor leitura
        for tick in ax.get_xticklabels():
            tick.set_rotation(60)

        self.fig.tight_layout()
        self.canvas.draw()

    def switch_to_week(self):
    # Mostrar gráfico para a última semana.
        self.plot_graph(days=7, title='Clientes adicionados por dia (última semana)')
        self.btn_week.setText(SHOW_WEEK)
        self.btn_month.setText(SHOW_MONTH)
        self.btn_all_time.setText(SHOW_ALL_TIME)
    
    
    def switch_to_month(self):
    # Mostrar gráfico para o último mês.
        self.plot_graph(days=30, title='Clientes adicionados por dia (último mês)')
        self.btn_week.setText(SHOW_WEEK)
        self.btn_month.setText(SHOW_MONTH)
        self.btn_all_time.setText(SHOW_ALL_TIME)

    def switch_to_all_time(self):
    # Mostrar gráfico total.
        self.plot_graph(days=None, title='Clientes adicionados por dia (total)')
        self.btn_week.setText(SHOW_WEEK)
        self.btn_month.setText(SHOW_MONTH)
        self.btn_all_time.setText(SHOW_ALL_TIME)
