# numbrix.py: Template para implementacao do projeto de Inteligencia Artificial 2021/2022.
# Devem alterar as classes e funcoes neste ficheiro de acordo com as instrucoes do enunciado.
# Alem das funcoes e classes ja definidas, podem acrescentar outras que considerem pertinentes.

# Grupo 26:
# 96858 Eduardo Duarte Silva Rangel Pamplona
# 96885 Jose Maria de Oliveira Soares Bonneville Franco

import string
import sys
import this
from search import Problem, Node, astar_search, breadth_first_tree_search, depth_first_tree_search, greedy_search, recursive_best_first_search


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

    # TODO: outros metodos da classe


class Board:
    """ Representacao interna de um tabuleiro de Numbrix. """

    def __init__(self, size: int, initial_positions):
        """ O construtor especifica o estado inicial. """
        self.lowest_path_number = None
        self.highest_path_number = None
        self.size = size
        self.positions = initial_positions

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

    def set_positions(self, positions) {
        self.positions = positions
    }

    def get_lowest_path_number(self) {
        return lowest_path_number
    }
    
    def get_highest_path_number(self) {
        return highest_path_number
    }

    def set_lowest_path_number(self, row: int, col: int, num: int) {
        self.lowest_path_number = (row, col, num)
    }

    def set_highest_path_number(self, row: int, col: int, num: int) {
        self.highest_path_number = (row, col, num)
    }

    def set_initial_lowest_path_number(self) {
        lowest = (None, None, self.size * self.size + 1)

        for row in range(size):
            for col in range(size):
                current_num = get_number(row, col)
                if current_num != 0 and current_num <= lowest:
                    lowest = (row, col, current_num)
                    
        self.lowest_path_number = lowest
    }

    def set_initial_highest_path_number(self) {
        highest = self.get_lowest_path_number()
        
        while True:
            (up, down) = adjacent_vertical_numbers(highest[0], highest[1])
            (left, right) = adjacent_horizontal_numbers(highest[0], highest[1])
            if up == highest[2] + 1:
                highest = (highest[0] - 1, highest[1], up)
            else if down == highest[2] + 1:
                highest = (highest[0] + 1, highest[1], down)
            else if left == highest[2] + 1:
                highest = (highest[0], highest[1] - 1, left)
            else if right == highest[2] + 1:
                highest = (highest[0], highest[1] + 1, right)
            else:
                break

        self.highest_path_number = highest
    }

    def check_set_straight_sequence(self, row: int, col: int) {
        root_num = (row, col, self.get_number(row, col))

        (up, down) = adjacent_vertical_numbers(root_num[0], root_num[1])
        (left, right) = adjacent_horizontal_numbers(root_num[0], root_num[1])

        for direction in range(4):
            if direction == 0: to_compare = up
            else if direction == 1: to_compare = down
            else if direction == 2: to_compare = left
            else: to_compare = right

            current_num = root_num
            candidate_positions = self.positions
            incrementer = 1
            
            
    
    @staticmethod    
    def parse_instance(filename: str):
        """ Le o ficheiro cujo caminho e passado como argumento e retorna
        uma instancia da classe Board. """

        with open(filename, 'r') as file:
            data = file.read()

        size = int(data[0])

        initial_positions = ()
        row = ()
        for item in data[2::]:
            if item != '\t' and item != '\n':
                row += (int(item), )
            if item == '\n':
                initial_positions += (row, )
                row = ()

        return Board(size, initial_positions)


    # TODO: outros metodos da classe

class Numbrix(Problem):
    def __init__(self, board: Board):
        """ O construtor especifica o estado inicial. """
        board.set_initial_lowest_path_number()
        board.set_initial_highest_path_number()
        self.initial_state = NumbrixState(board)
        pass

    def actions(self, state: NumbrixState):
        board = NumbrixState.get_board()
        lowest = board.get_lowest_path_number()
        highest = board.get_highest_path_number()
        actions = ()

        if lowest > 1:
            (up, down) = adjacent_vertical_numbers(lowest[0], lowest[1])
            (left, right) = adjacent_horizontal_numbers(lowest[0], lowest[1])
            if up == 0:
                actions += ((lowest[0] - 1, lowest[1], lowest[2] - 1), )
            if down == 0:   
                actions += ((lowest[0] + 1, lowest[1], lowest[2] - 1), )
            if left == 0:
                actions += ((lowest[0], lowest[1] - 1, lowest[2] - 1), )
            if right == 0:
                actions += ((lowest[0], lowest[1] + 1, lowest[2] - 1), )    
        else:
            (up, down) = adjacent_vertical_numbers(highest[0], highest[1])
            (left, right) = adjacent_horizontal_numbers(highest[0], highest[1])
            if up == 0:
                actions += ((highest[0] - 1, highest[1], highest[2] + 1), )
            if down == 0:   
                actions += ((highest[0] + 1, highest[1], highest[2] + 1), )
            if left == 0:
                actions += ((highest[0], highest[1] - 1, highest[2] + 1), )
            if right == 0:
                actions += ((highest[0], highest[1] + 1, highest[2] + 1), )

        return actions

    def result(self, state: NumbrixState, action):
        """ Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A acoo a executar deve ser uma
        das presentes na lista obtida pela execucao de 
        self.actions(state). """
        new_board = state.get_board()
        new_board.set_number(action[0], action[1], action[2])

        
        
        new_state = NumbrixState(new_board)

        return new_state

    def goal_test(self, state: NumbrixState):
        """ Retorna True se e so se o estado passado como argumento e
        um estado objetivo. Deve verificar se todas as posicoes do tabuleiro 
        estao preenchidas com uma sequencia de numeros adjacentes. """
        # TODO
        pass

    def h(self, node: Node):
        """ Funcao heuristica utilizada para a procura A*. """
        # TODO
        pass
    
    # TODO: outros metodos da classe


if __name__ == "__main__":
    # TODO:
    # Ler o ficheiro de input de sys.argv[1],
    inputFile = sys.argv[1]

    board = Board.parse_instance(inputFile)
    print(board.adjacent_vertical_numbers(1, 2))

    # Usar uma tecnica de procura para resolver a instancia,
    # Retirar a solucao a partir do no resultante,
    # Imprimir para o standard output no formato indicado.
