import os

print('Lista komend:\nsaldo\nsprzedaż\nzakup\nkonto\nlista\nmagazyn\nprzegląd\nkoniec')

plik_magazyn = 'Magazyn.txt'
plik_saldo = 'Saldo_konta.txt'
plik_przeglad = 'Przegląd.txt'

def save_to_file(plik, zawartosc):
    with open(plik, 'w') as file:
        file.write(str(zawartosc))

def load_magazyn(plik_magazyn):
    with open(plik_magazyn, 'r') as file:
        magazyn = eval(file.readlines()[0])
        return magazyn

def load_saldo(plik_saldo):
    with open(plik_saldo, 'r') as file:
        konto = float(file.readlines()[0])
        return konto

def update_przeglad(plik_przeglad, historia):
    with open(plik_przeglad, 'a', encoding='UTF-8') as file:
        for line in historia:
            file.write(line + '\n')

if os.path.exists(plik_magazyn):
    magazyn = load_magazyn(plik_magazyn)
    print('Wczytuje magazyn z pliku')
else:
    magazyn = dict()
    print('Brak pliku z magazynem. Tworzę pusty magazyn')

if os.path.exists(plik_saldo):
    konto = load_saldo(plik_saldo)
    print('Wczytano saldo z pliku')
else:
    konto = 0.0
    print('Saldo puste')

historia = []
historiaod = 0
historiado = 0

while True:
    komenda = input('Podaj komendę: ').lower()
    if komenda == 'saldo':
        historia.append('saldo')
        kwota = int(input('Wpisz kwotę: '))
        historia.append(f'kwota:{kwota}')
        if (konto + kwota < 0):
            print('Brak wystarczających środków')
        else:
            konto += kwota
            print(f'Aktualny stan konta: {konto}')
            save_to_file(plik_saldo, konto)

    elif komenda == 'zakup':
        historia.append('zakup')
        produkt = input('Podaj nazwę produktu: ')
        historia.append(f'Produkt: {produkt}')
        kwota = int(input('Wpisz kwotę: '))
        historia.append(f'Kwota: {kwota}')
        ilosc = int(input('Podaj ilość: '))
        historia.append(f'Podano ilość: {ilosc}')
        if (konto - kwota) < 0:
            print('Brak środków na koncie do realizacji zakupu')
        else:
            if produkt in magazyn:
                magazyn[produkt]['ilosc'] = magazyn[produkt]['ilosc'] + int(ilosc)
                magazyn[produkt]['kwota'] = magazyn[produkt]['kwota'] + int(kwota)
            else:
                magazyn[produkt] = {'kwota': kwota, 'ilosc': ilosc}
                magazyn[produkt]['ilosc'] = int(ilosc)
                magazyn[produkt]['kwota'] = int(kwota)
            konto = konto - int(kwota)
            print(magazyn)

    elif komenda == 'sprzedaż':
        historia.append('sprzedaż')
        produkt = input('Podaj nazwę produktu: ')
        historia.append(f'Podano nazwę produktu: {produkt}')
        kwota = int(input('Wpisz kwotę: '))
        historia.append(f'Kwota: {kwota}')
        ilosc = int(input('Podaj ilość: '))
        historia.append(f'Podano ilość: {ilosc}')
        if produkt in magazyn.keys():
            if (kwota < 0 or magazyn[produkt]['ilosc'] < ilosc):
                print('Nie można sprzedać więcej niż jest na magazynie')
            else:
                if produkt in magazyn:
                    magazyn[produkt]['ilosc'] = magazyn[produkt]['ilosc'] - int(ilosc)
                    magazyn[produkt]['kwota'] = magazyn[produkt]['kwota'] - int(kwota)
                else:
                    magazyn[produkt] = {'kwota': kwota, 'ilosc': ilosc}
                    magazyn[produkt]['ilosc'] = int(ilosc)
                    magazyn[produkt]['kwota'] = int(kwota)
                konto = konto + int(kwota)
                print(magazyn)
        else:
            print('Brak towaru na magazynie')

    elif komenda == 'lista':
        historia.append('lista')
        #for key in magazyn.keys():
            #print(f"Produkt:{produkt}, Ilość:{ilosc}, Kwota:{kwota}".format(produkt = key, ilosc = magazyn[key]['ilosc'], kwota = magazyn[key]['kwota']))
        for item in magazyn.items():
            print(item)

    elif komenda == 'magazyn':
        historia.append('magazyn')
        produkt = input('Podaj nazwę produktu: ')
        if produkt in magazyn:
            print(f'Produkt: {produkt}, ilość: {magazyn[produkt]['ilosc']}')
        else:
            print('Brak produktu w magazynie')

    elif komenda == 'konto':
        historia.append('konto')
        print(f'Aktualny stan konta: {konto}')
        historia.append(f'Stan konta: {konto}')

    elif komenda == 'przegląd':
        historia.append('przegląd')
        histodstr = input('Od: ')
        histdostr = input('Do: ')
        if len(histodstr) > 0:
            historiaod = int(histodstr) - 1
        else:
            historiaod = 0
        if len(histdostr) > 0:
            historiado = int(histdostr) - 1
        else:
            historiado = len(historia) - 1
        #historiaod = int(input('Od: '))
        #historiado = int(input('Do: '))
        if historiaod < 0 or historiado < 0 or historiado < historiado or historiado > len(historia) - 1:
            print(f'Niedozwolone wartości, historia zawiera: {len(historia)} wpisów')
        else:
            #print(f'{historiaod}:{historiado}')
            for i in range(historiaod, historiado + 1):
                print(f'lp {i} : {historia[i]}')

    if komenda == 'koniec':
        historia.append('koniec')
        save_to_file(plik_magazyn, magazyn)
        update_przeglad(plik_przeglad, historia)
        break