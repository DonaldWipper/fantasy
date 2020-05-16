import pandas as pd  # data processing, CSV file I/O (e.g. pd.read_csv)
import datetime
import math
import re
from html.parser import HTMLParser


def hasNumbers(inputString):
    return any(char.isdigit() for char in inputString)


class MyHTMLParser(HTMLParser):
    def __init__(self, flag_print_parse_log=False):
        HTMLParser.__init__(self)
        self.flag_print_parse_log = flag_print_parse_log
        self.is_tour = False
        self.cur_tag = None
        self.tours = {}
        self.leagues = []
        self.tour = None

    def handle_starttag(self, tag, attrs):
        if self.flag_print_parse_log == True:
            print("Start tag:", tag)
        self.cur_tag = tag

        for attr in attrs:
            if self.flag_print_parse_log == True:
                print("     attr:", attr)
            if attr[0] == "href" and attr[1].find("fantasy/football/league/") > -1:
                self.leagues.append(attr[1])
            if attr[0] == "id" and attr[1] == "fan_points_select":
                # print('start points')
                self.is_tour = True
            if self.is_tour == True and self.cur_tag == "option":
                self.tour = attr

    def handle_endtag(self, tag):
        if self.flag_print_parse_log == True:
            print("End tag  :", tag)

    def handle_data(self, data):
        if self.flag_print_parse_log == True:
            print("Data     :", data)
        if (
            self.is_tour == True
            and self.cur_tag == "option"
            and data.strip() != ""
            and hasNumbers(data.strip())
        ):
            number = re.search(r"\d+", data.strip()).group()
            self.tours[int(number)] = int(self.tour[1])

    def handle_comment(self, data):
        if self.flag_print_parse_log == True:
            print("Comment  :", data)

    def handle_entityref(self, name):
        c = chr(name2codepoint[name])
        if self.flag_print_parse_log == True:
            print("Named ent:", c)

    def handle_charref(self, name):
        if name.startswith("x"):
            c = chr(int(name[1:], 16))
        else:
            c = chr(int(name))
        if flag_print_parse_log == True:
            print("Num ent  :", c)

    def handle_decl(self, data):
        if self.flag_print_parse_log == True:
            print("Decl     :", data)
