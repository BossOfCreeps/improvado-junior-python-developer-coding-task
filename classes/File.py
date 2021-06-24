from abc import ABC, abstractmethod


class File(ABC):
    """
    Переменные для хранения D[], M[] и имени файла
    Структура D (любые значения) и M (точка числа):
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

        # Поэтому я пересоздаю её, чтобы адрес поменялся.
        self.D = dict()
        self.M = dict()
        # заносим адрес до папки
        self.file = file

    def __str__(self):
        """
        Даёт возможность вывести данные класса (применялось для поверки)
        """
        return str(dict({"D": self.D, "M": self.M}))

    def __eq__(self, other):
        """
        Сравнение файлов
        :param other: другой файл
        """
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

        # определяем минимальные длины D[*] и M[*]
        min_d = len(files[0].D)
        min_m = len(files[0].M)
        for arg in files:
            if len(arg.D) < min_d:
                min_d = len(arg.D)
            if len(arg.M) < min_m:
                min_m = len(arg.M)

        # переносим все значения в один(два) словарь(я)
        out_d = dict()
        out_m = dict()
        for arg in files:
            for index in range(1, min_d + 1):
                if index not in out_d.keys():
                    out_d[index] = list()
                for element in arg.D[str(index)]:
                    out_d[index].append(element)
            for index in range(1, min_m + 1):
                if index not in out_m.keys():
                    out_m[index] = list()
                for element in arg.M[str(index)]:
                    out_m[index].append(element)

        # объединяем значения D и М
        out_data = list()
        for key, data in out_d.items():
            out_data.append(data)
        for key, data in out_m.items():
            out_data.append(data)

        # транспонируем и вернём значения
        return out_data, min_d, min_m

    @staticmethod
    def _advanced_matrix(append_data, min_d):
        # проходим слегка модифицированным пузырьком все значения
        out_data = list()
        for j, row1 in enumerate(append_data):
            ms = dict()
            for row2 in append_data[j:]:
                # если нашли такое же значение
                if row1[:min_d] == row2[:min_d]:
                    # обновляем сумму в словаре
                    for i, M_row in enumerate(row2[min_d:]):
                        if i not in ms.keys():
                            ms[i] = 0
                        ms[i] += int(M_row)
            # добавляем части строк в матрицу
            out_data.append(row1[:min_d] + (*ms.values(),))

        # удалим повторения
        out_data = list(set(out_data))
        # сортируем
        out_data.sort()
        return out_data
