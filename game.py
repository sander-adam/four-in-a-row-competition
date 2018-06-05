'''
We are playing the classic 'four in a row' game. Two players (1/2, blue/red) play against each other. Player 1/blue start.
Chips can only be placed on the bottom of each column. First player to get four in a row (horizontally, vertically or 
diagonal) wins. 

Interface:

Rules:
'''
import pandas as pd
import numpy as np
import random

from agents import *

class InvalidMove(Exception):
    '''Raise for invalid moves'''
    pass


class FourInARow:
    def __init__(self, agents):
        self.board_width = 7
        self.col_range = range(self.board_width)
        self.board_height = 6
        self.row_range = range(self.board_height)
        self.board = pd.DataFrame(0, index = self.row_range, columns = self.col_range, dtype = 'uint8')
        self.winner = 0
        self.status = 'new' # Game status in [new, playing, finished, error]
        self.agents = agents

    def play(self):
        print('We are ready to play some FourInARow')
        self.status = 'playing'
        self.turn = 0

        while True:
            self.turn += 1

            print('Ready for turn {turn}')
            print(self.board)

            # Determine move
            player = (self.turn % 2) + 1
            agent = self.agents[player]
            column = agent.move(self)
            
            # Execute move
            print(f'Player {player} ({agent.name}) plays column {column}')
            if self.move(column=column, player=player):
                print(self.board)
                print(f'Player {player} ({agent.name}) wins after {self.turn} turns!!')
                break


    def move(self, *, player=None, column=None):
        '''Make a move '''
        assert column in list(range(7))
        assert player in [1,2]

        
        row = (self.board[column] == 0).sum() - 1
        if row < 0:
            raise InvalidMove 

        self.board.loc[row, column] = player
        return self.check_winner(player, column)

    def check_winner(self, player, column_index):
        '''Check whether the selected player has won'''
        added_chip_row = self.board[column_index].idxmax(player)
        
        dirs = (
            (0,1),
            (1,0),
            (1,1),
            (1, -1),
        )

        for row_dir, col_dir in dirs:
            row_length = 1

            row,col = added_chip_row, column_index,
            while True:
                row += row_dir
                col += col_dir
                if (row in self.row_range) and (col in self.col_range) and (self.board.loc[row, col] == player):
                    row_length += 1
                else:
                    break
            
            row,col = added_chip_row, column_index,
            while True:
                row -= row_dir
                col -= col_dir
                if (row in self.row_range) and (col in self.col_range) and (self.board.loc[row, col] == player):
                    row_length += 1
                else:
                    break

            if row_length >= 4:
                return True
        return False

    def legal_moves(self):
        return list(self.board.columns[self.board.loc[0] == 0])



agent1 = RandomMove()
agent2 = AllLeft()

game = FourInARow(agents = {1: agent1, 2: agent2})

game.play()
