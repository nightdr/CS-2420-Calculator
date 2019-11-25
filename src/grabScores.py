import re

from bs4 import BeautifulSoup


def get_gradescope_scores(html_filepath, score_dict):
    with open(html_filepath, "r") as f:
        soup = BeautifulSoup(f, "html.parser")

    project_table = soup.find(id="assignments-student-table")

    projects = project_table.tbody.find_all("tr")

    for project in projects:
        title = project.th.text.lower()
        point_string = project.td.text

        # filters out projects that aren't graded or turned in
        if len(point_string.split()) == 3:
            # gets percentage from point_string
            # e.g. "90.0 / 100.0" -> split() -> ["90.0", "/", "100.0"] -> 90.0 / 100.0 -> 0.9
            percentage = float(point_string.split()[0]) / float(point_string.split()[2])

            # add percentages to their respective categories
            if "midterm" in title:
                score_dict["midterms"].append(percentage)
            elif "lab" in title:
                if "challenge" in title:
                    score_dict["programming challenges"].append(percentage)
                else:
                    score_dict["participation"].append(percentage)
            else:
                score_dict["assignments"].append(percentage)


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

        score = project.find_all("span", {"class": "grade"})[0].text
        parse_int_array = re.findall("\d+", score)

        # if there is a grade listed
        if len(parse_int_array) > 0:
            score = int(parse_int_array[0])
            total = int(project.find_all("td", {"class": "points_possible"})[0].text)
            if total != 0:
                percentage = score / total

                # add scores not recorded on gradescope to score_dict
                if project_type == "participation":
                    if "lab" in title and ("worksheet" in title or "hand in" in title):
                        score_dict["participation"].append(percentage)
                elif project_type == "homeworks":
                    score_dict["homework"].append(percentage)
