Some testing of the network is available using pytest.

Please ensure the network is in a "fresh" state by running `manage-network restart` in the parent directory.

Run `pytest -x -rA network_testing.py` to run some unit tests on the iroha multinode network.
- `pytest` is a python testing program. It will automatically read the `network_testing.py` file and determine how to apply the tests within
- `-x` means to break from the program when one test fails. This is done because later tests rely on earlier tests (e.g. one of the first tests is creating a domain. If this test fails then the next test, creating an asset in that domain, will also fail)
- `-rA` means we will get more information on all tests at the end of testing, rather than just the failed tests.

`network_testing.py` holds some documentation in the function docstrings about what is being tested, and the names provide a summary.

Also, please note these tests were developed in python 3.10.0 and have not been checked on other versions. If you find that the tests fail on your machine, this may be the culprit, although I have not employed any 3.10 specific features.