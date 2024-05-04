import pandas as pd
import bs4 as bs
import urllib.request 
from functools import wraps
import os
from typing import List

# definitions of pages and races with sprints
pages = ["race-result", "fastest-laps", "pit-stop-summary", "starting-grid", "qualifying", "sprint-results", "sprint-grid", "sprint-qualifying", "practice-3", "practice-2", "practice-1"]
pages_normal = ["race-result", "fastest-laps", "pit-stop-summary", "starting-grid", "qualifying", "practice-3", "practice-2", "practice-1"]
pages_sprint22 = ["race-result", "fastest-laps", "pit-stop-summary", "starting-grid", "qualifying", "sprint-results", "sprint-grid", "practice-2", "practice-1"]
pages_sprint = ["race-result", "fastest-laps", "pit-stop-summary", "starting-grid", "qualifying", "sprint-results", "sprint-grid", "sprint-qualifying", "practice-1"]

sprints_2022 = ["2022/races/1109/italy", "2022/races/1115/austria", "2022/races/1137/brazil"]
sprints_2023 = ["2023/races/1207/azerbaijan", "2023/races/1213/austria", "2023/races/1216/belgium", "2023/races/1221/qatar", "2023/races/1222/united-states", "2023/races/1224/brazil"]
sprints_2024 = ["2024/races/1233/china"]

sprints = ["2022/races/1109/italy", "2022/races/1115/austria", "2022/races/1137/brazil", "2023/races/1207/azerbaijan", "2023/races/1213/austria", "2023/races/1216/belgium", "2023/races/1221/qatar", "2023/races/1222/united-states", "2023/races/1224/brazil", "2024/races/1233/china"]

years = [2022, 2023, 2024]

url_dict = {}

# adjust urls 
for year in years:
    for page in pages:
        page_name = page.replace("-", "_")
        list_name = f"urls_{year}_{page_name}"
        url_dict[list_name] = []

# read races urls from txt file
urls = []
with open('urls/races_url.txt', 'r') as file:
    for line in file:
        line = line.strip()
        urls.append(line)

# replace page in urls
def replace_page_in_urls(urls: List[str]) -> List[str]:
    sprints = ["2022/races/1109/italy", "2022/races/1115/austria", "2022/races/1137/brazil", "2023/races/1207/azerbaijan", "2023/races/1213/austria", "2023/races/1216/belgium", "2023/races/1221/qatar", "2023/races/1222/united-states", "2023/races/1224/brazil", "2024/races/1233/china"]
    pages_normal = ["race-result", "fastest-laps", "pit-stop-summary", "starting-grid", "qualifying", "practice-3", "practice-2", "practice-1"]
    pages_sprint22 = ["race-result", "fastest-laps", "pit-stop-summary", "starting-grid", "qualifying", "sprint-results", "sprint-grid", "practice-2", "practice-1"]
    pages_sprint = ["race-result", "fastest-laps", "pit-stop-summary", "starting-grid", "qualifying", "sprint-results", "sprint-grid", "sprint-qualifying", "practice-1"]
    pages = ["race-result", "fastest-laps", "pit-stop-summary", "starting-grid", "qualifying", "sprint-results", "sprint-grid", "sprint-qualifying", "practice-3", "practice-2", "practice-1"]
    updated_urls = []

    for url in urls:
        for sprint_race in sprints:
            sprint_year = sprint_race.split("/")[0]
            if sprint_race in url:
                if int(sprint_year) == 2022:
                    for page in pages_sprint22:
                        updated_url = url.replace("race-result", page)
                        updated_urls.append(updated_url)
                else:
                    for page in pages_sprint:
                        updated_url = url.replace("race-result", page)
                        updated_urls.append(updated_url)
                    break

        else:
            for page in pages_normal:
                updated_url = url.replace("race-result", page)
                updated_urls.append(updated_url)

    return updated_urls

# write updated urls to the txt file
updated_urls = replace_page_in_urls(urls)
updated_urls_txt = "urls/updated_urls.txt"
with open(updated_urls_txt, "w") as file:
    for url in updated_urls:
        file.write(url + "\n")

# append updated url to dictionary which contains lists with appropriate results
for url in updated_urls:
    for year in years:
        for page in pages:
            if f"{year}" in url and f"{page}" in url:
                page_name = page.replace("-", "_")
                list_name = f"urls_{year}_{page_name}"
                url_dict[list_name].append(url)

# write final urls to the file
final_urls = "urls/final_urls.txt"
with open(final_urls, "w") as file:
    for url_list in url_dict.values():
        for url in url_list:
            file.write(url + "\n")

for list_name, url_list in url_dict.items():
    #print(f"{list_name}: {url_list}")
    #print(list_name)
    pass


# download the data from F1 web page and save them to proper directories
def download_data() -> None:
    for list_name, url_list in url_dict.items():
        for url in url_list:
            for year in years:
                for page in pages:
                    if f'{year}' in url and page in url:
                        source=urllib.request.urlopen(url).read()
                        soup=bs.BeautifulSoup(source,'lxml')
                        data_table=soup.find_all('table')[0]
                        data=pd.read_html(str(data_table),flavor='bs4',header=[0])[0]
                        data = data.loc[:, ~data.columns.str.contains('^Unnamed')]
                    
                        page = page.replace("-", "_")
                        directory = f"data/{year}/{page}"
                        os.makedirs(directory, exist_ok=True)
                        race = int(url.split("races/")[1].split("/")[0])
                        country = url.split("races/")[1].split("/")[1]
                        country = country.replace("-", " ")
                        country = country.title()
                        if country == "Italy" and (race == 1109 or race == 1209):
                            country = "Imola"
                        data.to_csv(f"{directory}/{country}.csv", index=False)


def add_mising_column_to_data(files: List[str]) -> None:
    for file in files:
        df = pd.read_csv(file)
        df['Time'] = ','
        df.to_csv(file, index=False)

    
# delete 3 unnecessary files which were downloaded, because f1 web page has problems with urls
def delete_incorrect_data(files: List[str]) -> None:
    for file in files:
        if os.path.exists(file):
            os.remove(file)
            print(f"The file {file} has been deleted.")
        else:
            print(f"The file {file} does not exist.")


paths_files_to_add_missing_column = ['data/2022/starting_grid/Imola.csv', 'data/2022/starting_grid/Austria.csv', 'data/2022/starting_grid/Brazil.csv']
paths_to_delete = ['data/2022/practice_3/Imola.csv', 'data/2022/practice_3/Austria.csv', 'data/2022/practice_3/Brazil.csv']


def preprocess_data() -> None:
    try:
        download_data()
        add_mising_column_to_data(paths_files_to_add_missing_column)
        delete_incorrect_data(paths_to_delete)
        print("Data was processed successfully")

    except Exception as e:
        print(f"An error occurred while processing data! {e}")

if __name__=="__main__":
    preprocess_data()