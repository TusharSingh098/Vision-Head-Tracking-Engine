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

def reset_game(width):
    return {
        "score": 0,
        "level": 1,
        "speed": 5,
        "start_time": time.time(),
        "game_over": False,
        "asteroids": make_asteroids(width, 3),
    }

def load_image(path, target_width):
    image = cv2.imread(path, cv2.IMREAD_UNCHANGED)
    height, width = image.shape[:2]
    new_height = max(1, int(target_width * height / width))
    return cv2.resize(image, (target_width, new_height))

def put_image(frame, image, x, y):
    image_h, image_w = image.shape[:2]
    x_int, y_int = int(x), int(y)

    x1, y1 = max(0, x_int), max(0, y_int)
    x2, y2 = min(frame.shape[1], x_int + image_w), min(frame.shape[0], y_int + image_h)

    if x1 >= x2 or y1 >= y2: return

    src_x1, src_y1 = max(0, -x_int), max(0, -y_int)
    src_x2, src_y2 = src_x1 + (x2 - x1), src_y1 + (y2 - y1)

    crop = image[src_y1:src_y2, src_x1:src_x2]
    if crop.size == 0: return

    if crop.shape[2] == 4:
        alpha = crop[:, :, 3:4] / 255.0
        frame[y1:y2, x1:x2] = (
            alpha * crop[:, :, :3] + (1 - alpha) * frame[y1:y2, x1:x2]
        ).astype(np.uint8)
    else:
        frame[y1:y2, x1:x2] = crop

SHUTTLE_WIDTH = 50
ASTEROID_WIDTH = 40
airplane = load_image("shuttle1.png", SHUTTLE_WIDTH)
asteroid = load_image("asteroid.png", ASTEROID_WIDTH)

cap = cv2.VideoCapture(0)
screen_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
screen_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
game = reset_game(screen_width)

while True:
    ret, frame = cap.read()
    if not ret: break
    frame = cv2.flip(frame, 1)

    # hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    # mask = cv2.inRange(hsv, np.array([0, 0, 0]), np.array([179, 120, 100]))
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
    _, thresh = cv2.threshold(gray, 80, 255, cv2.THRESH_BINARY_INV)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    center_x = screen_width // 2
    if contours:
        biggest = max(contours, key=cv2.contourArea)
        cv2.drawContours(frame, [biggest], -1, (0, 255, 0), 2)
        if cv2.contourArea(biggest) > 1000:
            moments = cv2.moments(biggest)
            if moments["m00"] != 0:
                center_x = int(moments["m10"] / moments["m00"])

    ship_w, ship_h = airplane.shape[1], airplane.shape[0]
    ship_x = max(0, min(screen_width - ship_w, center_x - ship_w // 2))
    ship_y = screen_height - ship_h - 20

    if not game["game_over"]:
        new_level = int((time.time() - game["start_time"]) // 10) + 1
        if new_level > game["level"]:
            game["level"] = new_level
            game["speed"] += 1
            game["asteroids"] += make_asteroids(screen_width, 2)

        for ast in game["asteroids"]:
            ast[1] += game["speed"]

            if has_collision(ship_x, ship_y, ship_w, ship_h, ast[0], ast[1], asteroid.shape[1], asteroid.shape[0]):
                game["game_over"] = True

            if ast[1] > screen_height:
                ast[0] = random.randint(0, screen_width - asteroid.shape[1])
                ast[1] = random.randint(-300, -50)
                game["score"] += 1

    put_image(frame, airplane, ship_x, ship_y)
    for ast in game["asteroids"]:
        put_image(frame, asteroid, ast[0], ast[1])

    cv2.putText(frame, f"Score: {game['score']}", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    cv2.putText(frame, f"Level: {game['level']}", (20, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

    if game["game_over"]:
        overlay = frame.copy()
        cv2.rectangle(overlay, (0, 0), (screen_width, screen_height), (0, 0, 0), -1)
        frame = cv2.addWeighted(overlay, 0.6, frame, 0.4, 0)
        cv2.putText(frame, "GAME OVER", (screen_width // 2 - 180, screen_height // 2), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 4)
        cv2.putText(frame, "Press R to Restart", (screen_width // 2 - 140, screen_height // 2 + 100), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

    cv2.imshow("Final Game with Images", frame)
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"): break
    if key == ord("r") and game["game_over"]:
        game = reset_game(screen_width)

cap.release()
cv2.destroyAllWindows()