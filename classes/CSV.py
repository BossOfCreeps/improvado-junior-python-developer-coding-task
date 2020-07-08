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

