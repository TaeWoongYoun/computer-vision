import cv2

def edge():
    img = cv2.imread("./image/cat.png")
    
    if img is None:
        print("Image not found.")
        return

    # 그레이스케일로 변환
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # BGR 이미지를 그레이스케일로 변환

    # 에지 검출
    lowerThreshold = 100  # 하한 임계값 설정
    upperThreshold = 200  # 상한 임계값 설정
    imgCanny = cv2.Canny(imgGray, lowerThreshold, upperThreshold)  # Canny 에지 검출

    # 결과 이미지 표시
    cv2.imshow("Edge Detection", imgCanny)  # 에지 검출 결과 이미지 창을 생성하고 표시
    cv2.waitKey(0)  # 키 입력 대기
    cv2.destroyAllWindows()  # 모든 창 닫기

edge()
