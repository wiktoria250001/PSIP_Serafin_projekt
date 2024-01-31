import psycopg2 as ps
import requests as rq
from tkinter import *
from tkintermapview import TkinterMapView

db_params=ps.connect(
    database='postgres',
    user='postgres',
    password='wiki3476',
    host='localhost',
    port=5433
)
cursor=db_params.cursor()

create_jednostki_policji='''
    CREATE TABLE IF NOT EXISTS jednostki_policji (
    id INT PRIMARY KEY,
    nazwa TEXT(50),
    lokalizacja TEXT(50)
    );
'''
cursor.execute(create_jednostki_policji)
db_params.commit()

create_policjanci='''
    CREATE TABLE IF NOT EXISTS policjanci (
    id INT PRIMARY KEY,
    imie TEXT(50),
    nazwisko TEXT(50),
    miejscowosc TEXT(50),
    placowka TEXT(50)
    );
'''
cursor.execute(create_policjanci)
db_params.commit()

create_incydenty='''
    CREATE TABLE IF NOT EXISTS incydenty (
    id INT PRIMARY KEY,
    lokalizacja TEXT(50),
    typ TEXT(50),
    jednostka_policji TEXT(50)
    );
'''
cursor.execute(create_incydenty)
db_params.commit()


def auto_id_posterunki_dodawanie():

    sql_query_1 = f"SELECT * FROM public.jednostki_policji ORDER BY id ASC;"
    cursor.execute(sql_query_1)
    query_result = cursor.fetchall()
    nr=[]
    if not query_result:
        nr.append('1')
    else:
        for row in query_result:
            nr.append(row[0])
    return int(max(nr))+1

def auto_id_posterunki_aktualizacja():

    sql_query_1 = f"SELECT * FROM public.jednostki_policji ORDER BY id ASC;"
    cursor.execute(sql_query_1)
    query_result = cursor.fetchall()
    l_nr=[]  #lsta indeksow
    for row in query_result:
        l_nr.append(row[0])
    for idx, id in enumerate(l_nr):
        sql_query_2 = f"UPDATE public.jednostki_policji SET id='{idx+1}' WHERE id='{id}';"
        cursor.execute(sql_query_2)
        db_params.commit()


def auto_id_pracownicy_dodawanie():
    sql_query_1 = f"SELECT * FROM public.policjanci ORDER BY id ASC;"
    cursor.execute(sql_query_1)
    query_result = cursor.fetchall()
    nr = []
    if not query_result:
        nr.append('1')
    else:
        for row in query_result:
            nr.append(row[0])
    return int(max(nr)) + 1


def auto_id_pracownicy_aktualizacja():
    sql_query_1 = f"SELECT * FROM public.policjanci ORDER BY id ASC;"
    cursor.execute(sql_query_1)
    query_result = cursor.fetchall()
    l_nr = []  # lsta indeksow
    for row in query_result:
        l_nr.append(row[0])
    for idx, id in enumerate(l_nr):
        sql_query_2 = f"UPDATE public.policjanci SET id='{idx + 1}' WHERE id='{id}';"
        cursor.execute(sql_query_2)
        db_params.commit()


def auto_id_incydenty_dodawanie():
    sql_query_1 = f"SELECT * FROM public.incydenty ORDER BY id ASC;"
    cursor.execute(sql_query_1)
    query_result = cursor.fetchall()
    nr = []
    if not query_result:
        nr.append('1')
    else:
        for row in query_result:
            nr.append(row[0])
    return int(max(nr)) + 1


def auto_id_incydenty_aktualizacja():
    sql_query_1 = f"SELECT * FROM public.incydenty ORDER BY id ASC;"
    cursor.execute(sql_query_1)
    query_result = cursor.fetchall()
    l_nr = []  # lsta indeksow
    for row in query_result:
        l_nr.append(row[0])
    for idx, id in enumerate(l_nr):
        sql_query_2 = f"UPDATE public.incydenty SET id='{idx + 1}' WHERE id='{id}';"
        cursor.execute(sql_query_2)
        db_params.commit()

def get_coordinates(address):
    Url = "https://nominatim.openstreetmap.org/search"
    atrybut = {"q": address, "format": "json"}
    odp = rq.get(Url, atrybut)
    data = odp.json()
    latitude = data[0]["lat"]
    longitude = data[0]["lon"]
    return [float(latitude), float(longitude)]


