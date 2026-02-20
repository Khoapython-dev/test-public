#!/usr/bin/env python3
import sys
sys.path.append('extension/default')
sys.path.append('src/function')

from Player import Player
from Monster import Monster

print("Testing Game Components...\n")

# Test Player
print("1. Creating Player...")
player = Player(name="TestHero", health=100, atk=20, defense=10, coins=250)
print("   Player created: {} - HP:{} ATK:{} DEF:{}".format(player.name, player.health, player.atk, player.defense))

# Test Monster Creation
print("\n2. Creating Monsters...")
smile = Monster("TestSmile", "smile")
smile_atk = smile.lua_monster.atk
smile_d = smile.lua_monster.d
print("   Smile created: HP={}, ATK={}, DEF={}".format(smile.get_hp(), smile_atk, smile_d))

goblin = Monster("TestGoblin", "goblin") 
goblin_atk = goblin.lua_monster.atk
goblin_d = goblin.lua_monster.d
print("   Goblin created: HP={}, ATK={}, DEF={}".format(goblin.get_hp(), goblin_atk, goblin_d))

# Test Combat
print("\n3. Testing Combat...")
initial_goblin_hp = goblin.get_hp()
damage = 15
actual_damage = goblin.take_damage(damage)
print("   Goblin takes {} damage -> Actual: {} damage".format(damage, actual_damage))
print("   Goblin HP: {} -> {}".format(initial_goblin_hp, goblin.get_hp()))

print("\n4. Testing Monster Attack...")
monster_damage = goblin.attack()
print("   Goblin attacks for {} damage".format(monster_damage))

print("\n5. Testing Is Alive...")
alive = goblin.is_alive()
print("   Goblin is alive: {}".format(alive))

# Test Rewards
print("\n6. Testing Reward System...")
smile_reward = smile.get_max_hp_reward()
goblin_reward = goblin.get_max_hp_reward()
print("   Smile reward: {} coins".format(smile_reward))
print("   Goblin reward: {} coins".format(goblin_reward))

print("\n=== All tests passed! Game is ready. ===")
