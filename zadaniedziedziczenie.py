import json, sys, csv, pickle

class Base:
    def __init__(self, filename ='in.json'):
        self.filename = filename
        self.data = {}

    def read(self):
        pass

    def write(self, out_file):
        pass

    def apply_changes(self, changes):
        for change in changes:
            x, y, value = change.split(',')
            x, y = int(x), int(y)
            self.data[y][x] = value

class JSONFormat(Base):
    def read(self):
        with open(self.filename, 'r', encoding="utf-8") as f:
            self.data = json.load(f)

    def write(self, out_file):
        with open(out_file, 'w', encoding="utf-8") as f:
            json.dump(self.data, f)

class CSVFormat(Base):
    def read(self):
        with open(self.filename, 'r', encoding="utf-8") as f:
            reader = csv.reader(f)
            self.data = [row for row in reader]

    def write(self, out_file):
        with open(out_file, 'w', encoding="utf-8", newline='') as f:
            writer = csv.writer(f)
            writer.writerows(self.data)

class TxtFormat(Base):
    def read(self):
        with open(self.filename, 'r', encoding="utf-8") as f:
            self.data = [line.strip().split(',') for line in f.readlines()]

    def write(self, out_file):
        with open(out_file, 'w', encoding="utf-8") as f:
            for row in self.data:
                f.write(','.join(row) + '\n')

class PickleFormat(Base):
    def read(self):
        with open(self.filename, 'rb') as f:
            self.data = pickle.load(f, fix_imports=True, encoding='ASCII', errors='strict')


    def write(self, out_file):
        with open(out_file, 'wb') as f:
            pickle.dump(self.data, f, protocol=pickle.HIGHEST_PROTOCOL)

def get_format(filename):
    if filename.endswith('.json'):
        return JSONFormat(filename)
    elif filename.endswith('.csv'):
        return CSVFormat(filename)
    elif filename.endswith('.txt'):
        return TxtFormat(filename)
    elif filename.endswith('.pickle'):
        return PickleFormat(filename)
    else:
        raise ValueError("Nieobsługiwany typ pliku!")

def main():

    print(sys.argv)

    in_file = sys.argv[1]
    out_file = sys.argv[2]
    changes = sys.argv[3:]

    format = get_format(in_file)
    format.read()

    format.apply_changes(changes)

    out_format = get_format(out_file)
    out_format.data = format.data
    out_format.write(out_file)

main()

