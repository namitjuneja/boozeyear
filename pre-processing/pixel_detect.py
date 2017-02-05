import cv2
from matplotlib import pyplot as plt

# mouse callback function
def mouse_callback(event, x, y, params, flags):
    if event == cv2.EVENT_LBUTTONDOWN:
        print x, y

img = cv2.imread('final.jpg')
rows,cols,ch = img.shape

cv2.namedWindow('image', cv2.WINDOW_NORMAL)  # Can be resized
cv2.resizeWindow('image', cols, rows)  # Reasonable size window
cv2.setMouseCallback('image', mouse_callback)  # Mouse callback


cv2.imshow('image', img)
k = cv2.waitKey(0) & 0xFF
if k == 27:
    cv2.destroyAllWindows()


