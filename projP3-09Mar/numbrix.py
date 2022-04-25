import copy
import sys
from search import Problem, Node, depth_first_tree_search, breadth_first_tree_search, astar_search, recursive_best_first_search
import time

# numbrix.py: Template para implementacao do projeto de Inteligencia Artificial 2021/2022.
# Devem alterar as classes e funcoes neste ficheiro de acordo com as instrucoes do enunciado.
# Alem das funcoes e classes ja definidas, podem acrescentar outras que considerem pertinentes.

# Grupo 26:
# 96858 Eduardo Duarte Silva Rangel Pamplona
# 96885 Jose Maria de Oliveira Soares Bonneville Franco

class NumbrixState:
    state_id = 0

    def __init__(self, board):
        self.board = board
        self.id = NumbrixState.state_id
        NumbrixState.state_id += 1

    def __lt__(self, other):
        return self.id < other.id 

    def get_board(self):
        return self.board


class Board:
    """ Representacao interna de um tabuleiro de Numbrix. """

    def __init__(self, size: int, initial_positions: list, empty_positions: list, on_board: dict, off_board: dict):
        """ O construtor especifica o estado inicial. """
        self.size = size
        self.positions = initial_positions
        self.empty_positions = empty_positions
        self.on_board = on_board
        self.off_board = off_board
        self.next_off_board_key = 0
        self.coordinate_on_off_dict()

    def get_size(self):
        return self.size

    def get_number(self, row: int, col: int):
        """ Devolve o valor na respetiva posicao do tabuleiro. """
        return self.positions[row][col]

    def set_number_on_board(self, row: int, col: int, num: int):
        self.positions[row][col] = num   
        self.on_board[(row, col)] = num
        del self.off_board[num]
        self.empty_positions.remove((row, col))

    def set_number_off_board(self, num: int, possible_positions: list):
        self.off_board[num] = possible_positions
    
    def adjacent_vertical_numbers(self, row: int, col: int):
        """ Devolve os valores imediatamente abaixo e acima, 
        respectivamente. """
        if row == 0:
            up = None
        else:
            up = self.get_number(row - 1, col)
        if row == self.size - 1:
            down = None
        else:
            down = self.get_number(row + 1, col)
        return (up, down)
    
    def adjacent_horizontal_numbers(self, row: int, col: int):
        """ Devolve os valores imediatamente a esquerda e a direita, 
        respectivamente. """
        if col == 0:
            left = None
        else:
            left = self.get_number(row, col - 1)
        if col == self.size - 1:
            right = None
        else:
            right = self.get_number(row, col + 1)
        return (left, right)

    def set_positions(self, positions):
        self.positions = positions

    def get_on_board_key(self, value: int):
        for key, val in self.on_board.items():
            if val == value:
                return key
        return None

    def coordinate_on_off_dict(self):
        prev_value = ()
        next_value = ()
        off_board_index = 0
        self.next_off_board_key = 0
        
        while True:

            sorted_on_board = dict(sorted(self.on_board.items(), key = lambda item: item[1]))
            off_board_index = 0

            for key in self.off_board:
                for value in sorted_on_board.values():
                    if value < key:
                        (prev_row, prev_col) = self.get_on_board_key(value)
                        prev_value = (prev_row, prev_col, value)
                    else:
                        (next_row, next_col) = self.get_on_board_key(value)
                        next_value = (next_row, next_col, value)
                        break   
                
                possible_positions = self.manhattan_interception(key, prev_value, next_value)

                if len(possible_positions) == 1:
                    self.set_number_on_board(possible_positions[0][0], possible_positions[0][1], key)

                    if self.next_off_board_key == key:
                        self.next_off_board_key = 0

                    if len(self.off_board) == 0:
                        return
                    break

                else:
                    if self.next_off_board_key == 0:
                        self.next_off_board_key = key

                    if len(possible_positions) < len(self.off_board[self.next_off_board_key]):
                        self.next_off_board_key = key

                    self.set_number_off_board(key, possible_positions)
                    off_board_index += 1

                    if off_board_index == len(self.off_board):
                        return                
           
   
    def manhattan_interception(self, num: int, lower_pos: tuple, higher_pos: tuple):
        possible_positions = []
        parity = None

        if lower_pos != ():
            lower_diff = abs(lower_pos[2] - num)
            if lower_diff % 2 == 0:
                if (lower_pos[0] + lower_pos[1]) % 2 == 0:
                    parity = 0
                else:
                    parity = 1
            else:
                if (lower_pos[0] + lower_pos[1]) % 2 != 0:
                    parity = 0
                else:
                    parity = 1

        if higher_pos != ():
            higher_diff = abs(higher_pos[2] - num)
            if parity == None:
                if higher_diff % 2 == 0:
                    if (higher_pos[0] + higher_pos[1]) % 2 == 0:
                        parity = 0
                    else:
                        parity = 1
                else:
                    if (higher_pos[0] + higher_pos[1]) % 2 != 0:
                        parity = 0
                    else:
                        parity = 1

        for position in self.empty_positions:
            if lower_pos != () and higher_pos != ():
                if abs(position[0] - lower_pos[0]) + abs(position[1] - lower_pos[1]) <= lower_diff and abs(position[0] - higher_pos[0]) + abs(position[1] - higher_pos[1]) <= higher_diff:
                    if (parity == 0 and (position[0] + position[1]) % 2 == 0) or (parity == 1 and (position[0] + position[1]) % 2 != 0):
                        possible_positions.append(position)

            elif lower_pos == ():
                if abs(position[0] - higher_pos[0]) + abs(position[1] - higher_pos[1]) <= higher_diff:
                    if (parity == 0 and (position[0] + position[1]) % 2 == 0) or parity == 1 and (position[0] + position[1]) % 2 != 0:
                        possible_positions.append(position)

            elif higher_pos == ():
                if abs(position[0] - lower_pos[0]) + abs(position[1] - lower_pos[1]) <= lower_diff:
                    if (parity == 0 and (position[0] + position[1]) % 2 == 0) or parity == 1 and (position[0] + position[1]) % 2 != 0:
                        possible_positions.append(position)
        
        return possible_positions
    
    def to_string(self):
        out = ""
        for r in range(self.size):
            c = 0
            for c in range(self.size):
                out += str(self.positions[r][c])
                if c != self.size - 1:
                    out += '\t'
            if r < self.size - 1:
                out += '\n'

        return out

    @staticmethod    
    def parse_instance(filename: str):
        """ Le o ficheiro cujo caminho e passado como argumento e retorna
        uma instancia da classe Board. """

        with open(filename, 'r') as file:
            data = file.read()

        it = 1
        size_str = ''
        for item in data:
            if item != '\n':
                it += 1
                size_str += item
            else:
                break
        size = int(size_str)   

        on_board = {}
        off_board = {}

        for i in range(size * size):
            off_board[i + 1] = []

        r = 0
        c = 0

        initial_positions = []
        empty_positions = []
        row = []
        num = ''
        for item in data[it::]:
            if item != '\t' and item != '\n':
                num += item
            elif item == '\t':
                row.append(int(num))
                if int(num) != 0:
                    on_board[(r, c)] = int(num)
                    del off_board[int(num)]  
                else:
                    empty_positions.append((r, c), )    
                num = ''
                c += 1
            elif item == '\n':
                row.append(int(num))
                if int(num) != 0:
                    on_board[(r, c)] = int(num)
                    del off_board[int(num)]
                else:
                    empty_positions.append((r, c), )    
                num = ''
                initial_positions.append(row)
                r += 1
                c = 0
                row = []        

        return Board(size, initial_positions, empty_positions, on_board, off_board)


