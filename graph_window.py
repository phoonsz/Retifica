import datetime
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import pandas as pd
semana='Mostrar última semana'
tt="%Y-%m-%d"
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
        start_date = (datetime.date.today() - datetime.timedelta(days=30)).strftime(tt)
        end_date = datetime.date.today().strftime(tt)
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
            start_date = (datetime.date.today() - datetime.timedelta(days=7)).strftime(tt)
            end_date = datetime.date.today().strftime(tt)
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