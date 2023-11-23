import random
import time
import TrackerFacial
from colorama import Fore, Style

class Game:
    def __init__(self, size):
        self.size = size
        self.map = [[None for _ in range(size)] for _ in range(size)]
        self.player = None
        self.monster = None

    def generate_player(self):
        x = random.randint(0, self.size - 1)
        y = random.randint(0, self.size - 1)
        self.player = Player(x, y)
        self.map[y][x] = self.player

    def generate_monster(self):
        x = random.randint(0, self.size - 1)
        y = random.randint(0, self.size - 1)
        self.monster = Monster(x, y)
        self.map[y][x] = self.monster

    def generate_items(self, num_items):
        for _ in range(num_items):
            x = random.randint(0, self.size - 1)
            y = random.randint(0, self.size - 1)
            item = random.choice([Food(), Weapon(25, "💣"), Weapon(20, "🗡️"),
                                  Weapon(30, "🏹")])
            if self.map[y][x] is None:
                self.map[y][x] = item
            else:
                self.generate_items(1)

    def display_map(self):
        for row in self.map:
            for cell in row:
                if cell is None:
                    print(" -", end=" ")
                elif isinstance(cell, Player):
                    print("👨‍🌾", end=" ")
                elif isinstance(cell, Monster):
                    print("🧟‍♂️", end=" ")
                elif isinstance(cell, Food):
                    print(cell.symbol, end=" ")
                elif isinstance(cell, Weapon):
                    print(cell.symbol, end=" ")
            print()

    def move(self, x1, y1, x2, y2, mover):
        if isinstance(mover, Player) and isinstance(self.map[y2][x2], Weapon):
            mover.inventory.append(self.map[y2][x2])
        elif isinstance(self.map[y2][x2], Food):
            mover.health += 10
            print(Fore.GREEN + "¡Tu vida ha aumentado 10 puntos!" + Style.RESET_ALL)
        elif isinstance(self.map[y2][x2], Monster):
            player.health -= 10
            print("No te acerques al Zombie si no lo vas atacar, ¡Ten cuidado! \nAcabas de perder 10 de vida")
            return
        elif isinstance(self.map[y2][x2], Player):
            player.health -= 10
            print("El Zombie atacó al Jugador, ahora la vida del Jugador es: ",
                  Fore.RED + str(player.health) + Style.RESET_ALL)
            return

        self.map[y2][x2] = mover
        self.map[y1][x1] = None
        mover.x, mover.y = x2, y2

    def move_player(self, direction):
        x, y = self.player.x, self.player.y

        if direction == "Arriba" and y > 0:
            self.move(x, y, x, y - 1, self.player)

        elif direction == "Abajo" and y < self.size - 1:
            self.move(x, y, x, y + 1, self.player)

        elif direction == "Izquierda" and x > 0:
            self.move(x, y, x - 1, y, self.player)

        elif direction == "Derecha" and x < self.size - 1:
            self.move(x, y, x + 1, y, self.player)

    def move_monster(self):
        x, y = self.monster.x, self.monster.y
        directions = ["Arriba", "Abajo", "Izquierda", "Derecha"]
        direction = random.choice(directions)

        if direction == "Arriba" and y > 0:
            self.move(x, y, x, y - 1, self.monster)

        elif direction == "Abajo" and y < self.size - 1:
            self.move(x, y, x, y + 1, self.monster)

        elif direction == "Izquierda" and x > 0:
            self.move(x, y, x - 1, y, self.monster)

        elif direction == "Derecha" and x < self.size - 1:
            self.move(x, y, x + 1, y, self.monster)

    def check_attack_status(self):
        player_x, player_y = self.player.x, self.player.y
        monster_x, monster_y = self.monster.x, self.monster.y

        if player_x == monster_x and abs(player_y - monster_y) == 1:
            return True
        elif player_y == monster_y and abs(player_x - monster_x) == 1:
            return True
        else:
            return False

    def attack_monster(self, weapon):
        self.monster.health -= weapon.damage
        print(Fore.RED + "¡Haz atacado al Zombie! Ahora su vida es de: ",
              Fore.RED + str(self.monster.health) + Style.RESET_ALL)

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.health = 50
        self.inventory = []


class Monster:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.health = 40


class Item:
    def __init__(self):
        pass


class Food(Item):
    def __init__(self):
        super().__init__()
        self.symbol = "🍫"


class Weapon(Item):
    def __init__(self, damage, symbol):
        super().__init__()
        self.damage = damage
        self.symbol = symbol

game = Game(4)
game.generate_player()
game.generate_monster()
game.generate_items(12)
game.display_map()


def get_weapon_attack():
    direction, gesture = TrackerFacial.capture_direction_and_gesture()
    weapon_dict = {weapon: weapon.symbol for weapon in player.inventory}
    if gesture == "Pulgar hacia arriba (Bomba)":
        if "💣" in weapon_dict.values():
            weapon = next(key for key, value in weapon_dict.items() if value == "💣")
            game.attack_monster(weapon)
            player.inventory.remove(weapon)
        else:
            print("No tienes ninguna bomba en tu inventario, ¡Vuelve a intentarlo!")
            get_weapon_attack()

    elif gesture == "Espada":
        if "🗡️" in weapon_dict.values():
            weapon = next(key for key, value in weapon_dict.items() if value == "🗡️")
            game.attack_monster(weapon)
            player.inventory.remove(weapon)
        else:
            print("No tienes ninguna espada en tu inventario, ¡Vuelve a intentarlo!")
            get_weapon_attack()
    elif gesture == "Dos dedos horizontales (Arco)":
        if "🏹" in weapon_dict.values():
            weapon = next(key for key, value in weapon_dict.items() if value == "🏹")
            game.attack_monster(weapon)
            player.inventory.remove(weapon)
        else:
            print("No tienes ningún arco en tu inventario, ¡Vuelve a intentarlo!")
            get_weapon_attack()
    else:
        print("No haz hecho un gesto correcto, ¡Vuelve a intentarlo!")
        get_weapon_attack()


def move_monster():
    print("Preparando movimiento del Zombie...")
    time.sleep(3)
    game.move_monster()
    print("La vida del Zombie es: ", game.monster.health)
    game.display_map()


while True:
    player = game.player
    print("Mira a la dirección a la que quieras atacar y presiona 'Q' cuando estes listo")
    if len(player.inventory) != 0:
        print("Tienes en tu inventario los siguientes objetos: ")
        weapons = [weapon.symbol for weapon in player.inventory]
        print(",".join(weapons))
        if (game.check_attack_status()):
            attack = input("¿Deseas atacar al Zombie? (s/n): ").lower()
            if attack == "s":
                print("A continuación realiza el gesto correspondiente al arma que quieres usar")
                get_weapon_attack()
                print("¡Buen ataque!, realiza tu siguiente movimiento")
                if game.monster.health <= 0:
                    print("¡El juego ha finalizado!")
                    print("¡El ganador es el JUGADOR!")
                    break

    direction, gesture = TrackerFacial.capture_direction_and_gesture()

    if direction == "Frente":
        while direction == "Frente":
            print("Debes mirar hacia alguna direccion, moverse hacia al frente no es una opción")
            direction, gesture = TrackerFacial.capture_direction_and_gesture()
    else:
        game.move_player(direction)

    print("Tu vida actual es: ", player.health)
    game.display_map()

    move_monster()

    if game.player.health <= 0:
        print("¡El juego ha finalizado!")
        print("¡El ganador es el ZOMBIE!")
        break
    elif game.monster.health <= 0:
        print("El juego ha finalizado!")
        print("¡El ganador es el JUGADOR!")
        break
