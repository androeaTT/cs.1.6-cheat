import pygame
import json



class MenuSprite(pygame.sprite.Sprite):
    def __init__(self, locale, sprite_list, x=0, y=0):
        super().__init__()
        self.__FONT_SIZE = 74
        self.__current_text = ""
        self.visible = False
        self.__current_menu_page = 0
        self.__main_list = sprite_list

        self.__locale_json = self.__get_locale(locale)
        strings = self.__locale_json["strings"]
        self.__menu_strings = [
            f"""
            {strings["mainMenuTitle"]}\r\n 
            {strings[f"mainMenuItem1"]}\r\n 
            {strings[f"mainMenuItem2"]}\r\n 
            {strings[f"mainMenuItem3"]}\r\n 
            {strings[f"mainMenuItem4"]}\r\n 
            {strings[f"mainMenuHint1"]}\r\n 
            {strings[f"mainMenuHint2"]}
            """
        ]

        self.x = x
        self.y = y
        self.font = pygame.font.Font("jc/assets/gui/minecraft.ttf", self.__FONT_SIZE)
        self.image = self.font.render(self.__current_text, True, (255, 255, 255))
        self.rect = self.image.get_rect(center=(self.x, self.y))

    def visible_toggle(self, state="nonchanged"):
        if state == "nonchanged":
            state = not state
        else:
            self.visible = state
        
        if self.visible:
            self.__main_list.add(self)
        else:
            self.__main_list.remove(self)


    def __get_locale(self, sysName):
        with open(f'jc/assets/strings/{sysName}.json') as file:
            return json.load(file)
            
    def set_menu_page(self, page):
        new_text = self.__menu_strings[page]

        self.image = self.font.render(new_text, True, (255, 255, 255))

        old_center = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = old_center

        self.__current_menu_page = page


    