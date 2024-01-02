# Import necessary libraries
from tensorflow.keras.models import load_model  # Import the load_model function from TensorFlow
import cv2 as cv  # Import OpenCV library
import imutils  # Import the imutils library

# Load the pre-trained brain tumor detection model
model = load_model('brain_tumor_detector.h5')

# Define a function to predict whether a brain tumor is present in the given image
def predictTumor(image):
    #-------------------------PREPROCESSING (IMAGE AUGMENTATION)------------------------
    # Convert the input image to grayscale
    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    # Apply Gaussian blur to the grayscale image
    gray = cv.GaussianBlur(gray, (5, 5), 0)

    #--------------------------SEGMENTATION--------------------------------------
    # Threshold the image to create a binary image
    thresh = cv.threshold(gray, 45, 255, cv.THRESH_BINARY)[1]
    # Perform erosion and dilation to remove small regions of noise
    thresh = cv.erode(thresh, None, iterations=2)
    thresh = cv.dilate(thresh, None, iterations=2)

    # Find contours in the thresholded image
    cnts = cv.findContours(thresh.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    # Find the largest contour
    c = max(cnts, key=cv.contourArea)

    # Find extreme points (left, right, top, bottom) of the largest contour
    extLeft = tuple(c[c[:, :, 0].argmin()][0])
    extRight = tuple(c[c[:, :, 0].argmax()][0])
    extTop = tuple(c[c[:, :, 1].argmin()][0])
    extBot = tuple(c[c[:, :, 1].argmax()][0])

    # Crop a new image from the original image using the extreme points
    new_image = image[extTop[1]:extBot[1], extLeft[0]:extRight[0]]

    # Resize the cropped image to a specific size and normalize it
    image = cv.resize(new_image, dsize=(240, 240), interpolation=cv.INTER_CUBIC)
    image = image / 255.0

    # Reshape the image to match the model's input shape
    image = image.reshape((1, 240, 240, 3))
    
    #-------------------------CLASSIFICATION---------------------------------------
    # Use the loaded model to predict whether a tumor is present in the cropped image
    res = model.predict(image)
    print("Prediction Value: " + str(res))

    # Return the prediction result
    return res
