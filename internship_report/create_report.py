import argparse
import datetime
import os
from math import ceil
from dateutil.relativedelta import relativedelta
from ingest_data import create_collection
from query_data import create_report_from_blog, create_report_from_reports, save_report
from translate_report import translate_report

START_DATE = datetime.date(2023, 3, 1) # first ever blog entry date

def calculate_days_diff(start_date=START_DATE, end_date=datetime.date.today()):
    days_diff = (end_date-start_date).days
    return days_diff

def get_files_names(folder_path, date_limit, start_date):
    files = os.listdir(folder_path)
    files.sort()

    en_files = []
    for file in files:
        if ('_index' not in file) and ('.pt' not in file):
            year = int(file[:4])
            month = int(file[5:7])
            day = int(file[8:10])
            file_date = datetime.date(year, month, day)

            if calculate_days_diff(file_date, date_limit) >= 0 and calculate_days_diff(start_date, file_date) >= 0:
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

    parser.add_argument("--folder_path", default="./content/posts/")
    parser.add_argument("--date_limit", default=datetime.date.today())

    args = parser.parse_args()

    days_diff = calculate_days_diff(end_date=args.date_limit)

    if days_diff <= 90:
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
    translate_report()

if __name__ == "__main__":
    main()