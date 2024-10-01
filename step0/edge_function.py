import json
import pandas as pd
from datetime import datetime, time

# 파일 경로 설정 (Colab 환경에서 직접 참조)
METADATA_FILE_PATH = '/content/metadata.json'  # JSON 파일 경로 (예: S3에서 다운로드된 파일 경로)
COMPARISON_FILE_PATH = '/content/comparison.xlsx'  # Excel 파일 경로

# JSON 파일 로드 함수
def load_json_from_file(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)
        if isinstance(data, list):
            return data
        else:
            return [data]  # 단일 객체일 경우 리스트로 변환

# Excel 파일 로드 함수
def load_excel(file_path):
    return pd.read_excel(file_path)

# 시간 문자열을 datetime 객체로 변환하는 함수
def parse_time(time_str):
    if isinstance(time_str, time):
        return time_str
    return datetime.strptime(time_str, '%H:%M:%S').time()

# 날짜 문자열을 datetime 객체로 변환하는 함수
def parse_date(date_str):
    return datetime.strptime(date_str, '%Y:%m:%d')

# 메인 함수
def process_metadata():
    # JSON 데이터 로드
    json_data = load_json_from_file(METADATA_FILE_PATH)

    # Excel 데이터 로드
    comparison_data = load_excel(COMPARISON_FILE_PATH)

    results = []

    for data in json_data:
        metadata_lat = round(data['GpsLatitude'], 4)
        metadata_lon = round(data['GpsLongitude'], 4)
        date = parse_date(data['Date'])
        time = parse_time(data['Time'])
        weekday = date.strftime('%A')

        print(f"Checking metadata: Lat {metadata_lat}, Lon {metadata_lon}, Date {date}, Time {time}")

        for index, row in comparison_data.iterrows():
            comparison_lat = round(float(row['Latitude']), 4)
            comparison_lon = round(float(row['Longitude']), 4)

            print(f"  Comparing with: Lat {comparison_lat}, Lon {comparison_lon}")

            if metadata_lat == comparison_lat and metadata_lon == comparison_lon:
                print("    Match found!")
                # 요일에 따른 단속 시간 가져오기
                if weekday in ['Saturday', 'Sunday']:
                    start_time = parse_time(row[f'{weekday[:3]}StartTime'])
                    end_time = parse_time(row[f'{weekday[:3]}EndTime'])
                else:
                    start_time = parse_time(row['WeekdayStartTime'])
                    end_time = parse_time(row['WeekdayEndTime'])

                print(f"    Checking time: {time} between {start_time} and {end_time}")

                # 시간 비교하여 불법주정차 여부 확인
                if start_time <= time <= end_time:
                    results.append({
                        '날짜': data['Date'],
                        '시각': data['Time'],
                        '위치': (metadata_lat, metadata_lon),
                        '불법주정차 여부': True
                    })
                else:
                    results.append({
                        '날짜': data['Date'],
                        '시각': data['Time'],
                        '위치': (metadata_lat, metadata_lon),
                        '불법주정차 여부': False
                    })
                break

    # 결과 출력
    print(results)

# 함수 실행
process_metadata()
