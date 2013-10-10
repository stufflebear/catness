import cv2, cv
from os import listdir
from os.path import isfile, join
import numpy
from PIL import Image
import matplotlib.pyplot as plt


def getCats(folder):
    names = [f for f in listdir(folder) if f[-4:] == ".jpg"]
    prepictures = [Image.open(folder + f).convert("L") for f in names]

    pictures = [numpy.asarray(p, dtype=numpy.uint8) for p in prepictures]
    labels = range(len(names))
    return names, numpy.array(labels), numpy.array(pictures)


names, labels, pictures = getCats("pictures/cats/small/")
newImage = pictures[0].reshape(1, 60000)
print "Read pictures"
model = cv2.createFisherFaceRecognizer(10)
print "Created model"
model.train(pictures, labels)
print "Trained model"
ev = model.getMat("eigenvectors").transpose()
mean = model.getMat("mean")
for fface in ev:
    projection = (newImage - mean) * ev
#subspaceProject(eigenvectors, mean, images[0])
plt.imshow(mean.reshape(300, 200))
plt.show()
