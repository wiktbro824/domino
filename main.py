
import random
import sys
from collections import Counter
import operator

def Shuffle():
    global computer_pieces
    global player_pieces
    global stock_pieces
    random.seed()
    palette = []
    for i in range(0, 7):
        for j in range(0, 7):
            if i <= j:
                palette.append([i, j])
    random.shuffle(palette)
    computer_pieces = palette[:7:]
    player_pieces = palette[7:14:]
    stock_pieces = palette[14::]



def counter_elements(pieces):
    elements = {0:0, 1: 0, 2:0, 3:0, 4:0, 5:0, 6:0}
    for i in range(len(pieces)):
        for j in range(len(pieces[i])):
            for k in range(7):
                if pieces[i][j] == k:
                    elements[k] += 1
    return elements

y = 0
value_of_elem = {}
def value(counter, new_elem, y, keys, value_of_elem):
    if keys:
        value_of_elem[y] = 0
        for i, z in keys:
            value_of_elem[y] = new_elem[i] + new_elem[z]
            del keys[0]
            y += 1
            value(counter, new_elem, y, keys, value_of_elem)
    return value_of_elem

def create_stock():
    global computer_pieces
    global player_pieces
    global stock_pieces
    global domino
    status = ''; domino = '0'
    while status == '':
        Shuffle()
        for i in range(0, len(computer_pieces)):
            if computer_pieces[i][0] == computer_pieces[i][1]:
                if int(domino[0]) < computer_pieces[i][0]:
                    domino = computer_pieces[i]
                    status = 'player'
            if player_pieces[i][0] == player_pieces[i][1]:
                if int(domino[0]) < player_pieces[i][0]:
                    domino = player_pieces[i]
                    status = 'computer'
    if status == 'computer':
        player_pieces.remove(domino)
    else:
        computer_pieces.remove(domino)
    return status

first_move = create_stock()
domino = [domino]



def move(first_move):
    print(70*"=")
    print("Stock size:", len(stock_pieces))
    print("Computer pieces:", len(computer_pieces), "\n")
    show_domino()

    print("\nYour pieces:")
    for i in range(len(player_pieces)):
        print(f'{i+1}:{player_pieces[i]}')

    if len(computer_pieces) == 0:
        print("\nStatus: The game is over. The computer won!")
        sys.exit()
    elif len(player_pieces) == 0:
        print("\nStatus: The game is over. You won!")
        sys.exit()
    else:
        if first_move == 'computer':
            input("\nStatus: Computer is about to make a move. Press Enter to continue...")
        else:
            print("\nStatus: It's your turn to make a move. Enter your command.")
    return first_move

counter = 0
def player_make_move(first_move, counter):
    try:
        move = int(input())
        if -len(player_pieces) <= move <= len(player_pieces):
            if move < 0:
               counter = 0
               correct_move_player(move, player_pieces)
            elif move > 0:
                counter = 0
                correct_move_player(move, player_pieces)
            else:
                if not stock_pieces:
                    counter += 1
                    if counter == 2:
                        print("Status: The game is over. It's a draw!")
                        sys.exit()
                else:
                    b = stock_pieces.pop()
                    player_pieces.append(b)
        else:
            print("Invalid input. Please try again.")
            player_make_move(first_move, counter)
    except ValueError:
        print("Invalid input. Please try again.")
        player_make_move(first_move, counter)
    return counter

def correct_move_player(move, pieces):
    if move < 0:
        if domino[0][0] == pieces[(move*-1)-1][1]:
            b = pieces.pop(((move*-1) - 1))
            domino.insert(0, b)
        elif domino[0][0] in pieces[(move*-1)-1]:
            pieces[(move * -1) - 1][1], pieces[(move * -1) - 1][0] = pieces[(move * -1) - 1][0], pieces[(move * -1) - 1][1]
            b = pieces.pop(((move*-1) - 1))
            domino.insert(0, b)
        else:
            print("Illegal move. Please try again.")
    elif move > 0:
        if domino[len(domino)-1][1] == pieces[move-1][0]:
            b = pieces.pop(move - 1)
            domino.append(b)
        elif domino[len(domino)-1][1] in pieces[move-1]:
            pieces[move - 1][1], pieces[move - 1][0] = pieces[move - 1][0], pieces[move - 1][1]
            b = pieces.pop((move - 1))
            domino.append(b)
        else:
            print("Illegal move. Please try again.")
            player_make_move(first_move, counter)
def correct_move_computer(counter, move, pieces):
    if domino[0][0] == pieces[move][1]:
        counter = 0
        b = pieces.pop(move)
        domino.insert(0, b)
    elif domino[0][0] in pieces[move]:
        counter = 0
        pieces[move][1], pieces[move][0] = pieces[move][0], pieces[move][1]
        b = pieces.pop(move)
        domino.insert(0, b)
    elif domino[len(domino)-1][1] == pieces[move][0]:
        counter = 0
        b = pieces.pop(move)
        domino.append(b)
    elif domino[len(domino)-1][1] in pieces[move]:
        counter = 0
        pieces[move][1], pieces[move][0] = pieces[move][0], pieces[move][1]
        b = pieces.pop(move)
        domino.append(b)
    else:
        del value_of_elem[move]
        if not value_of_elem:
            if not stock_pieces:
                counter += 1
                if counter == 2:
                    print("Status: The game is over. It's a draw!")
                    sys.exit()
            else:
                b = stock_pieces.pop()
                computer_pieces.append(b)
                #player_make_move(first_move, counter)
        else:
            computer_make_move(value_of_elem, counter)

def computer_make_move(value_of_elem, counter):
    move = max(value_of_elem, key=value_of_elem.get)
    correct_move_computer(counter, move, computer_pieces)
    '''if not stock_pieces:
        counter += 1
        if counter == 2:
            print("Status: The game is over. It's a draw!")
            sys.exit()
    else:
        b = stock_pieces.pop()
        computer_pieces.append(b)
    return counter
'''
def change_player(first_move):
    if first_move == 'player':
        first_move = 'computer'
    else:
        first_move = 'player'
    return first_move

def check_snake():
    counter = 0
    if domino[0][0] == domino[len(domino)-1][1]:
        for i in range (len(domino)):
            for j in range (len(domino[i])):
                if domino[i][j] == domino[0][0]:
                    counter += 1
    if counter == 8:
        print("Status: The game is over. It's a draw!")
        sys.exit()

def show_domino():
    if len(domino) > 6:
        res = [domino[0], domino[1], domino[2], '...' , domino[-3], domino[-2], domino[-1]]
        print(*res, sep = "")
    else:
        print(*domino, sep = "")

def game(first_move, counter):
    check_snake()
    move(first_move)

    if first_move == 'player':
        player_make_move(first_move, counter)
        game(change_player(first_move), counter)
    else:
        value_of_elem.clear()
        elem_domino = counter_elements(domino)
        elem_comp = counter_elements(computer_pieces)
        new_elem = dict(Counter(elem_domino) + Counter(elem_comp))
        keys = computer_pieces.copy()
        computer_make_move(value(counter, new_elem, y, keys, value_of_elem), counter)
        game(change_player(first_move), counter)


game = game(first_move, counter)