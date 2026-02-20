-- file riêng cho các quái vật

Smile = {}
Smile.__index = Smile

function Smile:structINIT(name)
    local obj = {
        name = name,
        hp = 100,
        atk = math.random(10, 25),
        def = math.random(3, 12)
    }
    setmetatable(obj, self)
    return obj
end

-- Factory function để tạo Smile
function Smile.new(name)
    return Smile:structINIT(name)
end

-- Methods
function Smile:attack()
    return math.random(self.atk - 5, self.atk + 5)
end

function Smile:take_damage(damage)
    local actual_damage = math.max(0, damage - self.def)
    self.hp = self.hp - actual_damage
    return actual_damage 
end

function Smile:is_alive()
    return self.hp > 0
end

function Smile:display_status()
    print(self.name .. " - HP: " .. self.hp .. ", ATK: " .. self.atk .. ", DEF: " .. self.def)
end

-- Helper functions cho Python interop
function smile_attack(monster)
    return Smile.attack(monster)
end

function smile_take_damage(monster, damage)
    return Smile.take_damage(monster, damage)
end

function smile_is_alive(monster)
    return Smile.is_alive(monster)
end

function smile_display_status(monster)
    return Smile.display_status(monster)
end
