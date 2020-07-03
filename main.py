"""
                                                    код(%)      гугл(%)
18.10-18.20 - начало. создание систеым классов      100         0
18.20-18.30 - тест csv                              50          50
18.30-18.40 - транспонирование                      20          80
18.40-19.10 - написнаие логики обратки данных СSV   100         0
19.10-19.30 - написнаие логики обратки данных JSON  95          5
19.30-20.00 - написание логики дял XML              10          90
06.30-07.20 - написание логики для TSV              90          10
08.20-09.20 - начал делать advanced                 100         0
09.30-10.00 - написание бонусов                     100         0

итого 6 часов 20 минут                           285 мин        95 мин
                                        (4 часов 45 мин)        (1 час 35 мин)
"""

import csv
import json
from xml.dom import minidom


class File:
    # переменные для хранения D[], M[] и имени файла
    D = dict()
    M = dict()
    file = str

    def __init__(self, file):
        """
        Функция инициализации
        :param file: адрес до файла
        """

        # проверка на то, что переданный тип адреса файла - строка
        if type(file) != str:
            raise Exception("В качестве адреса файла должна быть строка")

        # Тут у меня возникла проблема, связанная с тем, что в двух классах потомках dict был одниим.
        # Видимо из-за тоогоч dict - адресная перменненная. Поэтому я пересоздаю её, чтобы адрес поменялся.
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


class CSV(File):
    def __init__(self, file):
        super().__init__(file)

        # проверка типа
        if file.split(".")[-1] != "csv":
            raise Exception("Неподходящий тип")

        # открываем файл, записываем его список (получается список списков) и транпонируем (список tuple'ов)
        with open(file) as f:
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

        for index, values in self.M.items():
            for i, value in enumerate(values):
                if not str(value).isnumeric():
                    print("Значение в столбце M должно быть числом. Файл {}, строка {}, индекс {}. "
                          "Заменено на 0.".format(self.file, i + 1, index))
                    self.M[index][i] = 0


class JSON(File):
    def __init__(self, file):
        super().__init__(file)

        # проверка типа
        if file.split(".")[-1] != "json":
            raise Exception("Неподходящий тип")

        # открываем файл и сразу передохим в fields
        with open(file) as f:
            fields = json.load(f)['fields']

        # проодим по элментам массива
        for field in fields:
            for D_M, data in field.items():
                index = D_M[1:]

                if D_M[0] == "D":
                    # если такой индекс ещё не встречался, то создаём его со значением пустого массива
                    if index not in self.D.keys():
                        self.D[index] = list()
                    # заносим данные
                    self.D[index].append(data)
                elif D_M[0] == "M":
                    if index not in self.M.keys():
                        self.M[index] = list()
                    self.M[index].append(data)
                else:
                    raise Exception("Допускаются только D и М")

        for index, values in self.M.items():
            for i, value in enumerate(values):
                if not str(value).isnumeric():
                    print("Значение в столбце M должно быть числом. Файл {}, строка {}, индекс {}. "
                          "Заменено на 0.".format(self.file, i + 1, index))
                    self.M[index][i] = 0


class XML(File):
    def __init__(self, file):
        super().__init__(file)

        # проверка типа
        if file.split(".")[-1] != "xml":
            raise Exception("Неподходящий тип")

        # считываем данные из файла
        doc = minidom.parse(file)
        # ищем все object
        for item in doc.getElementsByTagName("object"):
            # считываем значения (value) и запоисываем их для каждого object
            values = list()
            for row in item.getElementsByTagName("value"):
                values.append(row.firstChild.nodeValue)

            # заносим значения в словари
            index = item.attributes["name"].value[1:]
            if item.attributes["name"].value[0] == "D":
                self.D[index] = list(values)
            elif item.attributes["name"].value[0] == "M":
                self.M[index] = list(values)
            else:
                raise Exception("Допускаются только D и М")

        for index, values in self.M.items():
            for i, value in enumerate(values):
                if not str(value).isnumeric():
                    print("Значение в столбце M должно быть числом. Файл {}, строка {}, индекс {}. "
                          "Заменено на 0.".format(self.file, i + 1, index))
                    self.M[index][i] = 0


