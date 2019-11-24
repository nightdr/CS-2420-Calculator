import grabScores
import re
from time import sleep
import tkinter as tk
from tkinter import filedialog


def get_directory(title):
    root = tk.Tk()
    root.withdraw()

    file_path = filedialog.askopenfilename(filetypes=[("html files", "*.html")], title=title)

    return file_path


def calculate_class_percentage():
    class_percentage = 0
    weight_total = 0

    # compute weighted percentage
    for key in scores:
        # if there are scores recorded
        if len(scores[key]) != 0:
            weight_total += weights[key]
            # add weighted percentage (weight * average percentage) to class_percentage
            class_percentage += weights[key] * (sum(scores[key]) / len(scores[key]))

    # divide class percentage by used weights
    class_percentage /= weight_total
    class_percentage *= 100

    return class_percentage


def calculate_final_score():
    calculate_boolean = input("Calculate percentage needed on final for grade? (Y or N)\n")
    if calculate_boolean.lower() == "y":
        # get desired percentage
        user_percentage_array = re.findall("\d+", input("Desired percentage: \n"))
        # if number found in input
        if len(user_percentage_array) > 0:
            user_percentage = float(user_percentage_array[0])
            # calculate final score needed
            final_needed = (user_percentage - 0.80 * class_percentage) / 0.20
            print("Final score needed for ", user_percentage, "%: ", final_needed, "%", sep="")
        else:
            print("No percentage found")


scores = {
    "participation": [],
    "programming challenges": [],
    "homework": [],
    "midterms": [],
    "final": [],
    "assignments": [],
}

weights = {
    "participation": 0.10,
    "programming challenges": 0.08,
    "homework": 0.07,
    "midterms": 0.20,
    "final": 0.20,
    "assignments": 0.35
}

if __name__ == "__main__":
    # get documents from user
    print("Select Gradescope Document: ")
    sleep(0.5)
    gradescope_document = get_directory("Select Gradescope Document")

    print("Select Canvas Document: ")
    sleep(0.5)
    canvas_document = get_directory("Select Canvas Document")

    # if documents selected
    if gradescope_document and canvas_document:
        # grab scores from documents
        grabScores.get_gradescope_scores(gradescope_document, scores)
        grabScores.get_canvas_scores(canvas_document, scores)

        class_percentage = calculate_class_percentage()
        print("Current percentage: ", round(class_percentage, 2), "%", sep="")

        # run final percentage dialog
        calculate_final_score()

    else:
        print("Files not selected")
