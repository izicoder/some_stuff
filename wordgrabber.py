#!/usr/bin/env python3
from sys import argv
from lxml import html
from requests import get

# global variables

WORD = (
    argv[1]
    if len(argv) == 2
    else "example")

FILE = (
    argv[2]
    if len(argv) == 3
    else "grab.txt")

# working functions


def gen_url(word):
    return "http://merriam-webster.com/dictionary/" + word


def get_page(word):
    page = get(gen_url(word))
    return page.text


def print_to_file(defs):
    with open(FILE, "w") as f:
        print(WORD, file=f)
        for i in defs:
            print("-"*15, file=f)
            print(i, file=f)

# main function


def main():
    tree = html.fromstring(get_page(WORD))
    defs = tree.xpath(
        "//div/ul/li"
        "/p[@class='definition-inner-item']"
        "/span/text()")
    print_to_file(defs)

# running

if __name__ == "__main__":
    main()
