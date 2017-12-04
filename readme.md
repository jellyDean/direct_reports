Milestone Calculator Usage <br /> 
4/26/16 <br />
Dean Hutton <br />

# Summary
This guide illustrates how to run the direct_reports.py program for upcoming milestone calculations. 
Direct_reports.py was built with Python 2.7.7 so it is recommended to use that version of the interpreter 
while running. If you are running on Mac OSX it will be installed by default. This can be checked by running 
```python ­V``` on the terminal. Any version of Python between 2.7 and including 2.9 will work fine with this program.
It is recommended to use a python Virtual Environment to run this application but it is not required.

# Required Python Libraries
In order to run direct_reports.py the following Python libraries must be installed in your virtual environment. Again,
it is recommended to use a virtual environment to house all these libraries and install them via PIP. 

1. nose 1.3.7 - To run unit tests
2. pip 9.0.1 - To install Python libraries
3. python-dateutil 2.6.1 - To convert strings to dateTime objects
4. setuptools - 38.23.3
5. six - 1.11.0 - Installed with python-dateutil
6. wsgiref - 0.1.2


# Setup and Usage
1. Setup and install a Python 2.7.10 Virtual Environment (VE). If you are unsure of how to do this see [here](http://www.pythonforbeginners.com/basics/how-to-use-python-virtualenv) 
2. Clone the repo ```git clone https://github.com/jellyDean/direct_reports.git ```
3. Open a terminal and CD in to your VE ``` cd /Users/deanhutton/workdir/Personal/VE/2.7.10/bin ```  
4. Activate the Virtual Environment ``` . activate.fish ```
5. Install the above Required Python Libraries via PIP
6. Navigate to the repo ``` cd /Users/deanhutton/workdir/Personal/Repos/direct_reports ```
7. Run the script by executing ``` python direct_reports.py -i employee_info.csv -rd 2011-03-24 ``` where ­i is the location of your input file and ­rd is the run date


# Running Tests
1. Follow steps 1-5 in the Setup and Usage section above
2. Navigate to the tests directory ``` cd /Users/deanhutton/workdir/Personal/Repos/direct_reports/tests ```
3. Enter ``` nosetests ``` in terminal and push enter
4. 5 Unit tests will run