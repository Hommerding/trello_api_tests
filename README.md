# trello_api_tests
Automated tests for Trello API using Python

1) Install requests: pip3.8.exe install requests
2) Install selenium: pip3.8.exe install selenium
3) Install HTML Test Runner: pip install html-TestRunner
4) Install XML Test Runner: pip install xmlrunner
5) Download and install Chrome webdriver: https://chromedriver.chromium.org/downloads. Make sure to 
6) Add the path to chromedriver.exe to PATH environment variable
7) Create a Trello user using user/password method (https://trello.com/signup)
8) Login to Trello using the user/password created in the step #7
9) Navigate to https://trello.com/app-key and take note of the API key
10) On the same page, click on the link to generate a token manually
11) At the bottom of Server Token page, click on the Permit button to grant the permissions to Server Token
12) Take note of the generated token
13) Run the tests using the following command line: 
python trello_api_test.py [API key] [Server Token] [Trello user] [Trello password], 
e.g. python trello_api_test.py abcdef0123456789 11112222333344445555aaaabbbbccccddddeeee user@email.com somepassword
14) By the end of the test execution, a HTML report will be generated on the folder html_report
15) Screenshots of the testcases screens will be saved on the root tests folder
