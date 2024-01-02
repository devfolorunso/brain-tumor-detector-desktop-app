import numpy as np  # Import the NumPy library
import cv2 as cv  # Import the OpenCV library

class DisplayTumor:
    curImg = 0  # Initialize a variable to store the current image
    Img = 0  # Initialize a variable to store the image

    def readImage(self, img):
        # Convert the input image to a NumPy array
        self.Img = np.array(img)
        self.curImg = np.array(img)

        # Convert the image to grayscale
        gray = cv.cvtColor(np.array(img), cv.COLOR_BGR2GRAY)

        # Apply thresholding to create a binary image
        self.ret, self.thresh = cv.threshold(gray, 0, 255, cv.THRESH_BINARY_INV + cv.THRESH_OTSU)

    def getImage(self):
        # Return the current image
        return self.curImg

    # Noise removal
    def removeNoise(self):
        # Define a kernel for morphological operations
        self.kernel = np.ones((3, 3), np.uint8)

        # Perform morphological opening to remove noise
        opening = cv.morphologyEx(self.thresh, cv.MORPH_OPEN, self.kernel, iterations=2)

        # Update the current image
        self.curImg = opening

    def displayTumor(self):
        # Sure background area
        sure_bg = cv.dilate(self.curImg, self.kernel, iterations=3)

        # Finding sure foreground area
        dist_transform = cv.distanceTransform(self.curImg, cv.DIST_L2, 5)
        ret, sure_fg = cv.threshold(dist_transform, 0.7 * dist_transform.max(), 255, 0)

        # Find unknown region.
        sure_fg = np.uint8(sure_fg)
        unknown = cv.subtract(sure_bg, sure_fg)

        # Marker labeling
        ret, markers = cv.connectedComponents(sure_fg)

        # Add one to all labels so that sure background is not 0, but 1
        markers = markers + 1

        # Now mark the region of unknown with zero
        markers[unknown == 255] = 0

        # Apply watershed algorithm to segment the image
        markers = cv.watershed(self.Img, markers)

        # Mark tumor region in the original image
        self.Img[markers == -1] = [255, 0, 0]

        # Convert the image to the BGR color space
        tumorImage = cv.cvtColor(self.Img, cv.COLOR_HSV2BGR)

        # Update the current image with the segmented tumor region
        self.curImg = tumorImage
