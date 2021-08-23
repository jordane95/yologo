'''draw predefined shapes with ASCII char'''

def draw_plus(ascii_mat, Sx, Sy, W, H):
    size = (W+H)//2
    if size <= 2:
        ascii_mat[Sy][Sx] = '+'
    elif size <= 4:
        ascii_mat[Sy][Sx+2] = "|"
        ascii_mat[Sy+1][Sx:Sx+5] = ["-", "-", "+", "-", "-"]
        ascii_mat[Sy+2][Sx+2] = "|"
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
    pass

def draw_rhombus(ascii_mat, Sx, Sy, W, H):
    pass

def draw_inv_triangle(ascii_mat, Sx, Sy, W, H):
    pass

def draw_unk(ascii_mat, Sx, Sy, W, H):
    pass
