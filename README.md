# HTTP-Stress

Lightweight tools for stress testing a set of http endpoints

## Setup

Create a python 3.5+ based environment (via virtualenv or conda), source it 
and install the dependencies via `pip install -r requirements.txt`

## Example Usage

If you don't have a server up, you can modify sample_server.py and bring it up
```shell
$ python -m aiohttp.web -H localhost -P 9000 server:init
```

Then you can generate the test requests and run them
```shell
# show input template
$ cat http_requests_template.csv
%t,http://localhost:9000/jobs,GET,{"headers": {"Accept": "application/json"}}
%t,http://localhost:9000/status,GET,{"headers": {"Accept": "application/json"}}
%t,http://localhost:9000/jobs,POST,{"files": {"zip_file": "sleep_count_8.zip"}, "data": {"model": "test", "job_name": "sleep_8_%i"}, "headers": {"Accept": "application/json"}}

# generate 6 requests over 10 time steps from template
$ python generate_requests.py -n 6 -t 10 http_requests_template.csv > http_requests.csv

# show generated requests
$ cat http_requests.csv
10,http://localhost:9000/jobs,POST,{"files": {"zip_file": "sleep_count_8.zip"}, "data": {"model": "test", "job_name": "sleep_8_0"}, "headers": {"Accept": "application/json"}}
1,http://localhost:9000/status,GET,{"headers": {"Accept": "application/json"}}
1,http://localhost:9000/jobs,POST,{"files": {"zip_file": "sleep_count_8.zip"}, "data": {"model": "test", "job_name": "sleep_8_2"}, "headers": {"Accept": "application/json"}}
1,http://localhost:9000/jobs,GET,{"headers": {"Accept": "application/json"}}
9,http://localhost:9000/jobs,GET,{"headers": {"Accept": "application/json"}}
5,http://localhost:9000/jobs,GET,{"headers": {"Accept": "application/json"}}

# run them
$ python http_stress.py http_requests.csv
3,http://localhost:9000/jobs,POST,{"result": "OK"}
3,http://localhost:9000/jobs,POST,{"result": "OK"}
4,http://localhost:9000/jobs,POST,{"result": "OK"}
4,http://localhost:9000/status,GET,{"result": "OK"}
9,http://localhost:9000/jobs,GET,{"result": "OK"}
10,http://localhost:9000/jobs,POST,{"result": "OK"}
```
