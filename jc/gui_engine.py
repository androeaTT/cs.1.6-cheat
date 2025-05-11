import pygame
import win32gui
import win32con
import pygetwindow as gw
import win32process

class mainWindow:
    def __init__(self):
        pygame.init()
        self.cs_title = "Counter-Strike"
        self.main_list = pygame.sprite.Group()
        self.esp_list = pygame.sprite.Group()
        self.Screen = pygame.display.set_mode((100, 100), pygame.NOFRAME | pygame.SRCALPHA | pygame.HWSURFACE)
        self.Screen, self.Width, self.Height = self.__set_window_transparent(self.__get_pygame_hwnd(), self.get_target_window())
    
    def update(self):
        self.Screen = self.__update_position(self.__get_pygame_hwnd(), self.Screen, self.get_target_window())
        self.Screen.fill((0, 0, 0, 0))
        self.main_list.draw(self.Screen)
        self.esp_list.draw(self.Screen)
        pygame.display.flip()

    def get_pid(self):
        window = gw.getWindowsWithTitle(self.cs_title)[0]
        hwnd = window._hWnd  
        _, pid = win32process.GetWindowThreadProcessId(hwnd) 
        return pid

    def get_target_window(self):
        window = gw.getWindowsWithTitle(self.cs_title)[0]
        return window
    
    def __get_pygame_hwnd(self):
        hwnd = pygame.display.get_wm_info()['window']
        return hwnd
    def get_sizes(self, target_window):
        left, top, right, bottom = target_window.left, target_window.top, target_window.right, target_window.bottom
        width = right - left
        height = bottom - top
        return (width, height, left, top)

    def __set_window_transparent(self, hwnd, target_window):
        width, height, left, top = self.get_sizes(target_window)
        screen = pygame.display.set_mode((width, height), pygame.NOFRAME | pygame.SRCALPHA | pygame.HWSURFACE)
        win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, left, top, width, height, 0)
        ex_style = win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)
        win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE, ex_style | win32con.WS_EX_LAYERED | win32con.WS_EX_TRANSPARENT)
        win32gui.SetLayeredWindowAttributes(hwnd, 0, 0, win32con.LWA_COLORKEY)
        return screen, width, height
    
    def __update_position(self, hwnd, screen, target_window):
        left, top, right, bottom = target_window.left, target_window.top, target_window.right, target_window.bottom
        width = right - left
        height = bottom - top
        if screen.get_width() != width or screen.get_height() != height:
            screen = pygame.display.set_mode((width, height), pygame.NOFRAME | pygame.SRCALPHA | pygame.HWSURFACE)
        win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, left, top, width, height, 0)
        return screen