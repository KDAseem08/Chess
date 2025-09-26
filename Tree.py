import script
import copy
import chessAI


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
        temp_board_obj = copy.deepcopy(board_object)
        temp_board_obj.update_board(move = legal_move)
        node.children.append(Node(data = [temp_board_obj,chessAI.eval(temp_board_obj.getboard())]))
    

def expand_to_depth(node, depth, colour_to_move):
    if depth == 0:
        return
    Expand(node, colour_to_move)
    next_colour = "Black" if colour_to_move == "White" else "White"
    for child in node.children:
        expand_to_depth(child, depth - 1, next_colour)




def minimax(node,depth,maximising_player):
    # Credit to Sebastian Lague. Watched his minimax video and this implementation heavily relies on the shown pseudocode and recursive techniques.
    # Maximising_player is True if the colour of that player is White . False if colour is Black.
    if depth == 0 or (not node.children):
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
    
def GetBestMove(node,children,colour):
    if (node.children == []):
        return None
    if colour == "White":
        
        best_child = max(node.children, key=lambda child: child.minimax)
    else:
        best_child = min(node.children, key=lambda child: child.minimax)

    return best_child

        

TestGame = script.ChessGame()
RootNode = Node(data=[TestGame.board, chessAI.eval(TestGame.get_board())])
expand_to_depth(RootNode, depth=5, colour_to_move=TestGame.colour_to_move)

# Now you can run minimax:
score = minimax(RootNode, depth=5, maximising_player=True)
print("Best score for White:", score)

#Lets try pitting two minimax bots against each other and checkout the first 5 moves
count = 0 
currentNode = RootNode


    
