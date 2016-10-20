import cv2
import numpy as np
import glob
import os


dirPath = os.path.dirname(os.path.abspath(__file__))
files = glob.glob(dirPath + "/DEPTH/*.png")

print "Press 'a' to display all images"
print "Press 'q' to close"

delay = 0
for f in files:
    img = cv2.imread(f, -1)

    img = (img - 500) / 8.0
    img = img.astype(np.uint8)

    cv2.imshow("", img)
    chr = cv2.waitKey(delay)

    if chr == ord('a'):
        delay = 25
    elif chr == ord('q'):
        break

cv2.destroyAllWindows()