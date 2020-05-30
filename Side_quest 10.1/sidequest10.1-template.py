#
# CS1010S --- Programming Methodology
#
# Sidequest 10.1 Template
#
# Note that written answers are commented out to allow us to run your #
# code easily while grading your problem set.

from random import *
from puzzle import GameGrid

###########
# Helpers #
###########

def accumulate(fn, initial, seq):
    if not seq:
        return initial
    else:
        return fn(seq[0],
                  accumulate(fn, initial, seq[1:]))

def flatten(mat):
    return [num for row in mat for num in row]



###########
# Task 1  #
###########

def new_game_matrix(n):
    m = []
    for i in range(n):
        row = []
        for j in range(n):
            row.append(0)
        m.append(row)
    return m

def has_zero(mat):
    new_mat=flatten(mat)
    if 0 in new_mat:
        return True
    else:
        return False

def add_two(mat):
    if has_zero(mat):
        pos_with_zero=[]
        for row in range(len(mat)):
            for col in range(len(mat[row])):
                if mat[row][col]==0:
                    pos_with_zero.append((row,col))
        rand_pos=randint(0,len(pos_with_zero)-1)
        row,col=pos_with_zero[rand_pos][0],pos_with_zero[rand_pos][1]
        mat[row][col]=2
    return mat


                                                     
###########
# Task 2  #
###########

def game_status(mat):
    new_mat=flatten(mat)
    if 2048 in new_mat:
        return 'win'
    elif has_zero(mat) or same_tile(mat):
        return 'not over'
    else:
        return 'lose'

def same_tile(mat):
    for row in mat:
        for j in range(len(row)-1):
            if row[j]==row[j+1]:
                return True
            
    for i in range(len(mat[0])):
        for m in range(len(mat)-1):
            if mat[m][i]==mat[m+1][i]:
                return True
    return False
###########
# Task 3a #
###########
def transpose(mat):
    t_list=[]
    for i in range(len(mat)):
        for j in range(len(mat[i])):
            if len(t_list)<=j:
                t_list.append([mat[i][j]])
            else:
                t_list[j].append(mat[i][j])
    return t_list

    
###########
# Task 3b #
###########

def reverse(mat):
    return list(map(lambda x: x[::-1],mat))


############
# Task 3ci #
############    
def merge_left2(mat):
    flat_mat=flatten(mat)
    old_sum=accumulate(lambda x,y: x+y,0,flat_mat) 
    def helper(mat):
        non_zero=list(filter(lambda x: x!=0,mat))
        new_mat=[]
        counter=0
        while counter<len(non_zero)-1:
            if non_zero[counter]==non_zero[counter+1]:
                new_mat.append(non_zero[counter]+non_zero[counter+1])
                counter+=2
            else:
                new_mat.append(non_zero[counter])
                counter+=1
        zeros_to_add=len(mat)-len(new_mat)
        lst_0=[0]*zeros_to_add
        new_mat.extend(lst_0)
        return new_mat
    new_mat2=list(map(helper,mat)) #map to all other rows
    def is_valid(new_mat2):
        if new_mat2==mat:
            return False
        else:
            return True
    new_sum=accumulate(lambda x,y:x+y, 0,flatten(new_mat2))
    score_increment=abs(new_sum-old_sum)
    return (new_mat2,is_valid,score_increment)

def merge_left(mat):
    sum_inc = 0
    new_mat = []
    for row in mat:
        
        new_row = [elem for elem in row]
        for i in range(len(row)):
            pointer = i-1
            while pointer >=0:

                if new_row[pointer] == 0:
                    if pointer == 0:
                        new_row[pointer] = new_row[i]
                        new_row[i] = 0
                        break
                    pointer -= 1

                elif new_row[pointer] == new_row[i]:
                    new_row[pointer] = 2*new_row[pointer]
                    new_row[i] = 0
                    cursor = pointer-1
                    while cursor>=0 and new_row[cursor] == new_row[cursor+1]:
                        new_row[cursor] = 2*new_row[cursor]
                        new_row[cursor+1] = 0
                        cursor -= 1
                    break

                elif new_row[pointer]!=new_row[i]:
                    new_row[pointer+1] = new_row[i]
                    if pointer+1 < i:
                        new_row[i] = 0
                    break

        for i in range(len(new_row)):
            if new_row[i] > max(row[i:]):
                sum_inc += new_row[i]

        new_mat.append(new_row)
    
    is_valid = new_mat != mat
    return new_mat, is_valid, sum_inc
    
            


