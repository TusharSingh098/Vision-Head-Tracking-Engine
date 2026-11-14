import cv2
import numpy as np
import random


class Asteroid:
    def __init__(self, screen_width):
        self.x = random.randint(0, screen_width)
        self.y = 0
        self.speed = random.randint(5, 10)
        self.radius = 20

    def move(self):
        self.y += self.speed

    def draw(self, frame):
        cv2.circle(frame, (self.x, self.y), self.radius, (0, 0, 255), -1)


cap = cv2.VideoCapture(0)
screen_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
screen_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

asteroids = []
score = 0

while True:
    ret, frame = cap.read()
    if not ret:
        break
        
    frame = cv2.flip(frame, 1)
        
    if np.random.rand() < 0.03: 
        asteroids.append(Asteroid(screen_width))
        
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY_INV)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    cx, cy = -1, -1
    if contours:
        biggest_contour = max(contours, key=cv2.contourArea)
        cv2.drawContours(frame, [biggest_contour], -1, (0, 255, 0), 2)
        
        if cv2.contourArea(biggest_contour) > 500:
            M = cv2.moments(biggest_contour)
            if M["m00"] != 0:
                cx = int(M["m10"] / M["m00"])
                cy = int(M["m01"] / M["m00"])
                
                cv2.circle(frame, (cx, cy), 25, (255, 0, 0), -1) 
            
    for ast in asteroids[:]:
        ast.move()
        ast.draw(frame)
        
        if cx != -1 and cy != -1:
            dist = np.sqrt((ast.x - cx)**2 + (ast.y - cy)**2)
            # if dist < ast.radius + 25: 
            if dist < ast.radius: 
                asteroids.remove(ast)
                score += 1
                continue
                
        if ast.y > screen_height:
            asteroids.remove(ast)

    cv2.putText(frame, f"Score: {score}", (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 3)
    
    cv2.imshow('Complete System', frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()