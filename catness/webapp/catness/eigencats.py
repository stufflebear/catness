import cv2, cv
from os import listdir
from os.path import isfile, join
import numpy
from PIL import Image
from scipy.spatial.distance import cosine
import matplotlib.pyplot as plt


def getCats(folder):
    names = [f for f in listdir(folder) if f[-4:] == ".jpg"]
    prepictures = [Image.open(folder + f).convert("L") for f in names]

    pictures = [numpy.asarray(p, dtype=numpy.uint8) for p in prepictures]
    labels = range(len(names))
    print "Read pictures"
    return names, numpy.array(labels), numpy.array(pictures)


def normalizePixels(picture):
    return picture * 255.0 / picture.max()


def display(picture):
    Image.fromarray(normalizePixels(picture).reshape(300, 200)).show()


def createModel(pictures, labels):
    model = cv2.createFisherFaceRecognizer(10)
    model.train(pictures, labels)
    print "Trained model"
    return model


def getCuteness(picture, model):
    """
    Returns a cuteness score based on cosine distance from average cat
    """
    mean = model.getMat("mean")
    ui, si, vi = numpy.linalg.svd(picture)
    um, sm, vm = numpy.linalg.svd(mean.reshape(200, 300))
    cos = cosine(si, sm)
    return cos


def cuteOrNot(picture):
    cutenessValue = getCuteness(picture, model)
    if cutenessValue > 0.01:
        return True
    else:
        return False

names, labels, pictures = getCats("catness/pictures/cats/small/")
model = createModel(pictures, labels)

if __name__ == "__main__":
    names, labels, pictures = getCats("pictures/cats/small/")
    newImage = pictures[4]
    print newImage.shape
    model = createModel(pictures, labels)
    mean = model.getMat("mean")
    display(mean)
    print len(pictures)
    print "Pic 4's similarity:", getCuteness(newImage, model)
    allSums = [getCuteness(pic, model) for pic in pictures]
    print allSums
    print "max:", max(allSums)
    print "min:", min(allSums)
    print "avg:", sum(allSums) / len(allSums)
    print [cuteOrNot(pic, model) for pic in pictures]
