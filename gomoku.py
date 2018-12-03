
def is_empty(board):
    
    count = 0
    for sublists in board:
        for elements in sublists:
            if elements == " " :
                count += 1
    if count == 64:
        return True
    else:
        return False
    
def test_is_bounded():
    board = make_empty_board(8)
    x = 6; y = 2; d_x = -1 ; d_y = 1; length = 2
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    print_board(board)
    
    y_end = 3
    x_end = 5

    if is_bounded(board, y_end, x_end, length, d_y, d_x) == 'SEMIOPEN':
        print("TEST CASE for is_bounded PASSED")
    else:
        print("TEST CASE for is_bounded FAILED")


def is_bounded(board, y_end, x_end, length, d_y, d_x):


    count_empty = 0
    count_other = 0
    
    if (x_end*d_x)  == 7 or (y_end*d_y) == 7:
        count_other +=1
    else:
        
        if board[y_end+ d_y][x_end + d_x] == " ":
            count_empty +=1
        else:
            count_other +=1
            
    if (x_end-length*d_x) +1 == 0 or (y_end - length*d_y)+1 == 0:
        count_other +=1
    elif (x_end-length*d_x)  > 7 or (y_end - length*d_y) > 7:  
        count_other +=1  
    else:
        if board[y_end - (length*d_y)][x_end - (length* d_x)] == " ":
            count_empty +=1
        elif board[y_end - (length*d_y)][x_end - (length* d_x)] != " ":
            count_other +=1


    if count_empty == 1 and count_other == 1:
        return "SEMIOPEN"
        
    if count_empty == 0 and count_other == 2:
        return "CLOSED"
        
    if count_empty == 2 and count_other == 0:
        return "OPEN"


def test_detect_row():
    board = make_empty_board(8)
    x = 3; y = 3; d_x = 1; d_y = 1; length = 5
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")

    print_board(board)
    if detect_row(board, "w", 0,0,length,d_y,d_x) == (0,1):
        print("TEST CASE for detect_row PASSED")
    else:
        print("TEST CASE for detect_row FAILED")
        
  
def is_in_board(board, y, x):
    
    return 0<=y<len(board) and 0 <=x<len(board[0])
    
def detect_row(board, col, y_start, x_start, length, d_y, d_x):

    open_seq_count = 0
    semi_open_seq_count= 0
    j = 0
    i = 0
    while y_start + i*d_y < 8 and x_start + i*d_x < 8 :
        if board[y_start + i*d_y][x_start + i*d_x] == col:
            
            if j == length-1:
                if y_start + i*d_y == 7 or x_start + i*d_x == 7 :
                    if is_bounded(board, y_start + i*d_y , i*d_x + x_start , length, d_y, d_x)== "OPEN":
                        open_seq_count +=1
                        
                    elif is_bounded(board, y_start + i*d_y  , i*d_x + x_start , length, d_y, d_x)== "SEMIOPEN":
                        semi_open_seq_count += 1
                elif is_in_board(board, y_start + (i+1)*d_y, x_start + (1+i)*d_x) and board[y_start + (i+1)*d_y][x_start + (i+1)*d_x] != col:
                
                    if is_bounded(board, y_start + i*d_y , i*d_x + x_start , length, d_y, d_x)== "OPEN":
                        open_seq_count +=1
                        
                    elif is_bounded(board, y_start + i*d_y  , i*d_x + x_start , length, d_y, d_x)== "SEMIOPEN":
                        semi_open_seq_count += 1
            j +=1
        else:
            j = 0
        i += 1

    return open_seq_count, semi_open_seq_count

    
def detect_row_closed(board, col, y_start, x_start, length, d_y, d_x):

    close_seq_count = 0

    j = 0
    i = 0
    while y_start + i*d_y < 8 and x_start + i*d_x < 8 :
        if board[y_start + i*d_y][x_start + i*d_x] == col:
            
            if j == length-1:
                if y_start + i*d_y == 7 or x_start + i*d_x == 7 :
                    
                    if is_bounded(board, y_start + i*d_y , i*d_x + x_start , length, d_y, d_x)== "CLOSED":
                        close_seq_count +=1

                        
                elif is_in_board(board, y_start + (i+1)*d_y, x_start + (1+i)*d_x) and board[y_start + (i+1)*d_y][x_start + (i+1)*d_x] != col:
                
                    if is_bounded(board, y_start + i*d_y , i*d_x + x_start , length, d_y, d_x)== "CLOSED":
                        close_seq_count +=1

                    
            j +=1
        else:
            j = 0
        i += 1
    return close_seq_count

