import PySimpleGUI as sg
import random

"""
Organiza uma lista usando algoritmo "bubble_sort" e geradores para mostrar barra por barra na tela se organizando
Codigo copiado de:
https://github.com/PySimpleGUI/PySimpleGUI/blob/73a1b085ee07074a0057b05a37c18cd70a026576/DemoPrograms/Demo_Sort_Visualizer.py

"""

BAR_SPACING, BAR_WIDTH, EDGE_OFFSET = 11, 10, 3
DATA_SIZE = GRAPH_SIZE = (700, 500)


# Ordenara a lista "arr" usando algoritmo de ordenação por bolha
def bubble_sort(arr):
    # Funcao que troca os valores
    def swap(i, j):
        arr[i], arr[j] = arr[j], arr[i]

    # Tamanho da lista usado para controlar o loop de iteração
    n = len(arr)
    swapped = True
    x = -1

    # Enquanto swapped(trocado) for true
    while swapped:
        swapped = False
        x += 1
        # Loop for de 1 ate n - 0,1,2,3... pois a ultima posicao nao precisa comparar pois ja sei que ela é a maior
        for i in range(1, n - x):
            # Se lista na pos [0] > [1]... [1] > [2]
            if arr[i - 1] > arr[i]:
                # Faz a troca
                swap(i-1, i)
                # Mantem como true
                swapped = True
                # Ele ta retornando alocando aqui uma lista da primeira troca, esta é a pos 0 dele,
                # entao quando "partially_sorted_list = bsort.__next__()" o que acontece é que a lista recebe
                # a lista 0,1,2.... ate chegar na ultima e cada lista é uma repetição do algoritmo bolha
                # assim eu consigo atualizar o grafico vez por vez para ver as barras indo ate o final
                yield arr


# Aqui é passado o grafico e a lista dos numeros do grafico
def draw_bars(graph, items):
    # Vai passar por todos os numeros ou seja barras e desenhar
    for i, item in enumerate(items):
        graph.draw_rectangle(top_left=(i * BAR_SPACING + EDGE_OFFSET, item),
                             bottom_right=(i * BAR_SPACING + EDGE_OFFSET + BAR_WIDTH, 0),
                             fill_color='#76506d')


def main():
    sg.theme('LightGreen')
    # Gere uma lista para organizar
    num_bars = DATA_SIZE[0]//(BAR_WIDTH+1)
    list_to_sort = [DATA_SIZE[1]//num_bars*i for i in range(1, num_bars)]
    # Funcao para embaralhar a lista
    random.shuffle(list_to_sort)

    # Define a janela
    graph = sg.Graph(GRAPH_SIZE, (0,0), DATA_SIZE)
    layout = [[graph],
                [sg.Text('Speed     Faster'),
                 sg.Slider((0, 20), orientation='h', default_value=10, key='-SPEED-'),
                 sg.Text('Slower')]]

    window = sg.Window('Sort Demonstration', layout, finalize=True)
    # Desenha as barras iniciais
    draw_bars(graph, list_to_sort)

    # Espera o usuario apertar ok
    sg.popup('Click ok to begin Bubblesort')

    # Gera um iterador para organizar
    bsort = bubble_sort(list_to_sort)

    timeout = 10
    while True:
        event, values = window.read(timeout=timeout)
        if event == sg.WIN_CLOSED:
            break
        try:
            partially_sorted_list = bsort.__next__()
        except:
            sg.popup('Sorting done')
            break

        # Limpa o grafico
        graph.erase()
        # desenha o grafico
        draw_bars(graph, partially_sorted_list)
        # recebe o valor do slider para a velocidade de gerar o grafico
        timeout = int(values['-SPEED-'])


    window.close()


if __name__ == '__main__':
    main()
