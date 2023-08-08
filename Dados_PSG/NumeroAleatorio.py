import PySimpleGUI as sg
import numpy as np
import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import time


# Função para atualizar numero gerado
def update_num():
    num_aleatorio = np.random.randint(1, 100)
    lista_nums.append(num_aleatorio)
    elemento_texto = window['-TEXT-']
    elemento_texto.update(f"Numero aleatorio: {num_aleatorio}")


def tempo():
    milisegundos = datetime.datetime.now().strftime(".%f")
    tempo_gerado.append(round(float(milisegundos), 2))


def plotar_fig(tempo_ger, num_ger, window):
    fig = plt.figure(dpi=100)
    ax1 = fig.add_subplot(211)
    ax2 = fig.add_subplot(212)

    # Plotar gráfico de linha dos valores de tempo
    ax1.plot(tempo_ger)
    ax1.set_xlabel('Amostra')
    ax1.set_ylabel('Tempo (milissegundos)')

    # Plotar gráfico de linha dos valores de tempo
    ax2.plot(num_ger)
    ax2.set_xlabel('Amostra')
    ax2.set_ylabel('Tempo (milissegundos)')
    def draw_figure(canvas, figure):
        figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
        figure_canvas_agg.draw()
        figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
        return figure_canvas_agg

    fig_canvas_agg = draw_figure(window['-CANVAS-'].TKCanvas, fig)


# Cria o layout da janela
layout = [[sg.Button('Gerar Numero', enable_events=True, key='-GERAR-')],
          [sg.Text('Numero aleatorio: x', key='-TEXT-', size=(25, 1))],
          [sg.Canvas(key='-CANVAS-', size=(700, 500), pad=(15, 15))],
          [sg.Button('Grafico')]]

window = sg.Window('Gerar int aleatorio', layout)

tempo_gerado = []
lista_nums = []
while True:
    event, values = window.read()

    if event == sg.WIN_CLOSED:
        break

    if event == '-GERAR-':
        for i in range(100):
            time.sleep(0.01)
            for j in range(2):
                update_num()
                tempo()
        plotar_fig(tempo_gerado, lista_nums, window)

print(tempo_gerado)
window.close()