def detect_rows_closed(board, col, length):
    close_seq_count = 0
    i = 0
    
    while i < 8 :
        
        close_seq_count += detect_row_closed(board, col,  i, 0 , length, 0, 1)
        
        close_seq_count += detect_row_closed(board, col,  0, i , length, 1, 0)
        
        if i == 0:
            close_seq_count += detect_row_closed(board, col,  0, i , length, 1, 1)

        else:
            close_seq_count += detect_row_closed(board, col,  0, i , length, 1, 1)

            close_seq_count += detect_row_closed(board, col,  i, 0 , length, 1, 1)

        if i !=7:
            close_seq_count += detect_row_closed(board, col,  0, i , length, 1, -1)

            close_seq_count += detect_row_closed(board, col,  i, 7 , length, 1, -1)

        i+=1
    
    return close_seq_count
        
def test_detect_rows():
    
    board = make_empty_board(8)
    x = 7; y = 0; d_x = -1; d_y = 1; length = 3; col = 'w'
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    print_board(board)
    
    if detect_rows(board, col,length) == (1,0):
        print("TEST CASE for detect_rows PASSED")
    else:
        print("TEST CASE for detect_rows FAILED")
        
           
def detect_rows(board, col, length):
    open_seq_count, semi_open_seq_count = 0, 0
    i = 0
    
    while i < 8 :
        
        open_seq_count += detect_row(board, col,  i, 0 , length, 0, 1)[0]
        semi_open_seq_count += detect_row(board, col,  i, 0 , length, 0 ,1)[1]
        
        open_seq_count += detect_row(board, col,  0, i , length, 1, 0)[0]
        semi_open_seq_count += detect_row(board, col,  0, i , length, 1 ,0)[1]
        
        
        if i == 0:
            open_seq_count += detect_row(board, col,  0, i , length, 1, 1)[0]
            semi_open_seq_count += detect_row(board, col,  0, i , length, 1 ,1)[1]
        else:
            open_seq_count += detect_row(board, col,  0, i , length, 1, 1)[0]
            semi_open_seq_count += detect_row(board, col,  0, i , length, 1 ,1)[1]
            open_seq_count += detect_row(board, col,  i, 0 , length, 1, 1)[0]
            semi_open_seq_count += detect_row(board, col, i, 0 , length, 1 ,1)[1]
        
        if i !=7:
            open_seq_count += detect_row(board, col,  0, i , length, 1, -1)[0]
            semi_open_seq_count += detect_row(board, col,  0, i , length, 1 ,-1)[1]
            open_seq_count += detect_row(board, col,  i, 7 , length, 1, -1)[0]
            semi_open_seq_count += detect_row(board, col, i, 7 , length, 1 ,-1)[1]
        i+=1
    

    return open_seq_count, semi_open_seq_count

def test_search_max():
    board = make_empty_board(8)
    x = 5; y = 0; d_x = 0; d_y = 1; length = 4; col = 'w'
    put_seq_on_board(board, y, x, d_y, d_x, length, col)
    x = 6; y = 0; d_x = 0; d_y = 1; length = 4; col = 'b'
    put_seq_on_board(board, y, x, d_y, d_x, length, col)
    
    print_board(board)
    
    if search_max(board) == (4,6):
        print("TEST CASE for search_max PASSED")
    else:
        print("TEST CASE for search_max FAILED")
    
def get_free_squares(board):
    free_y = []
    free_x = []
    for i in range(8):
        for j in range(8):
            if board[i][j] == " ":
                free_y.append(i)
                free_x.append(j)
    return free_y, free_x

def search_max(board):
    move_y = 0
    move_x = 0
    max_val = -100000

    y = get_free_squares(board)[0]
    x = get_free_squares(board)[1]
    for i in range(len(y)):
        board[y[i]][x[i]] = "b"
        if score(board) > max_val :
            max_val = score(board)
            move_y = y[i]
            move_x = x[i]
        board[y[i]][x[i]] = " "     

    return move_y, move_x

