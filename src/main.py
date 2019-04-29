import sys
import parsing
from telegram.ext import Updater, CommandHandler
import logging


def main():
    for arg in sys.argv:
        parsing.parse_main_page(arg)


if __name__ == '__main__':
    main()
