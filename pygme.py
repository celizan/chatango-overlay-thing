import pygame
import win32api
import win32con
import win32gui
import ch
import tkinter as tk
import multiprocessing
import time
import html

pygame.init()
pygame.font.init()
myfont = pygame.font.SysFont('Arial Bold', 50)
pygame.display.set_caption('ghetto ass overlay')
global chatcount
global chatstore
chatstore = ["apple", "banana", "cherry", "other thing"]
chatcount = 0 #message counter 

screen = pygame.display.set_mode((800, 600)) # For borderless, use pygame.NOFRAME
done = False
fuchsia = (255, 0, 128)  # Transparency color
dark_red = (139, 0, 0)
screen.fill(fuchsia)  # Transparent background

# Create layered window
hwnd = pygame.display.get_wm_info()["window"]
win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE,
                       win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE) | win32con.WS_EX_LAYERED)
# Set window transparency color
win32gui.SetLayeredWindowAttributes(hwnd, win32api.RGB(*fuchsia), 0, win32con.LWA_COLORKEY)
win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 600, 300, 0, 0, win32con.SWP_NOSIZE)

class bot(ch.RoomManager):
   def onMessage(self, room, user, message):
     global chatcount
     global chatstore 
     ctext = "{0}: {1}".format(user.name.title(), message.body)
     #shift everything in chat table to make room for new message   
     print(ctext)
     chatstore[0] = chatstore[1]
     chatstore[1] = chatstore[2]
     chatstore[2] = chatstore[3]
     chatstore[3] = ctext
             
     screen.fill(fuchsia)
     x = 0
     #draw everything in chat table
     while x < 4:
      print(x)
      textsurface = myfont.render(html.unescape(chatstore[x]), False, (0, 255, 0))
      screen.blit(textsurface,(0, 50*x))
      pygame.display.update()
      x = x +1

   #every bot tick update the GUI
   def _tick(self):
    now = time.time()
    for task in set(self._tasks):
      if task.target <= now:
        task.func(*task.args, **task.kw)
        if task.isInterval:
          task.target = now + task.timeout
        else:
          self._tasks.remove(task)
    pygame.display.update()
    pygame.event.get()
   
    

   
rooms = ["vidyatendency"]
username = "botstero"
password = "123qwe"
bot.easy_start(rooms,username,password)
