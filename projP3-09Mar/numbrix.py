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
        
    # TODO: outros metodos da classe


class Board:
    """ Representacao interna de um tabuleiro de Numbrix. """

    def __init__(self, size: int, initial_positions):
        """ O construtor especifica o estado inicial. """
        self.size = size
        self.positions = initial_positions

    def get_number(self, row: int, col: int):
        """ Devolve o valor na respetiva posicao do tabuleiro. """
        return self.positions[row][col]
    
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
    
    def adjacent_horizontal_numbers(self, row: int, col: int) -> (int, int):
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
        # TODO
        pass

    def actions(self, state: NumbrixState):
        """ Retorna uma lista de acoes que podem ser executadas a
        partir do estado passado como argumento. """
        # TODO
        pass

    def result(self, state: NumbrixState, action):
        """ Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A acoo a executar deve ser uma
        das presentes na lista obtida pela execucao de 
        self.actions(state). """
        # TODO
        pass

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
