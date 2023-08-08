import PySimpleGUI as sg
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


def read_table():
    # Cria layout para ler o arquivo
    sg.set_options(auto_size_buttons=True)
    layout = [
        [sg.Text('Dataset (arquivo CSV)', size=(16,1)), sg.InputText(),
         sg.FileBrowse(file_types=(("CSV Files", "*.csv"),("Text Files", "*.txt")))],
        [sg.Submit(), sg.Cancel()]
    ]

    window1 = sg.Window('Input file', layout)

    # Tenta ler
    try:
        event, values = window1.read()
        window1.close()
    except:
        window1.close()
        return

    # Nome do arquivo = values[0]
    filename = values[0]

    # Se o nome estiver em branco, retorna entao sai da funcao
    if filename == '':
        return

    dados = []
    lista_cabecalho = []

    if filename is not None:
        # Pega o nome do arquivo
        fn = filename.split('/')[-1]

        try:
            if colnames_checked:
                # O pandas ler o arquivo csv
                df = pd.read_csv(filename, sep=',', engine='python')

                # Usando a primeira linha que sao os nomes das colunas
                lista_cabecalho = list(df.columns)

                # Cria lista de dados tirando linha 0, que é o nome das colunas
                dados = df[1:].values.tolist()

            else:
                # Caso o arquivo nao tenha nome de colunas
                df = pd.read_csv(filename, sep=',', engine='python', header=None)

                # Cria nome de colunas (coluna0...)
                lista_cabecalho = ['coluna' + str(x) for x in range(len(df.iloc[0]))]
                df.columns = lista_cabecalho

                # Le o restante em uma lista de linha
                dados = df.values.tolist()

            # Descarta NAN?
            if dropnan_checked:
                df = df.dropna()
                dados = df.values.tolist()

            window1.close()
            return (df, dados, lista_cabecalho, fn)

        except:
            sg.popup_error("Error ao ler o arquivo")
            window1.close()
            return



def show_table(dados, lista_cabecalho, fn):
    # Funcao que mostra os dados do arquivo em uma tabela
    layout = [
        [sg.Table(values=dados,
                  headings=lista_cabecalho,
                  pad=(25,25),
                  display_row_numbers=False,
                  auto_size_columns=True,
                  num_rows=min(25, len(dados)))]
    ]

    window = sg.Window(fn, layout, grab_anywhere=False)

    event, values = window.read()
    window.close()


def show_estatisticas(df):
    # Funcao que Mostra as estatisticas do data frama

    # describe calculas as estatisticas do df e .T tranpoem, ou seja troca linha por coluna para ficar mais legivel
    stats = df.describe().T

    # Lista cabecalho das estatisticas
    lista_cabecalho = list(stats.columns)

    dados = stats.values.tolist()

    for i, d in enumerate(dados):
        d.insert(0,list(stats.index)[i])

    # Adiciona coluna dos nomes das linhas
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


def sklearn_model(output_var):
    # Builds and fits a ML model
    from sklearn.ensemble import RandomForestClassifier

    # Remove coluna de saida (var dependente) para obter as caracteristicas (var independente)
    X = df.drop([output_var], axis=1)

    # Define a coluna de saida
    y = df[output_var]

    # Cria classificador Random Forest 20 estimadores e profundidade 4 para cada arvor
    clf = RandomForestClassifier(n_estimators=20, max_depth=4)

    # Ajusta e treina o modelo com caracteristicas X e y
    clf.fit(X, y)
    # Calcula a pontuação de precisao do modelo nos dados de treinamento
    return clf, np.round(clf.score(X, y), 3)


# ===================================================
# Definindo a janela
layout = [
    [sg.Button('Carregar dados', size=(10,1), enable_events=True, key='-READ-'),
     sg.Checkbox('Coluna tem nomes?', size=(15,1), key='colnames-check', default=True),
     sg.Checkbox('Descartas NAN?', size=(15,1), key='drop-nan', default=True)],
    [sg.Button('Mostrar dados', size=(10,1), enable_events=True, key='-SHOW-',),
     sg.Button('Mostrar estatisticas', size=(15,1), enable_events=True, key='-STATS-',)],
    [sg.Text("", size=(50,1), key='-loaded-', pad=(5,5),)],
    [sg.Text('Selecione output coluna', size=(18,1), pad=(5,5),)],
    [sg.Listbox(values=(''), key='colnames', size=(30,3), enable_events=True), ],
    [sg.Text("", size=(50,1), key='-prediction-', pad=(5,5),)],
    [sg.ProgressBar(50, orientation='h', size=(100,20), key='progressbar')],
]

# Criar janela
window = sg.Window("Pima", layout, size=(600,300))
progress_bar = window['progressbar']
prediction_text = window['-prediction-']
colnames_checked = False
dropnan_checked = False
read_successful = False

while True:
    event, values = window.read()
    loaded_text = window['-loaded-']

    if event in (sg.WIN_CLOSED, 'Exit'):
        break

    if event == '-READ-':
        if values['colnames-check'] == True:
            colnames_checked = True
        if values['drop-nan'] == True:
            dropnan_checked = True

        try:
            df, dados, lista_cabecalho, fn = read_table()
            read_successful = True
        except:
            pass

        if read_successful:
            loaded_text.update(f'Dataset carregado: {fn}')
            col_vals = [i for i in df.columns]
            window.Element('colnames').Update(values=col_vals)

    if event == '-SHOW-':
        if read_successful:
            show_table(dados, lista_cabecalho, fn)
        else:
            loaded_text.update('No dataset was loaded')

    if event == '-STATS-':
        if read_successful:
            show_estatisticas(df)
        else:
            loaded_text.update('No dataset was loaded')

    if event == 'colnames':
        if len(values['colnames']) != 0:
            output_var = values['colnames'][0]
            if output_var != 'Class variable':
                sg.Popup("Coluna selecionada errada", title='Wrong')
            else:
                prediction_text.update("Fitting model...")
                for i in range(50):
                    event,values = window.read(timeout=10)
                    progress_bar.UpdateBar(i + 1)

                _, score = sklearn_model(output_var)
                prediction_text.update("Accuracy of Random Forest model is: {}".format(score))