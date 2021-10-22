import enum

class Conditions(enum.Enum):
    EQUAL = 0
    GREATER = 1
    SMALLER = 2
    SMALLER_OR_EQUAL = 3
    GREATER_OR_EQUAL = 4

class CustomFonts(enum.Enum):
    BUTTON = ("Arial", 16)
    TITLE = ("Arial", 20)
    SUBTITLE = ("Arial", 18)
    ERROR = ("Arial", 20)
    SECTION = ("ArialBold", 24)