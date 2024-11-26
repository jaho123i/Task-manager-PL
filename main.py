from datetime import datetime
import os

# błąd wyrzucany przy podaniu złych danych
class InvalidValueError(Exception):
    "W przypadku gdy podano złe dane"
    pass


# główna klasa, odpowiada za wszystkie funkcjonalności
class TaskManager:
    # konstruktor - tworzy listę i FileHandler danego obiektu
    # zwraca TaskManager
    def __init__(self):
        self.list = []
        self.file_handler = FileHandler()

    # dodaje nowe zadania do listy sprawdzając poprawność daty
    # nic nie zwraca, może wyrzucać InvalidValueError
    def dodaj(self):
        priorytet, termin, kategoria, opis = input(
            'Podaj priorytet, termin (dd/mm/rr H:M), kategoria, opis (oddziel średnikiem i spacją):\n').split("; ")
        try:
            self.list.append(Task(priorytet, datetime.strptime(termin, '%d/%m/%y %H:%M'), kategoria, opis))
        except Exception:
            raise InvalidValueError('Zła data!')

    # dodaje podane zadanie do listy
    # przyjmuje zadanie, nic nie zwraca
    def dodaj_gotowe(self, zadanie):
        self.list.append(zadanie)

    # usuwa element z listy pytając o index i sprawdzając jego poprawność
    # nic nie zwraca, może wyrzucać InvalidValueError
    def usun(self):
        index = int(input('Podaj numer zadania do usunięcia '))
        if len(self.list) > index >= 0:
            self.list.pop(index)  # ???
        else:
            raise InvalidValueError('Zły index!')

    # pozwala edytować opis, priorytet, termin i kategorię (wyświetla obecną cechę i prosi o nową wersję)
    # nic nie zwraca, może wyrzucać InvalidValueError
    def edytuj(self):
        index = int(input('Podaj numer zadania do edycji '))
        if len(self.list) > index >= 0:
            atrybut = input("Który element zmienić? 0 -> opis; 1 -> priorytet; 2 -> termin; 3 -> kategoria ")
            if atrybut == '0':
                self.list[index].opis = input(f'Stara wersja: {self.list[index].opis} \nPodaj nową: ')
            elif atrybut == '1':
                self.list[index].priorytet = input(f'Stara wersja: {self.list[index].priorytet} \nPodaj nową: ')
            elif atrybut == '2':
                self.list[index].termin = datetime.strptime(
                    input(f'Stara wersja: {self.list[index].termin} \nPodaj nową: '), '%d/%m/%y %H:%M')
            elif atrybut == '3':
                self.list[index].kategoria = input(f'Stara wersja: {self.list[index].kategoria} \nPodaj nową: ')
        else:
            raise InvalidValueError('Zły index!')

    # pozwala edytować stan wykonania i automatycznie zapisuje czas wykonania na podstawie różnicy terminu i obecnego czasu
    # nic nie zwraca, może wyrzucać InvalidValueError
    def zakoncz(self):
        index = int(input('Podaj numer zadania do zakończenia '))
        if len(self.list) > index >= 0:
            if not self.list[index].wykonane:
                self.list[index].wykonane = True  # ???
                self.list[index].czas_wykonania = self.list[index].termin - datetime.now()
            else:
                raise InvalidValueError('Zadanie już zakończono')
        else:
            raise InvalidValueError('Zły index!')

    # wyświetla na konsoli pełną listę zadań z numeracją od 0
    # nic nie zwraca
    def wyswietl(self):
        print('\n')
        for i in range(len(self.list)):
            print(f'{str(i)} -> {str(self.list[i])}')  # ???
        print('\n')

    # wyświetla na konsoli listę zrobionych zadań z numeracją od 0
    # nic nie zwraca
    def wyswietl_zrobione(self):
        print('\n')
        for i in range(len(self.list)):
            if self.list[i].wykonane:
                print(f'{str(i)} -> {str(self.list[i])}')  # ???
        print('\n')

    # wyświetla na konsoli listę NIEzrobionych zadań z numeracją od 0
    # nic nie zwraca
    def wyswietl_niezrobione(self):
        print('\n')
        for i in range(len(self.list)):
            if not self.list[i].wykonane:
                print(f'{str(i)} -> {str(self.list[i])}')  # ???
        print('\n')

    # wyświetla na konsoli filtrowaną pod kątem statusu, priorytetu lub terminu listę zadań z numeracją od 0
    # nic nie zwraca, może wyrzucać InvalidValueError
    def filtruj(self):
        cecha = input('Jaka cecha Cię interesuje? 0 -> status; 1 -> priorytet; 2 -> termin')
        if cecha == '0':
            zrobione = input('zrobione czy niezrobione?\n').lower()
            if zrobione == 'zrobione':
                self.wyswietl_zrobione()
            if zrobione == 'niezrobione':
                self.wyswietl_niezrobione()
        elif cecha == '1':
            prio = input('Jaki priorytet:\n').lower()
            print('\n')
            for i in range(len(self.list)):
                if str(self.list[i].priorytet).lower().__contains__(prio):
                    print(f'{str(i)} -> {str(self.list[i])}')  # ???
            print('\n')
        elif cecha == '2':
            try:
                ter = datetime.strptime(input('Jaki miesiąc (mm/rr):\n'),'%m/%y')
                print(ter)
            except Exception:
                raise InvalidValueError('Zła data!')
                return
            print('\n')
            for i in range(len(self.list)):
                if ter.month == self.list[i].termin.month and ter.year == self.list[i].termin.year:
                    print(f'{str(i)} -> {str(self.list[i])}')  # ???
            print('\n')
        else:
            raise InvalidValueError('Zły index!')

    # wyświetla na konsoli statystyki dotyczące procenta wykonanych zadań i średniego czasu wykonania
    # nic nie zwraca
    def statystyki(self):
        wykonanynych = 0
        sredni_czas_ukonczenia = 0
        for zadanie in self.list:
            if zadanie.wykonane:
                wykonanynych += 1
                sredni_czas_ukonczenia += zadanie.czas_wykonania.days
        if wykonanynych > 0:
            sredni_czas_ukonczenia /= wykonanynych
            wykonanynych /= len(self.list)
        print(f'Wykonano już {wykonanynych*100}% zadań, \n'
              f'Średni czas ukończenia (minus oznacza przed terminem): {sredni_czas_ukonczenia} dni')


