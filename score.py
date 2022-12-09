import math
import components as com


class Score:
    def __init__(self, height_top=100, xy_speed=20):
        self.pi = math.pi * 2
        self.dist = 0
        self.level = 0
        self.point = 0
        self.color_bg = com.BLUE
        self.height_top = height_top
        self.height_now = height_top
        self.x_speed = 0
        self.y_speed = 0
        self.xy_speed = xy_speed
        self.speed_planer = 0
        self.mouse_y = 0


    def update_dist(self, rate=0.2):
        self.dist += self.x_speed * rate
        self.level = int(self.dist // 1000) + 1

    def update_speed_planer(self):
        self.speed_planer = int((self.x_speed ** 2 + self.y_speed ** 2) ** 0.5 * 6.6)

    def update_point(self, size=1):
        self.point += size

    def update_height(self, rate=1):
        self.height_now += self.y_speed * rate

    def update_xy_speed_real(self, h):
        x_plain = self.xy_speed ** 2 * 0.000009
        if self.xy_speed < 4:  # Cваливание
            if self.y_speed < -5:
                rot_speed = 0.007
                self.pi -= rot_speed * math.pi
                self.y_speed -= 0.1
                self.x_speed = self.x_speed * math.cos(self.pi)
                if int(math.degrees(self.pi)) < -40:
                    self.pi = math.radians(320)
                    self.xy_speed = abs(self.y_speed) + 1
            else:
                self.y_speed -= 0.1
        else:
            if self.mouse_y > h // 2:  # Мышка в НИЖНЕЙ половине экрана
                rot_speed = self.xy_speed * (self.mouse_y - h / 2) / (h / 2) * 0.0004
                self.pi += rot_speed * math.pi
                self.y_speed = self.xy_speed * math.sin(self.pi)
                self.x_speed = self.xy_speed * math.cos(self.pi)
            if self.mouse_y < h // 2:  # Мышка в ВЕРХНЕЙ половине экрана
                rot_speed = self.xy_speed * (((h / 2) - self.mouse_y) / (h / 2)) * 0.0002
                self.pi -= rot_speed * math.pi
                self.y_speed = self.xy_speed * math.sin(self.pi)
                self.x_speed = self.xy_speed * math.cos(self.pi)

            if 0 <= math.degrees(self.pi) <= 180:
                degree = math.degrees(self.pi)
                corn = degree / 90 if degree <= 90 else (180 - degree) / 90
                self.xy_speed -= corn * 0.3 + x_plain
            if 180 < math.degrees(self.pi) <= 360:
                degree = math.degrees(self.pi)
                corn = degree / 270 if degree <= 270 else (360 - degree) / 270
                self.xy_speed += corn * 0.3 - x_plain
            if self.pi <= 0:
                self.pi = math.pi * 2
            elif self.pi >= math.pi * 2:
                self.pi = 0

    def update_xy_speed_easy(self, h):
        try:
            self.pi = (math.atan(self.y_speed/self.x_speed))
        except ZeroDivisionError:
            self.pi = -math.pi // 2 if self.y_speed < 0 else math.pi // 2
        x_plain = self.xy_speed ** 2 * 0.00001
        xy_speed_top = (self.mouse_y - h / 2) / (h / 2) * 0.07
        xy_speed_down = (((h / 2) - self.mouse_y) / (h / 2)) * 0.07
        y_speed_top = -((self.mouse_y - h / 2) / (h / 2) * self.xy_speed) + 1
        y_speed_down = ((((h / 2) - self.mouse_y) / (h / 2)) * self.xy_speed) - 1
        x_speed = (1 - abs(self.y_speed) / self.xy_speed) * self.xy_speed
        d_turb = 0.01 * self.xy_speed
        c_turb = 0.01 * self.xy_speed

        if self.xy_speed <= 3:
            if self.y_speed < -5 and self.mouse_y > h / 2:
                self.xy_speed = abs(self.y_speed)
            elif self.y_speed > -5:
                self.y_speed -= 0.07
                self.x_speed += 0.001
        else:
            if self.mouse_y > h / 2:  # Угол атаки -
                if self.y_speed < 0:  # Когда самолет литит вниз
                    if 0 < self.xy_speed: self.xy_speed += xy_speed_top - x_plain
                if self.y_speed >= 0:  # Когда самолет летит вверх
                    self.xy_speed -= xy_speed_top + x_plain
                if y_speed_top < self.y_speed: self.y_speed -= d_turb
                elif y_speed_top >= self.y_speed: self.y_speed += d_turb
                self.x_speed = x_speed
            if self.mouse_y <= h / 2:  # Угол атаки +
                if self.y_speed <= 0:  # Когда самолет литит вниз
                    if 0 < self.xy_speed: self.xy_speed += xy_speed_down - x_plain
                if self.y_speed > 0:  # Когда самолет летит вверх
                    if self.xy_speed > 3: self.xy_speed -= xy_speed_down + x_plain
                if y_speed_down > self.y_speed: self.y_speed += c_turb
                elif y_speed_down < self.y_speed: self.y_speed -= c_turb
                self.x_speed = x_speed

    def update_mouse_y(self, pos):
        self.mouse_y = pos

    def update_mod(self, mod):
        self.mod = mod

    def update_status(self, status):
        self.status = status
