import cv2
from os import listdir
from os.path import isfile, join
import Image
import numpy


def getCats(folder):
    labels = [f for f in listdir(folder) if f[-4:] == ".jpg"]
    pictures = [cv2.imread(folder + f) for f in labels]
    return (numpy.array(labels),
            numpy.array(pictures))

model = cv2.createEigenFaceRecognizer(threshold=100.0)
#help(model)
labels, pictures = getCats("pictures/cats/")
model.train(pictures, labels)
