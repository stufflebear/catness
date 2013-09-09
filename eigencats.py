import cv2
from os import listdir
from os.path import isfile, join
import numpy

NUM_EIGENFACES = 10


def getCats(folder):
    names = [f for f in listdir(folder) if f[-4:] == ".jpg"]
    pictures = [cv2.imread(folder + f) for f in names]
    labels = [num for num in range(0, len(names))]
    return (numpy.array(labels),
            numpy.array(pictures))

model = cv2.createEigenFaceRecognizer(NUM_EIGENFACES)
labels, pictures = getCats("pictures/cats/")
model.train(pictures, labels)
eigenvectors = model.getMat("eigenvectors")
eigenvectorsTranspose = eigenvectors.transpose()
numColumns = eigenvectors.shape[1] # shape is (40000, NUM_EIGENFACES)
for num in range(0, min(NUM_EIGENFACES, numColumns)):
    ev = eigenvectorsTranspose[num]
    notZeroes = [i for i in ev if i != 0]
    print "notZeroes for eigenface number " + str(num) + ": " + str(notZeroes) # Why are they all zeroes?
    evNorm = numpy.ndarray(ev.shape)
    cv2.normalize(ev, evNorm, 0, 255, cv2.NORM_MINMAX)
    cv2.imwrite("eigenface.png", evNorm.reshape(200, 200))
