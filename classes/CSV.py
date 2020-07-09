from classes.File import File
import csv


class CSV(File):
    def __init__(self, file):
        super().__init__(file)

        # проверка типа
        if file.split(".")[-1] != "csv":
            raise Exception("Неподходящий тип")

    def read_data(self):
        # открываем файл, записываем его список (получается список списков) и транпонируем (список tuple'ов)
        with open(self.file) as f:
            file_data = list(csv.reader(f))
            matrix = list(zip(*file_data))

        # проходим по всем ИЗНАЧАЛЬНО столбцам
        for row in matrix:
            # выделяем индекс
            index = row[0][1:]
            # если начинается с D, то записываемв D[*], если с M в M[*], иначе ошибка
            if row[0][0] == "D":
                self.D[index] = list(row[1:])
            elif row[0][0] == "M":
                self.M[index] = list(row[1:])
            else:
                raise Exception("Допускаются только D и М")

        self.validation()

    @staticmethod
    def _write_to_file(file, data, min_D, min_M, name_M):
        with open(file, 'w') as out_file:
            tsv_writer = csv.writer(out_file, delimiter=',', lineterminator='\n')
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
        matrix, min_D, min_M = CSV._make_matrix(files)
        matrix = list(zip(*matrix))
        # сортируем
        matrix.sort(key=lambda i: i[0])
        # записываем файл
        CSV._write_to_file(out, matrix, min_D, min_M, name_M="M")

    @staticmethod
    def advanced(out, *files):
        matrix, min_D, min_M = CSV._make_matrix(files)
        matrix = list(zip(*matrix))
        out_data = File._advanced_matrix(matrix, min_D)
        # записываем файл
        CSV._write_to_file(out, out_data, min_D, min_M, name_M="MS")