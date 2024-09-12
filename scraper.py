from bs4 import BeautifulSoup as BS
import requests
import pandas
from io import StringIO
import time

def get_team_data(league_uri, league_id, season, file, number_of_teams=10):
    base_url = "https://fbref.com"
    data = requests.get(f"{base_url}/en/comps/{str(league_id)}/{str(season)}/{str(season)}-{str(league_uri)}")
    time.sleep(4)
    soup = BS(data.content, 'html.parser')
    table = soup.find("table", id=f'results{str(season)}{league_id}1_overall')

    left_side = table.find_all('td', class_='left')

    links = []
    for td in left_side:
        links.extend(td.find_all('a'))

    club_names = list([l.get_text() for l in links])

    uris = list([l.get('href') for l in links])
    squad_uris = [uri.replace(f'{str(season)}/', '') for uri in uris]

    squad_urls = [base_url+uri for uri in squad_uris]


    data_dict = [
        {"team_name": club_names[i], "squad_link": squad_urls[i]}
        for i in range(number_of_teams)
    ]
    squad = []

    for team in data_dict:
        response = requests.get(team['squad_link'])
        time.sleep(4)
        new_soup = BS(response.content, 'html.parser')

        big_logo = new_soup.find('img', class_='teamlogo').get('src')

        squad_data = new_soup.find('table', id='stats_standard_9').find('tbody').find_all('tr')


        for player in squad_data:
            name = player.find('th').get_text()
            player_page = player.find('th').find('a').get('href')
            position = player.find('td', {'data-stat': 'position'}).get_text()
            country = player.find('td', {'data-stat': 'nationality'}).get_text()
            age = player.find('td', {'data-stat': 'age'}).get_text()

            temp_response = requests.get(f'{base_url}{player_page}')
            time.sleep(4)
            temp_soup = BS(temp_response.content, 'html.parser')
            media_item = temp_soup.find('div', class_='media-item')
            if media_item:
                picture = media_item.find('img').get('src')
            else:
                picture = 'https://img.freepik.com/free-vector/blue-circle-with-white-user_78370-4707.jpg?t=st=1726169296~exp=1726172896~hmac=c369fdbb9efe89fcdb13b0bd15bc6b62b3db3fad7e4b8a52064909e6b818e930&w=826'

            
            player_data = {
                    'team_name' : team['team_name'],
                    'team_logo' : big_logo,
                    'name': name,
                    'position': position.split(',')[0],
                    'picture': picture,
                    'country': country,
                    'age': age.split('-')[0]
                }
            squad.append(player_data)

    team_data = pandas.DataFrame(squad)
    team_data.to_csv(f"data/{str(file)}", index=False)

    print('Script executed successfully!\nView .csv file to see the data')
    return


"""
Pass the following arguements to the function call below:
1. URI containing league name for the league to be scraped
2. League ID gotten from the link's URL
3. Last season's year bracket
4. .csv file name for the scraped data to be saved to. Note that the file would be created in the data/ directory of the project
5. Number of teams to be included in the scraping.

See README file for more details
"""

get_team_data("Premier-League-Stats", "9", "2023-2024", "premier_league_test.csv")
