import PySimpleGUI as sg
import numpy as np


# Função para atualizar numero gerado
def update_num():
    num_aleatorio = np.random.randint(1, 11)
    lista_nums.append(num_aleatorio)
    elemento_texto = window['-TEXT-']
    elemento_texto.update(f"Numero aleatorio: {num_aleatorio}")


# Cria o layout da janela
layout = [[sg.Button('Gerar Numero', enable_events=True, key='-GERAR-')],
          [sg.Text('Numero aleatorio: x', key='-TEXT-', size=(25, 1))],
          [sg.Multiline(expand_x=True, expand_y=True, no_scrollbar=True, size=(25,5), key='-MLINE_LISTA-')]]

window = sg.Window('Gerar int aleatorio', layout)

lista_nums = []
while True:
    event, values = window.read()

    if event == sg.WIN_CLOSED:
        break

    if event == '-GERAR-':
        update_num()
        window['-MLINE_LISTA-'].update(lista_nums)



window.close()

