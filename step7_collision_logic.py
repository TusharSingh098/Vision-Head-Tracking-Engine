import cv2
import numpy as np
import random
import time


def has_collision(ship_x, ship_y, ship_w, ship_h, asteroid_x, asteroid_y, asteroid_w, asteroid_h):

    padding = 0.1

    ship_left = ship_x + int(ship_w * padding)
    ship_right = ship_x + ship_w - int(ship_w * padding)
    ship_top = ship_y + int(ship_h * padding)
    ship_bottom = ship_y + ship_h - int(ship_h * padding)

    asteroid_left = asteroid_x + int(asteroid_w * padding)
    asteroid_right = asteroid_x + asteroid_w - int(asteroid_w * padding)
    asteroid_top = asteroid_y + int(asteroid_h * padding)
    asteroid_bottom = asteroid_y + asteroid_h - int(asteroid_h * padding)

    return (
        ship_left < asteroid_right and
        ship_right > asteroid_left and
        ship_top < asteroid_bottom and
        ship_bottom > asteroid_top
    )

def make_asteroids(width, count):

    return [
        [random.randint(0, max(1, width - 40)), random.randint(-500, -50)]
        for _ in range(count)
    ]

cap = cv2.VideoCapture(0)
screen_width = 640

asteroids = make_asteroids(screen_width, 3)
speed = 5

while True:
    ret, frame = cap.read()
    if not ret: break
    frame = cv2.flip(frame, 1)
    
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, np.array([0, 0, 0]), np.array([179, 120, 100])) 
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    center_x = screen_width // 2
    if contours:
        biggest = max(contours, key=cv2.contourArea)
        cv2.drawContours(frame, [biggest], -1, (0, 255, 0), 2)
        if cv2.contourArea(biggest) > 1000:
            moments = cv2.moments(biggest)
            if moments["m00"] != 0:
                center_x = int(moments["m10"] / moments["m00"])
    
    ship_w, ship_h = 50, 50
    ship_x = max(0, min(screen_width - ship_w, center_x - ship_w // 2))
    ship_y = frame.shape[0] - ship_h - 20
    
    cv2.rectangle(frame, (ship_x, ship_y), (ship_x + ship_w, ship_y + ship_h), (255, 0, 0), -1)

    ast_w, ast_h = 40, 40

    for ast in asteroids:
        ast[1] += speed
        
        cv2.rectangle(frame, (ast[0], ast[1]), (ast[0] + ast_w, ast[1] + ast_h), (0, 0, 255), -1)
        
        if has_collision(ship_x, ship_y, ship_w, ship_h, ast[0], ast[1], ast_w, ast_h):
            print("HIT!")
            
        if ast[1] > frame.shape[0]:
            ast[0] = random.randint(0, screen_width - ast_w)
            ast[1] = random.randint(-300, -50)

    cv2.imshow("Collision Detection", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
