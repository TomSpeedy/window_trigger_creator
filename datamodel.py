# This Python file uses the following encoding: utf-8


class DataModel:
    def __init__(self, reader, fileName):
        self.reader = reader
        self.attributeNames, self.data = self.reader.readWfFile(fileName)

    def scalarAttributes(self):
        scalarAttributes = []
        vectorMarker = "[["
        for attributeName in self.attributeNames:
            if vectorMarker not in attributeName:
                scalarAttributes.append(attributeName)
        return scalarAttributes
        #TODO init the model using the reader

    def classes(self):
        return self.data.keys()
