# file cho các quái vật, dùng để interface với Lua monsters
# phát triển bởi KHoapython-dev

from lupa import LuaRuntime

lua = LuaRuntime(unpack_returned_tuples=True)

class Monster:
    """Wrapper class cho Lua monsters"""
    def __init__(self, name: str, monster_type: str):
        self.name = name
        self.monster_type = monster_type
        self.lua_monster = None
        self._init_lua_monster()
    
    def _init_lua_monster(self):
        """Khởi tạo Lua monster script"""
        try:
            monster_script = open(f"extension/mod/{self.monster_type}.lua", "r").read()
            lua.execute(monster_script)
            
            # Gọi hàm factory new() để tạo monster
            factory = lua.globals()[self.monster_type + "_create"] or lua.globals()[self.monster_type.capitalize()].new
            self.lua_monster = lua.globals()[self.monster_type.capitalize()].new(self.name)
        except FileNotFoundError:
            raise FileNotFoundError(f"Monster script for {self.monster_type} not found.")
    
    def attack(self) -> int:
        """Quái vật tấn công"""
        helper = lua.globals()[f"{self.monster_type}_attack"]
        return int(helper(self.lua_monster))
    
    def take_damage(self, damage: int) -> int:
        """Quái vật nhận damage"""
        helper = lua.globals()[f"{self.monster_type}_take_damage"]
        return int(helper(self.lua_monster, damage))
    
    def is_alive(self) -> bool:
        """Kiểm tra xem quái vật còn sống hay không"""
        helper = lua.globals()[f"{self.monster_type}_is_alive"]
        result = helper(self.lua_monster)
        return bool(result)
    
    def display_status(self):
        """Hiển thị trạng thái quái vật"""
        helper = lua.globals()[f"{self.monster_type}_display_status"]
        helper(self.lua_monster)
    
    def get_hp(self) -> int:
        """Lấy HP của quái vật"""
        return int(self.lua_monster.hp)
    
    def get_max_hp_reward(self) -> int:
        """Lấy số tiền thưởng khi đánh bại"""
        # Smile: 100 hp -> 150 coins, Goblin: 120 hp -> 200 coins
        if self.monster_type == "smile":
            return 150
        elif self.monster_type == "goblin":
            return 200
        return 100
