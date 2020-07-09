from classes.File import File
import json


class JSON(File):
    def __init__(self, file):
        super().__init__(file)

        # проверка типа
        if file.split(".")[-1] != "json":
            raise Exception("Неподходящий тип")

    def read_data(self):
        # открываем файл и сразу передохим в fields
        with open(self.file) as f:
            fields = json.load(f)['fields']

        # проодим по элментам массива
        for field in fields:
            for word, data in field.items():
                index = word[1:]

                if word[0] == "D":
                    # если такой индекс ещё не встречался, то создаём его со значением пустого массива
                    if index not in self.D.keys():
                        self.D[index] = list()
                    # заносим данные
                    self.D[index].append(data)
                elif word[0] == "M":
                    if index not in self.M.keys():
                        self.M[index] = list()
                    self.M[index].append(data)
                else:
                    raise Exception("Допускаются только D и М")

        self.validation()

    @staticmethod
    def basic(out, *files):
        matrix, min_D, min_M = JSON._make_matrix(files)
        matrix = list(zip(*matrix))
        matrix.sort(key=lambda i: i[0])

        out_data = list()
        for values in matrix:
            temp_dict = dict()
            for i, value in enumerate(values):
                if i < min_D:
                    temp_dict["D{}".format(i+1)] = value
                else:
                    temp_dict["M{}".format(i+1-min_D)] = value
            out_data.append(temp_dict)

        # записываем файл
        with open(out, 'w') as outfile:
            json.dump({"fields": out_data}, outfile)

    @staticmethod
    def advanced(out, *files):
        matrix, min_D, min_M = File._make_matrix(files)
        matrix = list(zip(*matrix))
        data = File._advanced_matrix(matrix, min_D)
        out_data = list()

        for values in data:
            temp_dict = dict()
            for i, value in enumerate(values):
                if i < min_D:
                    temp_dict["D{}".format(i + 1)] = value
                else:
                    temp_dict["MS{}".format(i + 1 - min_D)] = value
            out_data.append(temp_dict)

        with open(out, 'w') as outfile:
            json.dump({"fields": out_data}, outfile)

