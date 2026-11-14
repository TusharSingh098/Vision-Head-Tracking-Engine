import cv2


airplane = cv2.imread('shuttle3.png')

airplane = cv2.resize(airplane, (100, 100))
h, w = airplane.shape[:2]

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    
    if not ret:
        break

    x, y = 100, 200
    
    frame[y:y+h, x:x+w] = airplane
        
    cv2.imshow('Camera with Airplane', frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
