from ursina import *
import random as r
from live_commands import *
import threading

#EMOTVI API SETUP
your_client_id = 'IgoNF2VyyqPkJ0nWqwir7slED8egiMs3H8RuznIo'
your_app_client_secret = '8nb3aqcFd0ZwUcLHNPI6JcUP3M2kIsuO8TIu0FscLXoZecmzKGvZ292ZPJmj68COg1PQhcXvugbrJ9pCRcDZy0x6h253rCb3t0J0x0OWj2Dmky6wgzXvQ0ImrnjtYVVH'

l = LiveCommand(your_client_id, your_app_client_secret)

trained_profile_name = 'Alvaro'

#GAME CODE
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
  global points, start, jump, l, dino

  points += 1
  label.text = f'Points: {points} Dino Y: {dino.y} Jump: {jump} Command: {l.currentCommand}'
  for ground in pair:
    ground.x -= 6*time.dt
    if ground.x < -35:
      ground.x += 100
  for c in cacti:
    c.x -= 6*time.dt
  if dino.intersects().hit:
    dino.texture= 'assets\hit'
    application.pause()
    l.c.close()


sound = Audio(
  'assets\\beep',
  autoplay=False
)


def input(key):
  if key == 'space':
    if dino.y < 0.01:
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

camera.orthographic = True
camera.fov = 10

#RUNNING THE 2 PROGRAMS
def runGame():
  print("Starting game")
  app.run()

def runAPI():
  print("Starting API")
  global l, trained_profile_name
  l.start(trained_profile_name)

t = threading.Thread(target=runAPI)
t.start()
runGame()
