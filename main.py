import copy
import Engine 
import HelperMethods
from HelperMethods import evaluate_position
from HelperMethods import sync_piece_positions
import graphical_interface



class Node():
    def __init__(self,game,eval_score = None, children = None):
        if (children == None):
            children = []
        self.game = game
        self.eval_score = eval_score
        self.children = children


def Expand(node: Node):
    board_object = node.game.board
    board_array = board_object.getboard()
    colour_to_move = node.game.colour_to_move
    for legal_move in HelperMethods.GetAllLegalMoves(board_array,colour = colour_to_move):
        # Need to create a temp game to check
        temp_game = copy_game(board_object, colour_to_move)
        if temp_game.play(move=legal_move):  # Use play to ensure all checks are performed
            node.children.append(Node(game=temp_game))


def expand_to_depth(node, depth):
    if depth == 0:
        return
    Expand(node)
    if not node.children:
        return
    for child in node.children:
        expand_to_depth(child, depth - 1)


def copy_game(board_object, colour_to_move):
    """
    Create a deep copy of the game state, including the board and the colour to move.
    """
    new_board_array = copy.deepcopy(board_object.getboard())
    sync_piece_positions(new_board_array)
    new_game = Engine.ChessGame()
    new_game.board = Engine.Board(custom_position=new_board_array)
    new_game.colour_to_move = colour_to_move
    return new_game


def minimax(node,depth,maximising_player):
    # Maximising_player is True if the colour of that player is White . False if colour is Black.
    if depth == 0 or not node.children:
        node.eval_score = evaluate_position(node.game, node.game.colour_to_move)
        return node.eval_score

    if maximising_player:
        max_eval = float("-inf")
        for child in node.children:
            eval = minimax(child,depth - 1,False)
            max_eval = max(max_eval,eval)
        node.eval_score = max_eval
        return max_eval
    else:
        min_eval = float("inf")
        for child in node.children:
            eval = minimax(child,depth - 1,True)
            min_eval = min(min_eval,eval)
        node.eval_score = min_eval
        return min_eval

def GetBestMove(node,colour):
    if (node.children == []):
        return None
    if any(child.eval_score is None for child in node.children):
        raise ValueError("Some child nodes have no minimax value set!")
    if colour == "White":
        best_child = max(node.children, key=lambda child: child.eval_score)
    else:
        best_child = min(node.children, key=lambda child: child.eval_score)

    return best_child


def get_opp_col(col):
    if col == "White":
        return "Black"
    else:
        return "White"

# Lets try pitting two minimax bots against each other and checkout the first 5 moves
TestGame = Engine.ChessGame()

# print(f"Creating Tree")
# expand_to_depth(RootNode, depth=3, colour_to_move=TestGame.colour_to_move)

# # Call minimax to calculate minimax values for all nodes
# print("Running minimax...")
# minimax(RootNode, depth=3, maximising_player=True)

count = 0
colour_to_move = "White"

# I play White , the bot plays black .
while (True):

    if TestGame.colour_to_move == "White":

        # Get Human move
        x = input("Enter move (eg: 'e2-e4'): ")
        move = graphical_interface.parse_algebraic(x)
        if move:
            TestGame.play(move)
            count += 1
            # I also need to update the currentNode
            # I have the current node and the move and so I need to play the move and check if any of the chidrens board state matches.
            #match = None

            # for child in currentNode.children:
            #     #print("Child node board states:")
            #     # for child in currentNode.children:
            #     #     child.data[0].drawboard()
            #     #     print("--------------------------------------")
            #     if child.data[0].getboard() == TestGame.board.getboard():
            #         match = child
            #         currentNode = match
            #         break

            # if match is None:
            #     print("Error: No matching child node found!")
            #     break

        else:
            print("Invalid Move format")
            continue

        if TestGame.is_checkmate("Black"):
            print("White wins!")
            print("Checkmate board state:")
            TestGame.board.drawboard()
            print("---------------------------------------------------------")
            break
    else:
        # Now from current node , expand to depth 3 and fill it with minimax
        print("Bot thinking")
        #score = evaluate_position(TestGame, TestGame.colour_to_move)
        currentNode = Node(game=TestGame)
        expand_to_depth(currentNode, depth=2)


        # Call minimax to calculate minimax values for all nodes
        minimax(currentNode, depth=2, maximising_player=False)

        print("-------Depth 1 Children --------")
        for child in currentNode.children:
            print(f"Child eval: {child.eval_score}")
            child.game.board.drawboard()
            print("---------------------------------------------------------")

        print("-------End of Depth 1 Children --------")
        
        best_child = GetBestMove(currentNode, TestGame.colour_to_move)
        if best_child is None:
            print(f"No valid moves for {TestGame.colour_to_move}. Game over.")
            break

        TestGame = best_child.game
        count += 1

        if TestGame.is_checkmate("White"):
            print("Black wins!")
            print("Checkmate board state:")
            TestGame.board.drawboard()
            print("---------------------------------------------------------")
            break

    TestGame.board.drawboard()
    print("---------------------------------------------------------")

    # When trained till depth n , n moves can be played before the bot has no more children to reach to
    # White plays ceil (n/2) mvoes
