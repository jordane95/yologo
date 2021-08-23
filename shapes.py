'''draw predefined shapes with ASCII char'''

# all shapes of different sizes can be found in ./predefined/ folder
# these functions can be seen as hard coding of the predefined shapes
# note that all functions do almost the same thing: draw a shape in the background
# except that the shape to be drawn is different for each function
# they all have the following three arguments
#   ascii_mat: two dimenstional list, representing the background of ascii encoding of images
#   Sx: starting corinate of x dimension, coorespond to the sencond index of ascii_mat
#   Sy: start point of dimension y, cooresponding to the first index of ascii_mat
#   W: width, in x dimension
#   H: height, in y dimension
# in other words, the region to be drawn is ascii_mat[Sy:Sy+H, Sx:Sx+W]


def draw_plus(ascii_mat, Sx, Sy, W, H):
    size = (W+H)//2
    if size <= 2:
        ascii_mat[Sy][Sx] = '+'
    elif size <= 4:
        ascii_mat[Sy][Sx+2]      =            "|"
        ascii_mat[Sy+1][Sx:Sx+5] = ["-", "-", "+", "-", "-"]
        ascii_mat[Sy+2][Sx+2]    =            "|"
        pass
    else: pass
    pass

def draw_square(ascii_mat, Sx, Sy, W, H):
    size = (W+H)//2
    if size <= 2:
        ascii_mat[Sy][Sx:Sx+3] = ['[', '_', ']']
    else:
        for i in range(W):
            ascii_mat[Sy][i+Sx] = "-"
            ascii_mat[Sy+H][i+Sx] = "-"
        for j in range(H):
            ascii_mat[Sy+j][Sx] = "|"
            ascii_mat[Sy+j][Sx+W] = "|"
    pass

def draw_triangle(ascii_mat, Sx, Sy, W, H):
    size = (W+H)//2
    if size <= 1:
        ascii_mat[Sy][Sx] = "^"
    elif size <=4:
        for i in range(3):
            ascii_mat[Sy+i][Sx+2-i] = "/"
        for i in range(3):
            ascii_mat[Sy+i][Sx+3+i] = "\\"
        ascii_mat[Sy+2][Sx+1] = ascii_mat[Sy+2][Sx+4] = "_"
    else:
        pass
    pass

def draw_circle(ascii_mat, Sx, Sy, W, H):
    size = (W+H)//2
    if size <= 2:
        ascii_mat[Sy][Sx] = "O"
    elif size <= 4:
        ascii_mat[Sy][Sx+1] = ascii_mat[Sy][Sx+3] = 'o'
        ascii_mat[Sy+1][Sx] = ascii_mat[Sy+1][Sx+4] = 'o'
        ascii_mat[Sy+2][Sx+1] = ascii_mat[Sy+2][Sx+3] = 'o'
    else:
        center = [Sx+round(W/2), Sy+round(H/2)]
        Sx = center[0]-5
        Sy = center[1]-3
        ascii_mat[Sy][Sx+4] = ascii_mat[Sy][Sx+7] = "="
        ascii_mat[Sy+1][Sx+1] = ascii_mat[Sy+1][Sx+10] = "="
        ascii_mat[Sy+2][Sx] = ascii_mat[Sy+2][Sx+11] = "="
        ascii_mat[Sy+3][Sx] = ascii_mat[Sy+3][Sx+11] = "="
        ascii_mat[Sy+4][Sx+1] = ascii_mat[Sy+4][Sx+10] = "="
        ascii_mat[Sy+5][Sx+4] = ascii_mat[Sy+5][Sx+7] = "="
    pass

def draw_ellipse(ascii_mat, Sx, Sy, W, H):
    pass

def draw_cross(ascii_mat, Sx, Sy, W, H):
    size = (W+H)//2
    if size <= 2:
        ascii_mat[Sy][Sx] = "X"
    elif size <= 4:
        ascii_mat[Sy][Sx] = ascii_mat[Sy+1][Sx+1] = "\\"
        ascii_mat[Sy][Sx+1] = ascii_mat[Sy+1][Sx] = "/"
    else:
        ascii_mat[Sy][Sx] = ascii_mat[Sy+2][Sx+2] = "\\"
        ascii_mat[Sy][Sx+2] = ascii_mat[Sy+2][Sx] = "/"
        ascii_mat[Sy+1][Sx+1] = "X"
    pass

def draw_hexagon(ascii_mat, Sx, Sy, W, H):
    size = (W+H)//2
    if size <= 2:
        ascii_mat[Sy][Sx] = "*"
    elif size <=4:
        ascii_mat[Sy][Sx] = ascii_mat[Sy+1][Sx+2] = "/"
        ascii_mat[Sy][Sx+2] = ascii_mat[Sy+1][Sx] = "\\"
        ascii_mat[Sy+1][Sx+1] = "_"
    pass

def draw_rhombus(ascii_mat, Sx, Sy, W, H):
    pass

def draw_inv_triangle(ascii_mat, Sx, Sy, W, H):
    pass

def draw_unk(ascii_mat, Sx, Sy, W, H):
    pass
