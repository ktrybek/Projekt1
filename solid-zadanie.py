import os

class Manager:
    def __init__(self):
        self.saldo = 0.0
        self.historia = []
        self.magazyn = {}
        self.saldo_file = ""
        self.magazyn_file = ""
        self.historia_file = ""

    def file_exists(self, filepath):
        return os.path.isfile(filepath)

    def load_data(self):
        self.saldo = self.load_saldo_from_file(self.saldo_file)
        self.magazyn = self.load_magazyn_from_file(self.magazyn_file)
        self.historia = self.load_historia_from_file(self.historia_file)

    def assign(self, saldo_file, magazyn_file, historia_file):
        self.saldo_file = saldo_file
        self.magazyn_file = magazyn_file
        self.historia_file = historia_file
        self.load_data()

    def save_saldo_to_file(self):
        with open(self.saldo_file, "w") as fd:
            fd.write(str(self.saldo))

    def save_magazyn_to_file(self):
        with open(self.magazyn_file, "w") as fd:
            for nazwa_produktu, produkt in self.magazyn.items():
                fd.write(f"{nazwa_produktu},{produkt['ilosc']},{produkt['cena']}\n")

    def save_historia_to_file(self):
        with open(self.historia_file, "a") as fd:
            for operacja in self.historia:
                fd.write(operacja + "\n")

    def load_saldo_from_file(self, filepath):
        if not self.file_exists(filepath):
            return 0.0
        with open(filepath, "r") as fd:
            content = fd.read().strip()
        return float(content) if content and content.replace('.', '', 1).isdigit() else 0.0

    def load_magazyn_from_file(self, filepath):
        magazyn = {}
        if not self.file_exists(filepath):
            return magazyn
        with open(filepath, "r") as fd:
            for line in fd:
                parts = line.strip().split(",")
                if len(parts) != 3:
                    continue
                nazwa, ilosc, cena = parts
                magazyn[nazwa] = {"ilosc": int(ilosc), "cena": float(cena)}
        return magazyn

    def load_historia_from_file(self, filepath):
        if not self.file_exists(filepath):
            return []
        with open(filepath, "r") as fd:
            return [line.strip() for line in fd.readlines()]

    def execute(self, komenda):
        komenda = komenda.strip().lower()
        if komenda == "koniec":
            print("Zakończenie programu")
            self.save_magazyn_to_file()
            self.save_historia_to_file()
            return False

        elif komenda == "saldo":
            saldo = float(input("Podaj kwotę do dodania lub odjęcia z konta: "))
            self.saldo += saldo
            self.historia.append(f"Saldo zmienione. Nowe saldo: {self.saldo}")
            self.save_saldo_to_file()

        elif komenda == "konto":
            print("Stan konta wynosi: ", self.saldo)
            self.historia.append(f"Stan konta: {self.saldo}")

        elif komenda == "zakup":
            nazwa_produktu = input("Podaj nazwę produktu: ")
            ilosc = int(input("Podaj liczbę produktów: "))
            cena = float(input("Cena produktu: "))
            koszt = cena * ilosc

            if koszt > self.saldo:
                print("Nie masz wystarczających środków")
                return True

            self.saldo -= koszt
            if nazwa_produktu in self.magazyn:
                self.magazyn[nazwa_produktu]["ilosc"] += ilosc
            else:
                self.magazyn[nazwa_produktu] = {"ilosc": ilosc, "cena": cena}

            self.historia.append(f"Zakup: {nazwa_produktu}, Ilość: {ilosc}, Cena: {cena}, Stan konta: {self.saldo}")

        elif komenda == "sprzedaż":
            nazwa_produktu = input("Podaj nazwę produktu: ")
            ilosc = int(input("Podaj liczbę produktów: "))
            cena = float(input("Cena produktu: "))

            if nazwa_produktu in self.magazyn and self.magazyn[nazwa_produktu]["ilosc"] >= ilosc:
                self.magazyn[nazwa_produktu]["ilosc"] -= ilosc
                self.saldo += cena * ilosc
                if self.magazyn[nazwa_produktu]["ilosc"] == 0:
                    del self.magazyn[nazwa_produktu]
                self.historia.append(f"Sprzedaż: {nazwa_produktu}, Ilość: {ilosc}, Cena: {cena}, Stan konta: {self.saldo}")
            else:
                print("Brak wystarczającej ilości w magazynie lub brak produktu.")

        elif komenda == "magazyn":
            nazwa_produktu = input("Podaj nazwę produktu: ")
            if nazwa_produktu in self.magazyn:
                produkt = self.magazyn[nazwa_produktu]
                print(f"Produkt: {nazwa_produktu}; Ilość: {produkt['ilosc']}; Cena: {produkt['cena']}")
            else:
                print("Brak produktu w magazynie")
            self.historia.append(f"Zapytanie o produkt: {nazwa_produktu}")

        elif komenda == "lista":
            if not self.magazyn:
                print("Zero produktów w magazynie")
            else:
                print("Stan magazynu:")
                for nazwa_produktu, produkt in self.magazyn.items():
                    print(f"Produkt: {nazwa_produktu}, Ilość: {produkt['ilosc']}, Cena: {produkt['cena']}")
            self.historia.append("Wyświetlono stan magazynu")

        elif komenda == "przegląd":
            od = input("Podaj index 'od': ").strip()
            do = input("Podaj index 'do': ").strip()

            od = int(od) if od else 0
            do = int(do) if do else len(self.historia)

            if od < 0 or do > len(self.historia) or od > do:
                print(f"Nieprawidłowy zakres. Liczba zapisanych komend: {len(self.historia)}")
                return True

            for i in range(od, do):
                print(f"{i}: {self.historia[i]}")

        else:
            print("Nieprawidłowa komenda. Spróbuj ponownie.")

        return True

def main():
    manager = Manager()
    manager.assign("Saldo.txt", "Magazyn.txt", "Historia.txt")

    while True:
        print("\nWybierz komendę: Saldo; Sprzedaż; Zakup; Konto; Lista; Magazyn; Przegląd; Koniec")
        komenda = input("Wpisz komendę: ")
        if not manager.execute(komenda):
            break
main()