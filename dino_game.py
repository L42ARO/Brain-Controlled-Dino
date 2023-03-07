from ursina import *
import random as r
from live_commands import *
import threading
import time

your_app_client_id = ''
your_app_client_secret = ''

    # Init live advance
l = LiveCommand(your_app_client_id, your_app_client_secret)

trained_profile_name = 'Neo' # Please set a trained profile name here




app = Ursina()
#window.fullscreen = True
window.color = color.white


dino = Animation('assets\dino',
                 collider='box',
                 x=-5)

ground1 = Entity(
  model='quad',
  texture='assets\ground',
  scale=(50,0.5,1),
  z=1
)
ground2 = duplicate(ground1, x=50)
pair = [ground1, ground2]



cactus = Entity(
  model='quad',
  texture='assets\cacti',
  x = 20,
  collider='box'
)
cacti = []
def newCactus():
  new = duplicate(cactus,
                  x=12+r.randint(0,5))
  cacti.append(new)
  invoke(newCactus, delay=2)

newCactus()



label = Text(
  text = f'Points: {0}',
  color=color.black,
  position=(-0.5, 0.4)
)
points = 0
start = 0
jump = False

def update():
  global points, l, start, dino, jump
  points += 1
  label.text = f'Command: {l.currentCommand} Dino Y: {dino.y} Points: {points} Jump: {jump}'
  for ground in pair:
    ground.x -= 4*time.dt
    if ground.x < -35:
      ground.x += 100
  for c in cacti:
    c.x -= 4*time.dt
  if dino.intersects().hit:
    dino.texture= 'assets\hit'
    application.pause()
    l.c.close()
  jumpCheck()

sound = Audio(
  'assets\\beep',
  autoplay=False
)


def jumpCheck():
  global l, jump #<--------
  if l.currentCommand == 'lift':#<--------
    if dino.y < 0.01 and jump == False: #<--------
      jump = True #<-----
      sound.play()
      dino.animate_y(
        2,
        duration=0.4,
        curve= curve.out_sine
      )
      dino.animate_y(
        0,
        duration=0.4,
        delay=0.4,
        curve = curve.in_sine
      )
  if jump==True and dino.y>1.9:
    jump=False

camera.orthographic = True
camera.fov = 10

def runGame():
    print("Running game")
    app.run()

def runAPI():
    global l, trained_profile_name
    print("Running API")
    l.start(trained_profile_name)

t = threading.Thread(target=runAPI)
t.start()
time.sleep(2)
runGame()