from bs4 import BeautifulSoup as BS
import requests
import pandas
from io import StringIO

def get_team_data(league_uri, league_id, season, file, number_of_teams=10):
    base_url = "https://fbref.com"
    data = requests.get(f"{base_url}/en/comps/{str(league_id)}/{str(season)}/{str(season)}-{str(league_uri)}")

    soup = BS(data.content, 'html.parser')
    table = soup.find("table", id=f'results{str(season)}{league_id}1_overall')

    left_side = table.find_all('td', class_='left')

    links = []
    for td in left_side:
        links.extend(td.find_all(['img', 'a']))


    images = list(filter(None, [l.get("src") for l in links]))
    club_names = list(filter(lambda x: x != '', [l.get_text() for l in links]))

    uris = list(filter(None, [l.get('href') for l in links]))
    squad_uris = [uri.replace(f'{str(season)}/', '') for uri in uris]

    squad_urls = [base_url+uri for uri in squad_uris]

    # Using range 10 because I only want the top 10
    data_dict = [
        {"team_name": club_names[i], "logo": images[i], "squad_link": squad_urls[i]}
        for i in range(number_of_teams)
    ]

    team_data = pandas.DataFrame(data_dict)

    team_data.to_csv(str(file), index=False)

    return


get_team_data("Premier-League-Stats", "9", "2023-2024", "teams.csv")