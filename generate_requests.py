# -*- coding: utf-8 -*-
import argparse
import random

if __name__ == '__main__':

    # read template records from file 
    template_records = []
    parser = argparse.ArgumentParser(
        description=
    '''
    Generate n tests, each with a timestep selected randomly from range(0, t+1)
    
    Outputs requests as csv suitable for input to http_stress.py
    ''',
        formatter_class=argparse.RawTextHelpFormatter)

    parser.add_argument(
        "requests_template",
        help=
        '''
        csv file of template records of form:
        %t,url,method,config_json 
        
        where %t is a randomly selected time from range(0, t+1) and
        any %i within any record is replaced by the assigned record number
        ''')
    parser.add_argument(
        "-n",
        "--num_requests",
        type=int,
        help="total number of requests to generate")
    parser.add_argument(
        "-t",
        "--total_time",
        type=int,
        help=
        '''
        Total time over which requests should be run
        
        Defines the 't' in the range(0, t+1) from which a requests execution 
        time should be randomly assigned 
        ''')
     
    args = parser.parse_args()
    for line in open(args.requests_template, 'r'):
        template_records.append(line.strip())
    
    for i in range(args.num_requests):
        t = random.randint(0, args.total_time)
        n = random.randint(0, len(template_records)-1)
        selected_record = template_records[n]
        print(selected_record.replace('%t', str(t)).replace('%i', str(i)))
