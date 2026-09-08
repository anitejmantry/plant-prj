import numpy as np
import cv2

# RGB values of the 5x5 image
rgb_values = np.array([
    [[255,122,47], [255,122,47], [255,122,47], [255,122,47], [255,122,47]],

    [[255,122,47], [254,122,47], [243,151,28], [253,193,11], [255,122,47]],

    [[255,122,47], [251,213,185], [254,119,48], [6,125,95], [255,122,47]],

    [[255,122,47], [242,220,209], [255,122,47], [255,122,47], [255,122,47]],

    [[255,122,47], [255,122,47], [255,122,47], [255,122,47], [255,122,47]]
], dtype=np.uint8)

# Convert RGB to BGR because OpenCV uses BGR
bgr_image = cv2.cvtColor(rgb_values, cv2.COLOR_RGB2BGR)

# Save the reconstructed image
cv2.imwrite("reconstructed.png", bgr_image)

# Enlarge the image for better visibility (optional)
enlarged = cv2.resize(bgr_image, (500, 500), interpolation=cv2.INTER_NEAREST)

# Display the image
cv2.imshow("Reconstructed Image", enlarged)
cv2.waitKey(0)
cv2.destroyAllWindows()