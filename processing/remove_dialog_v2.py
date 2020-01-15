import re
from processing import globals
def remove_dialog(text, alpha):
    text = re.sub(r'[ \t]*-', '-', text)
    #print(text)
    final_text = ""
    i = 0
    while i < len(text):
        if i == 0 and text[i] == "-":
            while i < len(text) and text[i] != '\n':
                if text[i] in ".?!":
                    globals.NR_LINES_DIALOG_REMOVED += 1
                i += 1
        elif text[i] == "-" and text[i - 1] == "\n":
            while i < len(text) and text[i] != '\n':
                if text[i] in ".?!":
                    globals.NR_LINES_DIALOG_REMOVED += 1
                i += 1
        else:
            final_text += text[i]
            i += 1
    final_text = re.sub(r'[\n]+', '\n', final_text)
    #print(final_text)
    new_len = len(final_text)
    original_len = len(text)
    dialog_len = original_len - new_len
    alpha_dialog_cut = dialog_len * 1.0 / original_len * 100

    if int(alpha_dialog_cut) >= 99 - alpha or alpha_dialog_cut >= 100:
        new_alpha = 101
    else:
        new_alpha = int(100 * alpha / (100 - alpha_dialog_cut))
    return final_text, new_alpha

if __name__ == '__main__':
    text = r"Acasa el a spus: \" Ce bine e afaca!! nu stiu nimic.\"."
    print(str.splitlines(text))