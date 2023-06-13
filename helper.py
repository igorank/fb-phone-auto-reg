
def remove_line_by_text(filename: str, text: str) -> None:
    with open(filename, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    with open(filename, 'w', encoding='utf-8') as file_w:
        for line in lines:
            if line.find(text) == -1:
                file_w.write(line)
