# coding=utf-8
import numpy


def save_matrix(file_name, matrix=numpy,delimiter=","):
    """
сохраняет матрицу в фаил //
    :param file_name:
    :param matrix:
    :param delimiter:
    """
    file=open(file_name,"w+")
    (a,b)=matrix.shape

    for i in range(a):
        for j in range(b):
            file.write(str(matrix[i][j]))
            if j!=b-1:
                file.write(delimiter)
        file.write("\n")
    file.close()

def shov_matrix(matrix=numpy):
    numpy.set_printoptions(threshold=numpy.nan)
    print(matrix)

def separate_matrix_func(matrix=numpy,separate_with_underline_borders=True,return_borders=False,begin_index=2):
    """

    :param separate_with_underline_borders:
    :param matrix:
    :return: количество разных областей,трехмерный массив с границами
    """
    (a,b)=matrix.shape
    heap_index=begin_index
    checked_list=list()
    global_borders=list();borders_at_i=list()

    def in_matrix(x,y):
        if 0<=x<a and 0<=y<b:return True
        else:return False

    def ant(x,y):
        """
        Бегунок,который при нахождении 1 "расплывается"
        по всему множеству,определяя его границы
        :param x:
        :param y:
        """
        if in_matrix(x,y) and (not checked_list.__contains__( (x,y) )):
            if matrix[x][y]==1:
                checked_list.append((x,y))
                matrix[x][y]=heap_index
                ant(x-1,y);ant(x+1,y);ant(x,y-1);ant(x,y+1)
                return
            else:
                if matrix[x][y]==0:
                    borders_at_i.append((x,y))

                    if separate_with_underline_borders:
                        matrix[x][y]=-heap_index

    for i in range(a):
        for j in range(b):
            if(matrix[i][j]==1):
                borders_at_i=list() #обнуление списка,добавляемого в список списков границ
                ant(i,j)
                global_borders.append(borders_at_i)  # ну и костыль
                checked_list=list() #список проверенных в предыдущем случае границ
                heap_index+=1

    if return_borders:
        return (heap_index-1,global_borders)
    return (heap_index-1)

def read_matrix(file_name,delimiter=","):
    z=numpy.genfromtxt(file_name,delimiter=delimiter,dtype=int)
    return z

def count_max_range_in_set(borders=list(),scale_union=(10,10)):
    (scale_x,scale_y)=scale_union
    range_list=list()
    for i in borders:
        range=0
        for j in i:
            (x,y)=j

            for k in i:
                (x1,y1)=k
                iter_range=(x-x1)*scale_x*scale_x*(x-x1)+(y-y1)*scale_y*scale_y*(y-y1)
                if iter_range>range:range=iter_range
        range_list.append(numpy.sqrt(range))

    print("max ranges in union"+str(range_list))

    return range_list

def find_numeric_set(matrix=numpy,set_number=int):
    set_elements=list()
    (width,height)=matrix.shape
    for i in range(width):
        for j in range(height):
            if matrix[i][j]==set_number:
                set_elements.append((i,j))
    return set_elements

def find_border_of_numeric_set(matrix=numpy,set_number=int):
    set_border_elements = list()
    (width, height) = matrix.shape
    for i in range(width):
        for j in range(height):
            if matrix[i][j] == -set_number:
                set_border_elements.append((i, j))
    return set_border_elements

def count_numeric_set_square(matrix=numpy,scale_union=(10,10),set_number=int):
    dS=scale_union[0]*scale_union[1];square=0
    (width, height) = matrix.shape
    for i in range(width):
        for j in range(height):
            if matrix[i][j] == set_number:
                square+=dS
    return square

def count_set_border_square(matrix=numpy,scale_union=(10,10),set_number=int):
    dS=scale_union[0]*scale_union[1];square=0
    (width, height) = matrix.shape
    for i in range(width):
        for j in range(height):
            if matrix[i][j] == -set_number:
                square+=dS
    return square

def compare_martix(matrix_a=numpy,matrix_b=numpy):
    (width,height)=matrix_a.shape
    matrix_difference=numpy.zeros((width,height),dtype=int)

    if matrix_a.shape==matrix_b.shape:

        for i in width:
            for j in height:
                if matrix_a[i][j]!=matrix_b[i][j]:
                    matrix_difference[i][j]=1

        separate_matrix_func(matrix_difference,False)
        return matrix_difference


    else:
        print("matrix shapes not equal")