class Numbrix(Problem):
    def __init__(self, board: Board):
        """ O construtor especifica o estado inicial. """
        self.initial = NumbrixState(board)

    def actions(self, state: NumbrixState):
        board = state.get_board()
        actions = []

        if board.off_board.get(board.next_off_board_key) != None:
            for position in board.off_board[board.next_off_board_key]:
                actions.append((position[0], position[1], board.next_off_board_key))

        return actions

    def result(self, state: NumbrixState, action):
        """ Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A acoo a executar deve ser uma
        das presentes na lista obtida pela execucao de 
        self.actions(state). """

        new_board = copy.deepcopy(state.get_board())
        new_board.set_number_on_board(action[0], action[1], action[2])
        new_board.coordinate_on_off_dict()      

        new_state = NumbrixState(new_board)

        return new_state

    def goal_test(self, state: NumbrixState):
        """ Retorna True se e so se o estado passado como argumento e
        um estado objetivo. Deve verificar se todas as posicoes do tabuleiro 
        estao preenchidas com uma sequencia de numeros adjacentes. """

        board = state.get_board()
        key = board.get_on_board_key(1)  

        if key == None:
            return False
        else:
            current_pos = (key[0], key[1], 1)

            while True:

                (up, down) = board.adjacent_vertical_numbers(current_pos[0], current_pos[1])
                (left, right) = board.adjacent_horizontal_numbers(current_pos[0], current_pos[1])

                if up == current_pos[2]+1:
                    current_pos = (current_pos[0]-1, current_pos[1], current_pos[2]+1)
                elif down == current_pos[2]+1:
                    current_pos = (current_pos[0]+1, current_pos[1], current_pos[2]+1)
                elif left == current_pos[2]+1:
                    current_pos = (current_pos[0], current_pos[1]-1, current_pos[2]+1)
                elif right == current_pos[2]+1:
                    current_pos = (current_pos[0], current_pos[1]+1, current_pos[2]+1)
                else:
                    if current_pos[2] == board.get_size() * board.get_size():
                        return True
                    return False
                
    def h(self, node: Node):
        """ Funcao heuristica utilizada para a procura A*. """
        # TODO
        pass
    

if __name__ == "__main__":

    inputFile = sys.argv[1]

    board = Board.parse_instance(inputFile)

    problem = Numbrix(board)

    goal_node = depth_first_tree_search(problem)

    print(goal_node.state.get_board().to_string())
