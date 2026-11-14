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

if __name__ == "__main__":
    screen_w, screen_h = 500, 500
    
    ast = Asteroid(screen_w)
    
    while True:
        frame = np.zeros((screen_h, screen_w, 3), dtype=np.uint8)
        
        ast.move()
        ast.draw(frame)
        
        if ast.y > screen_h:
            ast = Asteroid(screen_w)
            
        cv2.imshow('Asteroid Logic Demo', frame)
        
        if cv2.waitKey(30) & 0xFF == ord('q'):
            break
            
    cv2.destroyAllWindows()
