import sys
from src import parsing
from src import bot

def main():
    for arg in sys.argv:
        parsing.parse_main_page(arg)


if __name__ == '__main__':
    main()
