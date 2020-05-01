import numpy as np

class AIPlayer:
    def __init__(self, player_number):
        self.player_number = player_number
        self.type = 'ai'
        self.player_string = 'Player {}:ai'.format(player_number)


    def valid_loc(row, col):
            return board[row][col] == 0

    def valid_check(self, board):
        valid = []
        for row in range(6):
            for col in range(7):
                if  board[row][col] == 0:
                    valid.append([row, col])
                    break
        return valid

    def opp_number(self,player_num):
        if (player_num == 1): 
            return 2
        else: 
            return 1


    def game_completed_count(self, board, player_num, depth):
        player_win_str = ('{0}' * depth).format(player_num)
        to_str = lambda a: ''.join(a.astype(str))

        def check_horizontal(b):
            total = 0
            for row in b:
                if player_win_str in to_str(row):
                    total += to_str(row).count(player_win_str) 
            return total

        def check_verticle(b):
            return check_horizontal(b.T)

        def check_diagonal(b):
            total = 0 
            for op in [None, np.fliplr]:
                op_board = op(b) if op else b
                root_diag = np.diagonal(op_board, offset=0).astype(np.int)
                if player_win_str in to_str(root_diag):
                    total += to_str(root_diag).count(player_win_str) 

                for i in range(1, b.shape[1]-3):
                    for offset in [i, -i]:
                        diag = np.diagonal(op_board, offset=offset)
                        diag = to_str(diag.astype(np.int))
                        if player_win_str in diag:
                            total += diag.count(player_win_str) 
            return total 
    
        return check_horizontal(board) + check_verticle(board) + check_diagonal(board)


    def game_completed(self,board, player_num):
        player_win_str = '{0}{0}{0}{0}'.format(player_num)
        #board = self.board
        to_str = lambda a: ''.join(a.astype(str))

        def check_horizontal(b):
            for row in b:
                if player_win_str in to_str(row):
                    return True
            return False

        def check_verticle(b):
            return check_horizontal(b.T)

        def check_diagonal(b):
            for op in [None, np.fliplr]:
                op_board = op(b) if op else b
                
                root_diag = np.diagonal(op_board, offset=0).astype(np.int)
                if player_win_str in to_str(root_diag):
                    return True

                for i in range(1, b.shape[1]-3):
                    for offset in [i, -i]:
                        diag = np.diagonal(op_board, offset=offset)
                        diag = to_str(diag.astype(np.int))
                        if player_win_str in diag:
                            return True

            return False

        return (check_horizontal(board) or
                check_verticle(board) or
                check_diagonal(board))


    def get_alpha_beta_move(self, board):

        def minVal(board,alpha,beta,depth,player, opponent):
            if depth == 5:
                return (self.evaluation_function(board))
            elif not self.valid_check(board):
                return (self.evaluation_function(board))
            else: 
                for row,col in self.valid_check(board):
                    board[row][col] = opponent 
                    result = maxVal(board, alpha, beta, depth+1, player, opponent)
                    beta = min (beta, result)
                    board[row][col] = 0
                    if beta<= alpha:
                        return beta 
                return beta


        def maxVal(board,alpha, beta, depth, player, opponent):
            if depth == 5:
                return (self.evaluation_function(board))
            elif not self.valid_check(board):
                return (self.evaluation_function(board))
            else: 
                for row, col in self.valid_check(board):
                    board[row][col] = player 
                    result = minVal(board,alpha,beta,depth+1, player, opponent)
                    v = max(alpha, result)
                    board[row][col] = 0
                    if v >= beta:
                        return v
                return v


        opponent = self.opp_number(self.player_number)

        board_values = []
        for row, col in self.valid_check(board):
            board[row][col] = self.player_number
            v = max(-1000000000, minVal(board,-1000000000, +1000000000, 1 , self.player_number, opponent))
            board[row][col] = 0
            board_values.append((v,col))
            maxvalueTuple = max(board_values,key=lambda board_values: board_values[1])

        maxVal = maxvalueTuple[0]
        for elem in board_values:
                if maxVal in elem:
                    max_index = elem
                    break

        return max_index[1]
        raise NotImplementedError('Whoops I don\'t know what to do')

    def get_expectimax_move(self, board):
        """
        Given the current state of the board, return the next move based on
        the expectimax algorithm.

        This will play against the random player, who chooses any valid move
        with equal probability

        INPUTS:
        board - a numpy array containing the state of the board using the
                following encoding:
                - the board maintains its same two dimensions
                    - row 0 is the top of the board and so is
                      the last row filled
                - spaces that are unoccupied are marked as 0
                - spaces that are occupied by player 1 have a 1 in them
                - spaces that are occupied by player 2 have a 2 in them

        RETURNS:
        The 0 based index of the column that represents the next move
        """
        def prob(board,val):
            total = val / len(self.evaluation_function(board))
            return total

        def max_val(board, depth, player,opponent):
            if not self.valid_check(board):
                return (self.evaluation_function(board))
            elif (depth == 5): 
                return (self.evaluation_function(board))
            else:
                for boardLocation in self.valid_check(board):
                    board[boardLocation[0]][boardLocation[1]] = player 
                    val = exp_val(board, depth + 1, player, opponent)
                    highestVal = max(-100000, val);
                return highestVal

        def exp_val(board, depth, player, opponent): 
            if not self.valid_check(board):
                return (self.evaluation_function(board))
            elif (depth == 5): 
                return (self.evaluation_function(board))
            else:
                val = 0
                for boardLocation in self.evaluation_function(board):
                    board[boardLocation[0]][boardLocation[1]] = opponent 
                    val += max_val(board , depth+1, player, opponent)

                probability = prob(val)
                return probability

        player = self.player_number
        opponent = self.opp_number(self.player_number)

        actions = []
        depth = 0

        if not self.valid_check(board):
            return self.evaluation_function(board)

        for boardLocation in self.valid_check(board):
            board[boardLocation[0]][boardLocation[1]] = player
            val = max(- 1000000, exp_val(board,depth + 1 , player, opponent))
            action = (val,col)
            actions.append(action)
            board[boardLocation[0]][boardLocation[1]] = 0

        maxTuple = max(values,key=lambda values: values[1]) 
        maxVal = maxTuple[0]

        for item in values:
            if maxVal in item:
                index = item[1]
                break

        return index

        raise NotImplementedError('Whoops I don\'t know what to do') 

    def evaluation_function(self, board):

        opponent = self.opp_number(self.player_number)

        player_depth4 = self.game_completed_count( board, self.player_number, 4)
        player_depth3 = self.game_completed_count( board, self.player_number, 3)
        player_depth2 = self.game_completed_count( board, self.player_number, 2)

        opponent_depth4 = self.game_completed_count( board, opponent, 4) 
        opponent_depth3 = self.game_completed_count( board, opponent, 3) 
        opponent_depth2 = self.game_completed_count( board, opponent, 2)

        player_depth4 *= 60
        player_depth3 *= 25
        player_depth2 *= 10

        opponent_depth4 *= 60
        opponent_depth3 *= 25
        opponent_depth2 *= 10

        return (player_depth4+player_depth3+player_depth2) - (opponent_depth4+opponent_depth3+opponent_depth2)


