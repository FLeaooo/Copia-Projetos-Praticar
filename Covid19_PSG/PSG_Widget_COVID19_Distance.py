import PySimpleGUI as sg
from geopy.distance import distance
from geopy.geocoders import Nominatim
from geopy.geocoders import options

from json import load as jsonload
from json import dump as jsondump

from os import path
from os import remove
from datetime import datetime
from webbrowser import open as webopen
from urllib import request
from csv import reader as csvreader

# Escolhendo o tema da janela do PSG
sg.theme('Dark Red')
# sg.theme('Light Green 6')

# Definição de variaveis
TXT_COLOR = sg.theme_text_color()
BG_COLOR = sg.theme_background_color()
ALPHA = 1.0
REFRESH_RATE_IN_MINUTES = 5
NUM_DATA_LINES = 5

# Configuração inicial
DEFAULT_SETTINGS = {'zipcode': 'New York, NY', 'country': 'United States', 'units':'miles'}

# Esta linha de codigo serve para construir o caminho completo para o arquivo C19-widget.cfg
#   pois o path dirname pega o caminho do arquivo atual e junta com o resto o "r" serve para pegar caracteres especiais
#   eu nao tinha entendido bem entao joguei no chat gpt e compreendi
SETTINGS_FILE = path.join(path.dirname(__file__), r'C19-widget.cfg')


# Funcao que tenta abrir o arquivo SETTINGS_FILE caso nao de ela recebe o DEFAULT_SETTINGS
def load_settings():
    try:
        with open(SETTINGS_FILE, 'r') as f:
            settings = jsonload(f)
    except:
        sg.popup_quick_message('No settings file found... Will create one for you', keep_on_top=True,
                               background_color='red', text_color='white')
        settings = change_settings(DEFAULT_SETTINGS)
        save_settings(settings)
    return settings


# Salva a configuracao
def save_settings(settings):
    with open(SETTINGS_FILE, 'w') as f:
        jsondump(settings, f)


def change_settings(settings):
    # Cria o layout o interessante é que ele usa settings.get que eu nunca tinha visto antes e entendi como funciona
    layout = [[sg.T('Zipcode OR City, State for you location')],
              [sg.I(settings.get('zipcode', ''), size=(15,1), key='zipcode')],
              [sg.T('Country')],
              [sg.I(settings.get('country', 'United States'), size=(15,1), key='country')],
              [sg.T('Distance'),
               # aqui a mesma coisa, interessante isto de usar o if e else false
              sg.R('Miles', 1, default=True if settings.get('units') == 'miles' else False, key='-MILES-'),
              sg.R('Kilometers', 1, default=True if settings.get('units') == 'kilometers' else False, key='-KILOMETERS-'), ],
              [sg.B('Ok', border_width=0, bind_return_key=True), sg.B('Cancel', border_width=0)],
              ]

    # Cria uma janela com base neste layout
    window = sg.Window('Settings', layout, keep_on_top=True, border_depth=0)
    event, values = window.read()
    window.close()

    # Se apertou ok entao settings troca de valores pelas info inseridas la
    if event == 'Ok':
        settings['zipcode'] = values['zipcode']
        settings['country'] = values['country']
        settings['units'] = 'miles' if values['-MILES-'] else 'kilometers'

    return settings


def distance_list(settings, window):
    # Setup geolocator
    options.default_user_agent = 'covid19-distance-widget'
    options.default_timeout = 7
    geolocator = Nominatim(user_agent="covid19-distance-widget")



    # Find location based on my zip code
    try:
        location = geolocator.geocode(f'{settings["zipcode"]} {settings["country"]}')
        my_loc = (location.latitude, location.longitude)
        window['-LOCATION-'].update(location.address)
        window['-LATLON-'].update(my_loc)
    except Exception as e:
        sg.popup_error(f'Exception computing distance. Exception {e}', 'Deleting your settings file so you can restart'
                        'from scratch', keep_on_top=True)
        remove(SETTINGS_FILE)
        exit(69)


    # Esta parte perguntei bastante ao chat gpt
    # Dowload and parse the CSV file
    file_url = r"https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv"


    # lista criada com o arquivo csv e converte ao formato utf-8
    data = [d.decode('utf-8') for d in request.urlopen(file_url).readlines()]

    # adiciona espaco em branco nas cidades ques nao tem nome
    for n, row in enumerate(data):
        data[n] = 'Unknown' + row if row[0] == "," else row

    # Separa cada linha em uma lista de dados
    data_split = [row[0:4] + row[-1:] for row in csvreader(data)]

    # Acha o dado da ultima atualização
    last_updated = data_split[0][-1]
    cities = data_split[1:]

    def distance_in_miles(my_loc, city_loc):
        return distance(my_loc, city_loc).miles


    # Adiciona e calcula a distancia de cada localização da cidade
    distances = []
    for n, row in enumerate(cities):
        city_loc = tuple(row[2:4])
        distances.append((distance_in_miles(my_loc,city_loc), n))


    # Localizações mais proximas
    dist_ranked = sorted(distances)
    top = dist_ranked[:10]

    # Criando dicionario das cidades mais proximas + miles
    top_dict = {}
    for n, row in enumerate(top):
        miles, index = row
        top_dict[n] = cities[index] + [miles]

    # Adicionando a distancia das top dict em uma lista
    distances = []
    for k, v in top_dict.items():
        distances.append([v[0],v[1], v[5]])

    return distances


