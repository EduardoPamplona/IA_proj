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

    def __init__(self, size: int, initial_positions):
        """ O construtor especifica o estado inicial. """
        self.lowest_path_number = None
        self.highest_path_number = None
        self.size = size
        self.positions = initial_positions
        self.manhattan_list = []

    def get_size(self):
        return self.size

    def get_number(self, row: int, col: int):
        """ Devolve o valor na respetiva posicao do tabuleiro. """
        return self.positions[row][col]

    def set_number(self, row: int, col: int, num: int):
        self.positions[row][col] = num    
    
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

    def get_lowest_path_number(self):
        return self.lowest_path_number
    
    def get_highest_path_number(self):
        return self.highest_path_number

    def set_lowest_path_number(self, row: int, col: int, num: int):
        self.lowest_path_number = (row, col, num)

    def set_highest_path_number(self, row: int, col: int, num: int):
        for tup in self.manhattan_list:
            if num >= tup[2]:
                self.manhattan_list.remove(tup)
        self.highest_path_number = (row, col, num)

    def set_initial_lowest_path_number(self):
        lowest = (None, None, self.size * self.size + 1)

        for row in range(self.size):
            for col in range(self.size):
                current_num = self.get_number(row, col)
                if current_num != 0:
                    self.manhattan_list.append((row, col, current_num),)
                    if current_num <= lowest[2]:
                        lowest = (row, col, current_num)

        self.manhattan_list.sort(key = lambda x: x[2])                    
                    
        self.lowest_path_number = lowest

    def set_initial_highest_path_number(self):
        self.set_highest_path_number(self.get_lowest_path_number()[0], self.get_lowest_path_number()[1], self.get_lowest_path_number()[2])

        changed_css = True

        while changed_css:
            changed_css = self.check_set_straight_sequence(self.get_highest_path_number()[0], self.get_highest_path_number()[1])

    def check_possible_path(self, row: int, col: int):
        root_num = (row, col, self.get_number(row, col))
        initial_highest = root_num

        while (True):
            (up, down) = self.adjacent_vertical_numbers(root_num[0], root_num[1])
            (left, right) = self.adjacent_horizontal_numbers(root_num[0], root_num[1])

            if up == root_num[2] + 1:
                root_num = (root_num[0] - 1, root_num[1], up)
                self.set_highest_path_number(root_num[0], root_num[1], root_num[2])
            elif down == root_num[2] + 1: 
                root_num = (root_num[0] + 1, root_num[1], down)
                self.set_highest_path_number(root_num[0], root_num[1], root_num[2])
            elif left == root_num[2] + 1:
                root_num = (root_num[0], root_num[1] - 1, left)
                self.set_highest_path_number(root_num[0], root_num[1], root_num[2])
            elif right == root_num[2] + 1:
                root_num = (root_num[0], root_num[1] + 1, right)
                self.set_highest_path_number(root_num[0], root_num[1], root_num[2])
            else:
                if initial_highest == self.get_highest_path_number():
                    return False
                return True        

    def check_set_straight_sequence(self, row: int, col: int):
        root_num = (row, col, self.get_number(row, col))
        initial_highest = root_num

        (up, down) = self.adjacent_vertical_numbers(root_num[0], root_num[1])
        (left, right) = self.adjacent_horizontal_numbers(root_num[0], root_num[1])
            
        up_pos = (row-1, col, up)
        down_pos = (row+1, col, down)
        left_pos = (row, col-1, left)
        right_pos = (row, col+1, right)

        direction_to_check = 0

        while True:
            candidate_positions = copy.deepcopy(self.positions)
            incrementer = 1
            while direction_to_check == 0 and up_pos[2] != None:
                if up_pos[2] == 0:
                    # the position is filled with the next number in the sequence
                    candidate_positions[up_pos[0]][up_pos[1]] = root_num[2] + incrementer

                    # up_pos is updated to the position above
                    up_pos = (up_pos[0]-1, up_pos[1], self.adjacent_vertical_numbers(up_pos[0], up_pos[1])[0])

                    incrementer += 1
                    
                elif up_pos[2] == root_num[2] + incrementer:
                    # the positions of this board are now updated to the candidate_positions because a 
                    # straight sequence was found
                    self.set_positions(candidate_positions)
                    # the hisghest_path_number is now the last number in the straight sequence
                    self.set_highest_path_number(up_pos[0], up_pos[1], up_pos[2])
                    break
                else:
                    break 
            
            while direction_to_check == 1 and down_pos[2] != None:
                if down_pos[2] == 0:
                    candidate_positions[down_pos[0]][down_pos[1]] = root_num[2] + incrementer
                    down_pos = (down_pos[0]+1, down_pos[1], self.adjacent_vertical_numbers(down_pos[0], down_pos[1])[1])
                    incrementer += 1
                elif down_pos[2] == root_num[2] + incrementer:
                    self.set_positions(candidate_positions)
                    self.set_highest_path_number(down_pos[0], down_pos[1], down_pos[2])
                    break
                else:
                    break 

            while direction_to_check == 2 and left_pos[2] != None:
                if left_pos[2] == 0:
                    candidate_positions[left_pos[0]][left_pos[1]] = root_num[2] + incrementer
                    left_pos = (left_pos[0], left_pos[1]-1, self.adjacent_horizontal_numbers(left_pos[0], left_pos[1])[0])
                    incrementer += 1
                elif left_pos[2] == root_num[2] + incrementer:
                    self.set_positions(candidate_positions)
                    self.set_highest_path_number(left_pos[0], left_pos[1], left_pos[2])
                    break
                else:
                    break 
            
            while direction_to_check == 3 and right_pos[2] != None:
                if right_pos[2] == 0:
                    candidate_positions[right_pos[0]][right_pos[1]] = root_num[2] + incrementer
                    right_pos = (right_pos[0], right_pos[1]+1, self.adjacent_horizontal_numbers(right_pos[0], right_pos[1])[1])
                    incrementer += 1
                    
                elif right_pos[2] == root_num[2] + incrementer:
                    self.set_positions(candidate_positions)
                    self.set_highest_path_number(right_pos[0], right_pos[1], right_pos[2])
                    break
                else:
                    break 
                    
            direction_to_check += 1

            if direction_to_check == 4:
                if initial_highest == self.get_highest_path_number():
                    return False
                return True    

    def check_possible_filling(self, root_num: tuple):
        
        self.set_highest_path_number(root_num[0], root_num[1], root_num[2])
        changed_cpp = True
        changed_css = True

        while changed_cpp or changed_css:
            changed_cpp = self.check_possible_path(self.get_highest_path_number()[0], self.get_highest_path_number()[1])
            changed_css = self.check_set_straight_sequence(self.get_highest_path_number()[0], self.get_highest_path_number()[1])

    def check_manhattan_distance_to_next(self, row: int, col: int, num: int):
        if self.manhattan_list == []:
            return True
        pos_to_compare = self.manhattan_list[0]
        return abs(row - pos_to_compare[0]) + abs(col - pos_to_compare[1]) <= pos_to_compare[2] - num

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

        initial_positions = []
        row = []
        num = ''
        for item in data[it::]:
            if item != '\t' and item != '\n':
                num += item
            elif item == '\t':
                row.append(int(num))
                num = ''
            elif item == '\n':
                row.append(int(num))
                num = ''
                initial_positions.append(row)
                row = []

        return Board(size, initial_positions)


