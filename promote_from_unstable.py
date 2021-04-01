import requests
import logging

FORMAT = '%(message)s'
logging.basicConfig(level=logging.INFO, format=FORMAT)

specs_to_promote = []
tests_not_counted = {}

# Enter build numbers separated by spaces
# Example: 3984 3972 4012 3948 3936
builds_input = input()
builds = builds_input.split(' ')

def create_passed_tests_list(build, test_list):
    url = 'https://mm-cypress-report.s3.amazonaws.com/%s-master-e20-unstable-mattermost-enterprise-edition:master/all.json' % build

    response = requests.get(url).json()
    results = response['results']

    for tests in results:
        filepath, filename = tests['file'].split('cypress/integration/', 1)
        suite = tests['suites'][0]
        suite_tests = suite['tests']
        title = suite['title']
        for test in suite_tests:
            if not (suite['failures'] or suite['skipped'] or suite['pending']):
                test_list.append(test['title'])

        # Nested `describe` and `it` blocks are excluded for now
        # Will flush this out in the future
        if not suite_tests:
            tests_not_counted[filename] = title

def compare_passed_tests():
    passed_tests = []
    for build in builds:
        if passed_tests:
            next_test_list = []
            create_passed_tests_list(build, next_test_list)
            passed_tests = list(set(passed_tests) & set(next_test_list))
        else:
            create_passed_tests_list(build, passed_tests)
    logging.info("Total tests to promote: %s" % str(len(passed_tests)))
    return passed_tests

list_to_promote = compare_passed_tests()
logging.info("--------------------The following tests have passed in all reports: --------------------")
for to_promote in list_to_promote:
    logging.info(to_promote)
