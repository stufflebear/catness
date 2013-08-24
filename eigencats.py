import cv2
from os import listdir
from os.path import isfile, join
import Image
import numpy
from scipy import io
import math
import matplotlib.pyplot as plt
from numpy import linalg
import sys, os


def norm(dist):
    dist = list(dist)
    total = sum(dist)
    for i in range(len(dist)):
        dist[i] = float(dist[i]) / total
    return numpy.array(dist)

def grayscale(image):
  output = numpy.sum(image, axis=2) / 3
  output = output.astype(image.dtype)
  return output

# Returns processed images from a given database. The second and third
# arguments are to cut down on repetitive image processing.
#
# @param processedData: if all masked and centered images already exist 
#   in database, set to true. Else, false
#
def getProcessedImages(database):
    allImages = []
    names = []
    validExt = ['.jpg']

    sum = numpy.zeros((200, 200, 3))
    count = 0
    for dirname, dirnames, filenames in os.walk(database):
        for filename in filenames:
            name, ext = os.path.splitext(filename)
            if ext in validExt and 'reconstruct' not in name:
                im = cv2.imread(os.path.join(dirname, filename))
                allImages.append(im)
                if 'Average' not in name:
                    names.append(name)
                    sum = sum+im
                    count += 1
    meanImage = sum/count
    cv2.imwrite(os.path.join(dirname, "Average.jpg"),  meanImage)
    for i in range(len(allImages)):
        allImages[i] = allImages[i] - meanImage
    return (allImages, names)

def greyCollapse(images):
    newImages = []
    for image in images:
        grayed = grayscale(image)
        newImage = []
        for x in range(len(grayed)):
            newImage.extend(grayed[x])
        newImages.append(newImage)
    return newImages

def uncollapseAll(images):
    newImages = []
    for image in images:
        newImage = []
        count = 0
        row = []
        for x in range(len(image)):
            if x % 200 == 0:
                row = []
            rgb = image[x]
            row.append(rgb)
            if (x+1) % 200 == 0:
                count +=1
                newImage.append(row)
        newImages.append(newImage)
    return numpy.array(newImages)

# Distance functions #

def euDist(p, q):
    if len(p) != len(q):
        print "ERROR: WE'RE DOING SOMETHING WRONG"
        return -1
    sums = 0
    for i in range(len(p)):
        sums += (q[i] - p[i])**2
    return sums**0.5

def mahaDist(x, y, cov):
    x = numpy.array(x).reshape((len(x),1))
    y = numpy.array(y).reshape((len(y),1))
    cov = numpy.array(cov)
    term1 = numpy.transpose(x-y)
    term2 = numpy.linalg.inv(cov)
    term3 = x-y
    result = numpy.dot(numpy.dot(term1, term2),term3)
    if result[0][0] < 0:
        print "OH SHIT, SOMETHING WENT WRONG"
        return -1
    result = result[0][0]**0.5
    return result
                
# Computing the Eigenfaces #
# Step 1: Compute eigenvalue/vectors of ATA
# Step 2: Compute eigenfaces from precomputed values

def getEigenFaces(images):
    # Compute eigenvalues/vectors of ATA
    images = numpy.transpose(images)
    product = numpy.dot(numpy.transpose(images), images)
    print "shape of ATA. Should be (num_images, num_images): " + str(product.shape)
    eigvalues, eigvectors = numpy.linalg.eig(product)
    print "Shape of eigenvectors ", numpy.array(eigvectors).shape
    combined = zip(eigvalues, eigvectors)
    combined.sort(reverse=True)
    eigvalues, eigvectors = zip(*combined)

    print "eigenvalues: " + str(eigvalues)

    # Compute eigenfaces
    AV = numpy.dot(images, eigvectors)
    sigma = numpy.diag([math.fabs(x)**0.5 for x in eigvalues])
    eigenfaces = AV
    eigenfaces = numpy.transpose(eigenfaces)
    return eigenfaces

def getPercents(image, eigenfaces):
    sizes = [i.size for i in eigenfaces]
    percents = [numpy.dot(norm(eigenfaces[i]), image) for i in range(10)]
    return 5*numpy.array(norm(percents))

def compare(newCat, allCats, eigenfaces, distFn):
    studPercents = getPercents(newCat, eigenfaces)
    dists = []
    for i in range(len(allCats)):
        celebPercents = getPercents(allCats[i], eigenfaces)
        dist = distFn(studPercents, celebPercents)
        dists.append(dist)
    min1, val1 = argAndMin(dists)
    dists[min1] = float("inf")
    min2, val2 = argAndMin(dists)
    return (min1, min2)
        
def argAndMin(l):
    minVal = float("inf")
    minIndex = -1
    for i in range(len(l)):
        if l[i] < minVal:
            minVal = l[i]
            minIndex = i
    return (minIndex, minVal)

 
if __name__ == '__main__':

    newCat = cv2.imread(sys.argv[1])
    catToCompare = numpy.array(greyCollapse([newCat])[0])

    catsDir = os.path.abspath(os.path.join(os.curdir, 'pictures/cats'))

    images, names = getProcessedImages(catsDir)
    print names
    averageFace = cv2.imread(os.path.join(catsDir, "Average.jpg"))
    averageFace = greyCollapse([averageFace])[0]
    imagesGC = greyCollapse(images)

    eigenfaces = getEigenFaces(imagesGC)
    singleFace = eigenfaces[0]

    eigenImages = uncollapseAll(numpy.array(eigenfaces))
    
    for i in range(10):
        cv2.imwrite("pictures/eigencats/eigen"+str(i)+".jpg", eigenImages[i])
        print "Wrote eigen"+str(i)+".jpg"

    mostSimilar, secondMostSimilar = compare(catToCompare, imagesGC, eigenfaces, euDist)
    print sys.argv[1] + " matches " + names[mostSimilar] + " and " + names[secondMostSimilar]
