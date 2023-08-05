import PySimpleGUI as sg
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import matplotlib.pyplot as plt
# matplotlib.use('TkAgg')

"""
Codigo copiado de 
https://github.com/PySimpleGUI/PySimpleGUI/blob/73a1b085ee07074a0057b05a37c18cd70a026576/DemoPrograms/Demo_Pyplot_Bar_Chart2.py
"""

# ------------------------------- PASTE YOUR MATPLOTLIB CODE HERE -------------------------------

label = ['Adventure', 'Action', 'Drama', 'Comedy', 'Thriller/Suspense', 'Horror', 'Romantic Comedy', 'Musical',
         'Documentary', 'Black Comedy', 'Western', 'Concert/Performance', 'Multiple Genres', 'Reality']
no_movies = [941, 854, 4595, 2125, 942,
             509, 548, 149, 1952, 161, 64, 61, 35, 5]

index = np.arange(len(label))
# [ 0  1  2  3  4  5  6  7  8  9 10 11 12 13]
plt.bar(index, no_movies)
plt.xlabel('Genre', fontsize = 5)
plt.ylabel('No of Movies', fontsize = 5)
plt.xticks(index, label, fontsize = 5, rotation=30)
plt.title('Market Share for Each Genre 1995-2017')

# ------------------------------- END OF YOUR MATPLOTLIB CODE -------------------------------

# ------------------------------- Beginning of Matplotlib helper code -----------------------


# Desenhar figura em um "canvas"
def draw_figure(canvas, figure, loc=(0, 0)):
    # Classe usada para desenhar graficos GUI
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
    return figure_canvas_agg


# ------------------------------- Beginning of GUI CODE -------------------------------

sg.theme('Light Brown 3')

fig = plt.gcf()  # Recebe a figura atual armazena em fig

figure_x, figure_y, figure_w, figure_h = fig.bbox.bounds

# Define a janela
layout = [[sg.Text('Plot test', font='Any 18')],
          [sg.Canvas(size=(figure_w, figure_h), key='-CANVAS-')],
          [sg.OK(pad=((figure_w / 2, 0), 3), size=(4, 2))]
          ]

# Cria a janela sem o grafico
window = sg.Window('Demo Application - Embedding Matplotlib in PySimpleGUI',
                   layout, force_toplevel=True, finalize=True)

# Adiciona o grafico na janela
fig_photo = draw_figure(window['-CANVAS-'].TKCanvas, fig)

event, values = window.read()

window.close()