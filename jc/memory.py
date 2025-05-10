from pymem import Pymem
from pymem.process import module_from_name
import time 

class MemoryAccess:
    def __init__(self, pid, offsets):
        self.offsets = offsets
        
        self.pm = Pymem()
        self.pm.open_process_from_id(pid)
        self.client = module_from_name(self.pm.process_handle, "client.dll").lpBaseOfDll
        self.hw = module_from_name(self.pm.process_handle, "hw.dll").lpBaseOfDll
        self.entities_list_full = self.get_entity()
        
    def get_entity(self):
        players = []
        for i in range(0, 256):
            player_offset = i * 0x250



            player = {
                "name" : self.pm.read_string(self.hw + self.offsets["m_dwEntityOrigin"] + player_offset),
                "x" : self.pm.read_float(self.hw + self.offsets["m_dwEntityOrigin"] + 0x84 + player_offset),
                "z" : self.pm.read_float(self.hw + self.offsets["m_dwEntityOrigin"] + 0x88 + player_offset),
                "y" : self.pm.read_float(self.hw + self.offsets["m_dwEntityOrigin"] + 0x8C + player_offset),
                "timer" : self.pm.read_float(self.hw + self.offsets["m_dwEntityOrigin"] + 0x7C + player_offset)

            }
            if not player["name"] == '':
                players.append(player)
        return players

    def remove_inactive(self, first_read, second_read):
        final = []
        for i in range(0, len(second_read)):
            try:
                if not first_read[i]["timer"] == second_read[i]["timer"]:
                    final.append(second_read[i])
            except:
                pass
        return final




    def update(self):
        self.local_player_pitch = self.pm.read_float(self.hw + self.offsets["m_dwViewAngles"])
        self.local_player_yaw = self.pm.read_float(self.hw + self.offsets["m_dwViewAngles"] + 0x4)
        self.local_player_x = self.pm.read_float(self.client + self.offsets["m_dwLocalOrigin"])
        self.local_player_z = self.pm.read_float(self.client + self.offsets["m_dwLocalOrigin"] + 0x4)
        self.local_player_y = self.pm.read_float(self.client + self.offsets["m_dwLocalOrigin"] + 0x8)
        self.local_player_fov_scale = self.pm.read_float(self.hw + self.offsets["m_dwFovScale1"])
        ent = self.get_entity()
        self.entities_list = self.remove_inactive(self.entities_list_full, ent)
        self.entities_list_full = ent
        

        
        
        



        
        


    