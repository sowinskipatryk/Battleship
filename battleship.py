import string
import random
import time

TARGET_HIT = ' X '
TARGET_MISSED = ' . '
TARGET_HIDDEN = ' | '
TARGET_REVEALED = ' O '

SHIPS = [6, 4, 4, 3, 3, 2, 2]


class Battlefield:

    def __init__(self):
        self.battlefield = [[TARGET_HIDDEN for _ in range(1, 11)] for _ in range(1, 11)]

    def show_battlefield(self, tagged=True):
        if tagged:
            print('  ', end='')
            print("".join([str(i).rjust(4) for i in range(1, 11)]))
            idx = 0
            for x in self.battlefield:
                print(f"{string.ascii_uppercase[idx]} ".rjust(4), end='')
                print(' '.join(x))
                idx += 1
        else:
            for x in self.battlefield:
                print(' '.join(x))
        print('')

    def place_ship(self, row, col, length, direction):
        if direction.upper() == 'H':
            for a in range(length):
                self.battlefield[row][col + a] = TARGET_REVEALED
        elif direction.upper() == 'V':
            for b in range(length):
                self.battlefield[row + b][col] = TARGET_REVEALED

    def is_placement_correct(self, row, col, length, direction):
        boundary_boxes = []
        if direction.upper() == 'H':
            if col + length > 10:
                return False
            for x in range(row-1, row+2):
                for y in range(col-1, col+length+1):
                    try:
                        boundary_boxes.append(self.battlefield[x][y])
                    except IndexError:
                        pass
        elif direction.upper() == 'V':
            if row + length > 10:
                return False
            for x in range(row-1, row+length+1):
                for y in range(col-1, col+2):
                    try:
                        boundary_boxes.append(self.battlefield[x][y])
                    except IndexError:
                        pass
        if all(n != TARGET_REVEALED for n in boundary_boxes):
            return True

    def generate_battlefield(self):
        opps_ships = SHIPS[:]

        while opps_ships:
            direction = random.choice(['H', 'V'])
            row, col = [random.randint(0, 9) for _ in range(2)]
            if not self.is_placement_correct(row, col, opps_ships[0], direction):
                continue
            else:
                self.place_ship(row, col, opps_ships.pop(0), direction)

    def all_ships_destroyed(self):
        flatten_battlefield = [x for y in self.battlefield for x in y]
        if not any(x == TARGET_REVEALED for x in flatten_battlefield):
            return True

    def hit(self, row, col):
        if self.battlefield[row][col] == TARGET_REVEALED:
            self.battlefield[row][col] = TARGET_HIT
            return True
        else:
            self.battlefield[row][col] = TARGET_MISSED

    def is_correct_move(self, row, col):
        if row not in range(10) or col not in range(10):
            print("This is not a valid move.")
            print("You have already shot at this field or it is not on the battlefield.")
            return False
        if self.battlefield[row][col] == TARGET_HIT or self.battlefield[row][col] == TARGET_MISSED:
            return False
        return True


def convert_field_to_num(field):
    letter, number = field[0].upper(), int(field[1:]) - 1
    letter_id = [x for x in string.ascii_uppercase[:10]].index(letter)
    return letter_id, number


players_ships = SHIPS[:]


def main():
    print('\nLet\'s play battleships!\n')
    time.sleep(1)
    player = Battlefield()
    opp = Battlefield()
    moves = Battlefield()
    game_finished = False
    while players_ships:
        player.show_battlefield()
        first_field = input(f'Enter the first field of your ship (size {players_ships[0]}): ')
        direction = input('\nEnter the direction of your ship - (H)orizontal / (V)ertical: \n')
        row, col = first_field[0].upper(), int(first_field[1:]) - 1
        row = [x for x in string.ascii_uppercase[:10]].index(row)
        if not player.is_placement_correct(row, col, players_ships[0], direction):
            print('\nThe ships cannot overlap and must fit on the battlefield.')
            print('Choose another place for your ship.\n')
            continue
        else:
            player.place_ship(row, col, players_ships.pop(0), direction)
    time.sleep(1.5)
    print('Your final ship placement:\n')
    time.sleep(1.5)
    player.show_battlefield()
    opp.generate_battlefield()
    while not game_finished:
        player_turn = True
        while player_turn:
            time.sleep(1)
            print('Your turn: \n')
            time.sleep(0.5)
            moves.show_battlefield()
            row, col = convert_field_to_num(input('Enter the field to shoot at: '))
            if not moves.is_correct_move(row, col):
                continue
            if opp.hit(row, col):
                moves.battlefield[row][col] = TARGET_HIT
                print('\nGreat! It\'s a hit!\n')
                time.sleep(1.5)
                if opp.all_ships_destroyed():
                    print('Player wins!')
                    player_turn = False
                    opp_turn = False
                    game_finished = True
            else:
                moves.battlefield[row][col] = TARGET_MISSED
                time.sleep(0.5)
                print('\nYou missed this time.\n')
                player_turn = False
                opp_turn = True
        while opp_turn:
            time.sleep(1.5)
            print('Opponent\'s turn.\n')
            row, col = [random.randint(0, 9) for _ in range(2)]
            if not player.is_correct_move(row, col):
                continue
            if player.hit(row, col):
                time.sleep(1.5)
                print('Opponent has hit your ship!')
                time.sleep(1.5)
                if player.all_ships_destroyed():
                    print('Opponent wins!')
                    opp_turn = False
                    game_finished = True
            else:
                time.sleep(1.5)
                print('Opponent missed.\n')
                opp_turn = False
            time.sleep(0.5)
            player.show_battlefield()
            time.sleep(0.5)


if __name__ == '__main__':
    main()
