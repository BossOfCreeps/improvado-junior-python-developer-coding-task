from abc import ABC, abstractmethod


class File(ABC):
    """
    переменные для хранения D[], M[] и имени файла
    Структура D (любые значения) и M (точко числа):
    {
        "1" : ["a", "b", "c" ... "b"],
        "2" : ["1", "0", "1" ... "5"],
        ...
        "n" : ["a", "c", "b" ... "b"],
    }
    """
    D = dict()
    M = dict()
    file = str

    @abstractmethod
    def __init__(self, file):
        """
        Функция инициализации
        :param file: адрес до файла
        """

        # проверка на то, что переданный тип адреса файла - строка
        if type(file) != str:
            raise Exception("В качестве адреса файла должна быть строка")

        # Тут у меня возникла проблема, связанная с тем, что в двух классах потомках dict был одниим.
        # Видимо из-за того что dict - адресная перменненная. Поэтому я пересоздаю её, чтобы адрес поменялся.
        self.D = dict()
        self.M = dict()
        # заносим адрес до папки
        self.file = file

    def __str__(self):
        """
        Даёт возмоднсоть вывести данные класса (применялось для поверки)
        :return:
        """
        return str(dict({"D": self.D, "M": self.M}))

    def __eq__(self, other):
        return self.D == other.D and self.M == other.M

    def validation(self):
        # проверка на, то все значения M - числа
        for index, values in self.M.items():
            for i, value in enumerate(values):
                if not str(value).isnumeric():
                    print("Значение в столбце M должно быть числом. Файл {}, строка {}, индекс {}. "
                          "Заменено на 0.".format(self.file, i + 1, index))
                    self.M[index][i] = 0
                else:
                    self.M[index][i] = int(self.M[index][i])

    @staticmethod
    def _make_matrix(files):
        if len(files) == 0:
            raise Exception("Необходимо передать параметр")

        for arg in files:
            if arg in File.__subclasses__():
                raise Exception("Допускаются только тип File")

        # определяем минимальыне длины D[*] и M[*]
        min_D = len(files[0].D)
        min_M = len(files[0].M)
        for arg in files:
            if len(arg.D) < min_D:
                min_D = len(arg.D)
            if len(arg.M) < min_M:
                min_M = len(arg.M)

        # переносим все значения в один(два) словарь(я)
        out_D = dict()
        out_M = dict()
        for arg in files:
            for index in range(1, min_D + 1):
                if index not in out_D.keys():
                    out_D[index] = list()
                for element in arg.D[str(index)]:
                    out_D[index].append(element)
            for index in range(1, min_M + 1):
                if index not in out_M.keys():
                    out_M[index] = list()
                for element in arg.M[str(index)]:
                    out_M[index].append(element)

        # обыединяем зачения D и М
        out_data = list()
        for key, data in out_D.items():
            out_data.append(data)
        for key, data in out_M.items():
            out_data.append(data)

        # транспонируем и вернём заначения
        return out_data, min_D, min_M

    @staticmethod
    def _advanced_matrix(append_data, min_D):
        # проходим слегка модифицированным пузырьком все значения
        out_data = list()
        for j, row1 in enumerate(append_data):
            MS = dict()
            for row2 in append_data[j:]:
                # если нашли такое же значение
                if row1[:min_D] == row2[:min_D]:
                    # обновляем сумму в словаре
                    for i, M_row in enumerate(row2[min_D:]):
                        if i not in MS.keys():
                            MS[i] = 0
                        MS[i] += int(M_row)
            # добавляем части строк в матрицу
            out_data.append(row1[:min_D] + (*MS.values(),))

        # удалим повторения
        out_data = list(set(out_data))
        # сортируем
        out_data.sort()
        return out_data
