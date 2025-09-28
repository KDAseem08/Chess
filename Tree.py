import script
import copy
import chessAI
Vfrom chessAI import sync_piece_positions


class Node():
    def __init__(self,data, children = None):
        # data should be in form (Board(), eval(Board().getboard()))
        if (children == None):
            children = []
        self.data = data
        self.children = children
        self.minimax = None


def Expand(node: Node,colour_to_move):
    board_object = node.data[0]
    board_array = board_object.getboard()
    for legal_move in chessAI.GetAllLegalMoves(board_array,colour = colour_to_move):
        # Need to create a temp gme to check
        temp_game = copy_game(board_object, colour_to_move)
        if temp_game.play(move=legal_move):  # Use play to ensure all checks are performed
            node.children.append(
                Node(
                    data=[
                        copy_game(temp_game.board, temp_game.colour_to_move).board,
                        chessAI.eval(temp_game.get_board()),
                    ]
                )
            )


def expand_to_depth(node, depth, colour_to_move):
    if depth == 0:
        return
    Expand(node, colour_to_move)
    if not node.children:
        return
    next_colour = "Black" if colour_to_move == "White" else "White"
    for child in node.children:
        expand_to_depth(child, depth - 1, next_colour)


def copy_game(board_object, colour_to_move):
    """
    Create a deep copy of the game state, including the board and the colour to move.
    """
    new_board_array = copy.deepcopy(board_object.getboard())
    sync_piece_positions(new_board_array)
    new_game = script.ChessGame()
    new_game.board = script.Board(custom_position=new_board_array)
    new_game.colour_to_move = colour_to_move
    return new_game


def minimax(node,depth,maximising_player):
    # Credit to Sebastian Lague. Watched his minimax video and this implementation heavily relies on the shown pseudocode and recursive techniques.
    # Maximising_player is True if the colour of that player is White . False if colour is Black.
    if depth == 0 or not node.children:
        node.minimax = node.data[1]
        return node.data[1]
    
    if maximising_player:
        max_eval = float("-inf")
        for child in node.children:
            eval = minimax(child,depth - 1,False)
            max_eval = max(max_eval,eval)
        node.minimax = max_eval
        return max_eval
    else:
        min_eval = float("inf")
        for child in node.children:
            eval = minimax(child,depth - 1,True)
            min_eval = min(min_eval,eval)
        node.minimax = min_eval
        return min_eval

def GetBestMove(node,colour):
    if (node.children == []):
        return None
    if colour == "White":
        best_child = max(node.children, key=lambda child: child.minimax)
    else:
        best_child = min(node.children, key=lambda child: child.minimax)

    return best_child


def get_opp_col(col):
    if col == "White":
        return "Black"
    else:
        return "White"

# Lets try pitting two minimax bots against each other and checkout the first 5 moves
TestGame = script.ChessGame()
RootNode = Node(data=[TestGame.board, chessAI.eval(TestGame.get_board())])

print(f"Creating Tree")
expand_to_depth(RootNode, depth=3, colour_to_move=TestGame.colour_to_move)

print("------- depth 0 ------")
print(RootNode)

print("------- depth 1 ------")
print(len(RootNode.children))

print("------- depth 2 ------")
sum = 0 
depth2 = RootNode.children

list1 = []
for x in depth2:
    list1.extend(x.children)
    sum += len(x.children)
print(sum)




print("------depth 3 ------")
sum2 = 0
for node in list1:
    sum2 += len(node.children)
print(sum2)



count = 0
currentNode = RootNode
colour_to_move = "White"

# while(count != 3):
#     currentNode.data[0].drawboard()
#     best_child_node = GetBestMove(currentNode, colour=colour_to_move)
#     if best_child_node is None:
#         print(f"No valid moves for {colour_to_move}. Game over.")
#         break
#     colour_to_move = get_opp_col(colour_to_move)
#     currentNode = best_child_node
#     count += 1
