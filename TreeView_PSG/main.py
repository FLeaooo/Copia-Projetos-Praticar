import PySimpleGUI as sg

sg.set_options(font=('Arial Bold', 14))

# Criando uma lista, para fazer arvores de dados.
# "": identifica que é o nivel raiz da arvore
# BIO: é o identificador unico da linha sera usado como a chave do elemento da arvore
# Biology: O nome da disciplina
# Outros elementos: Vazios pois nas outras linhas serao as notas do aluno e nesta é a disciplina
# "ADR-BIO" é para identificar o nome(ADR) do aluno e a materia(BIO)
data_alunos = [
    ["","BIO", "Biology", "", "", ""],
    ["BIO", "ADR-BIO", "Adrian", 97, 83, 92],
    ["BIO", "LIA-BIO", "Liam", 89, 91, 101],
    ["BIO", "CEL-BIO", "Celia", 101, 95, 102],
    ["","CHM", "Chemistry", "", "", ""],
    ["CHM", "ADR-CHM", "Adriam", 85, 91, 99],
    ["CHM", "LIA-CHM", "Liam", 86, 100, 92],
    ["CHM", "CEL-CHM", "Celia", 99, 101, 98]
]

headings = ['Quiz 1', 'Homework 1', 'Quiz 2']


# Gera um treedata do PysimpleGUI
def generate_tree_data_object(data):
    tree_data = sg.TreeData()
    for row in data:
        tree_data.Insert(row[0], row[1], row[2], row[3:])
    return tree_data


# Extraindo as chaves das materias dos dados
def extract_subjects(data):
    subjects = []
    for i in range(len(data)):
        # Caso pos 1 da lista seja "" quer dizer que é uma materia
        if data[i][0] == "":
            # Adiciona a chave da materia na lista de subjects
            subjects.append(data[i][1])
    return subjects


# criando lista das chaves das materias
subject_list = extract_subjects(data_alunos)

# Criando o layout da janela do PysimpleGUI
layout = [
    [sg.Tree(
        data=generate_tree_data_object(data_alunos),
        headings=headings,
        auto_size_columns=True,
        key='-TREE-',
        show_expanded=True,
        enable_events=True,
        expand_x=True,
        expand_y=True
    )],
    [sg.Text('Subject'), sg.Input('', enable_events=True, size=(10,1), key='-SUBJECT_CODE-', justification='right'),
     sg.Text('Subject Name:'), sg.Input('', enable_events=True, size=(10,1), key='-SUBJECT_NAME-', justification='right')],
    [sg.Button('Insert Subject', expand_x=True)],
    [sg.Text('Subject:'), sg.Combo(subject_list, default_value=subject_list[0], key='-SUBJECT-', enable_events=True)],
    [sg.Text('Name:'), sg.Input('', size=(10, 1), enable_events=True, justification='right', key='-NAME-')],
    [sg.Text('Prova 1:'), sg.Input('', size=(3, 1), enable_events=True, justification='right', key='-PROVA1-'),
     sg.Text('Prova 2:'), sg.Input('', size=(3, 1), enable_events=True, justification='right', key='-PROVA2-'),
     sg.Text('Prova 3:'), sg.Input('', size=(3, 1), enable_events=True, justification='right', key='-PROVA3-')],
    [sg.Button('Inserir', expand_x=True), sg.Button('Delete', expand_x=True)]
]

window = sg.Window('Gradebook', layout, size=(600,600), resizable=True)


# Inserir materia, atualiza a arvore de elemento e cria uma nova materia, retorna lista de materias
def inserir_materia(codigo_materia, nome_materia, tree_element):
    # Adicionando nos dados do aluno a lista da nova materia
    data_alunos.append(["", codigo_materia, nome_materia, "", "", ""])
    # Criando uma arvore de dados com base nesta nova lista que é a mesma
    tree_data = generate_tree_data_object(data_alunos)
    # Atualiza a arvore de elementos para a arvore com novos dados
    tree_element.update(tree_data)
    # Cria a lista de materias e retorna ela
    subject_list=extract_subjects(data_alunos)
    return subject_list


def inserir_aluno(materia, nome, notas, tree_element):
    # Laço que passa em cada linha da lista de dados dos alunos
    for i in range(len(data_alunos)):
        # Caso esta linha seja a da materia que estou inserindo um novo aluno
        if data_alunos[i][0] == "" and data_alunos[i][1] == materia:
            # j = a linha que estou + 1
            j = i + 1
            # Isto é para o aluno ser adicionado na ultima linha daquela materia
            while(j < len(data_alunos) and (data_alunos[j][0] == data_alunos[i][1])):
                j += 1
            # Inserindo nos dados o aluno na posicao j
            data_alunos.insert(j, [materia, nome[0:2], nome, notas[0], notas[1], notas[2]])
            # Criando nova arvore de dados com este dados de alunos
            tree_data = generate_tree_data_object(data_alunos)
            # Atualizando a arvore de elemento para esta arvore de dados
            tree_element.update(tree_data)


def deletar_aluno(linha_selecionada, tree_element):
    # Passando em cada linha dos dados
    for row in data_alunos:
        # Caso a linha selecionada seja igual a linha que esta passando
        if linha_selecionada == row[1]:
            # Deletando a linha selecionada dos dados
            data_alunos.remove(row)
    # Criando uma arvore de dados com base nessa nova lista de dados
    tree_data = generate_tree_data_object(data_alunos)
    # Atualizar a arvore de elementos com base nesta nova arvore de dados
    tree_element.update(tree_data)



linha_selecionada = ""
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED:
        break

    if event == 'Insert Subject':
        # vai receber os dados da janelaa
        tree_element = window['-TREE-']
        # Inserindo materia e retorna a lista
        nova_lista_materias = inserir_materia(values['-SUBJECT_CODE-'], values['-SUBJECT_NAME-'], tree_element)
        # Atualizando a parte das materias da janela do combo
        window['-SUBJECT-'].update(value=nova_lista_materias[0], values=nova_lista_materias)

    if event == 'Inserir':
        # Vai receber a arvore da janela
        tree_element = window['-TREE-']
        # Chamando a funcao de inserir aluno, passando materias com base na propria janela
        inserir_aluno(values['-SUBJECT-'], values['-NAME-'], [values['-PROVA1-'], values['-PROVA2-'],
                                                              values['-PROVA3-']], tree_element)

    # Serve para saber qual a linha que esta selecionada na janela
    if event == '-TREE-':
        linha_selecionada = values['-TREE-'][0]

    if event == 'Delete':
        tree_element = window['-TREE-']
        deletar_aluno(linha_selecionada, tree_element)

window.close()