"""""
- pode ser necessário aplicar alguma suavização (borramento leve para retirar ruido)  // ok
- converter para HSV/HSL // ok
- thresholding da cor desejada (cor manual) // ok
- maior componente da mesma (quase)
- eliminação de ruído "topológico", dilatação/erosão // ok
"""""


import cv2
import numpy as np
# Reading the image
img2 = cv2.imread('blue2.jpg', cv2.IMREAD_UNCHANGED)

#redimensionar a imagem
scale_percent = 20  # percent of original size
width = int((img2.shape[1] * scale_percent / 200))
height = int((img2.shape[0] * scale_percent / 200))
dim = (width, height)

# resize image
img = cv2.resize(img2, dim, interpolation=cv2.INTER_AREA)

median = cv2.medianBlur(img, 5)

# convert to hsv colorspace
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

# lower bound and upper bound for Green color
lower_bound = np.array([90, 70, 0])     #red [1, 140, 0]     blue ([90,70,0])       green([50, 20, 20])
upper_bound = np.array([150, 255, 255])  #red [4, 255, 255]  blue ([150,255,255])     green([100, 255, 255])

# find the colors within the boundaries
mask = cv2.inRange(hsv, lower_bound, upper_bound)

#define kernel size
kernel = np.ones((7,7),np.uint8)

# Remove unnecessary noise from mask
mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

# Segment only the detected region
segmented_img = cv2.bitwise_and(median, median, mask=mask)

"""""
# Find contours from the mask
#contours, hierarchy = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
#output = cv2.drawContours(segmented_img, contours, -1, (0, 0, 255), 3)
# Showing the output


#maior componente cv2.IMREAD_GRAYSCALE
nb_components, output, stats, centroids = cv2.connectedComponentsWithStats(img, connectivity=4)
sizes = stats[:, -1]

max_label = 1
max_size = sizes[1]
for i in range(2, nb_components):
    if sizes[i] > max_size:
        max_label = i
        max_size = sizes[i]

img2 = np.zeros(output.shape)
img2[output == max_label] = 255
"""""
final = cv2.hconcat((img, median, segmented_img))
cv2.imshow('processing image', final)

cv2.waitKey(0)
cv2.destroyAllWindows()

