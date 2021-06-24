from classes.File import File
import csv


class TSV(File):
    def __init__(self, file):
        super().__init__(file)

        # проверка типа
        if file.split(".")[-1] != "tsv":
            raise Exception("Неподходящий тип")

    def read_data(self):
        # открываем файл, записываем его список (получается список списков) и транспонируем (список tuple'ов)
        with open(self.file) as f:
            file_data = list(csv.reader(f, delimiter='\t'))
            matrix = list(zip(*file_data))

        # проходим по всем ИЗНАЧАЛЬНО столбцам
        for row in matrix:
            # выделяем индекс
            index = row[0][1:]
            # если начинается с D, то записываем D[*], если с M в M[*], иначе ошибка
            if row[0][0] == "D":
                self.D[index] = list(row[1:])
            elif row[0][0] == "M":
                self.M[index] = list(row[1:])
            else:
                raise Exception("Допускаются только D, М и MS")

        self.validation()

    @staticmethod
    def _write_to_file(file, data, min_d, min_m, name_m):
        with open(file, 'w') as out_file:
            tsv_writer = csv.writer(out_file, delimiter='\t', lineterminator='\n')
            # шапка
            header = list()
            for index in range(1, min_d + 1):
                header.append("D{}".format(index))
            for index in range(1, min_m + 1):
                header.append("{}{}".format(name_m, index))
            tsv_writer.writerow(header)
            # данные
            tsv_writer.writerows(data)

    @staticmethod
    def basic(out, *files):
        matrix, min_d, min_m = TSV._make_matrix(files)
        matrix = list(zip(*matrix))
        # сортируем
        matrix.sort(key=lambda i: i[0])
        # записываем файл
        TSV._write_to_file(out, matrix, min_d, min_m, name_m="M")

    @staticmethod
    def advanced(out, *files):
        matrix, min_d, min_m = TSV._make_matrix(files)
        matrix = list(zip(*matrix))
        out_data = File._advanced_matrix(matrix, min_d)
        # записываем файл
        TSV._write_to_file(out, out_data, min_d, min_m, name_m="MS")

