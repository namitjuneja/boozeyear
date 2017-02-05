import cv2
from matplotlib import pyplot as plt
import numpy as np

img = cv2.imread('ttt.jpg')
rows, cols, ch = img.shape
print rows, cols, ch



pts2 = np.float32([[0,0],[cols,0],[0,rows],[cols,rows]])
def sahi(a, num):
    pts1 = np.float32(a)

    #real image marking
    # cv2.line(img, (0, rows/2), (cols, rows/2), (255, 255, 0), 40)
    # cv2.line(img, (cols/2, 0), (cols/2, rows), (255, 255, 0), 40)
    #
    # #actual boundaries
    # cv2.line(img, (560, 650), (368, 520), (255, 0, 0), 40)
    # cv2.line(img, (280, 387), (368, 520), (255, 0, 0), 40)
    # cv2.line(img, (280, 387), (389, 390), (255, 0, 0), 40)
    # cv2.line(img, (560, 650), (389, 390), (255, 0, 0), 40)


    M = cv2.getPerspectiveTransform(pts1,pts2)

    dst = cv2.warpPerspective(img,M,(cols, rows))


    cv2.imwrite("ttt" + num + ".jpg", dst)

    plt.subplot(121),plt.imshow(img),plt.title('Input')
    plt.subplot(122),plt.imshow(dst),plt.title('Output')
    plt.show()

a = [2, 8]
b = [959, 40]
c = [3, 596]
d = [959, 600]

sahi([a,[cols,0],[0,rows],[cols,rows]], "1")
sahi([a,b,[0,rows],[cols,rows]], "2")
sahi([a,b,c,[cols,rows]], "3")
sahi([a,b,c,d], "4")

#first kunal
# sahi([[82,1],[cols,0],[0,rows],[cols,rows]], "1")
# sahi([[82,1],[886,32],[0,rows],[cols,rows]], "2")
# sahi([[82,1],[886,32],[20, 561],[cols,rows]], "3")
# sahi([[82,1],[886,32],[20, 561],[848, 576]], "4")