def score(board):
    MAX_SCORE = 100000
    
    open_b = {}
    semi_open_b = {}
    open_w = {}
    semi_open_w = {}
    
    for i in range(2, 6):
        open_b[i], semi_open_b[i] = detect_rows(board, "b", i)
        open_w[i], semi_open_w[i] = detect_rows(board, "w", i)
        
    
    if open_b[5] >= 1 or semi_open_b[5] >= 1:
        return MAX_SCORE
    
    elif open_w[5] >= 1 or semi_open_w[5] >= 1:
        return -MAX_SCORE
        
    return (-10000 * (open_w[4] + semi_open_w[4])+ 
            500  * open_b[4]                     + 
            50   * semi_open_b[4]                + 
            -100  * open_w[3]                    + 
            -30   * semi_open_w[3]               + 
            50   * open_b[3]                     + 
            10   * semi_open_b[3]                +  
            open_b[2] + semi_open_b[2] - open_w[2] - semi_open_w[2])
            
def draw_is_win(board):
    frees = 0
    
    for i in range(8):
        for j in range(8):
            if board[i][j] == " ":
                frees +=1
    return frees
    
def is_win(board):
    
    for i in range(6,8):
        if detect_rows_closed(board, "b", i) >= 1:
            return "Continue playing"

        elif detect_rows(board, "b",i)[0] >= 1:
            return "Continue playing"

        elif detect_rows(board, "b",i)[1] >= 1:
            return "Continue playing"
    
        elif  detect_rows_closed(board, "w", i) == 1:
            return "Continue playing"
        
        elif  detect_rows(board, "w", i)[0] == 1:
            return "Continue playing"
        elif  detect_rows(board, "w", i)[1] == 1:
            return "Continue playing"
        
    if draw_is_win(board) == 0:
        return "Draw"
               
    elif  detect_rows_closed(board, "b", 5) == 1:
        return "Black won"
    elif detect_rows(board, "b",5)[0] == 1:
        return "Black won"
    elif detect_rows(board, "b",5)[0] == 1:
        return "Black won"
    elif detect_rows(board, "b",5)[1] == 1:
        return "Black won"
    
    elif  detect_rows_closed(board, "w", 5) == 1:
        return "White won"
    elif  detect_rows(board, "w", 5)[0] == 1:
        return "White won"
    elif  detect_rows(board, "w", 5)[1] == 1:
        return "White won"
        
    else:
        return "Continue playing"

def print_board(board):
    
    s = "*"
    for i in range(len(board[0])-1):
        s += str(i%10) + "|"
    s += str((len(board[0])-1)%10)
    s += "*\n"
    
    for i in range(len(board)):
        s += str(i%10)
        for j in range(len(board[0])-1):
            s += str(board[i][j]) + "|"
        s += str(board[i][len(board[0])-1]) 
    
        s += "*\n"
    s += (len(board[0])*2 + 1)*"*"
    
    print(s)
    

def make_empty_board(sz):
    board = []
    for i in range(sz):
        board.append([" "]*sz)
    return board
                


def analysis(board):
    for c, full_name in [["b", "Black"], ["w", "White"]]:
        print("%s stones" % (full_name))
        for i in range(2, 6):
            open, semi_open = detect_rows(board, c, i);
            print("Open rows of length %d: %d" % (i, open))
            print("Semi-open rows of length %d: %d" % (i, semi_open))


def play_gomoku(board_size):
    board = make_empty_board(board_size)
    board_height = len(board)
    board_width = len(board[0])
    
    while True:
        print_board(board)
        if is_empty(board):
            move_y = board_height // 2
            move_x = board_width // 2
        else:
            move_y, move_x = search_max(board)
            
        print("Computer move: (%d, %d)" % (move_y, move_x))
        board[move_y][move_x] = "b"
        print_board(board)
        analysis(board)
        
        game_res = is_win(board)
        if game_res in ["White won", "Black won", "Draw"]:
            return game_res
            

        print("Your move:")
        move_y = int(input("y coord: "))
        move_x = int(input("x coord: "))
        board[move_y][move_x] = "w"
        print_board(board)
        analysis(board)
        
        game_res = is_win(board)
        if game_res in ["White won", "Black won", "Draw"]:
            return game_res
        
