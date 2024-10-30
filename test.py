import cv2

def test():
    img = cv2.imread("./image/cat.png")
    
    if img is None:
        print("Image not found.")
        return
    
    cv2.imshow("img", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

test()
