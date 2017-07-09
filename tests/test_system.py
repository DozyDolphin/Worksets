import os
import unittest
import collections
from worksets.system import UbuntuWm as wm

print("Der eksekveres fra: " + os.getcwd)
os.chdir(os.getcwd() + "unity_worksets")

class SystemTest(unittest.TestCase):
    ''' Tests the system interface'''
    Xrandr_input = collections.namedtuple('Xrandr_input', 'input result')

    xrandr_test_1 = Xrandr_input(input=("TestScreen1 connected primary 1920x1080+0+0 (normal left inverted right x axis y axis) 521mm x 293mm\n"
                                        "TestScreen2 connected 1680x1050+1920+30 (normal left inverted right x axis y axis) 521mm x 293mm\n"
                                        "TestScreen3 connected 1280x800+3600+0 (normal left inverted right x axis y axis) 494mm x 320mm\n"
                                        "TestScreen4 connected 3440x1440+4880+40 (normal left inverted right x axis y axis) 494mm x 320mm"), result=['Screen1', 'Screen2', 'Screen3', 'Screen4'])

    xrandr_test_2 = Xrandr_input(input=("TestScreen1 connected primary 1920x1080+3440+0 (normal left inverted right x axis y axis) 521mm x 293mm\n"
                                        "TestScreen2 connected 1680x1050+1280+1440 (normal left inverted right x axis y axis) 521mm x 293mm\n"
                                        "TestScreen3 connected 1280x800+0+1440 (normal left inverted right x axis y axis) 494mm x 320mm\n"
                                        "TestScreen4 connected 3440x1440+0+0 (normal left inverted right x axis y axis) 494mm x 320mm"), result=['Screen4', 'Screen1', 'Screen3', 'Screen2'])

    xrandr_test_3 = Xrandr_input(input=("TestScreen1 connected primary 1920x1080+0+0 (normal left inverted right x axis y axis) 521mm x 293mm\n"
                                        "TestScreen2 connected 1680x1050+0+2520 (normal left inverted right x axis y axis) 521mm x 293mm\n"
                                        "TestScreen3 connected 1280x800+0+3570 (normal left inverted right x axis y axis) 494mm x 320mm\n"
                                        "TestScreen4 connected 3440x1440+0+1080 (normal left inverted right x axis y axis) 494mm x 320mm"), result=['Screen1', 'Screen4', 'Screen2', 'Screen3'])

    xrandr_test_4 = Xrandr_input(input=("TestScreen1 connected primary 1920x1080+0+1440 (normal left inverted right x axis y axis) 521mm x 293mm\n"
                                        "TestScreen2 connected 1680x1050+3200+1440 (normal left inverted right x axis y axis) 521mm x 293mm\n"
                                        "TestScreen3 connected 1280x800+1920+1440 (normal left inverted right x axis y axis) 494mm x 320mm\n"
                                        "TestScreen4 connected 3440x1440+0+0 (normal left inverted right x axis y axis) 494mm x 320mm"), result=['Screen4', 'Screen1', 'Screen3', 'Screen2'])

    xrandr_test_5 = Xrandr_input(input=("TestScreen1 connected primary 1920x1080+0+0 (normal left inverted right x axis y axis) 521mm x 293mm\n"
                                        "TestScreen2 connected 1680x1050+3440+800 (normal left inverted right x axis y axis) 521mm x 293mm\n"
                                        "TestScreen3 connected 1280x800+3440+0 (normal left inverted right x axis y axis) 494mm x 320mm\n"
                                        "TestScreen4 connected 3440x1440+0+0 (normal left inverted right x axis y axis) 494mm x 320mm"), result=['Screen1', 'Screen4', 'Screen3', 'Screen2'])

    xrandr_test_6 = Xrandr_input(input=("TestScreen1 connected primary 1920x1080+0+0 (normal left inverted right x axis y axis) 521mm x 293mm\n"
                                        "TestScreen2 connected 1680x1050+1920+30 (normal left inverted right x axis y axis) 521mm x 293mm\n"
                                        "TestScreen3 connected 3440x1440+3600+40 (normal left inverted right x axis y axis) 494mm x 320mm\n"
                                        "TestScreen4 connected 1280x800+4880+0 (normal left inverted right x axis y axis) 494mm x 320mm"), result=['Screen1', 'Screen2', 'Screen3', 'Screen4'])

    xrandr_inputs = [xrandr_test_1, xrandr_test_2, xrandr_test_3, xrandr_test_4, xrandr_test_5, xrandr_test_6]

    def test_parse_xrandr_output(self):

        for test_input in self.xrandr_inputs:
            output = wm._parse_xrandr_output(test_input)
            print(str(output))


if __name__ == '__main__':
    unittest.main()
