import pyautogui as mc
import time
import sys

print('Move mouse to x input (you have 5 seconds)')  # Getting the x input coordinates
for i in range(5, 0, -1):
    sys.stdout.write(str(i)+' ')
    sys.stdout.flush()
    time.sleep(1)
xInput = mc.position()
xInputx = xInput.x
xInputy = xInput.y
print('\n')

print('X input coordinates')
print('X:' + '{0:5d}'.format(xInputx) + ', Y:' + '{0:5d}'.format(xInputy) + '\n')

print('Move mouse to y input (you have 5 seconds)')  # Getting the y input coordinates
for i in range(5, 0, -1):
    sys.stdout.write(str(i)+' ')
    sys.stdout.flush()
    time.sleep(1)
yInput = mc.position()
yInputx = yInput.x
yInputy = yInput.y
print('\n')

print('Y input coordinates')
print('X:' + '{0:5d}'.format(yInputx) + ', Y:' + '{0:5d}'.format(yInputy))

# time.sleep(5)
#
# mc.moveTo(xInputx, xInputy, 2)
# mc.click()
#
# mc.moveTo(yInputx, yInputy, 2)
# mc.click()
#
# mc.typewrite('facebook.com')
# mc.press('enter')
