from src.tools import (
    calculator,
    write_note,
    read_note,
    list_notes,
    current_datetime,
    word_count,
)

print(calculator("25*8+10"))

print(write_note("todo.txt", "Buy Milk"))

print(read_note("todo.txt"))

print(list_notes())

print(current_datetime())

print(word_count("Hello my name is Maurya"))