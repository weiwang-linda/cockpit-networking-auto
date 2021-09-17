# cockpit-networking-auto

This project uses selenium and avocado to automate tests for:

    cockpit-networking
    cockpit-networking-IPv6

## Usage

1. Clone the repo
2. Enter the project directory, install the dependency packages and enter to the virtualenv
```sh
$ poetry shell
$ poetry update

```

3. Configure config.yml with correct parameters.
4. Run tests
```sh
$ python run.py $tags -m local -b chrome
```

**$tags** is the avocado tests filter, each test_*.py file must has one unique file level tag, zero or more subtags. For example, there is a test_a.py with a file level tag 'TEST_A', and a subtag 'SUB1', then:
```sh
tags='networking_tier1' means to run tier1 tests in test_netwroking_check.py
tags='networking_tier2' means to run tier2 tests in test_netwroking_check.py
tags='IPv6_tier1' means to run tier1 tests in test_netwroking_ipv6_check.py
tags='IPv6_tier2' means to run tier2 tests in test_netwroking_ipv6_check.py
```

**Note**:
In order to implement yaml-to-mux plugin of Avocado, only tests in one test_*.py file can be run at a time.

**$browser** defines browser type, includes chrome, firefox, ie. If this option is omitted, chrome is used.