# klasa pomocnicza, przechowuje wsystkie dane zadania
class Task:
    # konstruktor - tworzy nowe zadanie nadając mu piorytet, termin, kategorię i opis,
    # ustawia stan wykonania na False i czas wykonania na None
    # zwraca Task
    def __init__(self, priorytet, termin, kategoria, opis):
        self.priorytet = priorytet
        self.termin = termin
        self.kategoria = kategoria
        self.opis = opis
        self.wykonane = False
        self.czas_wykonania = None

    # w stringu wypisuje cechy zadania (poza czasem wykonania)
    # zwraca string
    def __str__(self):
        return str(self.opis) + '; Priorytet: ' + str(self.priorytet) + '; Termin: ' + str(
            self.termin) + '; Kategoria: ' + str(self.kategoria) + '; Wykonane: ' + str(self.wykonane)


# klasa pomocnicza, obsługuje działania z plikiem (zapis i odczyt)
class FileHandler:
    # zapisuje do pliku listę zadań
    # przyjmuje listę zadań i nazwę pliku docelowego, nic nie zwraca
    def zapis(self, task_m, nazwa):
        lista = task_m.list
        try:
            open(nazwa, "x")
        except Exception:
            print("Plik istnieje")
            return
        with (open(nazwa, "w") as file1):
            substr = ''
            for zadanie in lista:
                substr += str(zadanie.opis) + '; ' + str(zadanie.priorytet) + '; ' + str(zadanie.termin.day) + '.' + str(zadanie.termin.month) + '.' + str(zadanie.termin.year)[2] + str(zadanie.termin.year)[3] + '; '
                substr += str(zadanie.kategoria) + '; ' + str(zadanie.wykonane) + '; '  # ???
                if zadanie.czas_wykonania is not None:
                    substr += zadanie.czas_wykonania.days
                substr += '\n'
            file1.write(substr)
        print("Zapisano")

    # wczytuje listę zadań z pliku
    # przyjmuje nazwę pliku, zwraca listę zadań
    def odczyt(self, task_m, nazwa):
        try:
            open(nazwa, "r")
        except Exception:
            print("Plik nie istnieje")
            return
        with open(nazwa, "r") as file1:
            for line in file1.readlines():
                opis, priorytet, termin, kategoria, wykonane, czas_wykonania = line.split('; ')
                task = Task(priorytet, datetime.strptime(termin, '%d.%m.%y'), kategoria, opis)
                if wykonane == 'True':
                    task.wykonane = True
                else:
                    task.wykonane = False
                task_m.dodaj_gotowe(task)
                print('Wczytano zadanie')

# utworzenie listy
task_manager = TaskManager()

# główna pętla programu
while True:
    try:
        order = input('Co dalej? (help -aby wyświetlić opcje)\n')
        if order == 'end':
            break
        elif order == 'help':
            print('dodaj\nusun\nedytuj\nzakoncz\nfiltruj\nstaty\nzapisz\nczytaj')
        elif order == 'dodaj':
            task_manager.dodaj()
        elif order == 'usun':
            task_manager.usun()
        elif order == 'edytuj':
            task_manager.edytuj()
        elif order == 'zakoncz':
            task_manager.zakoncz()
        elif order == 'filtruj':
            task_manager.filtruj()
        elif order == 'staty':
            task_manager.statystyki()
        elif order == 'zapisz':
            nazwa = input('Podaj nazwę pliku')
            task_manager.file_handler.zapis(task_manager, nazwa)
        elif order == 'czytaj':
            nazwa = input('Podaj nazwę pliku')
            task_manager.file_handler.odczyt(task_manager, nazwa)
        else:
            print('Nie rozumiem')
    except Exception as exc:
        print(str(exc))

    task_manager.wyswietl()

# przyładowe zadanie do dodania:
# pilne; 21/3/07 23:59; praca; dokończyć projekt, który zlecił szef
