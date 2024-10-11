from bs4 import BeautifulSoup as BS
import requests
import pandas
from io import StringIO
import time
# from pprint import pprint

def get_team_data(league_uri, league_id, season, team_file, squad_file, number_of_teams=20):
    base_url = "https://fbref.com"
    data = requests.get(f"{base_url}/en/comps/{str(league_id)}/{str(league_uri)}")
    print('Getting started.....')
    time.sleep(4)
    soup = BS(data.content, 'html.parser')
    table = soup.find("table", id=f'results{str(season)}{league_id}1_overall')

    rows = table.find('tbody').find_all('tr')
    left_side = []
    for row in rows:
        left_side.append(row.find('td', class_='left'))
    links = []
    for td in left_side:
        links.extend(td.find_all('a'))

    club_names = list([l.get_text() for l in links])

    uris = list([l.get('href') for l in links])
    squad_uris = [uri.replace(f'{str(season)}/', '') for uri in uris]

    squad_urls = [base_url+uri for uri in squad_uris]

    last_match = []
    next_match = []
    for link in squad_urls:
        team_page = requests.get(link)
        print(link)
        time.sleep(4)
        team_soup = BS(team_page.content, 'html.parser')

        summary_div = team_soup.find('div', id='meta').find('div', {'data-template': 'Partials/Teams/Summary'})
        paragraphs = summary_div.find_all('p')
        last_fixture = ' '.join(paragraphs[4].find('a').get_text().split(' ')[1:]).strip()
        last_match.append(last_fixture)
        next_fixture = ' '.join(paragraphs[5].find('a').get_text().split(' ')[1:]).strip()
        next_match.append(next_fixture)
    data_dict = [
        {"team_name": club_names[i], "squad_link": squad_urls[i], "last_match" : last_match[i], "next_match" : next_match[i]}
        for i in range(number_of_teams)
    ]

    team_data = pandas.DataFrame(data_dict)
    team_data.to_csv(f"data/{str(team_file)}", index=False)
    print('Scraped and saved team data. Commencing squad data scraping.......')
    squad = []
    count = 0
    for team in data_dict:
        response = requests.get(team['squad_link'])
        time.sleep(4)
        new_soup = BS(response.content, 'html.parser')

        big_logo = new_soup.find('img', class_='teamlogo').get('src')

        squad_data = new_soup.find('table', id=f'stats_standard_{league_id}').find('tbody').find_all('tr')


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
        count += 1
        if count == 1:
            print(f'{count} team down {number_of_teams - count} teams to go')
        elif number_of_teams - count == 1:
            print(f'{count} teams down {number_of_teams - count} team to go')
        else:
            print(f'{count} teams down {number_of_teams - count} teams to go')
        
        if count%5 == 0:
            print('Taking a break😴😴, be back in a minute....literally......')
            time.sleep(60)
            print('Well that was refreshing😊😊, resuming scraping......')
    print('Scraped squad data successfully. Parsing and saving data.....')
    full_squad_data = pandas.DataFrame(squad)
    full_squad_data.to_csv(f"data/{str(squad_file)}", index=False)

    print('Script executed successfully!\nView .csv file to see the data')
    return


"""
Pass the following arguements to the function call below:
1. URI containing league name for the league to be scraped
2. League ID gotten from the link's URL
3. Last season's year bracket
4. .csv file name for the scraped team data to be saved to. Note that the file would be created in the data/ directory of the project
5. .csv file name for the scraped squad data to be saved to. Note that the file would be created in the data/ directory of the project
6. Number of teams to be included in the scraping.

See README file for more details
"""
get_team_data("Bundesliga-Stats", "20", "2024-2025","bundesliga_teams.csv", "bundesliga_squads.csv", 18)



# def get_match_data(team_uri, match_data_file):
#     print('Running script....')
#     base_url = 'https://fbref.com'
#     r = requests.get(f'{base_url}{team_uri}')
#     time.sleep(4)
#     match_details = BS(r.content, 'html.parser')

#     next_match = match_details.find('div', {'data-template' : 'Partials/Teams/Summary'}).find_all('p')[5].get_text().split('vs')[1]
#     last_match = match_details.find('div', {'data-template' : 'Partials/Teams/Summary'}).find_all('p')[4].get_text().split('at')[2]
#     last_match_link = match_details.find('div', {'data-template' : 'Partials/Teams/Summary'}).find_all('p')[4].find('a').get('href')

#     match_data = {
#         'last_match' : last_match,
#         'last_match_link' : base_url+last_match_link,
#         'next_match' : next_match
#     }

#     full_squad_data = pandas.DataFrame([match_data])
#     full_squad_data.to_csv(f"data/{str(match_data_file)}", index=False)
#     print('Done!')
#     return


# """
# Pass the following arguements to the function below:
# team_uri = Unique uri for each team
# match_data_file = .csv file name for storing team match data scraped
# """
# get_match_data('/en/squads/b8fd03ef/Manchester-City-Stats', 'match_data.csv')