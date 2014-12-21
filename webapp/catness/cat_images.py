from os import listdir
import Image
import sys
import os

from align import CropFace


def parseDotCat(catLabels):
    """
    Extract data from the .cat files in the cat database
    """
    labels = [int(x) for x in open(catLabels).readlines()[0].rstrip().split(" ")]
    assert(labels[0] == 9 and len(labels) == 19)
    metaData = {}
    metaData["leftEye"] = (labels[1], labels[2])
    metaData["rightEye"] = (labels[3], labels[4])
    metaData["mouth"] = (labels[5], labels[6])
    metaData["leftEarOut"] = (labels[7], labels[8])
    metaData["leftEarTop"] = (labels[9], labels[10])
    metaData["leftEarIn"] = (labels[11], labels[12])
    metaData["rightEarIn"] = (labels[13], labels[14])
    metaData["rightEarTop"] = (labels[15], labels[16])
    metaData["rightEarOut"] = (labels[17], labels[18])
    return metaData


def getAlignedImages(folder):
    """
    Returns aligned images from a cat databse folder
    """
    aligned = []
    rawInfoNames = [f for f in listdir(folder) if f[-4:] == ".cat"]
    for cat in rawInfoNames:
        name = cat[0:-4]
        metaData = parseDotCat(folder + cat)
        image = Image.open(folder + name)
        aligned.append((name,
                        CropFace(image,
                                 eye_left=metaData["leftEye"],
                                 eye_right=metaData["rightEye"],
                                 offset_pct=(0.1, 0.3),
                                 dest_sz=(200, 300))))
    return aligned

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print "Usage: python align.py [raw cat picture] [new cat picture]"
        sys.exit(0)
    inputDir = sys.argv[1]
    aligned = getAlignedImages(inputDir)
    path = "cats/" + "/".join(inputDir.split("/")[1:])
    if not os.path.exists(path):
        os.makedirs(path)
    for (name, image) in aligned:
        image.save(path + name)
