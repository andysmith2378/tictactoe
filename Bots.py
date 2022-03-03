import main
import random


class FirstOpen(main.Bot):
    pass


class RandomChoice(main.Bot):
    def __call__(self, board, player):
        return random.choice(RandomChoice.opencells(board))

    @staticmethod
    def opencells(board):
        return [ind for ind, member in enumerate(board) if member == '']


class Immediate(RandomChoice):
    def __call__(self, board, player):
        move = self.threeinarow(board, player)
        if move is None:
            return RandomChoice.__call__(self, board, player)
        return move

    def threeinarow(self, boardtuple, player):
        enemy = Immediate.fetchEnemy(player)
        block = None
        for candidate in RandomChoice.opencells(boardtuple):
            boardlist            = list(boardtuple)
            boardlist[candidate] = player
            if main.checkforwin(boardlist, player, main.Bot.THREE_IN_A_ROW):
                return candidate
            boardlist[candidate] = enemy
            if main.checkforwin(boardlist, enemy, main.Bot.THREE_IN_A_ROW):
                block = candidate
        return block

    @staticmethod
    def fetchEnemy(player):
        if player == main.Bot.PLAYER_1:
            return main.Bot.PLAYER_2
        return main.Bot.PLAYER_1


class Pairs(Immediate):
    TWO_TWO_IN_A_ROW = (((1, 2), (3, 6), (4, 8),         ),
                        ((4, 7), (0, 2),                 ),
                        ((0, 1), (5, 8), (4, 6),         ),
                        ((0, 6), (4, 5),                 ),
                        ((0, 8), (3, 5), (2, 6), (1, 7), ),
                        ((3, 4), (2, 8),                 ),
                        ((0, 3), (2, 4), (7, 8),         ),
                        ((1, 4), (6, 8),                 ),
                        ((6, 7), (0, 4), (2, 5),         ),)
    PREFERENCES      = (4, 0, 2, 6, 8, 1, 3, 5, 7)

    def __call__(self, board, player):
        move = self.threeinarow(board, player)
        if move is None:
            enemy = Immediate.fetchEnemy(player)
            block = None
            for centre, placeTuple in enumerate(Pairs.TWO_TWO_IN_A_ROW):
                if board[centre] == '':
                    for n, (first, second) in enumerate(placeTuple[:-1]):
                        occupants = board[first], board[second]
                        if '' in occupants:
                            if player in occupants:
                                if self.checkForSecond(board, n, placeTuple, player):
                                    return centre
                            if enemy in occupants:
                                if self.checkForSecond(board, n, placeTuple, enemy):
                                    block = centre
            if block is None:
                options = RandomChoice.opencells(board)
                for favourite in Pairs.PREFERENCES:
                    if favourite in options:
                        return favourite
                return main.Bot.__call__(self, board, player)
            return block
        return move

    def checkForSecond(self, board, indx, placeTuple, target):
        for left, right in placeTuple[indx+1:]:
            occupants = board[left], board[right]
            if ('' in occupants) and (target in occupants):
                return True
        return False


class Arborist(Immediate):
    RANGES = [range(9 - m) for m in range(10)]

    def __init__(self):
        Immediate.__init__(self)
        self.boards = [[''] * 9] * 10
        self.opensquares = [list(range(9))] * 10
        self.tree = [{}, tuple(self.boards[0])]
        self.branch(self.tree)
        self.bestmove = {main.Bot.PLAYER_1: {}, main.Bot.PLAYER_2: {}}
        self.evaluate(self.tree, main.Bot.PLAYER_1, main.Bot.PLAYER_1)
        self.evaluate(self.tree, main.Bot.PLAYER_2, main.Bot.PLAYER_1)

    def evaluate(self, subtree, player, turn):
        opponent = Immediate.fetchEnemy(player)
        if main.checkforwin(subtree[1], player):
            return player
        if main.checkforwin(subtree[1], opponent):
            return opponent
        if isinstance(subtree[0], list):
            return ''
        if player == turn:
            return self.playerturn(opponent, player, subtree)
        return self.opponentturn(opponent, player, subtree)

    def branch(self, subtree, depth=0, maxDepth=8):
        for crossindex in Arborist.RANGES[depth]:
            cross = self.opensquares[depth][crossindex]
            outcome, position = self.bud(depth, cross, crossindex, main.Bot.PLAYER_1)
            if outcome or depth >= maxDepth:
                subtree[0][cross] = [self.boards[depth+1], position]
            else:
                subtree[0][cross] = [{}, position]
                for noughtindex in Arborist.RANGES[depth+1]:
                    nought = self.opensquares[depth+1][noughtindex]
                    outcome, position = self.bud(depth+1, nought, noughtindex, main.Bot.PLAYER_2)
                    if outcome or depth >= maxDepth:
                        subtree[0][cross][0][nought] = [self.boards[depth+2], position]
                    else:
                        subtree[0][cross][0][nought] = [{}, position]
                        self.branch(subtree[0][cross][0][nought], depth+2)

    def bud(self, depth, move, rank, player):
        self.boards[depth+1] = self.boards[depth][:move] + [player] + self.boards[depth][move+1:]
        position = tuple(self.boards[depth+1])
        if main.checkforwin(self.boards[depth+1], player):
            return True, position
        self.opensquares[depth+1] = self.opensquares[depth][:rank] + self.opensquares[depth][rank+1:]
        return False, position

    def opponentturn(self, opponent, player, subtree):
        bestresult = player
        for move, branch in subtree[0].items():
            valueofbranch = self.evaluate(branch, player, player)
            if valueofbranch == opponent:
                bestresult = opponent
            elif valueofbranch == '':
                if bestresult == player:
                    bestresult = ''
        return bestresult

    def playerturn(self, opponent, player, subtree):
        bestmove = random.choice(list(subtree[0].keys()))
        bestresult = opponent
        for move, branch in subtree[0].items():
            valueofbranch = self.evaluate(branch, player, opponent)
            if valueofbranch == '':
                if bestresult == opponent:
                    bestresult = ''
                    bestmove = move
            elif valueofbranch == player:
                bestresult = player
                bestmove = move
        self.bestmove[player][subtree[1]] = bestmove
        return bestresult

    def __call__(self, board, player):
        return self.bestmove[player][board]
