import cv2
from os import listdir
from os.path import isfile, join
import numpy


def getCats(folder):
    names = [f for f in listdir(folder) if f[-4:] == ".jpg"]
    pictures = [cv2.imread(folder + f) for f in names]
    labels = [num for num in range(0, len(names))]
    return (numpy.array(labels),
            numpy.array(pictures))

model = cv2.createEigenFaceRecognizer(threshold=100.0)
#help(model)
labels, pictures = getCats("pictures/cats/")
model.train(pictures, labels)
