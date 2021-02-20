import os, sys, shutil, json
from preprocessing import *


def rename(dirs, parent_dir, question_names):
    need_rename = {}

    for student in dirs:
        student_path = os.path.join(parent_dir, student)
        # change question name
        unable = change_question_name(student_path, question_names)
        if unable:
            need_rename[student] = unable

    if need_rename:
        print("These files need to be renames to their question number: ")
        print(json.dumps(need_rename, indent=4))
        answer = confirmation(
            'Continue marking without renaming the above files? (y/n): ')
        if not answer:
            print("Exiting...")
            exit()


def confirmation(question):

    to_rename = input(question)
    if to_rename.lower() == 'n':
        return False
    elif to_rename.lower() == 'y':
        return True
    else:
        print("Please enter either 'y' or 'n'.")
        confirmation(question)


def parse_testcase(parent_dir):

    testcase_dir = os.path.join(parent_dir, 'testcase.py')
    try:
        with open(testcase_dir, 'r') as file:
            lines = ''.join(file.readlines()).split('\n')
    except Exception as e:
        print(e)
        print(f'Please create a testcase.py file in {parent_dir}')
    
    testcases = {"functions": dict()}

    for line in lines:
        if '#' in line:
            question_number = line[2:]
            question_number = f"q{'_'.join(question_number.split('.'))}"
            testcases[question_number] = []
        elif line:
            question_number = list(testcases.keys())[-1]
            testcases[question_number].append(line[6:-1])
            function = line.split('(')[1]
            if function not in testcases['functions']:
                testcases['functions'][question_number] = function

    return testcases


def mark_question(function, testcases):
    """
    mark one question and output the stats
    if error, note it as an error instead of 0
    """
    score = []

    for testcase in testcases:
        score.append(function(testcase))

    return sum(int(n) for n in score)
    