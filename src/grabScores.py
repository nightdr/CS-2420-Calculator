import re

from bs4 import BeautifulSoup


# necessary since gradescope lists "no submission" on missing assignments
def get_total_points(project_name):
    point_dict = {
        "lab07-circularqueue programming challenge": 20,
        "assignment5-sortinganalysis": 100,
        "assignment4-anagrams": 100,
        "lab04-sorting programming challenge": 10,
        "assignment03-sudoku": 100,
        "assignment 02-setonarraylist": 20,
        "assignment 01-matrix implementation": 10,
        "midterm 1": 100,
        "midterm 2": 100
    }
    if project_name in point_dict:
        return point_dict[project_name]
    else:
        return 0


def get_gradescope_scores(html_filepath, score_dict):
    with open(html_filepath, "r") as f:
        soup = BeautifulSoup(f, "html.parser")

    project_table = soup.find(id="assignments-student-table")

    projects = project_table.tbody.find_all("tr")

    for project in projects:
        title = project.th.text.lower()
        point_string = project.td.text

        earned_points = 0
        total_points = 0

        # don't use test assignment
        if title == "testassignment - do not submit anything":
            continue
        else:
            # if there is a score
            if len(point_string.split()) == 3:
                # "90.0 / 100.0" -> split() -> ["90.0", "/", "100.0"]
                earned_points = float(point_string.split()[0])
                total_points = float(point_string.split()[2])

            elif point_string.lower() == "no submission":
                time_remaining = project.find_all("span", {"class": "submissionTimeChart--timeRemaining"})
                # if project has time left to submit then skip it
                if len(time_remaining) > 0:
                    continue
                else:
                    total_points = get_total_points(title)
                    if total_points == 0:
                        continue

            # if project is submitted without being graded then skip it
            else:
                continue
        if total_points != 0:
            # add percentages to their respective categories
            if "midterm" in title:
                score_dict["midterms"][0] += earned_points
                score_dict["midterms"][1] += total_points
            elif "lab" in title:
                if "challenge" in title:
                    score_dict["programming challenges"][0] += earned_points
                    score_dict["programming challenges"][1] += total_points
                else:
                    score_dict["participation"][0] += earned_points
                    score_dict["participation"][1] += total_points
            else:
                score_dict["assignments"][0] += earned_points
                score_dict["assignments"][1] += total_points


def get_canvas_scores(html_filepath, score_dict):
    with open(html_filepath, "r") as f:
        soup = BeautifulSoup(f, "html.parser")

    project_table = soup.find(id="grades_summary")

    # get graded assignments
    projects = project_table.find_all("tr", {"class": ["student_assignment"]})
    projects = [project for project in projects if "assignment_graded" in project["class"]]

    for project in projects:
        title = project.th.a.text.lower()
        project_type = project.th.div.text.lower()

        parse_score_array = re.findall("\d+", project.find_all("span", {"class": "grade"})[0].text)

        # if there is a grade listed
        if len(parse_score_array) > 0:
            earned_points = int(parse_score_array[0])
            total_points = int(project.find_all("td", {"class": "points_possible"})[0].text)
            if total_points != 0:
                # add scores not recorded on gradescope to score_dict
                if project_type == "participation":
                    if "lab" in title and ("worksheet" in title or "hand in" in title):
                        score_dict["participation"][0] += earned_points
                        score_dict["participation"][1] += total_points
                elif project_type == "homeworks":
                    score_dict["homework"][0] += earned_points
                    score_dict["homework"][1] += total_points
