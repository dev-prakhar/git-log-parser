# Git Log Parser
A python library to parse git log command

## How to use
* Activate virtualenv `source git_log_env/bin/activate`
* Navigate to `main` directory `cd main`
* Run `python3 parse.py -h` --> This will generate the details on how to parse with different arguments

## Performance
* For fetching logs from a directory having `21,468` commits
    * CSV: `1.488 sec`
    * XML: `1.607 sec`
    * JSON: `1.627 sec`
