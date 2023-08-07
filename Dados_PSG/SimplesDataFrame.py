import PySimpleGUI as sg
import pandas as nd
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


def read_table():
    sg.set_options(auto_size_buttons=True)
    # Abre janela para abrir arquivo ou CSV ou txt
    filename = sg.popup_get_file(
        'Dataset to read',
        title='Dataset to read',
        no_window=True,
        file_types=(("CSV Files", "*.csv"), ('Text Files', '*.txt'))
    )

    if filename == '':
        return

    dados = []
    lista_cabecalhos = []
    nomes_colunas_prompt = sg.popup_yes_no('Este arquivo ja tem nome de colunas?')
    nan_prompt = sg.popup_yes_no('Descartar NaN (entradas vazias)?')

    if filename is not None:
        # Pegando o nome do arquivo e nao o caminho inteiro
        fn = filename.split('/')[-1]
        try:
            if nomes_colunas_prompt == 'Yes':
                # Le o arquivo
                df = pd.read_csv(filename, sep=',', engine='python')

                # Cria cabecalho com a primeira linha dos dados pois tem nomes de coluna
                lista_cabecalhos = list(df.columns)

                # Cria uma lista de listas descartando a primeira linha o cabecalho
                dados = df[1:].values.tolist()

            else:  # Caso o arquivo nao tenha nome de colunas
                df = pd.read_csv(filename, sep=',', engine='python', header=None)

                # Cria nome de colunas para cada coluna
                lista_cabecalhos = ['column' + str(x) for x in range(len(df.iloc[0]))]
                df.columns = lista_cabecalhos

                dados = df.values.tolist()

            if nan_prompt == 'Yes':
                df = df.dropna()

            return (df, dados, lista_cabecalhos, fn)

        except:
            sg.popup_error('Error reading file')
            return


def mostrar_tabela(dados, lista_cabecalhos, fn):
    layout = [
        [sg.Table(values=dados,
                  headings=lista_cabecalhos,
                  font='Helvetica',
                  pad=(25,25),
                  display_row_numbers=False,
                  auto_size_columns=True,
                  num_rows=min(25, len(dados)))]
    ]

    window = sg.Window(fn, layout, grab_anywhere=False)
    event, values = window.read()
    window.close()


def show_stats(df):
    # Calcula as estatisticas descritivas usando DataFrame df, .T para ser exibida por coluna
    stats = df.describe().T

    # Lista cabeçalho com base no Data frame
    lista_cabecalho = list(stats.columns)

    # Cria lista de listas com os dados, com base nas estatiticas, cada linha representa uma lista da tabela de exibicao
    dados = stats.values.tolist()

    # Percorre a lista de lista de estatisticas e enumerando
    for i, d in enumerate(dados):
        # Inseri na pos 0 da linha i o nome da linha
        d.insert(0,list(stats.index)[i])

    # A primeira coluna represenha as caracteristicas (Miles_per_Gallon, Cylinder...)
    lista_cabecalho = ['Feature'] + lista_cabecalho

    layout = [
        [sg.Table(values=dados,
                  headings=lista_cabecalho,
                  font='Helvetica',
                  pad=(10,10),
                  display_row_numbers=False,
                  auto_size_columns=True,
                  num_rows=min(25, len(dados)))]
    ]

    window = sg.Window('Estatisticas', layout, grab_anywhere=False)
    event, values = window.read()
    window.close()


def plot_fig(df):
    # Criando figura vazia para adicionar graficos depois do matplotlib com 100 dpi (pontor por polegada)
    fig = plt.figure(dpi=100)

    # X recebe o os dados do data frame da coluna [3]
    x = list(df.columns)[3]
    y = list(df.columns)[5]

    # Criando grafico
    fig.add_subplot(111).scatter(df[x], df[y], color='blue', edgecolor='k')

    plt.xlabel(x)
    plt.ylabel(y)

    # ------------------------------- END OF YOUR MATPLOTLIB CODE -------------------------------

    # ------------------------------- Beginning of Matplotlib helper code -----------------------

    def draw_figure(canvas, figure):
        # Canvas é o canvas onde a figura sera desenhada
        # Figure é o grafico
        # Cria uma figura canvas usando o Tkinter
        figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
        # Usa o TkAgg para desenhar e converter a figura em um widget para a GUI
        figure_canvas_agg.draw()
        figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
        return figure_canvas_agg

    # ------------------------------- Beginning of GUI CODE -------------------------------

    # define the window layout
    layout = [[sg.Text(f'Plot of {x} vs. {y}')],
              [sg.Canvas(key='-CANVAS-',
                         size=(700,500),
                         pad=(15,15))],
              [sg.Button('Ok')]
              ]

    # Cria a forma e mostra sem o grafico
    window = sg.Window('Plot',
                       layout,
                       size=(800,600),
                       finalize=True,
                       element_justification='center',
                       font='Helvetica 18')

    # Adiciona o grafico na janela
    fig_canvas_agg = draw_figure(window['-CANVAS-'].TKCanvas, fig)

    event, values = window.read()

    window.close()



def main():
    df, dados, lista_cabecalho, fn = read_table()

    # mostrar dados?
    show_prompt = sg.popup_yes_no('Mostrar dataset?')
    if show_prompt == 'Yes':
        mostrar_tabela(dados, lista_cabecalho, fn)

    # Mostrar estatisticas?
    stats_prompt = sg.popup_yes_no('Mostrar descrição das estatisticas?')
    if stats_prompt == 'Yes':
        show_stats(df)

    # Mostrar grafico?
    plot_prompt = sg.popup_yes_no('Mostrar grafico de disperção?')
    if plot_prompt == 'Yes':
        plot_fig(df)



if __name__ == '__main__':
    main()






