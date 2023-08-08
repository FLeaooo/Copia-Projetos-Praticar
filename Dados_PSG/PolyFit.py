import PySimpleGUI as sg
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


def gerar_dados():
    # Cria figura com 125 dpi
    fig_1 = plt.figure(dpi=125)

    # Gera 20 numeros de 0 a 10 com 3 casas decimais
    x = np.round(10*np.random.random(20), 3)
    """
    0.5 * x ** 2 = Cada valor de x é elevado ao quadrado e multiplicado por 0.5 isso cria uma curva parabolica
    + 3 * x     = Adiciona um componente linear a curva
    + 5         = Adiciona constante 5 a todos o que desloca a curva para cima
    np.ran...   = Adiciona um termo aleatorio a y, noise contra a escala de ruido aleatorio
    """
    y = 0.5*x**2+3*x+5+np.random.normal(scale=noise, size=20)

    p1 = plt.scatter(x, y, edgecolors='k')
    plt.xlabel('Y-Values')
    plt.ylabel('X-Values')
    plt.title('Scatter plot')

    figure_x, figure_y, figure_w, figure_h = fig_1.bbox.bounds
    return (x,y,fig_1,figure_x, figure_y, figure_w, figure_h)


def fit_redraw(x,y,model):
    fig_2 = plt.figure(dpi=125)

    # Tirando o minimo e maximo dos valores de x
    x_min, x_max = np.min(x), np.max(x)

    # Gerando valores de x e y de regressao para gerar a curva
    x_reg = np.arange(x_min, x_max, 0.01)
    # Cria funcao polimial com base no model e nos valores de x
    y_reg = np.poly1d(model)(x_reg)

    # Traça o grafico "original"
    p1 = plt.scatter(x, y, edgecolors='k')
    # traça a linha laranha com 3 de grossura
    p2 = plt.plot(x_reg, y_reg, color='orange', lw=3)

    plt.ylabel('Y-Values')
    plt.xlabel('X-Values')
    plt.title('Grafico de dispersão com fita')

    return fig_2


def draw_figure(canvas, figure, loc=(0,0)):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
    return figure_canvas_agg


def delete_fig_agg(fig_agg):
    fig_agg.get_tk_widget().forget()
    plt.close('all')


layout = [
    [sg.Button('Generate', enable_events=True, key='-GENERATE-'),
     sg.Button('Fit', enable_events=True, key='-FIT-', size=(10,1))],
    [sg.Text('Ruido gausiano (devio padrao)'),
     sg.Slider(range=(0,100), default_value=10, size=(20,20), orientation='h', key='-NOISE-')],
    [sg.Canvas(size=(350,350), key='-CANVAS-', pad=(20,20))],
    [sg.Button('Exit')]
]


window = sg.Window('Polynomial fitting', layout, size=(700,700))



fig_agg = None
while True:
    event, values = window.read()

    if event in (sg.WIN_CLOSED, 'Exit'):
        break

    if event == '-GENERATE-':
        noise = values['-NOISE-']
        # Se a figura nao é vazia, entao tem grafico, entao eu deleto
        if fig_agg is not None:
            delete_fig_agg(fig_agg)

        x,y,fig_1,figure_x,figure_y,figure_w,figure_h = gerar_dados()

        canvas_elem = window['-CANVAS-'].TKCanvas
        canvas_elem.Size = (int(figure_w), int(figure_h))

        fig_agg = draw_figure(canvas_elem, fig_1)

    if event == '-FIT-':
        model = np.polyfit(x, y, 2)
        if fig_agg is not None:
            delete_fig_agg(fig_agg)

        fig_2 = fit_redraw(x, y, model)

        canvas_elem = window['-CANVAS-'].TKCanvas
        fig_agg = draw_figure(canvas_elem, fig_2)


window.close()


