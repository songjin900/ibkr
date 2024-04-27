from datetime import datetime

minFormat = '%Y-%m-%d %H:%M:%S%z'
dayFormat = '%Y-%m-%d'

def remove_records_before_date(data_list, target_date):
    target_datetime = datetime.strptime(target_date, '%Y-%m-%d %H:%M:%S')
    filtered_data = [record for record in data_list if datetime.strptime(record[0], '%Y-%m-%d %H:%M:%S') >= target_datetime]
    return filtered_data