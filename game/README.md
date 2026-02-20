# 🎮 Turn-Based Monster Battle Game

Một trò chơi RPG turn-based đơn giản, nơi bạn chiến đấu với các quái vật, kiếm coins, và cải thiện nhân vật của mình.

## 🎯 Tính Năng

- **Turn-Based Combat System**: Chiến đấu tuần tự với AI quái vật
- **Hành Động Đa Dạng**: 
  - ⚔️ **Attack**: Tấn công quái vật
  - 🛡️ **Defend**: Bảo vệ bản thân (giảm damage nhận được 50%)
  - ⏭️ **Skip**: Bỏ qua lượt
  
- **Hai Loại Quái Vật**:
  - **Smile**: Yếu hơn, 100 HP, thưởng 150 coins
  - **Goblin**: Mạnh hơn, 120 HP, thưởng 200 coins

- **Hệ Thống Lưu Game**: Lưu lại tiến độ một cách tự động
- **Hệ Thống Nghỉ Ngơi**: Hồi HP bằng cách trả tiền tại quán
- **Thống Kê Nhân Vật**: Xem thông tin HP, ATK, DEF, Coins

## 🚀 Cách Chạy

### Yêu Cầu
- Python 3.7+
- lupa (cho Lua integration)

### Cài Đặt Dependencies

```bash
pip install lupa
```

### Chạy Game

```bash
cd game
python src/main.py
```

## 🎮 Hướng Dẫn Chơi

### Menu Chính
1. **New Game**: Tạo nhân vật mới (HP=100, ATK=20, DEF=10, Coins=250)
2. **Load Game**: Tải nhân vật đã lưu từ lần chơi trước
3. **Exit**: Thoát game

### Trong Game
1. **Explore**: Ra ngoài gặp quái vật (30% xác suất mỗi lượt)
2. **View Status**: Xem thước thông tin nhân vật
3. **Rest**: Nghỉ ngơi hồi 30 HP (chi phí 50 coins)
4. **Save & Quit**: Lưu game và thoát

### Chiến Đấu
- Chọn action: Attack, Defend, Skip, hoặc View Info
- Tính Damage:
  - **Player Attack**: `ATK + random(-5, 15)`
  - **Quái Vật Defense**: Giảm sát thương của player
  - **Chỉ Attack thực chất = Damage - Target DEF**

- **Defend**: Khi bạn defend, DEF tăng +50 cho lượt đó
- **Chiến Thắng**: Quái vật HP = 0 → Bạn thắng, nhận tiền thưởng
- **Thua Cuộc**: Bạn HP = 0 → Game Over

## 📂 Cấu Trúc File

```
game/
├── src/
│   ├── main.py              # Game loop chính
│   └── function/
│       ├── battle.py        # Hệ thống chiến đấu turn-based
│       ├── find_monster.py  # Random encounter quái vật
│       └── Monster.py       # Wrapper cho Lua monsters
├── extension/
│   ├── default/
│   │   └── Player.py        # Class nhân vật
│   └── mod/
│       ├── smile.lua        # Definition quái vật Smile
│       └── goblin.lua       # Definition quái vật Goblin
├── data/
│   ├── user/
│   │   └── user=*.json      # Lưu trữ nhân vật
│   ├── api/
│   ├── cache/
```

## 🛠️ Kiến Trúc Công Nghệ

- **Python 3** để game logic
- **Lua 5.4** để định nghĩa quái vật (OOP-style)
- **Lupa** để nhúng Lua vào Python
- **JSON** để lưu trữ dữ liệu người chơi

### Thiết Kế Monster

Mỗi quái vật được định nghĩa bằng Lua:
```lua
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

function Smile:attack()
    return math.random(self.atk - 5, self.atk + 5)
end

-- ... more methods
```

## 💡 Chiến Lược Chơi

1. **Early Game**: Attack liên tục để nhanh chết quái vật
2. **Tiết Kiệm**: Giữ tiền để Defend khi HP thấp
3. **Balance**: Tham gia Explore nhiều lần để kiếm coins cho Rest
4. **Nâng Cấp**: (V2.0) Có thể lên cấp HTK/ATK/DEF bằng coins

## 📊 Thống Kê Nhân Vật

| Thuộc Tính | Ban Đầu |
|-----------|--------|
| Health | 100 |
| Attack | 20 |
| Defense | 10 |
| Coins | 250 |

## 🐛 Known Issues

- Chưa được thêm một số tính năng advanced (Level Up, Special Skills)
- AI quái vật có thể cải tiến thêm

## 🔮 Features Sắp Tới (V2.0)

- [ ] Level Up system
- [ ] Special Attack Skills
- [ ] Equipment/Armor system
- [ ] Ability Upgrades (bằng coins)
- [ ] More Monster Types
- [ ] Boss Monsters
- [ ] Dungeon Levels
- [ ] HTML/Web UI

## 👨‍💻 Phát Triển

Tạo bởi **KHoapython-dev**

## 📝 License

MIT License - Tự do sử dụng, sửa đổi, phân phối

---

**Chúc bạn chơi vui! 🎮**
