import csv
import sys


def read_csv(filename):
    with open(filename, "r") as f:
        reader = csv.reader(f)
        return [row for row in reader]


def changes_in_file(in_file, out_file, changes):
    in_file_list = read_csv(in_file)
    out_file_list = []
    for idx, row in enumerate(in_file_list):
        for change in changes:
            x, y, value = change.split(",")
            y = int(y)
            x = int(x)
            if idx == y:
                row[x] = value
        out_file_list.append(row)
    write_csv(out_file, out_file_list)


def write_csv(filename, elements):
    with open(filename, "w", newline="") as f:
        writer = csv.writer(f)
        for element in elements:
            writer.writerow(element)


def main():
    print(sys.argv)

    in_file = sys.argv[1]
    out_file = sys.argv[2]
    changes = sys.argv[3:]

    changes_in_file(in_file, out_file, changes)
    print(f"Zmiany zapisano w pliku {out_file}")


main()