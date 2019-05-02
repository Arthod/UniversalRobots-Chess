from PIL import Image, ImageFilter
import numpy as np
import cv2
import time




def check_board_move(image_before, image_after):
    pass

def shrink_image(new_width, image, name="new_image.png"):
    hsize = new_width
    new_image = image.resize((new_width, hsize), Image.ANTIALIAS)
    new_image.save(name)
    return new_image

def find_difference(image_before, image_after):
    arr_before = np.asarray(image_before)
    arr_after = np.asarray(image_after)
    width, height = image_before.size

    difference = []
    for ix in range(width):
        difference.append([])
        for iy in range(height):
            diff_red = arr_after[ix][iy][0] - arr_before[ix][iy][0]
            diff_green = arr_after[ix][iy][1] - arr_before[ix][iy][1]
            diff_blue = arr_after[ix][iy][2] - arr_before[ix][iy][2]
            average_diff = round((diff_red+diff_green+diff_blue)/3)
            if average_diff < 10:
                difference[ix].append(0)
            else:
                difference[ix].append(255)
    diffe = np.asarray(difference)

    diff_img = Image.fromarray(np.uint8(diffe))
    shrunken_diff_img = shrink_image(8, diff_img, "difference_shrunken.png")
    diff_img.save("difference.png")

video = cv2.VideoCapture(1)

check, frame = video.read()

cv2.imshow("Capturing", frame)
cv2.imwrite("2.png", frame)

cv2.waitKey(0)

video.release()

img1 = Image.open("1.png")
img1_shrunken = shrink_image(8*35, img1, "1_shrunken.png")

img2 = Image.open("2.png")
img2_shrunken = shrink_image(8*35, img2, "2_shrunken.png")

print(find_difference(img2_shrunken, img1_shrunken))