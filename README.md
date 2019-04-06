# Git Log Parser
A python library to parse git log command

## How to use
* Activate virtualenv `source git_log_env/bin/activate`
* Navigate to `main` directory `cd main`
* Run `python3 parse.py -h` --> This will generate the details on how to parse with different arguments

## Performance
* For about `22,500` commits
    * CSV: `1.488 sec`
    * JSON: `1.627 sec`
    * XML: `24.227 sec` _Parsing to XML takes a long time_
