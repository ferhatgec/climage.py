# MIT License
#
# Copyright (c) 2021 Ferhat Geçdoğan All Rights Reserved.
# Distributed under the terms of the MIT License.
#
# climage[dot]py - an image format for commandline.
#
# github.com/ferhatgec/climage.py
# github.com/ferhatgec/climage
#

class climage_markers:
    SOF = 0x43
    SOF2 = 0x4C
    SOF3 = 0x49
    SOF4 = 0x6D
    SOF5 = 0x61
    SOF6 = 0x67
    SOF7 = 0x65

    SOW = 0x02
    SOH = 0x26

    Pixel8 = 0x30  # 0
    Pixel16 = 0x31  # 1
    Pixel32 = 0x32  # 2
    Pixel64 = 0x33  # 3

    ColorStart = 0x23  # #
    Continue = 0x2C  # ,


class climage_rgb:
    def __init__(self):
        self.r, self.g, self.b = 0, 0, 0

    def from_hex(self, __hex__: str) -> (int, int, int):
        __hex = int(__hex__, 16)

        self.r = (__hex >> 16) & 0xFF
        self.g = (__hex >> 8) & 0xFF
        self.b = __hex & 0xFF

        return self.r, self.g, self.b


class climage:
    def __init__(self):
        self.width, self.height = 0, 0
        self.r, self.g, self.b = 0, 0, 0

        self.__init = climage_rgb()

        self.layer_1d = []
        self.layer = []

        self.__sof, \
        self.__sof2, \
        self.__sof3, \
        self.__sof4, \
        self.__sof5, \
        self.__sof6, \
                    \
        self.__ok, \
        self.__sow, \
        self.__soh, \
        self.__color_start = False, False, False, False, False, False, False, False, False, False

        self.__current_hex = ''
        self.__generated_text_image = ''

        self.__color = '\x1b[48;2;'
        self.__character = '░░'

    def color_generate(self, data: []) -> str:
        return f'{self.__color}{data[0]};{data[1]};{data[2]}m'

    def generate(self):
        for line in self.layer:
            for child in line:
                self.__generated_text_image += f'{self.color_generate(child)}{self.__character}\x1b[0m'

            self.__generated_text_image += '\n'

        self.__generated_text_image += '\x1b[0m'

        print(self.__generated_text_image)

    def parse(self, data: str):
        for ch in data:
            if self.__color_start:
                if ord(ch) != climage_markers.Continue:
                    self.__current_hex += ch
                else:
                    self.r, self.g, self.b = self.__init.from_hex(self.__current_hex)

                    self.layer_1d.append([self.r, self.g, self.b])

                    self.__color_start = False
                    self.__current_hex = ''

                continue
            else:
                if ch == '\n' and len(self.layer_1d) > 0:
                    self.layer.append(self.layer_1d)
                    self.layer_1d = []

                    continue

            if ord(ch) == climage_markers.SOF:
                self.__sof = True
            elif ord(ch) == climage_markers.SOF2:
                self.__sof2 = True
            elif ord(ch) == climage_markers.SOF3:
                self.__sof3 = True
            elif ord(ch) == climage_markers.SOF4:
                self.__sof4 = True
            elif ord(ch) == climage_markers.SOF5:
                self.__sof5 = True
            elif ord(ch) == climage_markers.SOF6:
                self.__sof6 = True

                if self.__sof \
                        and self.__sof2 \
                        and self.__sof3 \
                        and self.__sof4 \
                        and self.__sof5:
                    self.__ok = True
                else:
                    print('SOF markers are not defined')
                    exit(1)
            elif ord(ch) == climage_markers.SOW:
                self.__sow = True
            elif ord(ch) == climage_markers.SOH:
                self.__soh = True
            elif ord(ch) == climage_markers.Pixel8 \
                    or ord(ch) == climage_markers.Pixel16 \
                    or ord(ch) == climage_markers.Pixel32 \
                    or ord(ch) == climage_markers.Pixel64:
                if self.__sow or self.__soh:
                    if ord(ch) == climage_markers.Pixel8:
                        if self.__sow:
                            self.width = 8
                        else:
                            self.height = 8
                    elif ord(ch) == climage_markers.Pixel16:
                        if self.__sow:
                            self.width = 16
                        else:
                            self.height = 16
                    elif ord(ch) == climage_markers.Pixel32:
                        if self.__sow:
                            self.width = 32
                        else:
                            self.height = 32
                    elif ord(ch) == climage_markers.Pixel64:
                        if self.__sow:
                            self.width = 64
                        else:
                            self.height = 64

            elif ord(ch) == climage_markers.ColorStart:
                self.__color_start = True