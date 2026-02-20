import json, os, random, time
from typing import List, Optional
from dataclasses import dataclass, field
from enum import Enum
import sys

sys.path.append('extension/default')
sys.path.append('src/function')

from Player import Player
from battle import Battle

# Game Main Loop
class Game:
    def __init__(self):
        self.player = None
        self.running = True
    
    def main_menu(self):
        """Hiển thị menu chính"""
        print("\n" + "="*60)
        print("🎮 TURN-BASED MONSTER BATTLE GAME 🎮")
        print("="*60)
        print("1. New Game")
        print("2. Load Game")
        print("3. Exit")
        
        choice = input("Enter your choice (1-3): ").strip()
        return choice
    
    def new_game(self):
        """Tạo game mới"""
        print("\n" + "="*60)
        print("📝 NEW GAME")
        print("="*60)
        
        name = input("Enter your character name: ").strip()
        if not name:
            name = "Hero"
        
        self.player = Player(
            name=name,
            health=100,
            atk=20,
            defense=10,
            coins=250,
            effect=None
        )
        
        print(f"\nWelcome, {self.player.name}!")
        print("Your adventure begins...")
        self.player.save()
        self.game_loop()
    
    def load_game(self):
        """Tải game đã lưu"""
        print("\n" + "="*60)
        print("📂 LOAD GAME")
        print("="*60)
        
        name = input("Enter your character name: ").strip()
        if not name:
            print("Name cannot be empty!")
            return
        
        try:
            self.player = Player.load(name)
            print(f"Welcome back, {self.player.name}!")
            self.player.display_info()
            self.game_loop()
        except FileNotFoundError:
            print(f"No save file found for player '{name}'.")
        except Exception as e:
            print(f"Error loading game: {e}")
    
    def game_loop(self):
        """Game loop chính"""
        while self.running and self.player.is_alive():
            print("\n" + "="*60)
            print(f"📍 Adventure Menu - HP: {self.player.health}/{100}")
            print("="*60)
            print("1. Explore (Fight Monsters)")
            print("2. View Status")
            print("3. Rest (Restore HP)")
            print("4. Save & Quit")
            
            choice = input("Enter your choice (1-4): ").strip()
            
            if choice == "1":
                self.explore()
            elif choice == "2":
                self.view_status()
            elif choice == "3":
                self.rest()
            elif choice == "4":
                self.save_and_quit()
                break
            else:
                print("Invalid choice! Try again.")
        
        if not self.player.is_alive():
            print(f"\n💀 {self.player.name} has been defeated...")
            print("GAME OVER")
    
    def explore(self):
        """Khám phá và gặp quái vật"""
        print("\n🗺️  You venture into the wilderness...")
        time.sleep(1)
        
        battle = Battle(self.player)
        battle.start_battle()
        
        if not self.player.is_alive():
            print("\nGame Over! Your adventure ends here.")
    
    def view_status(self):
        """Xem thông tin nhân vật"""
        print("\n" + "="*60)
        print("📊 CHARACTER STATUS")
        print("="*60)
        self.player.display_info()
    
    def rest(self):
        """Nghỉ ngơi để hồi máu"""
        if self.player.coins < 50:
            print("\n❌ Not enough coins to rest! (Need 50 coins)")
            return
        
        print("\n😴 You rest at an inn...")
        self.player.coins -= 50
        heal_amount = 30
        self.player.health = min(self.player.health + heal_amount, 100)
        print(f"✨ Restored {heal_amount} HP! Current HP: {self.player.health}")
        print(f"💰 Spent 50 coins. Remaining: {self.player.coins}")
    
    def save_and_quit(self):
        """Lưu và thoát game"""
        print("\n💾 Saving game...")
        self.player.save()
        print("Game saved! Thank you for playing!")
        self.running = False

def main():
    game = Game()
    
    while True:
        choice = game.main_menu()
        
        if choice == "1":
            game.new_game()
        elif choice == "2":
            game.load_game()
        elif choice == "3":
            print("Thanks for playing! Goodbye!")
            break
        else:
            print("Invalid choice! Please try again.")

if __name__ == "__main__":
    main()