Plays tic-tac-toe on a three-by-three board


Run a new game with:

    python -m runner.py


To add a new bot, create a subclass of main.Bot and add it to
BOTS_PLAYING at the top of runner.py here:

    BOTS_PLAYING = {Bot.PLAYER_1: new-bot-to-play-as-x,
                    Bot.PLAYER_2: Bots.RandomChoice()}


The __call__ method of each bot receives a nine-member tuple,
(0, 1, 2, 3, 4, 5, 6, 7, 8), representing the board,

+---+---+---+
| 0 | 1 | 2 |
+---+---+---+
| 3 | 4 | 5 |
+---+---+---+
| 6 | 7 | 8 |
+---+---+---+

where each 0, 1, 2, 3, 4, 5, 6, 7, 8 equals either:

'x' player-1 has placed an 'x' in this cell,
'o' player-2 has placed an 'o' in this cell or
'' neither player has placed a symbol in this cell;

and a symbol, either 'x' or 'o', telling the bot whether it
plays as player-1 or player-2:

'x' player-1,
'o' player-2.


It should return the index of the cell where the bot will
play its move: the integer 0 for cell-0, the integer 1 for
cell-1, etc.


For example, receiving the tuple,
('', '', 'x', '', 'x', 'x', '', 'o', 'o'),
representing the board,

   |   | x
---+---+---
   | x | x
---+---+---
   | o | o

and the symbol 'x', telling it it plays as player-1, a bot might
return the integer 6 to play to the bottom, leftmost cell and win


You can force one or both players to play random moves on certain
turns by sending a sequence of turn numbers, which start at 0, to
runner.py's play method. For example, to force a random move on
the first turn change the last line of runner.py
under "if __name__ == '__main__':" to

play([0,])