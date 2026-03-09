import os

import circle
import square

radius = float(os.getenv("r", 3))
side = float(os.getenv("a", 5))

print(f"--- Результаты вычислений ---")
print(f"Круг (r={radius}): площадь = {circle.area(radius)}")
print(f"Квадрат (a={side}): площадь = {square.area(side)}")
