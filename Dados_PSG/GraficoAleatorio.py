import PySimpleGUI as sg
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg



def gerar_dados():
    # Cria uma figura com tamanho 125
    fig1 = plt.figure(dpi=125)

    # Gera 20 valores aleatorios entre 0 e 10 e arredonda para 3 casas
    x = np.round(10*np.random.random(20), 3)
    y = np.round(10*np.random.random(20), 3)

    # Gera um grafico scatter com os numeros de x e y
    p1 = plt.scatter(x,y,edgecolors='k')

    plt.ylabel('Valores Y')
    plt.xlabel('Valores X')
    plt.title('Grafico scatter')

    # Obtem cordenadas e dimensoes da caixa limitadora
    figure_x, figure_y, figure_w, figure_h = fig1.bbox.bounds
    return (x, y, fig1, figure_x, figure_y, figure_w, figure_h)


def draw_figure(canvas, figure, loc=(0,0)):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
    return figure_canvas_agg


# Funcao para deletar a figura
def delete_fig_agg(fig_agg):
    fig_agg.get_tk_widget().forget()
    plt.close('All')


# Layout da janela
layout = [
    [sg.Button('Gera grafico de dispersão', enable_events=True, key='-GENERATE-')],
    [sg.Canvas(size=(350,350), key='-CANVAS-', pad=(20,20))],
    [sg.Button('Exit')]
]

# Cria a janela
window = sg.Window('Grafico aleatorio', layout, size=(700,700))


# Event loop
fig_agg = None
while True:
    event, values = window.read()
    if event in (sg.WIN_CLOSED, 'Exit'):
        break

    if event == '-GENERATE-':
        if fig_agg is not None:
            delete_fig_agg(fig_agg)
        _, _, fig1, figure_x, figure_y, figure_w, figure_h = gerar_dados()
        canvas_elem = window['-CANVAS-'].TKCanvas
        canvas_elem.Size = (int(figure_w), int(figure_h))
        fig_agg = draw_figure(canvas_elem, fig1)


window.close()