class TSV(File):
    def basic(self, *args):
        if len(args) == 0:
            raise Exception("Необходимо передать параметр")

        for arg in args:
            if arg in File.__subclasses__():
                raise Exception("Допускаются только тип File")

        # определяем минимальыне длины D[*] и M[*]
        min_D = len(args[0].D)
        min_M = len(args[0].M)
        for arg in args:
            if len(arg.D) < min_D:
                min_D = len(arg.D)
            if len(arg.M) < min_M:
                min_M = len(arg.M)

        # переносим все значения в один(два) словарь(я)
        out_D = dict()
        out_M = dict()
        for arg in args:
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

        # транспонируем
        out_data = list(zip(*out_data))

        # сортируем
        def keyFunc(item):
            return item[0]

        out_data.sort(key=keyFunc)

        # записываем файл
        with open(self.file, 'w') as out_file:
            tsv_writer = csv.writer(out_file, delimiter='\t', lineterminator='\n')
            # шапка
            header = list()
            for index in range(1, min_D + 1):
                header.append("D{}".format(index))
            for index in range(1, min_M + 1):
                header.append("M{}".format(index))
            tsv_writer.writerow(header)
            # данные
            tsv_writer.writerows(out_data)

    def advanced(self, *args):
        if len(args) == 0:
            raise Exception("Необходимо передать параметр")

        for arg in args:
            if arg in File.__subclasses__():
                raise Exception("Допускаются только тип File")

        # определяем минимальыне длины D[*] и M[*]
        min_D = len(args[0].D)
        min_M = len(args[0].M)
        for arg in args:
            if len(arg.D) < min_D:
                min_D = len(arg.D)
            if len(arg.M) < min_M:
                min_M = len(arg.M)

        # переносим все значения в один(два) словарь(я)
        out_D = dict()
        out_M = dict()
        for arg in args:
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
        append_data = list()
        for key, data in out_D.items():
            append_data.append(data)
        for key, data in out_M.items():
            append_data.append(data)

        # транспонируем
        append_data = list(zip(*append_data))

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
            # доавляем части строк в матрицу
            out_data.append(row1[:min_D] + (*MS.values(),))

        # удалим повторения
        out_data = list(set(out_data))

        # сортируем
        out_data.sort()

        # записываем файл
        with open(self.file, 'w') as out_file:
            tsv_writer = csv.writer(out_file, delimiter='\t', lineterminator='\n')
            # шапка
            header = list()
            for index in range(1, min_D + 1):
                header.append("D{}".format(index))
            for index in range(1, min_M + 1):
                header.append("MS{}".format(index))
            tsv_writer.writerow(header)
            # данные
            tsv_writer.writerows(out_data)

    def __eq__(self, other):
        super().__init__(self.file)

        # открываем первый файл
        with open(self.file) as f:
            self_file_data = list(csv.reader(f, delimiter='\t'))

        # открываем второй файл
        with open(other.file) as f:
            other_file_data = list(csv.reader(f, delimiter='\t'))

        return self_file_data == other_file_data


csv_1 = CSV("csv_data_1.csv")
csv_2 = CSV("csv_data_2.csv")
json_1 = JSON("json_data.json")
xml_1 = XML("xml_data.xml")

tsv_1 = TSV("basic_results.tsv")
tsv_2 = TSV("advanced_results.tsv")

tsv_1.basic(csv_1, csv_2, json_1, xml_1)
tsv_2.advanced(csv_1, csv_2, json_1, xml_1)

print(tsv_1 == TSV("_basic_results.tsv"))

"""БОНУСЫ 
1) в дальнейшем использовании программы возможно появление требования для работы с другими типами файлов, например .yaml 
Ответ: Для этого будет необходимо создать класс-наследник от File, который будет иметь метод __init__, 
парясящий полученный yaml в словари D и М 

2) входные файлы могут быть больших размеров
Ответ: я не могу без тестирования сказать нечего конкретного по поводу того, как моя система будет с большими данным, 
первоначальынх проблем я не вижу, но могу ошибаться.

3) возможность обработки строк с некорректными значениями без прекращения выполнения программы с информированием 
пользователя об ошибках в конце её выполнения
Ответ: как я понял это относится к общей форме файла (D... M...) - это обработка уже была и к тому, что M должо быть 
числом - эту обработку добавил

4) подумать об организации тестирования программы 
Ответ: дописал метод __eq__ для класса TSV, который сравнивает заченяи в двух файлах
"""
