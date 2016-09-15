import argparse
import random

if __name__ == '__main__':

    # read template records from file 
    template_records = []
    parser = argparse.ArgumentParser(
        description="Generate n tests, each with a timestep selected "
                    "randomly from a uniform distribution of 0 - t."
                    "Outputs stress test csv to stdout")
    parser.add_argument(
        "-f",
        "--tests_template",
        help="csv file of template records of form %t,url,method,config_json "
             "from which to generate actual tests (%i is replaced with record number)")
    parser.add_argument(
        "-n",
        "--num_tests",
        type=int,
        help="total number of tests to generate")
    parser.add_argument(
        "-t",
        "--total_time",
        type=int,
        help="total amount of time t")
     
    args = parser.parse_args()
    for line in open(args.tests_template, 'r'):
        template_records.append(line.strip())
    
    for i in range(args.num_tests):
        t = random.randint(0, args.total_time)
        n = random.randint(0, len(template_records)-1)
        selected_record = template_records[n]
        print(selected_record.replace('%t', str(t)).replace('%i', str(i)))
