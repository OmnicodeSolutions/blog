import argparse
import datetime
import os
from math import ceil
from dateutil.relativedelta import relativedelta
from ingest_data import create_collection
from query_data import create_report_from_blog, create_report_from_reports, save_report

START_DATE = '2023-10-03' # first ever blog entry date

def calculate_months_diff(date_limit_str):
    start_date = datetime.datetime.strptime(START_DATE,"%Y-%m-%d")
    date_limit = datetime.datetime.strptime(date_limit_str, "%Y-%m-%d")

    months_diff = (date_limit.year - start_date.year) * 12 + date_limit.month - start_date.month
    return months_diff

def calculate_days_diff(start_date_str, end_date_str):
    start_date = datetime.datetime.strptime(start_date_str,"%Y-%m-%d")
    end_date = datetime.datetime.strptime(end_date_str, "%Y-%m-%d")

    days_diff = (end_date-start_date).days
    return days_diff

def get_files_names(folder_path, date_limit, start_date):
    files = os.listdir(folder_path)
    files.sort()

    en_files = []
    for file in files:
        file_date = file[:10]
        if calculate_days_diff(file_date, date_limit) >= 0 and calculate_days_diff(start_date, file_date) >= 0:
            if ('.pt' not in file) and ('_index' not in file):
                en_files.append(file)
        else:
            break

    return en_files

def split_array(array, size):
    result = []
    for i in range(0, len(array), size):
        result.append(array[i:i+size])
    return result

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("--folder_path", default="../content/posts/")
    parser.add_argument("--date_limit", default=datetime.date.today())

    args = parser.parse_args()

    months_diff = calculate_months_diff(args.date_limit)

    if months_diff <= 3:
        files = get_files_names(args.folder_path, args.date_limit, START_DATE)
        create_collection(args.folder_path, files)
        report = create_report_from_blog()
    else:
        trimester_reports = []
        
        files = get_files_names(args.folder_path, args.date_limit, START_DATE)
        trimester_files = split_array(files, 90)

        for trimester in trimester_files:
            create_collection(args.folder_path, trimester)
            trimester_report = create_report_from_blog()
            trimester_reports.append(trimester_report)

        report = create_report_from_reports(trimester_reports)
    
    save_report(report)

if __name__ == "__main__":
    main()