import random

battlefield = []
ships = [6,4,4,3,3,2,2]

def create_battlefield():
	for i in range(10):
		battlefield.append([])
		for j in range(10):
			battlefield[i].append(".")

def place_the_ship(len, battlefield):
	max_num = ((10 - len + 1) * 10) - 1
	step = 10 - len + 1
	while True:
		row, col = divmod(random.randint(0, max_num), step)
		list_hor = []
		list_vert = []
		for i in range(-1, 2):
			for z in range(-1, len + 1):
				try:
					list_hor.append(battlefield[row + i][col + z])
					list_vert.append(battlefield[col + z][row + i])
				except IndexError:
					pass
		if all(v == '.' for v in list_hor):
			for k in range(len):
				battlefield[row][col + k] = 'X'
			break
		elif all(m == '.' for m in list_vert):
			for n in range(len):
				battlefield[col + n][row] = 'X'
			break
		else:
			continue
	return battlefield

def game_status():
	for x in range(10):
		print('    '.join(battlefield[x]))
		print('')

create_battlefield()

for ship in ships:
	battlefield = place_the_ship(ship, battlefield)

game_status()