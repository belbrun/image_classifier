from functions import *
from layers import *
import datautil

class NeuralNetwork():

    def __init__(self, errorFunction = simpleCost):
        self.errorFunction = errorFunction
        self.layers = []


    def addLayer(self, layer):
        """
        Add a layer to the neural network in sequential fashion.
        """
        self.layers.append(layer)

    def output(self, x):
        """
            Calculate the output for a single input instance x (one row from
            the training or test set)
        """

        for layer in self.layers:
            x = layer.propagateForward(x)
            #print(layer, x)

        return x

    def calculateOutputs(self, data):
        outputs = []

        for instance in data:
            outputs.append(self.output(instance))

        return outputs


    def feed(self, data):
        outputs = self.calculateOutputs(data)
        return outputs

    def feedForError(self, x, result):
        output = self.output(x)
        error = self.calculateError(output, result)
        return (output, error)

    def calculateError(self, output, result):

        errors = []
        for i in range(0, result.shape[0]):
            errors.append(self.errorFunction(output[i], result[i]))

        return np.array(errors)

    def getOverallError(self, outputs, results):

        overallError = 0
        for i in range(0, len(outputs)):
            for error in self.calculateError(outputs[i], results[i]):
                overallError += error #absoulte ?

        return error

    def learn(self, errors, learningRate):

        for index,layer in enumerate(self.layers[::-1]):
            #print('----------------')
            #print(layer, '\n', errors)
            errors = layer.propagateBackwards(errors, 2**(index-3))
            #learningRate *= 2


    def train(self, x, results, learningRate):
        output = self.output(x)
        errors = self.calculateError(output, results)
        self.learn(errors, learningRate)
        return errors

    def save(self, path):
        for (index, layer) in enumerate(self.layers):
            newPath = path + str(index) + '/'
            datautil.makeDirectory(newPath)
            layer.save(newPath)

    def load(path):
        network = NeuralNetwork(crossEntropyLoss)
        for (index, id) in enumerate(datautil.getLayerIds(path)):
            network.addLayer(\
                getLayerById(id).load(path + str(index) + '/'))
        return network

    def printNetwork(self):
        for layer in self.layers:
            print(layer)
            if isinstance(layer, ConvolutionLayer):
                print(layer.filters)
                print(layer.bias)
            if isinstance(layer, FullyConnectedLayer):
                print(layer.weights)
                print(layer.bias)