#############
# Task 3cii #
#############

def merge_right(mat):
    m_state = merge_left(reverse(mat))
    return reverse(m_state[0]), m_state[1], m_state[2]

def merge_up(mat):
    m_state = merge_left(transpose(mat))
    return transpose(m_state[0]), m_state[1], m_state[2]

def merge_down(mat):
    m_state = merge_right(transpose(mat))
    return transpose(m_state[0]), m_state[1], m_state[2]


###########
# Task 3d #
###########

def text_play():
    def print_game(mat, score):
        for row in mat:
            print(''.join(map(lambda x: str(x).rjust(5), row)))
        print('score: ' + str(score))
    GRID_SIZE = 4
    score = 0
    mat = add_two(add_two(new_game_matrix(GRID_SIZE)))
    print_game(mat, score)
    while True:
        move = input('Enter W, A, S, D or Q: ')
        move = move.lower()
        if move not in ('w', 'a', 's', 'd', 'q'):
            print('Invalid input!')
            continue
        if move == 'q':
            print('Quitting game.')
            return
        move_funct = {'w': merge_up,
                      'a': merge_left,
                      's': merge_down,
                      'd': merge_right}[move]
        mat, valid, score_increment = move_funct(mat)
        if not valid:
            print('Move invalid!')
            continue
        score += score_increment
        mat = add_two(mat)
        print_game(mat, score)
        status = game_status(mat)
        if status == "win":
            print("Congratulations! You've won!")
            return
        elif status == "lose":
            print("Game over. Try again!")
            return

# UNCOMMENT THE FOLLOWING LINE TO TEST YOUR GAME
#text_play()


# How would you test that the winning condition works?
# Your answer:
#


##########
# Task 4 #
##########

def make_state(matrix, total_score):
    return (matrix, total_score)

def get_matrix(state):
    return state[0]
    

def get_score(state):
    return state[1]

def make_new_game(n):
    matrix = new_game_matrix(n)
    return make_state(add_two(add_two(matrix)), 0)
    
def swipe(state, fn):
    m, score = get_matrix(state), get_score(state)
    new_m = fn(m)
    valid = new_m[1]
    score = score + new_m[2]
    if valid:
        res_m = add_two(new_m[0])
        return make_state(res_m, score), valid
    return make_state(new_m[0], score), valid

def left(state):
    return swipe(state, merge_left)

def right(state):
    return swipe(state, merge_right)

def up(state):
    return swipe(state, merge_up)

def down(state):
    return swipe(state, merge_down)


# Do not edit this #
game_logic = {
    'make_new_game': make_new_game,
    'game_status': game_status,
    'get_score': get_score,
    'get_matrix': get_matrix,
    'up': up,
    'down': down,
    'left': left,
    'right': right,
    'undo': lambda state: (state, False)
}

# UNCOMMENT THE FOLLOWING LINE TO START THE GAME (WITHOUT UNDO)
gamegrid = GameGrid(game_logic)




#################
# Optional Task #
#################

###########
# Task 5i #
###########

def make_new_record(mat, increment):
    "Your answer here"

def get_record_matrix(record):
    "Your answer here"

def get_record_increment(record):
    "Your answer here"

############
# Task 5ii #
############

def make_new_records():
    "Your answer here"

def push_record(new_record, stack_of_records):
    "Your answer here"

def is_empty(stack_of_records):
    "Your answer here"

def pop_record(stack_of_records):
    "Your answer here"

#############
# Task 5iii #
#############

# COPY AND UPDATE YOUR FUNCTIONS HERE
def make_state(matrix, total_score, records):
    "Your answer here"

def get_matrix(state):
    "Your answer here"

def get_score(state):
    "Your answer here"

def make_new_game(n):
    "Your answer here"

def left(state):
    "Your answer here"

def right(state):
    "Your answer here"

def up(state):
    "Your answer here"

def down(state):
    "Your answer here"

# NEW FUNCTIONS TO DEFINE
def get_records(state):
    "Your answer here"

def undo(state):
    "Your answer here"


# UNCOMMENT THE FOLLOWING LINES TO START THE GAME (WITH UNDO)
##game_logic = {
##    'make_new_game': make_new_game,
##    'game_status': game_status,
##    'get_score': get_score,
##    'get_matrix': get_matrix,
##    'up': up,
##    'down': down,
##    'left': left,
##    'right': right,
##    'undo': undo
##}
#gamegrid = GameGrid(game_logic)
