# This Python file uses the following encoding: utf-8


class WfReader:
    def __init__(self):
        self.PROPERTY_SEPARATOR = ":"
        self.WINDOW_VALUE_SEPARATOR = " "
        self.VECTOR_START_TOKEN = "["
        self.VECTOR_END_TOKEN = "]"

    def extractWindow(self, inputLine):
        inputTokens = inputLine.split(self.WINDOW_VALUE_SEPARATOR)
        print(inputTokens)
        NAN_VALUES = ["nan", "-nan", "NaN", "inf", "Inf", "-inf"]
        windowVector = []
        isVector = False
        for token in inputTokens:
            token = token.strip()
            print(".",token,".")
            if token == "":
                continue
            elif token in NAN_VALUES:
                token = "0"

            if token == self.VECTOR_START_TOKEN:
                isVector = True
                vectorFeature = []
            elif token == self.VECTOR_END_TOKEN:
                isVector = False
                windowVector.append(vectorFeature)
            else:
                if isVector:
                    vectorFeature.append(float(token))
                else:
                    windowVector.append(float(token))
        return windowVector

    def extractValue(self, inputLine):

        return inputLine[inputLine.find(self.PROPERTY_SEPARATOR) + 1:].strip()

    def readAttributeNames(self, fileStream):
            attributeCount = int(self.extractValue(fileStream.readline()))
            attributeNames = []
            for i in range(attributeCount):
                attributeNames.append(self.extractValue(fileStream.readline()))
            return attributeNames

    def readWfFile(self, inputFileName):
        #create (featureNames) dict<class, LIST of LIST>, where list either has doubles or vector of doubles
        featureMap = {}
        with open(inputFileName, "r") as fileStream:
            attributeNames = self.readAttributeNames(fileStream)
            line = fileStream.readline()
            while line != "":
                className = self.extractValue(line)
                exampleCount = int(self.extractValue(fileStream.readline()))
                windows = []
                for i in range(exampleCount):
                    line = fileStream.readline()
                    window = self.extractWindow(line)
                    windows.append(window)
                if className in featureMap:
                    featureMap[className] += windows
                else:
                    featureMap[className] = windows
                line = fileStream.readline()
        return attributeNames, featureMap


