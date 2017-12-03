"""
tests.py
Developer: Dean Hutton
Project: Direct Report Anniversary Calculator
Description: Unit tests for direct_reports.py
Date: 12/3/17
"""
import direct_reports
from datetime import datetime
import os


"""
Test that verifies the next 5 upcoming date milestones have a difference of 5 years between them. If the difference is 
not 5 error out and return an error message.
"""


def test_calculate_anniversary_dates():

    hire_date = datetime(2008, 7, 22, 0, 0)
    run_date = datetime(1000, 3, 24, 0, 0)

    anniversary_dates = direct_reports.calculate_anniversary_dates(
        hire_date,
        run_date
    )

    for count, anv_date in enumerate(anniversary_dates):
        next_year_incrementer = count + 1
        year = anv_date.year

        # Avoid list index out of range error
        if next_year_incrementer == len(anniversary_dates):
            break

        next_year = anniversary_dates[next_year_incrementer].year

        assert next_year - year == 5, 'The difference between the years is not equal to 5'


"""
Test that the types in the date structures read from a valid CSV are correct
"""


def test_etl_csv_file_with_valid_dates():
    test_file_path = "%s/%s" % (os.getcwd(), "test_employee_info_valid.csv")
    all_employee_dict, supervisor_employee_dict = direct_reports.etl_csv_file(
        test_file_path
    )

    for employee in all_employee_dict:
        assert all_employee_dict[employee] == 'Sorry, this person is not a supervisor'

    for supervisor in supervisor_employee_dict:
        employee_direct_reports = supervisor_employee_dict[supervisor]
        for employee in employee_direct_reports:
            assert isinstance(employee.get('last_name'), str), 'Employee last name should be of type string'
            assert isinstance(employee.get('first_name'), str), 'Employee first name should be of type string'
            assert isinstance(employee.get('employee_id'), str), 'Employee ID should be of type string'
            assert isinstance(employee.get('hire_date'), datetime), 'Employee hire date should be of type datetime'


"""
Test if there is an invalid date format in the CSV file
"""


def test_etl_csv_file_with_invalid_dates():
    test_file_path = "%s/%s" % (os.getcwd(), "test_employee_info_invalid_date.csv")
    all_employee_dict, supervisor_employee_dict = direct_reports.etl_csv_file(
        test_file_path
    )
    assert all_employee_dict == False
    assert supervisor_employee_dict == "There has been an error parsing a date in the input file. Please correct '1977-09-02BADBADBAD' at line '0' so that it follows follows the '2011-03-24' date format."


"""
Test if the CSV file has an invalid header
"""


def test_etl_csv_file_with_invalid_header():
    test_file_path = "%s/%s" % (os.getcwd(), "test_employee_info_invalid_header.csv")
    all_employee_dict, supervisor_employee_dict = direct_reports.etl_csv_file(
        test_file_path
    )
    assert all_employee_dict == False
    assert "CSV file must be employee_id,first_name,last_name,hire_date,supervisor_id" in supervisor_employee_dict


"""
Test if the milestone list for supervisors has the correct amount of supervisors
"""


def test_generate_milestone_data_with_valid_data():
    test_file_path = "%s/%s" % (os.getcwd(), "test_employee_info_valid.csv")
    run_date = datetime(1000, 3, 24, 0, 0)

    all_employee_dict, supervisor_employee_dict = direct_reports.etl_csv_file(test_file_path)
    supervisor_milestone_list, all_employee_dict = direct_reports.generate_milestone_data(
        supervisor_employee_dict,
        all_employee_dict,
        run_date
    )
    assert len(supervisor_milestone_list) == 8
    assert len(all_employee_dict) == 14
