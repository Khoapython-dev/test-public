# module này sẽ chứa các hàm liên quan đến chiến đấu giữa người chơi và quái vật
# phát triển bởi KHoapython-dev

import sys
import random
import time
sys.path.append('extension/default')
sys.path.append('src/function')

from Player import Player
from find_monster import encounter_monster
from Monster import Monster

# Hệ thống turn-based battle
class Battle:
    def __init__(self, player: Player):
        self.player = player
        self.monster = None
        self.turn = 0
        self.player_defended = False
        self.monster_defended = False
    
    def start_battle(self):
        """Bắt đầu trận chiến"""
        have, monster_type = encounter_monster()
        if not have:
            return False
        
        # Tạo quái vật
        monster_name = monster_type.capitalize()
        self.monster = Monster(monster_name, monster_type)
        
        print("\n" + "="*60)
        print(f"🔥 You encountered a {monster_name}! 🔥")
        print("="*60)
        time.sleep(1)
        
        self.display_battle_info()
        
        # Vòng lặp chiến đấu
        while self.player.is_alive() and self.monster.is_alive():
            self.turn += 1
            self.player_defended = False
            self.monster_defended = False
            
            print(f"\n--- TURN {self.turn} ---")
            
            # Lượt người chơi
            self.player_turn()
            
            if not self.monster.is_alive():
                self.player_wins()
                return True
            
            time.sleep(1)
            
            # Lượt quái vật
            self.monster_turn()
            
            if not self.player.is_alive():
                self.player_loses()
                return False
            
            time.sleep(1)
        
        return False
    
    def display_battle_info(self):
        """Hiển thị thông tin trận đấu"""
        print(f"\nPlayer: HP={self.player.health} | ATK={self.player.atk} | DEF={self.player.defense}")
        print(f"Monster: HP={self.monster.get_hp()}")
    
    def player_turn(self):
        """Lượt hành động của người chơi"""
        print(f"\n[Player HP: {self.player.health}]")
        print(f"[Monster HP: {self.monster.get_hp()}]")
        
        while True:
            print("\nWhat do you do?")
            print("1. ⚔️  Attack")
            print("2. 🛡️  Defend")
            print("3. ⏭️  Skip")
            print("4. 📋 Info")
            
            choice = input("Enter your choice (1-4): ").strip()
            
            if choice == "1":
                self.player_attack()
                break
            elif choice == "2":
                self.player_defend()
                break
            elif choice == "3":
                self.player_skip()
                break
            elif choice == "4":
                self.display_battle_info()
                continue
            else:
                print("Invalid choice! Please try again.")
                continue
    
    def player_attack(self):
        """Người chơi tấn công"""
        damage = self.player.atk + random.randint(-5, 15)
        damage = max(1, damage)  # Damage tối thiểu là 1
        
        actual_damage = self.monster.take_damage(damage)
        print(f"⚔️  You attack for {actual_damage} damage!")
    
    def player_defend(self):
        """Người chơi phòng thủ"""
        self.player_defended = True
        print(f"🛡️  You take a defensive stance! (Defense +50% for this turn)")
    
    def player_skip(self):
        """Người chơi bỏ qua lượt"""
        print(f"⏭️  You skip your turn.")
    
    def monster_turn(self):
        """Lượt hành động của quái vật"""
        actions = ["attack", "defend", "skip"]
        weights = [60, 25, 15]  # AI: 60% tấn công, 25% phòng thủ, 15% bỏ qua
        
        action = random.choices(actions, weights=weights)[0]
        
        if action == "attack":
            self.monster_attack()
        elif action == "defend":
            self.monster_defend()
        else:
            self.monster_skip()
    
    def monster_attack(self):
        """Quái vật tấn công"""
        monster_damage = self.monster.attack()
        
        # Tính toán damage thực tế
        if self.player_defended:
            actual_damage = max(1, monster_damage - self.player.defense - 20)
            print(f"🔴 {self.monster.name} attacks for {monster_damage} damage, but your defense blocks {self.player.defense + 20}!")
            print(f"💔 You take {actual_damage} damage!")
        else:
            actual_damage = max(1, monster_damage - self.player.defense)
            print(f"🔴 {self.monster.name} attacks for {actual_damage} damage!")
        
        self.player.take_damage(actual_damage)
    
    def monster_defend(self):
        """Quái vật phòng thủ"""
        self.monster_defended = True
        print(f"🛡️  {self.monster.name} takes a defensive stance!")
    
    def monster_skip(self):
        """Quái vật bỏ qua lượt"""
        print(f"⏭️  {self.monster.name} skips their turn.")
    
    def player_wins(self):
        """Người chơi thắng"""
        print("\n" + "="*60)
        print("🏆 VICTORY! 🏆")
        print("="*60)
        reward = self.monster.get_max_hp_reward()
        self.player.earn_coins(reward)
        print(f"You defeated {self.monster.name}!")
        print(f"💰 Earned {reward} coins!")
        print(f"Total coins: {self.player.coins}")
    
    def player_loses(self):
        """Người chơi thua"""
        print("\n" + "="*60)
        print("💀 YOU HAVE BEEN DEFEATED! 💀")
        print("="*60)
        print(f"{self.monster.name} dealt the final blow...")
        
    
    