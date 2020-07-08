from classes.File import File
import csv
from collections import defaultdict


class TSV(File):
    def __init__(self, file):
        super().__init__(file)

        # проверка типа
        if file.split(".")[-1] != "tsv":
            raise Exception("Неподходящий тип")

    def read_data(self):
        # открываем файл, записываем его список (получается список списков) и транпонируем (список tuple'ов)
        with open(self.file) as f:
            file_data = list(csv.reader(f, delimiter='\t'))
            matrix = list(zip(*file_data))

        # проходим по всем ИЗНАЧАЛЬНО столбцам
        for row in matrix:
            # выделяем индекс
            index = row[0][1:]
            # если начинается с D, то записываемв D[*], если с M в M[*], иначе ошибка
            if row[0][0] == "D":
                self.D[index] = list(row[1:])
            elif row[0][0] == "M" or row[0][0] == "MS":
                self.M[index] = list(row[1:])
            else:
                raise Exception("Допускаются только D, М и MS")

        for index, values in self.M.items():
            for i, value in enumerate(values):
                if not str(value).isnumeric():
                    print("Значение в столбце M должно быть числом. Файл {}, строка {}, индекс {}. "
                          "Заменено на 0.".format(self.file, i + 1, index))
                    self.M[index][i] = 0

    @staticmethod
    def _write_to_file(file, data, min_D, min_M, name_M):
        with open(file, 'w') as out_file:
            tsv_writer = csv.writer(out_file, delimiter='\t', lineterminator='\n')
            # шапка
            header = list()
            for index in range(1, min_D + 1):
                header.append("D{}".format(index))
            for index in range(1, min_M + 1):
                header.append("{}{}".format(name_M, index))
            tsv_writer.writerow(header)
            # данные
            tsv_writer.writerows(data)

    @staticmethod
    def basic(out, *files):
        out_data, min_D, min_M = File._make_matrix(files)
        # сортируем
        out_data.sort(key=lambda i: i[0])
        # записываем файл
        TSV._write_to_file(out, out_data, min_D, min_M, name_M="M")

    @staticmethod
    def advanced(out, *files):
        append_data, min_D, min_M = File._make_matrix(files)

        # проходим слегка модифицированным пузырьком все значения
        out_data = list()
        for j, row1 in enumerate(append_data):
            MS = defaultdict()
            for row2 in append_data[j:]:
                # если нашли такое же значение
                if row1[:min_D] == row2[:min_D]:
                    # обновляем сумму в словаре
                    for i, M_row in enumerate(row2[min_D:]):
                        if i not in MS.keys():
                            MS[i] = 0
                        MS[i] += int(M_row)
            # доавляем части строк в матрицу
            out_data.append(row1[:min_D] + (*MS.values(),))

        # удалим повторения
        out_data = list(set(out_data))
        # сортируем
        out_data.sort()
        # записываем файл
        TSV._write_to_file(out, out_data, min_D, min_M, name_M="MS")

    def __eq__(self, other):
        return self.D == other.D and self.M == other.M