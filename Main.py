# coding=utf-8
import sys

import numpy

import Window
from Pic import picture

sys.setrecursionlimit(20000)
numpy.set_printoptions(threshold=numpy.nan)

folder='images/';forest=(40,90,50,100,50,100)
forest_hsv=(0.1388888888888889, 0.36458, 0.0625, 0.43478260869565216, 23, 95)
scale_union=(10,10)
#upper-default preferences

if __name__ == '__main__':
    window = Window.window_class()
    window.start__public()

    pic=picture(folder+"image.jpg")
    # //pic.pick_some_area((70,180,90,210))
    # //filter1=pic.find_filter_params_rect_simple((70,180,80,200),in_hsv=True)
    pic.one_thread_hsv_filter_and_union(forest_hsv, (5, 5), 0.8,False)

    pic.time_shov()
    pic.save()
