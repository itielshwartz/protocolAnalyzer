import csv
import glob
import os
from collections import defaultdict
from collections import namedtuple

base_values = ["first_name", "last_name", "full_name", "position", "committee", "date", "work_place", "role",
               "raw_line"]
Person = namedtuple('Person', base_values)

with open("full_names.csv") as f:
    raw_names = f.readlines()
    # List of israeli names
    names = set(name.strip() for name in raw_names)


def is_names_column(column):
    """
    :param column - list of names/ position
    :return:True if the column contain names
    """
    count_valid_name = 0
    for maybe_name in column:
        try:
            first_name, last_name = maybe_name.split(" ", 1)
            if first_name in names:
                count_valid_name += 1
        except Exception as e:
            pass
    return count_valid_name > len(column) * 0.25


def extract_people(file_name, committee=None, committee_date=None):
    """

    :param file_name: the file we are working on
    :param committee: the comititee name
    :param committee_date: the date the comitee took place
    :return: list of peoples, list of comittee_names that could not be parsed
    """
    peoples, problematic_names = [], []
    with open(file_name) as f:
        reader = csv.DictReader(f)
        left_column, right_column, raw_lines = [], [], []
        for row in reader:
            clean_data = row["header"].strip()
            if "מוזמנים" in clean_data:
                clean_data = row["body"].strip()
                if "-" in clean_data:
                    for line in clean_data.splitlines():
                        line = line.strip()
                        if line:
                            if line.count("-") == 1:
                                left_side, right_side = line.split("-")
                                left_column.append(left_side.strip())
                                right_column.append(right_side.strip())
                                raw_lines.append(line)
    comittee_names, positions = (left_column, right_column) if is_names_column(left_column) else (
        right_column, left_column)
    for full_name, position, raw_line in zip(comittee_names, positions, raw_lines):
        create_person(committee, committee_date, full_name, peoples, position, problematic_names, raw_line)
    return peoples, problematic_names


def create_person(committee, committee_date, full_name, peoples, position, problamtic_names, raw_line):
    '''
    Create the person and person attributes given data.
    '''
    try:
        first_name, last_name = full_name.split(" ", 1)
        role, work_place = "", ""
        if "," in position:
            role, work_place = position.split(",", 1)
        person = Person(first_name=first_name, last_name=last_name, position=position, full_name=full_name,
                        committee=committee, date=committee_date, raw_line=raw_line, role=role.strip(),
                        work_place=work_place.strip())
        peoples.append(person)
    except Exception as e:
        person = {"date": committee_date, "committee": committee, "line": raw_line}
        # pprint.pprint(person)
        problamtic_names.append(person)


protocol_dir = os.path.dirname(os.path.abspath(__file__))+"/**/*.csv"

def handle_files(file_path=None, file_prefix="/committee_"):
    '''
    The main function to start processing the files
    the function should be run (by default) with
    :return: peoples, errors
    '''
    peoples, errors = [], []
    for file_name in glob.iglob(os.path.dirname(__file__) + file_path, recursive=True):
        if file_prefix in file_name:
            _, partial_path = file_name.split(file_prefix)
            committee_name, raw_date, _ = partial_path.split("/")
            committee_date = raw_date.split("_")[1]
            people, problems = extract_people(file_name, committee=committee_name, committee_date=committee_date)
            peoples.extend(people)
            if problems:
                errors.append(problems)
    return peoples, errors


def analyze_jobs_per_person(peoples):
    """
    :param peoples:
    :return: full_name -> list of jobs
    """
    people_to_jobs = defaultdict(set)
    for people in peoples:
        if people.work_place:
            people_to_jobs[people.full_name].add(people.work_place)
        elif people.position:
            people_to_jobs[people.full_name].add(people.position)

    for people, jobs in people_to_jobs.items():
        jobs_to_filter = set()
        for curr_job in list(jobs):
            if curr_job not in jobs_to_filter:
                jobs_to_filter.update(set(filter(lambda job: curr_job != job and curr_job in job, jobs)))
        people_to_jobs[people] = jobs - jobs_to_filter
    people_to_jobs_clean = {k: "| ".join(v) for k, v in people_to_jobs.items() if len(v) > 1}
    return people_to_jobs_clean


def write_to_files(peoples, people_to_jobs_clean):
    with open('full_people_list.csv', 'w') as f:
        w = csv.writer(f)
        w.writerow(base_values)  # field header
        w.writerows([list(people) for people in peoples])

    with open('person_to_positions.csv', 'w') as f:
        w = csv.writer(f)
        w.writerow(["full_name", "positions"])  # field header
        w.writerows([c for c in people_to_jobs_clean.items()])


def main_flow():
    peoples, errors = handle_files(file_path=protocol_dir)
    people_to_jobs_clean = analyze_jobs_per_person(peoples)
    write_to_files(peoples, people_to_jobs_clean)


if __name__ == '__main__':
    main_flow()
