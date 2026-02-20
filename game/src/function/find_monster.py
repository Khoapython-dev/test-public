# module này quyết định người chơi có gặp quái vật hay không khi di chuyển trên bản đồ dựa theo xắc suất

import sys
import random
sys.path.append('extension/default')
sys.path.append('src/function')


NNN = ['d', 'd', 'n', 'n', 'n', 'n', 'n', 'e', 'n', 'e']  # xác suất gặp quái vật mỗi lần di chuyển
LIST = ['smile', 'goblin']

# hàm quyết định xem người chơi có gặp quái vật hay không dựa trên xác suất trong NNN
def encounter_monster():
    if random.choice(NNN) in ['d', 'e']:  # nếu chọn phải 'd' hoặc 'e', người chơi sẽ gặp quái vật
        monster = random.choice(LIST)  # chọn ngẫu nhiên một loại quái vật từ LIST
        return True, monster
    return False, None  # nếu không gặp quái vật, trả về False và None
    