class Numbrix(Problem):
    def __init__(self, board: Board):
        """ O construtor especifica o estado inicial. """
        board.set_initial_lowest_path_number()
        board.set_initial_highest_path_number()
        self.initial = NumbrixState(board)

    def actions(self, state: NumbrixState):
        board = state.get_board()
        lowest = board.get_lowest_path_number()
        highest = board.get_highest_path_number()
        actions = ()

        if lowest[2] > 1:
            (up, down) = board.adjacent_vertical_numbers(lowest[0], lowest[1])
            (left, right) = board.adjacent_horizontal_numbers(lowest[0], lowest[1])
            if up == 0:
                actions += ((lowest[0] - 1, lowest[1], lowest[2] - 1), )
            if down == 0:   
                actions += ((lowest[0] + 1, lowest[1], lowest[2] - 1), )
            if left == 0:
                actions += ((lowest[0], lowest[1] - 1, lowest[2] - 1), )
            if right == 0:
                actions += ((lowest[0], lowest[1] + 1, lowest[2] - 1), )    
        else:
            (up, down) = board.adjacent_vertical_numbers(highest[0], highest[1])
            (left, right) = board.adjacent_horizontal_numbers(highest[0], highest[1])
            if up == 0 and board.check_manhattan_distance_to_next(highest[0] - 1, highest[1], highest[2] + 1):
                actions += ((highest[0] - 1, highest[1], highest[2] + 1), )
            if down == 0  and board.check_manhattan_distance_to_next(highest[0] + 1, highest[1], highest[2] + 1):   
                actions += ((highest[0] + 1, highest[1], highest[2] + 1), )
            if left == 0  and board.check_manhattan_distance_to_next(highest[0], highest[1] - 1, highest[2] + 1):
                actions += ((highest[0], highest[1] - 1, highest[2] + 1), )
            if right == 0  and board.check_manhattan_distance_to_next(highest[0], highest[1] + 1, highest[2] + 1):
                actions += ((highest[0], highest[1] + 1, highest[2] + 1), )

        return actions

    def result(self, state: NumbrixState, action):
        """ Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A acoo a executar deve ser uma
        das presentes na lista obtida pela execucao de 
        self.actions(state). """

        board = state.get_board()  

        new_board = copy.deepcopy(board)
        new_board.set_number(action[0], action[1], action[2])

        if action[2] < new_board.get_lowest_path_number()[2]:
            new_board.set_lowest_path_number(action[0], action[1], action[2])

        else:
            new_board.check_possible_filling(action)

        new_state = NumbrixState(new_board)

        return new_state

    def goal_test(self, state: NumbrixState):
        """ Retorna True se e so se o estado passado como argumento e
        um estado objetivo. Deve verificar se todas as posicoes do tabuleiro 
        estao preenchidas com uma sequencia de numeros adjacentes. """

        board = state.get_board()
        current_pos = board.get_lowest_path_number()

        if current_pos[2] != 1:
            return False
        else:
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

    start_time = time.time()

    inputFile = sys.argv[1]

    board = Board.parse_instance(inputFile)
    
    problem = Numbrix(board)

    goal_node = breadth_first_tree_search(problem)

    print(goal_node.state.get_board().to_string())

    print("--- %s seconds ---" % (time.time() - start_time))
