import random


def print_board(state):
    print(9 * '-')
    for cell in range(0, len(state), 3):
        print(f'| {state[cell]} {state[cell + 1]} {state[cell + 2]} |')
    print(9 * '-')


def cell_free(state, i, j):
    return True if state[(i - 1) * 3 + j - 1] == ' ' else False


def game_finished(state):
    rows = [state[0:3], state[3:6], state[6:9]]
    columns = [state[0::3], state[1::3], state[2::3]]
    diags = [state[0::4], state[2:7:2]]
    lines = rows + columns + diags

    if 'XXX' in lines:
        print('X wins')
        return True
    elif 'OOO' in lines:
        print('O wins')
        return True
    elif state.count(' ') == 0:
        print('Draw')
        return True
    else:
        return False


def possible_win(state, player):
    rows = [state[0:3], state[3:6], state[6:9]]
    columns = [state[0::3], state[1::3], state[2::3]]
    diags = [state[0::4], state[2:7:2]]
    lines = rows + columns + diags

    if player * 3 in lines:
        return 'win'
    elif state.count(' ') == 0:
        return 'tie'
    else:
        for line in lines:
            if line.count(player) == 2 and ' ' in line:
                return 'possible win'


def make_move(state, player, row, col):
    return state[:(row - 1) * 3 + col - 1] + player + state[(row - 1) * 3 + col:]


def move_user(state, player):
    while True:
        try:
            row, col = map(int, input('Enter the coordinates: > ').split())
        except (ValueError, TypeError):
            print('You should enter numbers!')
        else:
            if row in range(1, 4) and col in range(1, 4):
                if cell_free(state, row, col):
                    return make_move(state, player, row, col)
                else:
                    print('This cell is occupied! Choose another one!')
            else:
                print('Coordinates should be from 1 to 3!')


def move_ai(state, player, difficulty):
    if difficulty == 'easy':
        return move_ai_easy(state, player)
    elif difficulty == 'medium':
        return move_ai_medium(state, player)
    else:
        return move_ai_hard(state, player)


def move_ai_easy(state, player):
    print('Making move level "easy"')
    while True:
        row, col = random.randint(1, 3), random.randint(1, 3)
        if cell_free(state, row, col):
            return make_move(state, player, row, col)


def move_ai_medium(state, player):
    print('Making move level "medium"')
    opponent = 'O' if player == 'X' else 'X'

    # Move to win the game
    if possible_win(state, player) == 'possible win':
        for row in range(1, 4):
            for col in range(1, 4):
                if cell_free(state, row, col):
                    state_next = make_move(state, player, row, col)
                    if possible_win(state_next, player) == 'win':
                        return state_next
    # Block opponent's winning move
    elif possible_win(state, opponent) == 'possible win':
        for row in range(1, 4):
            for col in range(1, 4):
                if cell_free(state, row, col):
                    state_next = make_move(state, opponent, row, col)
                    if possible_win(state_next, opponent) == 'win':
                        state_next = make_move(state, player, row, col)
                        return state_next
    # Random move
    else:
        while True:
            row, col = random.randint(1, 3), random.randint(1, 3)
            if cell_free(state, row, col):
                return make_move(state, player, row, col)


def move_ai_hard_simple(state, player):
    print('Making move level "hard"')
    if move_counter <= 1 and cell_free(state, 2, 2):
        return make_move(state, player, 2, 2)
    else:
        return move_ai_medium(state, player)


def minimax(state, player, depth, maximizing):
    opponent = 'O' if player == 'X' else 'X'

    if possible_win(state, player) == 'win':
        return 1
    elif possible_win(state, opponent) == 'win':
        return -1
    elif possible_win(state, player) == 'tie':
        return 0

    if maximizing:
        depth += 1
        best_score = -1000
        for row in range(1, 4):
            for col in range(1, 4):
                if cell_free(state, row, col):
                    state_next = make_move(state, player, row, col)
                    score = minimax(state_next, player, depth, False)
                    best_score = max(score, best_score)
        return best_score
    else:
        depth += 1
        best_score = 1000
        for row in range(1, 4):
            for col in range(1, 4):
                if cell_free(state, row, col):
                    state_next = make_move(state, opponent, row, col)
                    score = minimax(state_next, opponent, depth, True)
                    best_score = min(score, best_score)
        return best_score


def move_ai_hard(state, player):
    print('Making move level "hard"')

    if move_counter <= 1 and cell_free(state, 2, 2):
        return make_move(state, player, 2, 2)
    else:
        opponent = 'O' if player == 'X' else 'X'
        best_score = -1000
        best_row, best_col = 1, 1

        for row in range(1, 4):
            for col in range(1, 4):
                if cell_free(state, row, col):
                    state_next = make_move(state, player, row, col)
                    score = minimax(state_next, player, 0, False)
                    if score > best_score:
                        best_score = score
                        best_row, best_col = row, col

        return make_move(state, player, best_row, best_col)


def game_mode():
    options = ['user', 'easy', 'medium', 'hard']
    while True:
        # inp = input('Input inp: > ').split()
        inp = 'start easy hard'.split()
        if len(inp) == 1 and inp[0] == 'exit':
            return inp[0], None, None
        elif len(inp) == 3 and inp[0] == 'start' and inp[1] in options and inp[2] in options:
            return inp[0:3]
        else:
            print("Bad parameters!")


game_state = ' ' * 9
move_counter = 0

while True:
    mode, player1, player2 = game_mode()

    if mode == 'exit':
        break

    else:
        print_board(game_state)
        while True:
            if game_state.count('X') == game_state.count('O'):
                turn = 'X'
                current_player = player1
            else:
                turn = 'O'
                current_player = player2
            if current_player == 'user':
                game_state = move_user(game_state, turn)
            else:
                ai_difficulty = current_player
                game_state = move_ai(game_state, turn, ai_difficulty)
            print_board(game_state)
            move_counter += 1
            if game_finished(game_state):
                break
        break
