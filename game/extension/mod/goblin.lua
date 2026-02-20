-- file riêng cho quái vật

Goblin = {}
Goblin.__index = Goblin

function Goblin:structINIT(name)
    local obj = {
        name = name,
        hp = 120,
        atk = math.random(15, 35),
        def = math.random(5, 15)
    }
    setmetatable(obj, self)
    return obj
end

-- Factory function để tạo Goblin
function Goblin.new(name)
    return Goblin:structINIT(name)
end

-- Methods
function Goblin:attack()
    return math.random(self.atk - 5, self.atk + 5)
end

function Goblin:take_damage(damage)
    local actual_damage = math.max(0, damage - self.def)
    self.hp = self.hp - actual_damage
    return actual_damage 
end

function Goblin:is_alive()
    return self.hp > 0
end

function Goblin:display_status()
    print(self.name .. " - HP: " .. self.hp .. ", ATK: " .. self.atk .. ", DEF: " .. self.def)
end 

-- Helper functions cho Python interop
function goblin_attack(monster)
    return Goblin.attack(monster)
end

function goblin_take_damage(monster, damage)
    return Goblin.take_damage(monster, damage)
end

function goblin_is_alive(monster)
    return Goblin.is_alive(monster)
end

function goblin_display_status(monster)
    return Goblin.display_status(monster)
end




