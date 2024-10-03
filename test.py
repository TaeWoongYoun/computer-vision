import cv2

def test():
    img = cv2.imread("cat.png")  # 이미지를 읽어옵니다.
    
    if img is None:
        print("Image not found.")
        return
    
    cv2.imshow("img", img)  # 이미지를 창에 표시합니다.
    cv2.waitKey(0)  # 키 입력을 대기합니다.
    cv2.destroyAllWindows()  # 모든 창을 닫습니다.

test()