def dostep(event=None):

    haslo=wejscie_entry.get()
    if haslo=='SERAFIN':

        def policja():

            #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
            # RAMKA TABELA 1
            #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

            def pokaz_wszystko_jednostki_policji():
                listbox_posterunki.delete(0, END)
                sql_query_1 = f"SELECT * FROM public.jednostki_policji ORDER BY id ASC;"
                cursor.execute(sql_query_1)
                query_result = cursor.fetchall()
                for index, obiekt in enumerate(query_result):
                    listbox_posterunki.insert(index, f'Jednostka {obiekt[1]}')

                auto_id_posterunki_aktualizacja()

            def dodawanie_posterunku():
                nazwa=entry_posterunki_nazwa.get()
                miejsce=entry_posterunki_miejsce.get()

                sql_query_1 = f"INSERT INTO public.jednostki_policji(id, nazwa, lokalizacja) VALUES ('{auto_id_posterunki_dodawanie()}', '{nazwa}', '{miejsce}');"
                cursor.execute(sql_query_1)
                db_params.commit()

                entry_posterunki_nazwa.delete(0, END)
                entry_posterunki_miejsce.delete(0, END)

                pokaz_wszystko_jednostki_policji()

            def edytowanie_posterunku():
                sql_query_1 = f"SELECT * FROM public.jednostki_policji ORDER BY id ASC;"
                cursor.execute(sql_query_1)
                query_result = cursor.fetchall()

                i=listbox_posterunki.index(ACTIVE)

                entry_posterunki_nazwa.delete(0, END)
                entry_posterunki_miejsce.delete(0, END)

                entry_posterunki_nazwa.insert(0, query_result[i][1])
                entry_posterunki_miejsce.insert(0, query_result[i][2])

                button_posterunki_dodaj.config(text='Wprowadź zmiany', command=lambda: aktualizowanie_posterunku(i))

            def aktualizowanie_posterunku(i):
                sql_query_1 = f"SELECT * FROM public.jednostki_policji ORDER BY id ASC;"
                cursor.execute(sql_query_1)
                query_result = cursor.fetchall()

                nazwa=entry_posterunki_nazwa.get()
                miejsce=entry_posterunki_miejsce.get()

                sql_query_2 = f"UPDATE public.jednostki_policji SET nazwa='{nazwa}',lokalizacja='{miejsce}' WHERE nazwa='{query_result[i][1]}' and lokalizacja='{query_result[i][2]}';"
                cursor.execute(sql_query_2)
                db_params.commit()

                button_posterunki_dodaj.config(text='Dodaj posterunek', command=dodawanie_posterunku)

                entry_posterunki_nazwa.delete(0, END)
                entry_posterunki_miejsce.delete(0, END)

                pokaz_wszystko_jednostki_policji()

            def usuwanie_posterunku():
                i = listbox_posterunki.index(ACTIVE)

                sql_query_1 = f"DELETE FROM public.jednostki_policji WHERE id='{i+1}';"
                cursor.execute(sql_query_1)
                db_params.commit()

                pokaz_wszystko_jednostki_policji()

            def szczegoly_posterunki():
                sql_query_1 = f"SELECT * FROM public.jednostki_policji ORDER BY id ASC;"
                cursor.execute(sql_query_1)
                query_result = cursor.fetchall()

                i = listbox_posterunki.index(ACTIVE)

                nazwa=query_result[i][1]
                miejsce=query_result[i][2]
                print(get_coordinates(miejsce)[0])
                siedziba_wsp=f'{round(get_coordinates(miejsce)[0],4)}\n {round(get_coordinates(miejsce)[1],4)}\n'

                label_nazwa_jednostki_info_wartosc.config(text=nazwa)
                label_siedziba_jednostki_info_wartosc.config(text=miejsce)
                label_siedziba_jedn_wsp_szczegoly_wartosc.config(text=siedziba_wsp)

            # GUI
            okno_jednostki = Toplevel(root_wybierz)
            okno_jednostki.title('Jednostki policji')
            okno_jednostki.state('zoomed')

            rama_jednostki=Frame(okno_jednostki)
            rama_jednostki.grid(row=0, column=0)

            ramka_jednostki_naglowek = Frame(rama_jednostki)
            ramka_jednostki_lista = Frame(rama_jednostki)
            ramka_jednostki_dod_ed = Frame(rama_jednostki)
            ramka_jednostki_info = Frame(rama_jednostki)

            ramka_jednostki_naglowek.grid(row=0, column=0, pady=(0,10))
            ramka_jednostki_lista.grid(row=1, column=0)
            ramka_jednostki_dod_ed.grid(row=2, column=0, pady=40)
            ramka_jednostki_info.grid(row=3, column=0)

            # ---------------------------------------
            # ramka posterunki policji czesc. 1
            # ---------------------------------------
            label_jednostki_lista = Label(ramka_jednostki_naglowek, text='Lista posterunkow policji', font=('Arial', 12, 'bold', 'underline'))
            button_pokaz_calosc = Button(ramka_jednostki_naglowek, text='Pokaż wszystko', command=pokaz_wszystko_jednostki_policji)

            label_jednostki_lista.grid(row=0, column=0, padx=(250 - label_jednostki_lista.winfo_reqwidth() / 2), pady=5)
            button_pokaz_calosc.grid(row=1, column=0)

            # ---------------------------------------
            # ramka posterunki tworzona jest lista posterunkow
            # ---------------------------------------
            listbox_posterunki = Listbox(ramka_jednostki_lista, width=50)
            button_posterunki_wyswietl = Button(ramka_jednostki_lista, text='Pokaż dane posterunku', command=szczegoly_posterunki)
            button_posterunki_usun = Button(ramka_jednostki_lista, text='Usuń posterunek', command=usuwanie_posterunku)
            button_posterunki_zmien = Button(ramka_jednostki_lista, text='Edytuj posterunek', command=edytowanie_posterunku)

            listbox_posterunki.grid(row=1, column=0, columnspan=3, pady=(5, 0))
            button_posterunki_wyswietl.grid(row=2, column=0)
            button_posterunki_usun.grid(row=2, column=1)
            button_posterunki_zmien.grid(row=2, column=2)

            # ---------------------------------------
            # ramka posterunki formularz wyswietlania
            # ---------------------------------------
            label_posterunki_new = Label(ramka_jednostki_dod_ed, text='Dodaj lub edytuj:',
                                         font=('Arial', 12))
            label_posterunki_nazwa = Label(ramka_jednostki_dod_ed, text='Nazwa posterunku')
            label_posterunki_miejsce = Label(ramka_jednostki_dod_ed, text='Miejsce posterunku')

            entry_posterunki_nazwa = Entry(ramka_jednostki_dod_ed)
            entry_posterunki_miejsce = Entry(ramka_jednostki_dod_ed)

            label_posterunki_new.grid(row=0, column=0, columnspan=2)
            label_posterunki_nazwa.grid(row=1, column=0, sticky=W)
            label_posterunki_miejsce.grid(row=2, column=0, sticky=W)

            entry_posterunki_nazwa.grid(row=1, column=1, sticky=W)
            entry_posterunki_miejsce.grid(row=2, column=1, sticky=W)

            button_posterunki_dodaj = Button(ramka_jednostki_dod_ed, text='Dodaj posterunek', command=dodawanie_posterunku)
            button_posterunki_dodaj.grid(row=3, column=0, columnspan=2)

            # ---------------------------------------
            # ramka posterunki szczegoly
            # ---------------------------------------
            label_posterunki_info = Label(ramka_jednostki_info, text='Szczegóły jednostki policji:', font=('Arial', 10, 'bold'))
            label_nazwa_jednostki_info = Label(ramka_jednostki_info, text='Nazwa jednostki')
            label_nazwa_jednostki_info_wartosc = Label(ramka_jednostki_info, text='--pusto--', width=20)

            label_siedziba_jednostki_info = Label(ramka_jednostki_info, text='Siedziba jednostki')
            label_siedziba_jednostki_info_wartosc = Label(ramka_jednostki_info, text='--pusto--', width=20)

            label_siedziba_jedn_wsp_szczegoly = Label(ramka_jednostki_info, text='Współrzędne siedziby')
            label_siedziba_jedn_wsp_szczegoly_wartosc = Label(ramka_jednostki_info, text='--pusto--', width=20)

            label_posterunki_info.grid(row=0, column=0, columnspan=8, pady=10)

            label_nazwa_jednostki_info.grid(row=1, column=0)
            label_nazwa_jednostki_info_wartosc.grid(row=2, column=0)

            label_siedziba_jednostki_info.grid(row=1, column=1)
            label_siedziba_jednostki_info_wartosc.grid(row=2, column=1)

            label_siedziba_jedn_wsp_szczegoly.grid(row=1, column=2)
            label_siedziba_jedn_wsp_szczegoly_wartosc.grid(row=2, column=2)


            # RAMKA TABELA 2


            def pokaz_wszystkich_policjantow():
                listbox_policjanci.delete(0, END)
                sql_query_1 = f"SELECT * FROM public.policjanci ORDER BY id ASC;"
                cursor.execute(sql_query_1)
                query_result = cursor.fetchall()
                for index, obiekt in enumerate(query_result):
                    listbox_policjanci.insert(index, f'Policjant {obiekt[1]} {obiekt[2]}')

                auto_id_pracownicy_aktualizacja()

            def dodawanie_policjanta():
                imie = entry_policjanci_imie.get()
                nazwisko = entry_policjanci_nazwisko.get()
                miejsce=entry_policjanci_miejsce.get()
                placowka=entry_policjanci_placowka.get()

                sql_query_1 = f"INSERT INTO public.policjanci(id, imie, nazwisko, miejscowosc, placowka) VALUES ('{auto_id_pracownicy_dodawanie()}', '{imie}', '{nazwisko}', '{miejsce}', '{placowka}');"
                cursor.execute(sql_query_1)
                db_params.commit()

                entry_policjanci_imie.delete(0, END)
                entry_policjanci_nazwisko.delete(0, END)
                entry_policjanci_miejsce.delete(0, END)
                entry_policjanci_placowka.delete(0, END)

                pokaz_wszystkich_policjantow()

            def edytowanie_policjanta():
                sql_query_1 = f"SELECT * FROM public.policjanci ORDER BY id ASC;"
                cursor.execute(sql_query_1)
                query_result = cursor.fetchall()

                i = listbox_policjanci.index(ACTIVE)

                entry_policjanci_imie.delete(0, END)
                entry_policjanci_nazwisko.delete(0, END)
                entry_policjanci_miejsce.delete(0, END)
                entry_policjanci_placowka.delete(0, END)

                entry_policjanci_imie.insert(0, query_result[i][1])
                entry_policjanci_nazwisko.insert(0, query_result[i][2])
                entry_policjanci_miejsce.insert(0, query_result[i][3])
                entry_policjanci_placowka.insert(0, query_result[i][4])

                button_policjanci_dodaj.config(text='Zapisz', command=lambda: aktualizowanie_policjanta(i))

            def aktualizowanie_policjanta(i):
                sql_query_1 = f"SELECT * FROM public.policjanci ORDER BY id ASC;"
                cursor.execute(sql_query_1)
                query_result = cursor.fetchall()

                imie = entry_policjanci_imie.get()
                nazwisko = entry_policjanci_nazwisko.get()
                miejsce=entry_policjanci_miejsce.get()
                placowka=entry_policjanci_placowka.get()

                sql_query_2 = f"UPDATE public.policjanci SET imie='{imie}',nazwisko='{nazwisko}',miejscowosc='{miejsce}',placowka='{placowka}' WHERE imie='{query_result[i][1]}' and nazwisko='{query_result[i][2]}' and miejscowosc='{query_result[i][3]}' and placowka='{query_result[i][4]}';"
                cursor.execute(sql_query_2)
                db_params.commit()

                button_policjanci_dodaj.config(text='Dodaj policjanta', command=dodawanie_policjanta)

                entry_policjanci_imie.delete(0, END)
                entry_policjanci_nazwisko.delete(0, END)
                entry_policjanci_miejsce.delete(0, END)
                entry_policjanci_placowka.delete(0, END)

                pokaz_wszystkich_policjantow()

            def usuwanie_policjanta():
                i = listbox_policjanci.index(ACTIVE)

                sql_query_1 = f"DELETE FROM public.policjanci WHERE id='{i + 1}';"
                cursor.execute(sql_query_1)
                db_params.commit()

                pokaz_wszystkich_policjantow()

            def szczegoly_policjanta():
                sql_query_1 = f"SELECT * FROM public.policjanci ORDER BY id ASC;"
                cursor.execute(sql_query_1)
                query_result = cursor.fetchall()

                i = listbox_policjanci.index(ACTIVE)

                imie = query_result[i][1]
                nazwisko = query_result[i][2]
                miejscowosc = query_result[i][3]
                jednostka=query_result[i][4]

                label_imie_policjanci_info_wartosc.config(text=imie)
                label_nazwisko_policjanci_info_wartosc.config(text=nazwisko)
                label_miejscowosc_policjanci_szczegoly_wartosc.config(text=miejscowosc)
                label_placowka_policjanci_szczegoly_wartosc.config(text=jednostka)

            #GUI
            rama_policjanci = Frame(okno_jednostki)
            rama_policjanci.grid(row=0, column=1, pady=(5,0))

            ramka_policjanci_naglowek = Frame(rama_policjanci)
            ramka_policjanci_lista = Frame(rama_policjanci)
            ramka_policjanci_dod_ed = Frame(rama_policjanci)
            ramka_policjanci_info = Frame(rama_policjanci)

            ramka_policjanci_naglowek.grid(row=0, column=0, pady=(0,10))
            ramka_policjanci_lista.grid(row=1, column=0)
            ramka_policjanci_dod_ed.grid(row=2, column=0, pady=40)
            ramka_policjanci_info.grid(row=3, column=0)

            # ---------------------------------------
            # ramka odowlanie do posterunkow wyzej
            # ---------------------------------------
            label_policjanci_lista = Label(ramka_policjanci_naglowek, text='Lista policjantów',
                                          font=('Arial', 12, 'bold', 'underline'))
            button_pokaz_calosc_policjanci = Button(ramka_policjanci_naglowek, text='Pokaż wszystkich', command=pokaz_wszystkich_policjantow)

            label_policjanci_lista.grid(row=0, column=0, padx=(250 - label_jednostki_lista.winfo_reqwidth() / 2),
                                       pady=5)
            button_pokaz_calosc_policjanci.grid(row=1, column=0)

            # ---------------------------------------
            # ramka odwolanie do listy wyzej
            # ---------------------------------------
            listbox_policjanci = Listbox(ramka_policjanci_lista, width=50)
            button_policjanci_wyswietl = Button(ramka_policjanci_lista, text='Pokaż dane policjanta',
                                                command=szczegoly_policjanta)
            button_policjanci_usun = Button(ramka_policjanci_lista, text='Usuń policjanta', command=usuwanie_policjanta)
            button_policjanci_zmien = Button(ramka_policjanci_lista, text='Edytuj policjanta', command=edytowanie_policjanta)

            listbox_policjanci.grid(row=1, column=0, columnspan=3, pady=(10, 0))
            button_policjanci_wyswietl.grid(row=2, column=0)
            button_policjanci_usun.grid(row=2, column=1)
            button_policjanci_zmien.grid(row=2, column=2)

            # ---------------------------------------
            # ramka posterunki wyzejformularz
            # ---------------------------------------
            label_policjanci_new = Label(ramka_policjanci_dod_ed, text='Dodaj lub edytuj:',
                                         font=('Arial', 12))
            label_policjanci_imie = Label(ramka_policjanci_dod_ed, text='Imię')
            label_policjanci_nazwisko = Label(ramka_policjanci_dod_ed, text='Nazwisko')
            label_policjanci_miejsce = Label(ramka_policjanci_dod_ed, text='Miejscowość')
            label_policjanci_placowka = Label(ramka_policjanci_dod_ed, text='Nazwa jednostki policji')

            entry_policjanci_imie = Entry(ramka_policjanci_dod_ed)
            entry_policjanci_nazwisko = Entry(ramka_policjanci_dod_ed)
            entry_policjanci_miejsce = Entry(ramka_policjanci_dod_ed)
            entry_policjanci_placowka = Entry(ramka_policjanci_dod_ed)

            label_policjanci_new.grid(row=0, column=0, columnspan=2)
            label_policjanci_imie.grid(row=1, column=0, sticky=W)
            label_policjanci_nazwisko.grid(row=2, column=0, sticky=W)
            label_policjanci_miejsce.grid(row=3, column=0, sticky=W)
            label_policjanci_placowka.grid(row=4, column=0, sticky=W)

            entry_policjanci_imie.grid(row=1, column=1, sticky=W)
            entry_policjanci_nazwisko.grid(row=2, column=1, sticky=W)
            entry_policjanci_miejsce.grid(row=3, column=1, sticky=W)
            entry_policjanci_placowka.grid(row=4, column=1, sticky=W)

            button_policjanci_dodaj = Button(ramka_policjanci_dod_ed, text='Dodaj policjanta', command=dodawanie_policjanta)
            button_policjanci_dodaj.grid(row=5, column=0, columnspan=2)

            # ---------------------------------------
            # ramka posterunki wyzej szczegoly
            # ---------------------------------------
            label_policjanci_info = Label(ramka_policjanci_info, text='Szczegóły policjanta:', font=('Arial', 10, 'bold'))
            label_imie_policjanci_info = Label(ramka_policjanci_info, text='Imię policjanta')
            label_imie_policjanci_info_wartosc = Label(ramka_policjanci_info, text='--pusto--', width=20)

            label_nazwisko_policjanci_info = Label(ramka_policjanci_info, text='Nazwisko policjanta')
            label_nazwisko_policjanci_info_wartosc = Label(ramka_policjanci_info, text='--pusto--', width=20)

            label_miejscowosc_policjanci_szczegoly = Label(ramka_policjanci_info, text='Miejscowość policjanta')
            label_miejscowosc_policjanci_szczegoly_wartosc = Label(ramka_policjanci_info, text='--pusto--', width=20)

            label_placowka_policjanci_szczegoly = Label(ramka_policjanci_info, text='Posterunek policjanta')
            label_placowka_policjanci_szczegoly_wartosc = Label(ramka_policjanci_info, text='--pusto--', width=20)

            label_policjanci_info.grid(row=0, column=0, columnspan=8, pady=10)

            label_imie_policjanci_info.grid(row=1, column=0)
            label_imie_policjanci_info_wartosc.grid(row=2, column=0)

            label_nazwisko_policjanci_info.grid(row=1, column=1)
            label_nazwisko_policjanci_info_wartosc.grid(row=2, column=1)

            label_miejscowosc_policjanci_szczegoly.grid(row=1, column=2)
            label_miejscowosc_policjanci_szczegoly_wartosc.grid(row=2, column=2)

            label_placowka_policjanci_szczegoly.grid(row=1, column=3)
            label_placowka_policjanci_szczegoly_wartosc.grid(row=2, column=3)

            #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
            # RAMKA TABELA 3
            #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

            def pokaz_wszystkie_incydenty():
                listbox_incydenty.delete(0, END)
                sql_query_1 = f"SELECT * FROM public.incydenty ORDER BY id ASC;"
                cursor.execute(sql_query_1)
                query_result = cursor.fetchall()
                for index, obiekt in enumerate(query_result):
                    listbox_incydenty.insert(index, f'Incydent w miejscowości {obiekt[1]}')

                auto_id_incydenty_aktualizacja()

            def dodawanie_incydentu():
                miejsce=entry_incydenty_lokalizacja.get()
                typ=entry_incydenty_typ.get()
                jednostka=entry_incydenty_jednostka.get()

                sql_query_1 = f"INSERT INTO public.incydenty(id, lokalizacja, typ, jednostka_policji) VALUES ('{auto_id_incydenty_dodawanie()}', '{miejsce}', '{typ}', '{jednostka}');"
                cursor.execute(sql_query_1)
                db_params.commit()

                entry_incydenty_lokalizacja.delete(0, END)
                entry_incydenty_typ.delete(0, END)
                entry_incydenty_jednostka.delete(0, END)

                pokaz_wszystkie_incydenty()

            def edytowanie_incydentu():
                sql_query_1 = f"SELECT * FROM public.incydenty ORDER BY id ASC;"
                cursor.execute(sql_query_1)
                query_result = cursor.fetchall()

                i=listbox_incydenty.index(ACTIVE)

                entry_incydenty_lokalizacja.delete(0, END)
                entry_incydenty_typ.delete(0, END)
                entry_incydenty_jednostka.delete(0, END)

                entry_incydenty_lokalizacja.insert(0, query_result[i][1])
                entry_incydenty_typ.insert(0, query_result[i][2])
                entry_incydenty_jednostka.insert(0, query_result[i][3])

                button_incydenty_dodaj.config(text='Zapisz', command=lambda: aktualizowanie_incydentu(i))

            def aktualizowanie_incydentu(i):
                sql_query_1 = f"SELECT * FROM public.incydenty ORDER BY id ASC;"
                cursor.execute(sql_query_1)
                query_result = cursor.fetchall()

                miejsce=entry_incydenty_lokalizacja.get()
                typ=entry_incydenty_typ.get()
                jednostka=entry_incydenty_jednostka.get()

                sql_query_2 = f"UPDATE public.incydenty SET lokalizacja='{miejsce}',typ='{typ}', jednostka_policji='{jednostka}' WHERE lokalizacja='{query_result[i][1]}' and typ='{query_result[i][2]}' and jednostka_policji='{query_result[i][3]}';"
                cursor.execute(sql_query_2)
                db_params.commit()

                button_incydenty_dodaj.config(text='Dodaj incydent', command=dodawanie_incydentu)

                entry_incydenty_lokalizacja.delete(0, END)
                entry_incydenty_typ.delete(0, END)
                entry_incydenty_jednostka.delete(0, END)

                pokaz_wszystkie_incydenty()

            def usuwanie_incydentu():
                i = listbox_incydenty.index(ACTIVE)

                sql_query_1 = f"DELETE FROM public.incydenty WHERE id='{i+1}';"
                cursor.execute(sql_query_1)
                db_params.commit()

                pokaz_wszystkie_incydenty()

            def szczegoly_incydentu():
                sql_query_1 = f"SELECT * FROM public.incydenty ORDER BY id ASC;"
                cursor.execute(sql_query_1)
                query_result = cursor.fetchall()

                i = listbox_incydenty.index(ACTIVE)

                miejsce=query_result[i][1]
                typ=query_result[i][2]
                jednostka=query_result[i][3]

                label_lokalizacja_incydenty_info_wartosc.config(text=miejsce)
                label_typ_incydenty_info_wartosc.config(text=typ)
                label_jednostka_incydenty_szczegoly_wartosc.config(text=jednostka)

            # GUI
            rama_incydenty=Frame(okno_jednostki)
            rama_incydenty.grid(row=0, column=2)

            ramka_incydenty_naglowek = Frame(rama_incydenty)
            ramka_incydenty_lista = Frame(rama_incydenty)
            ramka_incydenty_dod_ed = Frame(rama_incydenty)
            ramka_incydenty_info = Frame(rama_incydenty)

            ramka_incydenty_naglowek.grid(row=0, column=0, pady=(0,10))
            ramka_incydenty_lista.grid(row=1, column=0)
            ramka_incydenty_dod_ed.grid(row=2, column=0, pady=40)
            ramka_incydenty_info.grid(row=3, column=0)

            # ---------------------------------------
            # ramka incydnety_
            # ---------------------------------------
            label_incydenty_lista = Label(ramka_incydenty_naglowek, text='Lista incydentów:', font=('Arial', 12, 'bold', 'underline'))
            button_pokaz_calosc_incydenty = Button(ramka_incydenty_naglowek, text='Pokaż wszystkie', command=pokaz_wszystkie_incydenty)

            label_incydenty_lista.grid(row=0, column=0, padx=(250 - label_jednostki_lista.winfo_reqwidth() / 2), pady=5)
            button_pokaz_calosc_incydenty.grid(row=1, column=0)

            # ---------------------------------------
            # ramka lista incydenty
            # ---------------------------------------
            listbox_incydenty = Listbox(ramka_incydenty_lista, width=50)
            button_incydenty_wyswietl = Button(ramka_incydenty_lista, text='Pokaż dane o incydencie', command=szczegoly_incydentu)
            button_incydenty_usun = Button(ramka_incydenty_lista, text='Usuń incydent', command=usuwanie_incydentu)
            button_incydenty_zmien = Button(ramka_incydenty_lista, text='Edytuj incydent', command=edytowanie_incydentu)

            listbox_incydenty.grid(row=1, column=0, columnspan=3, pady=(10, 0))
            button_incydenty_wyswietl.grid(row=2, column=0)
            button_incydenty_usun.grid(row=2, column=1)
            button_incydenty_zmien.grid(row=2, column=2)

            # ---------------------------------------
            # ramka formularz incydenty
            # ---------------------------------------
            label_incydenty_new = Label(ramka_incydenty_dod_ed, text='Dodaj i edytuj:',
                                         font=('Arial', 12))
            label_incydenty_lokalizacja = Label(ramka_incydenty_dod_ed, text='Miejsce incydentu')
            label_incydenty_typ = Label(ramka_incydenty_dod_ed, text='Typ incydentu')
            label_incydenty_jednostka = Label(ramka_incydenty_dod_ed, text='Jednostka odpowiedzialna')

            entry_incydenty_lokalizacja = Entry(ramka_incydenty_dod_ed)
            entry_incydenty_typ = Entry(ramka_incydenty_dod_ed)
            entry_incydenty_jednostka = Entry(ramka_incydenty_dod_ed)

            label_incydenty_new.grid(row=0, column=0, columnspan=2)
            label_incydenty_lokalizacja.grid(row=1, column=0, sticky=W)
            label_incydenty_typ.grid(row=2, column=0, sticky=W)
            label_incydenty_jednostka.grid(row=3, column=0, sticky=W)

            entry_incydenty_lokalizacja.grid(row=1, column=1, sticky=W)
            entry_incydenty_typ.grid(row=2, column=1, sticky=W)
            entry_incydenty_jednostka.grid(row=3, column=1, sticky=W)

            button_incydenty_dodaj = Button(ramka_incydenty_dod_ed, text='Dodaj incydent', command=dodawanie_incydentu)
            button_incydenty_dodaj.grid(row=4, column=0, columnspan=2)

            # ---------------------------------------
            # ramka incydenty_szczegoly
            # ---------------------------------------
            label_incydenty_info = Label(ramka_incydenty_info, text='Szczegóły incydentów:', font=('Arial', 10, 'bold'))
            label_lokalizacja_incydenty_info = Label(ramka_incydenty_info, text='Lokalizacja incydentu')
            label_lokalizacja_incydenty_info_wartosc = Label(ramka_incydenty_info, text='--pusto--', width=20)

            label_typ_incydenty_info = Label(ramka_incydenty_info, text='Typ incydentu')
            label_typ_incydenty_info_wartosc = Label(ramka_incydenty_info, text='--pusto--', width=20)

            label_jednostka_incydenty_szczegoly = Label(ramka_incydenty_info, text='Jednostka odpowiedzialna')
            label_jednostka_incydenty_szczegoly_wartosc = Label(ramka_incydenty_info, text='--pusto--', width=20)

            label_incydenty_info.grid(row=0, column=0, columnspan=8, pady=10)

            label_lokalizacja_incydenty_info.grid(row=1, column=0)
            label_lokalizacja_incydenty_info_wartosc.grid(row=2, column=0)

            label_typ_incydenty_info.grid(row=1, column=1)
            label_typ_incydenty_info_wartosc.grid(row=2, column=1)

            label_jednostka_incydenty_szczegoly.grid(row=1, column=2)
            label_jednostka_incydenty_szczegoly_wartosc.grid(row=2, column=2)

            rama_jednostki.mainloop()


        def mapa():

            def mapa_jednostki():
                sql_query_1 = f"SELECT * FROM public.jednostki_policji ORDER BY id ASC;"
                cursor.execute(sql_query_1)
                query_result = cursor.fetchall()

                mapa_jednostki = TkinterMapView(ramka_mapy, width=700, height=300, corner_radius=0)
                mapa_jednostki.set_position(52.2, 21.0)
                mapa_jednostki.set_zoom(6)
                mapa_jednostki.grid(row=8, column=0, columnspan=3, pady=(10,0))

                for row in query_result:
                    lokalizacja=get_coordinates(row[2])
                    mapa_jednostki.set_marker(lokalizacja[0], lokalizacja[1], text=f'{row[1]}', font=('Arial', 10, 'underline'), text_color='black')

            def mapa_policjanci():
                sql_query_1 = f"SELECT * FROM public.policjanci ORDER BY id ASC;"
                cursor.execute(sql_query_1)
                query_result = cursor.fetchall()

                mapa_policjantow = TkinterMapView(ramka_mapy, width=700, height=300, corner_radius=0)
                mapa_policjantow.set_position(52.2, 21.0)
                mapa_policjantow.set_zoom(6)
                mapa_policjantow.grid(row=8, column=0, columnspan=3, pady=(10,0))

                for row in query_result:
                    policjant_wsp=get_coordinates(row[3])
                    mapa_policjantow.set_marker(policjant_wsp[0], policjant_wsp[1], text=f'{row[1]} {row[2]}', font=('Arial', 10, 'underline'), text_color='black')

            def mapa_policjanci_jednostka():
                placowka=entry_mapki_prac_jedn.get()

                sql_query_1 = f"SELECT * FROM public.policjanci WHERE placowka='{placowka}' ORDER BY id ASC;"
                cursor.execute(sql_query_1)
                query_result = cursor.fetchall()

                mapa_pol_jedn = TkinterMapView(ramka_mapy, width=700, height=300, corner_radius=0)
                mapa_pol_jedn.set_position(52.2, 21.0)
                mapa_pol_jedn.set_zoom(6)
                mapa_pol_jedn.grid(row=8, column=0, columnspan=3, pady=(10,0))

                for row in query_result:
                    lokalizacja=get_coordinates(row[3])
                    mapa_pol_jedn.set_marker(lokalizacja[0], lokalizacja[1], text=f'{row[1]} {row[2]}', font=('Arial', 10, 'underline'), text_color='black')

            def mapa_incydenty_jednostka():
                jednostka=entry_mapki_int_jedn.get()

                sql_query_1 = f"SELECT * FROM public.incydenty WHERE jednostka_policji='{jednostka}' ORDER BY id ASC;"
                cursor.execute(sql_query_1)
                query_result = cursor.fetchall()

                mapa_inc_jedn = TkinterMapView(ramka_mapy, width=700, height=300, corner_radius=0)
                mapa_inc_jedn.set_position(52.2, 21.0)
                mapa_inc_jedn.set_zoom(6)
                mapa_inc_jedn.grid(row=8, column=0, columnspan=3, pady=(10,0))

                for row in query_result:
                    lokalizacja=get_coordinates(row[1])
                    mapa_inc_jedn.set_marker(lokalizacja[0], lokalizacja[1], text=f'{row[2]}', font=('Arial', 10, 'underline'), text_color='black')

            #00000000000000000000 GUI 0000000000000000000000
            root_wszystkie_mapy = Toplevel(root_wybierz)
            root_wszystkie_mapy.title('Mapy')
            root_wszystkie_mapy.state('zoomed')

            root_mapy=Frame(root_wszystkie_mapy)
            root_mapy.grid(row=0, column=0)

            ramka_mapy = Frame(root_mapy)
            ramka_mapy.grid(row=0, column=3, columnspan=2)

            # ---------------------------------------
            # ramka mapa
            # ---------------------------------------
            label_mapki_napis = Label(ramka_mapy, text='Mapy jednostek policji', font=('Arial', 12, 'bold', 'underline'))
            label_mapki_wybor = Label(ramka_mapy, text='Jaką mapę wyświetlić?')
            label_mapki_jednostka = Label(ramka_mapy, text='Mapa jednostek policji')
            button_mapki_jednostka = Button(ramka_mapy, text='Wyświetl', command=mapa_jednostki)
            label_mapki_pracownicy = Label(ramka_mapy, text='Mapa pracowników jednostek policji')
            button_mapki_pracownicy = Button(ramka_mapy, text='Wyświetl', command=mapa_policjanci)
            label_mapki_pracownicy_jednostki = Label(ramka_mapy, text='Mapa pracowników wybranej jednostki')
            label_mapki_prac_jedn = Label(ramka_mapy, text='Wpisz')
            entry_mapki_prac_jedn = Entry(ramka_mapy)
            button_mapki_prac_jedn = Button(ramka_mapy, text='Wyświetl', command=mapa_policjanci_jednostka)
            label_mapki_interwencje_jednostki = Label(ramka_mapy, text='Mapa incydentów wybranej jednostki')
            label_mapki_int_jedn = Label(ramka_mapy, text='Wpisz')
            entry_mapki_int_jedn = Entry(ramka_mapy)
            button_mapki_interwencje_jednostki = Button(ramka_mapy, text='Wyświetl', command=mapa_incydenty_jednostka)

            label_mapki_napis.grid(row=0, column=0, columnspan=3, pady=(10, 0))
            label_mapki_wybor.grid(row=1, column=0, columnspan=3)
            label_mapki_jednostka.grid(row=2, column=0, sticky=W)
            button_mapki_jednostka.grid(row=2, column=1, sticky=E)
            label_mapki_pracownicy.grid(row=3, column=0, sticky=W)
            button_mapki_pracownicy.grid(row=3, column=1, sticky=E)
            label_mapki_pracownicy_jednostki.grid(row=4, column=0, sticky=W)
            label_mapki_prac_jedn.grid(row=5, column=0, sticky=W)
            entry_mapki_prac_jedn.grid(row=5, column=0, padx=50, sticky=E)
            button_mapki_prac_jedn.grid(row=4, column=1, rowspan=2, sticky=E)
            label_mapki_interwencje_jednostki.grid(row=6, column=0, sticky=W)
            label_mapki_int_jedn.grid(row=7, column=0, sticky=W)
            entry_mapki_int_jedn.grid(row=7, column=0, padx=50, sticky=E)
            button_mapki_interwencje_jednostki.grid(row=6, column=1, rowspan=2, sticky=E)

            root_mapy.mainloop()


        root_wybierz=Toplevel(root_wejscie)
        root_wybierz.title('Elementy systemu')
        root_wybierz.geometry('150x80')

        ramka_elementy=Frame(root_wybierz)
        ramka_elementy.grid(row=0, column=0)

        label_elementy_opis=Label(ramka_elementy, text='Co otworzyć?')
        label_elementy_listy=Label(ramka_elementy, text='Listy')
        label_elementy_mapy=Label(ramka_elementy, text='Mapy')
        button_elementy_listy=Button(ramka_elementy, text='Wejdź', command=policja)
        button_elementy_mapy=Button(ramka_elementy, text='Wejdź', command=mapa)

        label_elementy_opis.grid(row=0, column=0, columnspan=2)
        label_elementy_listy.grid(row=1, column=0, sticky=W)
        label_elementy_mapy.grid(row=2, column=0, sticky=W)
        button_elementy_listy.grid(row=1, column=1, sticky=E)
        button_elementy_mapy.grid(row=2, column=1, sticky=E)

        root_wybierz.mainloop()

    else:
        wrong_label=Label(ramka_wejscie, text='Wpisz hasło jeszcze raz')
        wrong_label.grid(row=3, column=0, columnspan=2, padx=3)
        wejscie_entry.delete(0, END)
        wejscie_entry.focus()

root_wejscie=Tk()
root_wejscie.title('Policja - logowanie')
root_wejscie.geometry('200x100')

ramka_wejscie=Frame(root_wejscie)
ramka_wejscie.grid(row=0, column=0)

wejscie_napis=Label(ramka_wejscie, text='Wpisz hasło')
wejscie_entry=Entry(ramka_wejscie, width=22, show='•')
wejscie_entry.bind('<Return>', dostep)
wejscie_button=Button(ramka_wejscie, text='Wejdź', command=dostep)

wejscie_napis.grid(row=0, column=0, padx=30)
wejscie_entry.grid(row=1, column=0, padx=30)
wejscie_button.grid(row=2, column=0)

root_wejscie.mainloop()
# powoduje, że tabela nie wyswietla sie na sekundę