class RandomPlayer:
    def __init__(self, player_number):
        self.player_number = player_number
        self.type = 'random'
        self.player_string = 'Player {}:random'.format(player_number)

    def get_move(self, board):
        """
        Given the current board state select a random column from the available
        valid moves.

        INPUTS:
        board - a numpy array containing the state of the board using the
                following encoding:
                - the board maintains its same two dimensions
                    - row 0 is the top of the board and so is
                      the last row filled
                - spaces that are unoccupied are marked as 0
                - spaces that are occupied by player 1 have a 1 in them
                - spaces that are occupied by player 2 have a 2 in them

        RETURNS:
        The 0 based index of the column that represents the next move
        """
        valid_cols = []
        for col in range(board.shape[1]):
            if 0 in board[:,col]:
                valid_cols.append(col)

        return np.random.choice(valid_cols)


class HumanPlayer:
    def __init__(self, player_number):
        self.player_number = player_number
        self.type = 'human'
        self.player_string = 'Player {}:human'.format(player_number)

    def get_move(self, board):
        """
        Given the current board state returns the human input for next move

        INPUTS:
        board - a numpy array containing the state of the board using the
                following encoding:
                - the board maintains its same two dimensions
                    - row 0 is the top of the board and so is
                      the last row filled
                - spaces that are unoccupied are marked as 0
                - spaces that are occupied by player 1 have a 1 in them
                - spaces that are occupied by player 2 have a 2 in them

        RETURNS:
        The 0 based index of the column that represents the next move
        """

        valid_cols = []
        for i, col in enumerate(board.T):
            if 0 in col:
                valid_cols.append(i)

        move = int(input('Enter your move: '))

        while move not in valid_cols:
            print('Column full, choose from:{}'.format(valid_cols))
            move = int(input('Enter your move: '))

        return move

