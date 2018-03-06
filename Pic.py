import colorsys
import os
import time
import numpy
from PIL import Image, ImageDraw
import threading


class picture:
    globalFillmetpercent=float
    good_pixel_count=0.0
    fillmentPercent = 0.5
    imageName__private = '';imageExtension__private = ''
    image = Image;time_begin__private=time.time()
    values_min_max=tuple
    rect=tuple

    unionColor__private=(0, 255, 0)
    whiteColor__private=(255, 255, 255)
    borderColor__private=(255, 0, 0)

    def __init__(self,imageName):
        self.image = Image.open(imageName)
        a = str.split(imageName, '.')
        self.imageName__private = a[0];self.imageExtension__private = a[1]
        print("name=" + self.imageName__private + "   ext=" + self.imageExtension__private)
        self.time_begin__private=time.time()

    def save(self):
        """
        Сохрнение фото в начальном формате с подписью
        """
        self.image.save(self.imageName__private + "_worked." + self.imageExtension__private)

    def rgb_filter(self, values_min_max):
        """
        перекрашивание пикселов РГБ,не входящих в промежуток
        (a_min < pix_a < a_max) & (b_min < pix_b < b_max) & (c_min < pix_c < c_max)
        """
        good_pixel_count=0
        draw = ImageDraw.Draw(self.image)
        width = self.image.size[0];height = self.image.size[1]
        pix = self.image.load()

        self.values_min_max = values_min_max

        for i in range(width):
            for j in range(height):
                pix_a = pix[i, j][0];pix_b = pix[i, j][1];pix_c = pix[i, j][2]

                if self.condition_not_in_rgb(pix_a, pix_b, pix_c) :
                    draw.point((i, j), self.whiteColor__private)
                    good_pixel_count+=1
        self.globalFillmetpercent=good_pixel_count/width/height
    def hsv_filter(self, values_min_max):
        """
        перекрашивание пикселов в формате ХСВ,не входящих в промежуток
        (a_min < pix_a < a_max) & (b_min < pix_b < b_max) & (c_min < pix_c < c_max)
        """
        good_pixel_count=0
        draw = ImageDraw.Draw(self.image)
        width = self.image.size[0];height = self.image.size[1]
        pix = self.image.load()

        self.values_min_max = values_min_max

        for i in range(width):
            for j in range(height):
                pix_a = pix[i, j][0];pix_b = pix[i, j][1];pix_c = pix[i, j][2]

                if self.condition_not_in_hsv(pix_a, pix_b, pix_c) :
                    draw.point((i, j), self.whiteColor__private)
                    good_pixel_count+=1
        self.globalFillmetpercent=good_pixel_count/width/height

    def rgb_reverse_filter(self, values_min_max):
        """
        обратный фильтр:то,что проходит условие-в зеленый
        :param values_min_max: a_min, a_max, b_min, b_max, c_min, c_max
        """
        draw = ImageDraw.Draw(self.image)
        width = self.image.size[0];height = self.image.size[1]
        pix = self.image.load()

        self.values_min_max = values_min_max

        for i in range(width):
            for j in range(height):
                pix_a = pix[i, j][0];pix_b = pix[i, j][1];pix_c = pix[i, j][2]

                if not self.condition_not_in_rgb(pix_a, pix_b, pix_c):
                    draw.point((i, j), self.whiteColor__private)
                    continue
    def hsv_reverse_filter(self, values_min_max):
        """
        обратный фильтр:то,что проходит условие-в зеленый
        :param values_min_max: a_min, a_max, b_min, b_max, c_min, c_max
        """
        draw = ImageDraw.Draw(self.image)
        width = self.image.size[0];height = self.image.size[1]
        pix = self.image.load()

        self.values_min_max = values_min_max

        for i in range(width):
            for j in range(height):
                pix_a = pix[i, j][0];pix_b = pix[i, j][1];pix_c = pix[i, j][2]

                if not self.condition_not_in_hsv(pix_a, pix_b, pix_c):
                    draw.point((i, j), self.whiteColor__private)
                    continue

    def time_shov(self):
        print("time now is:=" + str(time.time() - self.time_begin__private))

    def find_filter_params_rect_simple(self, rect, x_pass_pixels=1, y_pass_pixels=1, in_hsv=False):
        """
        :param rect: tuple,which contains x,y,x1,y1 ON IMAGE
        :return tuple:filter parameters which was fount in this rect
        """
        draw = ImageDraw.Draw(self.image)
        width = self.image.size[0];height = self.image.size[1]
        pix = self.image.load()

        loc_x_coord=rect[0];loc_y_coord=rect[1]
        pix_a =pix[loc_x_coord,loc_y_coord][0];pix_b =pix[loc_x_coord,loc_y_coord][1]
        pix_c =pix[loc_x_coord,loc_y_coord][2]

        if in_hsv:(pix_a,pix_b,pix_c)=colorsys.rgb_to_hsv(pix_a,pix_b,pix_c)

        filer_values=[pix_a,pix_a ,pix_b,pix_b ,pix_c,pix_c]

        for i in range(rect[0],rect[2],x_pass_pixels):
            for j in range(rect[1], rect[3],y_pass_pixels):

                pix_a = pix[i, j][0];pix_b = pix[i, j][1];pix_c = pix[i, j][2]

                if in_hsv: (pix_a, pix_b, pix_c) = colorsys.rgb_to_hsv(pix_a, pix_b, pix_c)

                if pix_a<filer_values[0]:filer_values[0]=pix_a
                else:
                    if pix_a>filer_values[1]:filer_values[1]=pix_a
                #Расширение границы h

                if pix_b<filer_values[2]:filer_values[2]=pix_b
                else:
                    if pix_b>filer_values[3]:filer_values[3]=pix_b
                #Расширение границы s

                if pix_c<filer_values[4]:filer_values[4]=pix_c
                else:
                    if pix_c>filer_values[5]:filer_values[5]=pix_c
                #Расширение границы v
        return tuple(filer_values)

    def find_filter_params_rect(self,minus_dev,plus_dev,rect, x_pass_pixels=1, y_pass_pixels=1, in_hsv=False):
        """

        :param minus_dev:if (left deviation a)= mean-a*sigma
        :param plus_dev:same for plus
        :param rect: tuple,which contains x,y,x1,y1 ON IMAGE
        :param x_pass_pixels:
        :param y_pass_pixels:
        :param in_hsv:
        """
        draw = ImageDraw.Draw(self.image)
        width = self.image.size[0];height = self.image.size[1]
        pix = self.image.load()

        loc_x_coord=rect[0];loc_y_coord=rect[1]
        pix_a =pix[loc_x_coord,loc_y_coord][0];pix_b =pix[loc_x_coord,loc_y_coord][1]
        pix_c =pix[loc_x_coord,loc_y_coord][2]

        if in_hsv:(pix_a,pix_b,pix_c)=colorsys.rgb_to_hsv(pix_a,pix_b,pix_c)

        filer_values=[pix_a,pix_a ,pix_b,pix_b ,pix_c,pix_c]

        # for i in range(rect[0],rect[2],x_pass_pixels):
        #     for j in range(rect[1], rect[3],y_pass_pixels):
                
        return tuple(filer_values)

    def fool_union_of_filters(self,filter1,filter2):
        filter_to_return = list(filter1)
        for i in range(1,5,2):
            filter_to_return[i]=max(filter_to_return[i],filter2[i])
        for i in range(0,5,2):
            filter_to_return[i]=min(filter_to_return[i],filter2[i])
        return tuple(filter_to_return)

    def pick_some_area(self, rect,x_pass_pixels=1,y_pass_pixels=1):
        draw = ImageDraw.Draw(self.image)
        width = self.image.size[0];height = self.image.size[1]
        pix = self.image.load()

        for i in range(rect[0],rect[2],x_pass_pixels):
            for j in range(rect[1], rect[3],y_pass_pixels):
                pix_a = pix[i, j][0];pix_b = pix[i, j][1];pix_c = pix[i, j][2]
                middle_of_pix=int(numpy.mean((pix_a,pix_b,pix_c)))
                draw.point((i, j), (255,middle_of_pix,middle_of_pix))
                # draw.point((i, j), (255-pix_a,255-pix_b,255-pix_c))

    def hsv_big_pic_filter_and_union(self, values_min_max, scale, fillmentPercent,
                                     x_pass_pixels=2, y_pass_pixels=2, needMatr=False):
        draw = ImageDraw.Draw(self.image)
        width = self.image.size[0];height = self.image.size[1]
        pix = self.image.load()

        self.values_min_max = values_min_max
        px_width = scale[0];px_height = scale[1]

        x = int(width / px_width);y = int(height / px_height)
        good_pixel_count = 0

        matr = numpy.zeros((x, y), dtype=int)
        for i in range(x):
            for j in range(y):

                count = 0;need = int(px_height * px_width * fillmentPercent/x_pass_pixels/y_pass_pixels)

                for ii in range(i * px_width, (i + 1) * px_width,x_pass_pixels):
                    for jj in range(j * px_height, (j + 1) * px_height,y_pass_pixels):
                        if not self.condition_not_in_hsv \
                                    (pix[ii, jj][0], pix[ii, jj][1], pix[ii, jj][2]):
                            count += 1
                            good_pixel_count += 1

                if count >= need:
                    matr[i][j] = 1
                    for ii in range(i * px_width, (i + 1) * px_width):
                        for jj in range(j * px_height, (j + 1) * px_height):
                            draw.point((ii, jj), self.unionColor__private)
        self.globalFillmetpercent = good_pixel_count / width / height *x_pass_pixels*y_pass_pixels
        if needMatr:
            return matr
    def rgb_big_pic_filter_and_union(self, values_min_max, scale, fillmentPercent,
                                     x_pass_pixels=2, y_pass_pixels=2, needMatr=False):
        draw = ImageDraw.Draw(self.image)
        width = self.image.size[0];height = self.image.size[1]
        pix = self.image.load()

        self.values_min_max = values_min_max
        px_width = scale[0];px_height = scale[1]

        x = int(width / px_width);y = int(height / px_height)
        good_pixel_count = 0

        matr = numpy.zeros((x, y), dtype=int)
        for i in range(x):
            for j in range(y):

                count = 0;need = int(px_height * px_width * fillmentPercent/x_pass_pixels/y_pass_pixels)

                for ii in range(i * px_width, (i + 1) * px_width,x_pass_pixels):
                    for jj in range(j * px_height, (j + 1) * px_height,y_pass_pixels):
                        if not self.condition_not_in_rgb \
                                    (pix[ii, jj][0], pix[ii, jj][1], pix[ii, jj][2]):
                            count += 1
                            good_pixel_count += 1

                if count >= need:
                    matr[i][j] = 1
                    for ii in range(i * px_width, (i + 1) * px_width):
                        for jj in range(j * px_height, (j + 1) * px_height):
                            draw.point((ii, jj), self.unionColor__private)
        self.globalFillmetpercent = good_pixel_count / width / height *x_pass_pixels*y_pass_pixels
        if needMatr:
            return matr

    def hsv_filter_and_union(self, values_min_max, scale, fillmentPercent, needMatr=False,):

        draw = ImageDraw.Draw(self.image)
        width = self.image.size[0];height = self.image.size[1]
        pix = self.image.load()

        self.values_min_max = values_min_max
        px_width=scale[0];px_height=scale[1]

        x = int(width / px_width);y = int(height / px_height)

        matr = numpy.zeros((x, y), dtype=int)

        def imageProcessing(self,xBegin,xEnd):
            print("start! from " + str(xBegin) + " " +str(xEnd))
            for i in range(xBegin,xEnd):
                for j in range(y):

                    count = 0;need = int(px_height * px_width * fillmentPercent)

                    for ii in range(i * px_width, (i + 1) * px_width):
                        for jj in range(j * px_height, (j + 1) * px_height):
                            if not self.condition_not_in_hsv \
                                        (pix[ii, jj][0], pix[ii, jj][1], pix[ii, jj][2]):
                                count += 1
                                self.good_pixel_count += 1

                    if count >= need:
                        matr[i][j] = 1
                        for ii in range(i * px_width, (i + 1) * px_width):
                            for jj in range(j * px_height, (j + 1) * px_height):
                                draw.point((ii, jj), self.unionColor__private)
            self.globalFillmetpercent = self.good_pixel_count / width / height

        # parallels
        t1 = threading.Thread(target=imageProcessing,
                              args=(self, int(x / 4 * 0), int(x / 4 * (0 + 1)),))
        t2 = threading.Thread(target=imageProcessing,
                              args=(self, int(x / 4 * 1), int(x / 4 * (1 + 1)),))
        t3 = threading.Thread(target=imageProcessing,
                              args=(self, int(x / 4 * 2), int(x / 4 * (2 + 1)),))
        t4 = threading.Thread(target=imageProcessing,
            args=(self, int(x / 4 * 3), int(x / 4 * (3 + 1)),))

        t1.start();t2.start();t3.start();t4.start()

        t1.join();t2.join();t3.join();t4.join()

        if needMatr:
            return matr

    def rgb_filter_and_union(self, values_min_max, scale, fillmentPercent, needMatr=False):
        draw = ImageDraw.Draw(self.image)
        width = self.image.size[0];height = self.image.size[1]
        pix = self.image.load()

        self.values_min_max = values_min_max
        px_width=scale[0];px_height=scale[1]

        x = int(width / px_width);y = int(height / px_height)
        good_pixel_count=0

        matr = numpy.zeros((x, y), dtype=int)
        for i in range(x):
            for j in range(y):

                count = 0;need = int(px_height * px_width * fillmentPercent)

                for ii in range(i * px_width, (i + 1) * px_width):
                    for jj in range(j * px_height, (j + 1) * px_height):
                        if not self.condition_not_in_rgb\
                                    (pix[ii, jj][0], pix[ii, jj][1], pix[ii, jj][2]) :
                            count += 1
                            good_pixel_count += 1

                if count >= need:
                    matr[i][j] = 1
                    for ii in range(i * px_width, (i + 1) * px_width):
                        for jj in range(j * px_height, (j + 1) * px_height):
                            draw.point((ii, jj), self.unionColor__private)
        self.globalFillmetpercent = good_pixel_count / width / height
        if needMatr:
            return matr
    def one_thread_hsv_filter_and_union(self, values_min_max, scale, fillmentPercent, needMatr=False):
        draw = ImageDraw.Draw(self.image)
        width = self.image.size[0];height = self.image.size[1]
        pix = self.image.load()

        self.values_min_max = values_min_max
        px_width=scale[0];px_height=scale[1]

        x = int(width / px_width);y = int(height / px_height)
        good_pixel_count=0

        matr = numpy.zeros((x, y), dtype=int)
        for i in range(x):
            for j in range(y):

                count = 0;need = int(px_height * px_width * fillmentPercent)

                for ii in range(i * px_width, (i + 1) * px_width):
                    for jj in range(j * px_height, (j + 1) * px_height):
                        if not self.condition_not_in_hsv\
                                    (pix[ii, jj][0], pix[ii, jj][1], pix[ii, jj][2]) :
                            count += 1
                            good_pixel_count += 1

                if count >= need:
                    matr[i][j] = 1
                    for ii in range(i * px_width, (i + 1) * px_width):
                        for jj in range(j * px_height, (j + 1) * px_height):
                            draw.point((ii, jj), self.unionColor__private)
        self.globalFillmetpercent = good_pixel_count / width / height
        if needMatr:
            return matr

    def union(self,px_width, px_height,fillmentPercent,needMatr=False):
        """
        пробег по всем пикселам,и закрашивание квадрата при определенном проценте
        :param px_width:
        :param px_height:
        :param fillmentPercent:
        """
        draw = ImageDraw.Draw(self.image);pix = self.image.load()
        width = self.image.size[0];height = self.image.size[1]

        x = int(width / px_width);y = int(height / px_height)

        matr=numpy.zeros((x,y),dtype=int)
        for i in range(x):
            for j in range(y):

                count = 0;need = int(px_height * px_width * fillmentPercent)

                for ii in range(i * px_width, (i + 1) * px_width):
                    for jj in range(j * px_height, (j + 1) * px_height):
                        if (pix[ii, jj][0] != self.whiteColor__private[0]) & (pix[ii, jj][1] != self.whiteColor__private[1]) & \
                                (pix[ii, jj][2] != self.whiteColor__private[2]):
                            count += 1

                if count >= need:
                    matr[i][j]=1
                    for ii in range(i * px_width, (i + 1) * px_width):
                        for jj in range(j * px_height, (j + 1) * px_height):
                            draw.point((ii, jj), self.unionColor__private)
        if needMatr:
            return matr

    def draw_borders(self,scale=tuple,borders=numpy,number_of_set_to_draw=int):
        draw = ImageDraw.Draw(self.image);(px_width,px_height)=scale
        width = self.image.size[0];height = self.image.size[1]
        pix = self.image.load();(width, height) = borders.shape

        for i in range(width):
            for j in range(height):
                if borders[i][j] == -number_of_set_to_draw:

                    for ii in range(i * px_width, (i + 1) * px_width):
                        for jj in range(j * px_height, (j + 1) * px_height):
                            draw.point((ii, jj), self.borderColor__private)

    def condition_not_in_rgb(self, pix_a, pix_b, pix_c):
        if (self.values_min_max [0] > pix_a) :return True
        if (pix_a > self.values_min_max [1]) :return True

        if (self.values_min_max [2] > pix_b) :return True
        if (pix_b > self.values_min_max [3]) :return True

        if (self.values_min_max [4] > pix_c) :return True
        if (pix_c > self.values_min_max [5]) :return True
        else :return False
        # return not ((self.values_min_max [0] < pix_a < self.values_min_max [1]) &
        #             (self.values_min_max [2] < pix_b < self.values_min_max [3])
        #             & (self.values_min_max [4]< pix_c < self.values_min_max [5]))

    def condition_not_in_hsv(self, pix_a, pix_b, pix_c):
        hsv=colorsys.rgb_to_hsv(pix_a, pix_b, pix_c)

        if (self.values_min_max[0] > hsv[0]): return True
        if (hsv[0] > self.values_min_max[1]): return True

        if (self.values_min_max[2] > hsv[1]): return True
        if (hsv[1] > self.values_min_max[3]): return True

        if (self.values_min_max[4] > hsv[2]): return True
        if (hsv[2] > self.values_min_max[5]): return True
        else: return False

        # return not ((self.values_min_max[0] < hsv[0] < self.values_min_max[1]) &
        #             (self.values_min_max[2] < hsv[1]< self.values_min_max[3]) &
        #             (self.values_min_max[4] < hsv[2] < self.values_min_max[5]))


def is_file_exits(path="test"):
        # if os._exists(path):
        #     print("file exists:="+path)
        exists=True
        try:
            file = open(path)
            file.close()
        except IOError as e:
            print(u'не удалось открыть файл')
            exists=False
        if exists:
            open(path, 'tw', encoding='utf-8')
            if os._exists(path):
                print("file exists:="+path)
