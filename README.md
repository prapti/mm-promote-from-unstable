# mm-promote-from-unstable

### Dependency: `requests` -- an HTTP library for Python
To install `requests`, run this following instruction in a terminal:
`python3 -m pip install requests`

Run this script with python 3 to get a list of E2E tests that are consistently passing in the unstable branch.
1. Get the build numbers for the last few unstable test runs.
2. Run this script with the command `python3 promote_from_unstable.py`.
3. Input the build numbers in the terminal, separated by spaces.
4. The list of all tests passing commonly across all the unstable builds will get printed in the console.

**Note: Any test cases within nested `describe` or `it` blocks will be excluded. Please verify them manually**