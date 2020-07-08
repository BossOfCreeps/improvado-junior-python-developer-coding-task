from classes.File import File
from xml.dom import minidom


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
