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

