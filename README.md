# Pwned Finder
_**Version:** 0.01-ALPHA_

## Description
Finds 
## Usage
### Installation
1. Install virtualenv  (OPTIONAL)
```bash
$ python3 pip install virtualenv
```
2. Create and activate the project's virtual environment (OPTIONAL)
```bash
$ virtualenv pwnedFinder-v1
$ source pwnedFinder-v1/bin/activate
```

\** To deactivate the virtual environment use the following commands:
```bash
$ deactivate
```

3. Install the project's dependencies
```bash
$ pip install -r requirements.txt 
```
### Usage
General Usage:

```bash
$ python main.py -h
usage: main.py [-h] [--version] [--target TARGET] [--find-dumps]

Find in which dumps the credentials (username/email) provided is pwned.

optional arguments:
  -h, --help            show this help message and exit
  --version             Prints the version information and exits.
  --target TARGET, -t TARGET
                        List of targets to search for pwned credentials.
  --find-dumps, -fd     Attempts to find a downloadable dump containing the
                        target's password or hash

```

Usage Examples:

* Find if an username or email address has been breached
```bash
$ python main.py -t test@gmail.com
Found leaked databases containing credentials of the supplied target: test@gmail.com
Name: Tumblr
Name: WeHeartIt

```
* Get downloadable links to the dumps containing the target's username or email address
```bash
$ python main.py -t test@gmail.com -fd 
Found dump(s) containing credentials of the supplied target: test@gmail.com

            Name: 000webhost_13mil_plain_Oct_2015.7z
            Size: (286.17 MB)
            URL: https://cdn.databases.today/000webhost_13mil_plain_Oct_2015.7z

            Name: 000webhost.com.txt.gz
            Size: (315.25 KB)
            URL: https://cdn.databases.today/random/dumps/000webhost.com.txt.gz

```