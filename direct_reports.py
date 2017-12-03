"""
direct_reports.py
Developer: Dean Hutton
Project: Direct Report Anniversary Calculator
Date: 04/25/2016

References:
http://stackoverflow.com/questions/3483520/use-cases-for-the-setdefault-dict-method
http://stackoverflow.com/questions/9504356/convert-string-into-date-type-on-python
http://stackoverflow.com/questions/6740918/creating-a-dictionary-from-a-csv-file
http://stackoverflow.com/questions/674519/how-can-i-convert-a-python-dictionary-to-a-list-of-tuples
http://stackoverflow.com/questions/15741618/add-one-year-in-current-date-python
http://www.cyberciti.biz/faq/python-command-line-arguments-argv-example/
http://stackoverflow.com/questions/82831/how-to-check-whether-a-file-exists-using-python
"""

import csv
import sys
import argparse
import os.path
import pprint

from operator import itemgetter
from dateutil.relativedelta import relativedelta
from datetime import datetime


def calculate_anniversary_dates(hire_date, run_date):
    """
    Function that calculates the next 5 upcoming milestones for an employee and checks to see if
    they are greater than the run_date. If not greater than the run_date then keep calculating until there at least
    five milestones and then return

    :param datetime hire_date: The date the employee was hired
    :param datetime run_date: The run_date sent from the command line. Every mile stone must be greater than this

    :return: Returns 5 upcoming milestones for given hire_date and run_date
    :rtype: list
    """

    anniversary_dates = []
    year_increment = 5
    while len(anniversary_dates) < 5:
        new_date = hire_date + relativedelta(years=year_increment)
        year_increment += 5
        if new_date < run_date:
            continue
        anniversary_dates.append(new_date)

    return anniversary_dates


def etl_csv_file(input_file_location):
    """
    Reads and parses the input CSV file in a data structure that connects supervisors to their direct reports. It
    also keeps track of all the employees in a separate dict to later be used for printing.

    :param str input_file_location: The physical location of the input file on disk

    :return: Two dicts: One with the employee & supervisor relationship and another with all employees.
    :rtype: dict
    """

    all_employee_dict = {}
    supervisor_employee_dict = {}
    header_row = 'employee_id,first_name,last_name,hire_date,supervisor_id'

    with open(input_file_location, mode='r') as employee_csv_file:

        # verify the header exists. If the header is not correct error out and return
        first_row = next(employee_csv_file, None)
        if first_row.rstrip() != header_row:
            return False, "The header row in the %s CSV file must be %s" % (input_file_location, header_row)

        employee_csv_reader = csv.reader(employee_csv_file)
        for count, row in enumerate(employee_csv_reader):

            # validate each date in the input file can be casted to datetime object
            try:
                hire_date = datetime.strptime(row[3], '%Y-%m-%d')
            except ValueError as e:
                print (e)
                message = "There has been an error parsing a date in the input file. Please correct '{0}' at " \
                          "line '{1}' so that it follows follows the '2011-03-24' date format.".format(row[3], count)
                return False, message

            employee_id = row[0]
            employee = {
                'employee_id': employee_id,
                'first_name': row[1],
                'last_name': row[2],
                'hire_date': hire_date,
            }

            supervisor_id = row[4]

            #  This is used later to print out ALL employees according to requirements
            all_employee_dict[employee_id] = 'Sorry, this person is not a supervisor'

            # Append to list if key already exists
            group = supervisor_employee_dict.setdefault(supervisor_id, [])
            group.append(employee)

    return all_employee_dict, supervisor_employee_dict


def generate_milestone_data(supervisor_employee_dict, all_employee_dict, run_date):
    """
    Function that generates the milestone data to later be used during printing.

    :param dict supervisor_employee_dict: The supervisor and employee relationship dictionary
    :param dict all_employee_dict: All of the employess in one dict
    :param datetime run_date: The run_date sent from the command line. Every mile stone must be greater than this

    :return: Two dicts: One with the supervisor and employee milestones and another with employees that are not
    supervisors.

    :rtype: dict
    """
    supervisor_milestone_list = []
    for supervisor_id in supervisor_employee_dict:
        supervisor_milestone_dict = {}
        employees = supervisor_employee_dict[supervisor_id]
        employee_dict = {}

        milestone_counter = 0

        # Remove the supervisor from all the employees leaving the non-managers behind
        all_employee_dict.pop(supervisor_id, None)
        supervisor_milestone_dict['supervisor_id'] = supervisor_id

        for emp in employees:
            hire_date = emp.get('hire_date')
            emp_id = emp.get('employee_id')
            anv_dates = calculate_anniversary_dates(
                hire_date,
                run_date
            )

            # This is built to support employees that share a common milestone date
            for date in anv_dates:
                group = employee_dict.setdefault(date, [])
                group.append(emp_id)

        # Sort the dict by date by converting into tuple and sorting
        milestone_tuple = [(v, k) for k, v in employee_dict.iteritems()]
        sorted_ms_tup = sorted(milestone_tuple, key=itemgetter(1))
        upcoming_milestone_list = []

        for employee_id_list, milestone_date in sorted_ms_tup:
            for emp_id in employee_id_list:

                # Do not print out more than 5 milestones
                if milestone_counter == 5:
                    break

                upcoming_milestone = {
                    'employee_id': emp_id,
                    'anniversary_date': str(milestone_date)
                }
                upcoming_milestone_list.append(upcoming_milestone)
                milestone_counter += 1

        supervisor_milestone_dict['upcoming_milestones'] = upcoming_milestone_list
        supervisor_milestone_list.append(supervisor_milestone_dict)

    return supervisor_milestone_list, all_employee_dict


def main():
    """
    Main execution of program that is called when script is ran.
    """
    # Parse the required args for processing
    parser = argparse.ArgumentParser(description='This is a direct report calculator made by Dean Hutton')
    parser.add_argument('-i', '--input', help='Input file name used to run direct reports on.', required=True)
    parser.add_argument('-rd', '--run_date', help='The date to display direct reports for.', required=True)
    args = parser.parse_args()

    input_file_location = args.input

    # Do error checking making sure run_date is valid date and that input file exists
    if not os.path.isfile(input_file_location):
        print('There has been an error locating the input file. Please make sure this file exists {}'.format(args.input))
        sys.exit()

    try:
        run_date = datetime.strptime(args.run_date, '%Y-%m-%d')
    except ValueError as e:
        print("There has been an error parsing the run date. Please correct this date '{0}' "
              "so that it follows follows the '2011-03-24' date format.".format(args.run_date))
        sys.exit()

    all_employee_dict, supervisor_employee_dict = etl_csv_file(input_file_location)

    # Check to see if there was an error parsing the CSV file and if so print it and exit
    if not all_employee_dict:
        print supervisor_employee_dict
        sys.exit()

    supervisor_milestone_list, all_employee_dict = generate_milestone_data(
        supervisor_employee_dict,
        all_employee_dict,
        run_date
    )
    non_supervisor_list = []

    # Create placeholders for all employees that are not supervisors so they can be printed
    for non_supervisor_id in all_employee_dict:
        non_sv_dict = {}
        non_sv_dict['supervisor_id'] = non_supervisor_id
        non_sv_dict['upcoming_milestones'] = 'No direct reports'
        non_supervisor_list.append(non_sv_dict)

    # Combine supervisors with non-supervisors for printing
    final_output_list = supervisor_milestone_list + non_supervisor_list

    # # Print out the results
    print ('Plain Text')
    pprint.pprint(final_output_list)


if __name__ == "__main__":
    # execute only if run as a script
    main()