def update_display(window, distances, settings):
    # Se a distances não é vazia
    if distances is not None:
        values = distances
        out = [f'{"Location":27}{"Country":4}   {"Miles":6}{"Kilometers":8}']
        for i, data in enumerate(values):
            out.append(f'{data[0]:30} {data[1]:4} {data[-1]:8.2f} {data[-1] * 1.61:8.2f}')
        for i, line in enumerate(out):
            if i >= NUM_DATA_LINES:
                break
            window[i].update(line)
        window['-ZIP-'].update(settings['zipcode'])
        nearest = distances[0][-1]

        # Caso unidade seja km ele faz a conversao
        if settings.get('units') == 'kilometers':
            window['-NEAREST-'].update(f'{nearest*1.61:.2f} Kilometers')
        else:
            window['-NEAREST-'].update(f'{nearest:.2f} Miles')

    window['-UPDATED-'].update('Updated: ' + datetime.now().strftime("%B %d %I:%M:%S %p"))


def create_window():
    # Criando a janela aplicada
    PAD = (0,0)

    main_data_col = [[sg.T(size=(58,1), font='Courier 12', key=i, background_color=sg.theme_text_color(),
                           text_color=sg.theme_background_color(), pad=(0,0),)] for i in range(NUM_DATA_LINES)]

    layout = [[sg.T('COVID-19 Distance', font='Arial 35 bold', pad=PAD),
               sg.T('x', font=('Arial Black', 16), pad=((110,5),(0,0)), enable_events=True, key='-QUIT-')],
              [sg.T(size=(15,1), font='Arial 35 bold', key='-ZIP-', pad=PAD)],
              [sg.T(size=(18,1), font='Arial 30 bold', key='-NEAREST-', pad=PAD)],
              [sg.T(size=(70,2), key='-LOCATION-')],
              [sg.T(size=(40,1), key='-LATLON-')],
              [sg.Col(main_data_col, pad=(0,0))],
              [sg.T(size=(40,1), font='Arial 8', key='-UPDATED-')],
              [sg.T('Settings', key='-SETTINGS-', enable_events=True),
               sg.T('       Latest Statistics', key='-MOREINFO-', enable_events=True),
               sg.T('       Refresh', key='-REFRESH-', enable_events=True)],]

    window = sg.Window(layout=layout, title='COVID Distance Widget', margins=(0,0), finalize=True,
                       keep_on_top=True, no_titlebar=True, grab_anywhere=True, alpha_channel=ALPHA)

    for key in ['-SETTINGS-', '-MOREINFO-', '-REFRESH-', '-QUIT-']:
        window[key].set_cursor('hand2')

    return window


def main():
    settings = load_settings()

    window = create_window()

    distances = distance_list(settings, window)
    update_display(window, distances, settings)

    while True:
        event, values = window.read(timeout=REFRESH_RATE_IN_MINUTES * 60 * 1000)
        if event in (None, 'Exit', '-QUIT-'):
            break
        elif event == '-SETTINGS-':
            settings = change_settings(settings)
            save_settings(settings)
        elif event == '-MOREINFO-':
            webopen(r'https://www.arcgis.com/apps/opsdashboard/index.html#/bda7594740fd40299423467b48e9ecf6')

        if settings['zipcode']:
            distances = distance_list(settings, window)
            update_display(window, distances, settings)

    window.close()


if __name__ == '__main__':
    main()



