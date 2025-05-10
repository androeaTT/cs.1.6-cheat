import pygame
import time
import math
import os
import keyboard
from jc.gui_engine import mainWindow
from jc.sprites.menu import MenuSprite
from jc.memory import MemoryAccess
from jc.sprites.esp_border import EspBorder

offsets_config = {
    "m_dwEntityOrigin" : 0x120471C,
    "m_dwViewAngles" : 0x108AE94,
    "m_dwLocalOrigin" : 0x13E7F0,
    "m_dwFovScale1" : 0xEC9E20
}
player_fov = 100

window = mainWindow()

mem = MemoryAccess(
    offsets = offsets_config,
    pid = window.get_pid()
)


ms = MenuSprite()

clock = pygame.time.Clock()

keys_config = {
    "OpenMenu" : "INSERT"
}
def check_key(action):
    if action in keys_config:
        if keyboard.is_pressed(keys_config[action]):
            while keyboard.is_pressed(keys_config[action]):
                pass
            return True
        return False
    else:
        if keyboard.is_pressed(action):
            while keyboard.is_pressed(action):
                pass
            return True
        return False



import math

def world_to_screen(px, py, pz, yaw, pitch, ox, oy, oz, screen_width, screen_height, fov = 100):
    yaw = math.radians(yaw)
    pitch = math.radians(pitch)
    fov = math.radians(fov)
    
    dx = ox - px
    dy = oy - py
    dz = oz - pz
    
    distance = math.sqrt(dx**2 + dy**2 + dz**2)
    
    cos_yaw = math.cos(yaw)
    sin_yaw = math.sin(yaw)
    
    cos_pitch = math.cos(pitch)
    sin_pitch = math.sin(pitch)
    
    rot_x = dx * cos_yaw + dz * sin_yaw
    rot_z = -dx * sin_yaw + dz * cos_yaw
    
    rot_y = dy * cos_pitch - rot_z * sin_pitch
    rot_z = dy * sin_pitch + rot_z * cos_pitch
    
    if rot_z <= 0:
        return None, None, distance  # Объект за игроком, не отображаем
    
    fov_scale = 1 / math.tan(fov / 2)
    
    screen_x = (rot_x / rot_z) * fov_scale
    screen_y = (rot_y / rot_z) * fov_scale
    
    pixel_x = (screen_width / 2) * (1 + screen_x)
    pixel_y = (screen_height / 2) * (1 - screen_y)
    
    if 0 <= pixel_x <= screen_width and 0 <= pixel_y <= screen_height:
        return pixel_x, pixel_y, distance
    else:
        return None, None, distance 

while True:
    clock.tick(60)
    timedump = time.time()
    mem.update()
    window.esp_list = pygame.sprite.Group()
    width, height, left, top = window.get_sizes(window.get_target_window())
    for entity in mem.entities_list:
        boxpos = world_to_screen(
            mem.local_player_x,
            mem.local_player_y, 
            mem.local_player_z,
            mem.local_player_yaw + 270, 
            (0 - mem.local_player_pitch) * 1.5,
            entity["x"],
            entity["y"], 
            entity["z"],
            width, 
            height,
            fov = player_fov / (mem.local_player_fov_scale + 0.161) 
        )
        if boxpos == None:
            continue
        x, y, distance = boxpos
        if x != None and y != None:
            sprite = EspBorder(x,y, distance)
            window.esp_list.add(sprite)

    

    
    time.sleep(time.time() - timedump - 0.016)
    window.update()