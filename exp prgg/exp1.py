import cv2

img = cv2.imread("pic11.jpg")
cv2.imshow("Image Window", img)
cv2.waitKey(0)
cv2.destroyAllWindows()