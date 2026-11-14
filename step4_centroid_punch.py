import cv2
import numpy as np


cap = cv2.VideoCapture(0)

punch_h, punch_w = 40, 40

while True:
    ret, frame = cap.read()
    if not ret:
        break
        
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY_INV)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    if contours:
        biggest_contour = max(contours, key=cv2.contourArea)
        cv2.drawContours(frame, [biggest_contour], -1, (0, 255, 0), 2)
        
        M = cv2.moments(biggest_contour)
        if M["m00"] != 0:
            cx = int(M["m10"] / M["m00"])
            cy = int(M["m01"] / M["m00"])
            
            cv2.circle(frame, (cx, cy), 5, (0, 255, 0), -1)
            
            y1 = max(0, cy - punch_h//2)
            y2 = min(frame.shape[0], cy + punch_h//2)
            x1 = max(0, cx - punch_w//2)
            x2 = min(frame.shape[1], cx + punch_w//2)
            
            # cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), -1)

    cv2.imshow('Frame', frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
