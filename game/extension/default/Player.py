# file cho người chơi, bao gồm các thuộc tính và phương thức liên quan đến người chơi
# phát triển bởi KHoapython-dev

from dataclasses import dataclass, field
from typing import List, Optional
import json, os, time, random

# định nghĩa class Player với các thuộc tính cơ bản như name, health, attack, defense, coins và effect
@dataclass
class Player:
    name: str
    health: int
    atk: int
    defense: int
    coins: int
    effect: Optional[str] = None

    # phương thức để hiển thị thông tin của người chơi
    def display_info(self):
        print(f"Name: {self.name}")
        print(f"Health: {self.health}")
        print(f"Attack: {self.atk}")
        print(f"Defense: {self.defense}")
        print(f"Coins: {self.coins}")
        if self.effect:
            print(f"Effect: {self.effect}")

    # chúng ta sẽ dùng các hàm như cách các hàm quái vật
    # hàm nhận damage từ quái vật, tính toán damage sau khi trừ defense và cập nhật lại health của người chơi
    def take_damage(self, damage: int):
        self.health -= damage
        if self.health < 0:
            self.health = 0
    
    # hàm tấn công quái vật, tính toán damage dựa trên attack của người chơi và có thể có bonus từ effect
    def attack(self, monster):
        damage = self.atk
        # nếu người chơi có effect tăng damage, chúng ta sẽ áp dụng bonus
        if self.effect == "Damage Bonus":
            damage += int(self.atk * 0.2)  # tăng 20% damage
        monster.take_damage(damage)
        return damage
    
    # hàm để kiếm tiền sau khi đánh bại quái vật, số tiền kiếm được có thể dựa trên level của quái vật
    def earn_coins(self, amount: int):
        self.coins += amount

    # hàm để xác định xem người chơi có còn sống hay không
    def is_alive(self):
        return self.health > 0
    
    ## lưu ý: các hàm dưới dòng comment này không được dùng để cho người chơi game
    # hàm để lưu trạng thái của người chơi vào file JSON
    def save(self):
        player_data = {
            "name": self.name,
            "health": self.health,
            "attack": self.atk,
            "defense": self.defense,
            "coins": self.coins,
            "effect": self.effect
        }
        with open(f"data/user/user={self.name}.json", "w") as f:
            json.dump(player_data, f, indent=4) 

    # hàm để tải trạng thái của người chơi từ file JSON
    @staticmethod
    def load(name: str):
        try:
            with open(f"data/user/user={name}.json", "r") as f:
                player_data = json.load(f)
                return Player(
                    name=player_data["name"],
                    health=player_data["health"],
                    atk=player_data["attack"],
                    defense=player_data["defense"],
                    coins=player_data["coins"],
                    effect=player_data.get("effect")
                )
        except FileNotFoundError:
            print(f"No save file found for player '{name}'.")
            # có thể tạo sẵn file player nếu đây là lần đầu tiên chơi
            new_player = Player(name=name, health=100, atk=20, defense=10, coins=250)
            new_player.save()
            


    