#!/usr/bin/python
import re

class xbeebeacon(object):
    """docstring for xbeebeacon"""
    def __init__(self, RSS, SSID, BSS):
        super(xbeebeacon, self).__init__()
        self.BSS = BSS
        self.RSS = self.num(RSS)
        self.SSID = SSID


    def num(self, s):
        try:
            return int(s)
        except ValueError:
            return float(s)

def main(arg):
    pass

if __name__ == "__main__":
    main()