def put_seq_on_board(board, y, x, d_y, d_x, length, col):
    for i in range(length):
        board[y][x] = col        
        y += d_y
        x += d_x
        
def some_tests():
    board = make_empty_board(8)

    board[0][5] = "w"
    board[0][6] = "b"
    y = 5; x = 2; d_x = 0; d_y = 1; length = 3
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    print_board(board)
    analysis(board)
    
    # Expected output:
    #       *0|1|2|3|4|5|6|7*
    #       0 | | | | |w|b| *
    #       1 | | | | | | | *
    #       2 | | | | | | | *
    #       3 | | | | | | | *
    #       4 | | | | | | | *
    #       5 | |w| | | | | *
    #       6 | |w| | | | | *
    #       7 | |w| | | | | *
    #       *****************
    #       Black stones:
    #       Open rows of length 2: 0
    #       Semi-open rows of length 2: 0
    #       Open rows of length 3: 0
    #       Semi-open rows of length 3: 0
    #       Open rows of length 4: 0
    #       Semi-open rows of length 4: 0
    #       Open rows of length 5: 0
    #       Semi-open rows of length 5: 0
    #       White stones:
    #       Open rows of length 2: 0
    #       Semi-open rows of length 2: 0
    #       Open rows of length 3: 0
    #       Semi-open rows of length 3: 1
    #       Open rows of length 4: 0
    #       Semi-open rows of length 4: 0
    #       Open rows of length 5: 0
    #       Semi-open rows of length 5: 0
    
    y = 3; x = 5; d_x = -1; d_y = 1; length = 2
    
    put_seq_on_board(board, y, x, d_y, d_x, length, "b")
    print_board(board)
    analysis(board)
    
    # Expected output:
    #        *0|1|2|3|4|5|6|7*
    #        0 | | | | |w|b| *
    #        1 | | | | | | | *
    #        2 | | | | | | | *
    #        3 | | | | |b| | *
    #        4 | | | |b| | | *
    #        5 | |w| | | | | *
    #        6 | |w| | | | | *
    #        7 | |w| | | | | *
    #        *****************
    #
    #         Black stones:
    #         Open rows of length 2: 1
    #         Semi-open rows of length 2: 0
    #         Open rows of length 3: 0
    #         Semi-open rows of length 3: 0
    #         Open rows of length 4: 0
    #         Semi-open rows of length 4: 0
    #         Open rows of length 5: 0
    #         Semi-open rows of length 5: 0
    #         White stones:
    #         Open rows of length 2: 0
    #         Semi-open rows of length 2: 0
    #         Open rows of length 3: 0
    #         Semi-open rows of length 3: 1
    #         Open rows of length 4: 0
    #         Semi-open rows of length 4: 0
    #         Open rows of length 5: 0
    #         Semi-open rows of length 5: 0
    #     
    
    y = 5; x = 3; d_x = -1; d_y = 1; length = 1
    put_seq_on_board(board, y, x, d_y, d_x, length, "b");
    print_board(board);
    analysis(board);
    
    #        Expected output:
    #           *0|1|2|3|4|5|6|7*
    #           0 | | | | |w|b| *
    #           1 | | | | | | | *
    #           2 | | | | | | | *
    #           3 | | | | |b| | *
    #           4 | | | |b| | | *
    #           5 | |w|b| | | | *
    #           6 | |w| | | | | *
    #           7 | |w| | | | | *
    #           *****************
    #        
    #        
    #        Black stones:
    #        Open rows of length 2: 0
    #        Semi-open rows of length 2: 0
    #        Open rows of length 3: 0
    #        Semi-open rows of length 3: 1
    #        Open rows of length 4: 0
    #        Semi-open rows of length 4: 0
    #        Open rows of length 5: 0
    #        Semi-open rows of length 5: 0
    #        White stones:
    #        Open rows of length 2: 0
    #        Semi-open rows of length 2: 0
    #        Open rows of length 3: 0
    #        Semi-open rows of length 3: 1
    #        Open rows of length 4: 0
    #        Semi-open rows of length 4: 0
    #        Open rows of length 5: 0
    #        Semi-open rows of length 5: 0
