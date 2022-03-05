import string
import random
import time

TARGET_HIT = ' X '
TARGET_MISSED = ' . '
TARGET_HIDDEN = ' | '
TARGET_REVEALED = ' O '

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
        ships = [6, 4, 4, 3, 3, 2, 2]

        while ships:
            direction = random.choice(['H', 'V'])
            row, col = [random.randint(0, 9) for _ in range(2)]
            if not self.is_placement_correct(row, col, ships[0], direction):
                continue
            else:
                self.place_ship(row, col, ships.pop(0), direction)

def is_good_move(row, col, obj):
    if row not in range(10) or col not in range(10):
        print("This is not a valid move.")
        print("You have already shot at this field or it is not on the battlefield.")
        return False
    if obj.battlefield[row][col] == TARGET_HIT or obj.battlefield[row][col] == TARGET_MISSED:
        return False
    return True

def convert_field_to_num(field):
    letter, number = field[0].upper(), int(field[1:]) - 1
    letter_id = [x for x in string.ascii_uppercase[:10]].index(letter)
    return letter_id, number


def hit(obj, row, col):
    if obj.battlefield[row][col] == TARGET_REVEALED:
        obj.battlefield[row][col] = TARGET_HIT
        return True
    else:
        obj.battlefield[row][col] = TARGET_MISSED


def all_ships_destroyed(obj):
    flatten_battlefield = [x for y in obj.battlefield for x in y]
    if not any(x == TARGET_REVEALED for x in flatten_battlefield):
        return True


ships = [6, 4, 4, 3, 3, 2, 2]


def main():
    print('\nLet\'s play battleships!\n')
    time.sleep(1)
    player = Battlefield()
    opp = Battlefield()
    moves = Battlefield()
    game_finished = False
    while ships:
        player.show_battlefield()
        first_field = input(f'Enter the first field of your ship (size {ships[0]}): ')
        direction = input('\nEnter the direction of your ship - (H)orizontal / (V)ertical: ')
        row, col = first_field[0].upper(), int(first_field[1:]) - 1
        row = [x for x in string.ascii_uppercase[:10]].index(row)
        if not player.is_placement_correct(row, col, ships[0], direction):
            print('\nThe ships cannot overlap and must fit on the battlefield.')
            print('Choose another place for your ship.\n')
            continue
        else:
            player.place_ship(row, col, ships.pop(0), direction)
    print('Your final ship placement:\n')
    player.show_battlefield()
    opp.generate_battlefield()
    while not game_finished:
        player_turn = True
        while player_turn:
            print('Moves battlefield:')
            moves.show_battlefield()
            row, col = convert_field_to_num(input('Enter the field to shoot at: '))
            if not is_good_move(row, col, moves):
                continue
            if hit(opp, row, col):
                moves.battlefield[row][col] = TARGET_HIT
                print('Great! It\'s a hit!')
                time.sleep(2)
                if all_ships_destroyed(opp):
                    print('Player wins!')
                    player_turn = False
                    opp_turn = False
                    game_finished = True
            else:
                moves.battlefield[row][col] = TARGET_MISSED
                print('You missed this time.')
                player_turn = False
                opp_turn = True
        while opp_turn:
            row, col = [random.randint(0, 9) for _ in range(2)]
            if not is_good_move(row, col, player):
                continue
            if hit(player, row, col):
                print('Opponent has hit your ship!')
                time.sleep(2)
                if all_ships_destroyed(player):
                    print('Opponent wins!')
                    opp_turn = False
                    game_finished = True
            else:
                print('Opponent missed.')
                opp_turn = False
            player.show_battlefield()
            time.sleep(2)


if __name__ == '__main__':
    main()

# ships overlapping