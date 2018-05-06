import curses
from random import randrange,choice
from collections import defaultdict
import Gamefield

def transpose(field):
    return [list(row) for row in zip(*field)]#zip(*filed)相当于解压

def invert(field):
    return [row[::-1] for row in field]#

def get_user_action(keyboard):
    char = "N"
    while char not in action_dict:
        char = keyboard.getch()
    return action_dict[char] #返回行为

class GameField(object):
    def __init__(self,height=4,width=4,win=2048):
        self.height = height
        self.width = width
        self.win_value = win
        self.score = 0
        self.highscore = 0
        self.reset()

    def spawn(self):
        new_element = 4 if randrange(100) >50 else 2
        (i,j) = choice([(i,j) for i in range(self.width) for j in range(self.height) if self.field[i][j] == 0])
        self.field[i][j] = new_element

    def reset(self):
        if self.score > self.highscore:
            self.highscore = self.score
        self.score = 0
        self.field = [[0 for i in range(self.width)] for j in range(self.height)]
        self.spawn()
        self.spawn()

    def move(self,direction):
        def move_row_left(row):
            def tighten(row):
                new_row = [i for i in row if i != 0]
                new_row += [0 for i in range(len(row)-len(new_row))]
                return new_row

            def merge(row):
                new_row = row
                for i in range(1,len(new_row)):
                    if new_row[i-1] == new_row[i]:
                        new_row[i-1] *= 2
                        new_row[i] = 0
                        break
                return new_row
            return tighten(merge(tighten(row)))

        moves = {}
        moves['Left'] = lambda field: [move_row_left(row) for row in field]
        moves['Right'] = lambda field: invert(moves['Left'](invert(field)))
        moves['Up'] = lambda field:transpose(moves['Left'](transpose(field)))
        moves['Down'] = lambda field:transpose(moves['Right'](transpose(field)))

        if direction in moves:
            if self.move_is_possible(direction):
                self.field = moves[direction](self.field)
                self.spawn()
                return True
            else:
                return False
    def is_win(self):
        return any(any(i >= self.win_value for i in row) for row in self.field)

    def is_gameover(self):
        return not any(self.move_is_possible(move) for move in actions)

    def move_is_possible(self,direction):
        def row_is_left_movable(row):
            def change(i):
                if row[i] ==0 and row[i+1] != 0:
                    return True
                if row[i] !=0 and row[i+1] == row[i]:
                    return True
                return False
            return any(change(i) for i in range(len(row)-1))

        check = {}
        check['Left']  = lambda field: any(row_is_left_movable(row) for row in field)

        check['Right'] = lambda field: check['Left'](invert(field))

        check['Up']    = lambda field: check['Left'](transpose(field))

        check['Down']  = lambda field: check['Right'](transpose(field))
        if direction in check.keys():
            return check[direction](self.field)
        else:
            return False

    def draw(self,screen):
        help_string1 = '(W)Up (S)Down (A)Left (D)Right'
        help_string2 = '    (R)Restart (Q)Exit'
        gameover_string = '     GAME OVER'
        win_string = '    YOU WIN!'
        def cast(string):
            screen.addstr(string + '\n')

        def draw_hor_separator():
            line = '+' + ('+------' * self.width + '+')[1:]
            separator = defaultdict(lambda:line)
            if not hasattr(draw_hor_separator,'counter'):
                draw_hor_separator.counter = 0
            cast(separator[draw_hor_separator.counter])
            draw_hor_separator.counter += 1

        def draw_row(row):
            cast(''.join('|{: ^5} '.format(num) if num > 0 else '|      ' for num in row) + '|')

        screen.clear()

        cast('SCORE: ' + str(self.score))
        if 0 != self.highscore:
            cast('HIGHSCORE: ' + str(self.highscore))

        for row in self.field:
            draw_hor_separator()
            draw_row(row)

        draw_hor_separator()

        if self.is_win():
            cast(win_string)
        else:
            if self.is_gameover():
                cast(gameover_string)
            else:
                cast(help_string1)
        cast(help_string2)


actions = ['Up','Down','Left','Right','Restart','Exit']

letter_codes = [ord(ch) for ch in 'WSADRQwsadrq']

#zip()将对象中对应的元素打包成一个个元组
action_dict = dict(zip(letter_codes,actions * 2))
game_filed = GameField(win=2048)

def main(stdscr):
    def init():
        game_filed.reset()
        return 'Game'

    def not_game(state):
        game_filed.draw(stdscr)
        action = get_user_action(stdscr)
        responses = defaultdict(lambda:state)
        responses['Restart'],responses['Exit'] = 'Init','Exit'
        return responses[action]

    def game():
        #画出当前棋盘状态
        game_filed.draw(stdscr)
        #读取用户输入得到action
        action = get_user_action(stdscr)
        if action == 'Restart':
            return 'Init'
        if action == 'Exit':
            return 'Exit'

            if win:
                return 'Win'
            if fail:
                return 'Gameover'
        if game_filed.move(action):
            if game_filed.is_win():
                return 'Win'
            if game_filed.is_gameover():
                return 'Gameover'
        return 'Game'

    state_actions = {
            'Init':init,
            'Win':lambda:not_game('Win'),
            'Gameover':lambda:not_game('Gameover'),
            'Game':game,
    }

    curses.use_default_colors()

    state = 'Init'

    #状态机开始循环
    while state != 'Exit':
        state = state_actions[state]()

curses.wrapper(main)
