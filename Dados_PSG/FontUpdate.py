import PySimpleGUI as sg

# App que mostra como fonte funciona no PSG

lista_font = ['Arial ',
                'Helvetica ',
                'Times New Roman ',
                'Courier New ',
                'Verdana ',
                'Calibri ',
                'Georgia ',
                'Palatino ',
                'Tahoma ',
                'Impact ']

layout = [[sg.Text('Uma amostra de texto', size=(20,1), key='-TEXT-')],
          [sg.Combo(values=lista_font, default_value=lista_font[0], key='-COMBO_FONT-'),
           sg.Button('Trocar')],
          [sg.CB('Bold', key='-BOLD-', change_submits=True),
          sg.CB('Italics', key='-ITALICS-', change_submits=True),
          sg.CB('Underline', key='-UNDERLINE-', change_submits=True)],
          [sg.Slider((6, 50), default_value=12, size=(14,20),
                     orientation='h', key='-SLIDER-', change_submits=True),
           sg.Text('Font size')],
          [sg.Text('Font string = '), sg.Text('', size=(25,1), key='-FONTSTRING-')],
          [sg.Button('Exit')]]

window = sg.Window('Font string builder', layout)

font = 'Arial '
text_elem = window['-TEXT-']
while True:
    event, values = window.read()
    if event in (sg.WIN_CLOSED, 'Exit'):
        break

    # Eu criei um combo com lista de fonts e um botao trocar quando ele apertar o botao eu recebo o nome da font
    if event == 'Trocar':
        font = values['-COMBO_FONT-']

    # Aqui eu passo por todas as configurações da font e vou adicionando
    font_string = font
    font_string += str(int(values['-SLIDER-']))
    if values['-BOLD-']:
        font_string += ' bold'
    if values['-ITALICS-']:
        font_string += ' italic'
    if values['-UNDERLINE-']:
        font_string += ' underline'

    # Atualizo a font do [-TEXT-]
    text_elem.update(font=font_string)
    # Ultima linha que mostra a font e as outras opcoes
    window['-FONTSTRING-'].update('"'+font_string+'"')


window.close()