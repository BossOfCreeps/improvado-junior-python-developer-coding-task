from classes.File import File
from xml.dom import minidom
import xml.etree.ElementTree as ET


class XML(File):
    def __init__(self, file):
        super().__init__(file)

        # проверка типа
        if file.split(".")[-1] != "xml":
            raise Exception("Неподходящий тип")

    def read_data(self):
        # считываем данные из файла
        doc = minidom.parse(self.file)
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

        self.validation()

    @staticmethod
    def _write_to_file(out, data, min_D, min_M, name_M):
        matrix = list(zip(*data))

        # create the file structure
        data = ET.Element('root')
        items = ET.SubElement(data, 'objects')

        item = list(range(len(matrix)))
        for i, values in enumerate(matrix):
            item[i] = ET.SubElement(items, 'object')
            if i < min_D:
                item[i].set('name', 'D{}'.format(i + 1))
            else:
                item[i].set('name', '{}{}'.format(name_M, i + 1 - min_D))

            values = list(values)
            it = list(range(len(values)))
            for j, value in enumerate(values):
                it[j] = ET.SubElement(item[i], 'value')
                it[j].text = str(value)

        # create a new XML file with the results
        my_data = ET.tostring(data)
        my_file = open(out, "wb")
        my_file.write(my_data)

    @staticmethod
    def basic(out, *files):
        matrix, min_D, min_M = XML._make_matrix(files)
        matrix = list(zip(*matrix))

        # сортируем
        matrix.sort(key=lambda i: i[0])
        XML._write_to_file(out, matrix, min_D, min_M, name_M="M")

    @staticmethod
    def advanced(out, *files):
        matrix, min_D, min_M = XML._make_matrix(files)
        matrix = list(zip(*matrix))
        matrix = File._advanced_matrix(matrix, min_D)
        XML._write_to_file(out, matrix, min_D, min_M, name_M="MS")
