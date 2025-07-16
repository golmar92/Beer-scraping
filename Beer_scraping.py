import requests
from bs4 import BeautifulSoup

cities = ['wroclaw', 'katowice', 'gdansk', 'warszawa', 'gdynia']

def type_city():
    city = input("Type a city: ").lower()
    if city in cities:
        return city
    else:
        return "Wrong city."

def pubs_from_city(city):
    url = f"https://ontap.pl/{city}/multitapy"
    resp = requests.get(url)
    resp.raise_for_status()

    bs = BeautifulSoup(resp.text, "html.parser")

    pubs = []
    for pub_data in bs.select("div.col-lg-3.col-md-4.col-xs-12.col-sm-6")[1:]:
        pub_body = pub_data.select_one(".panel-body")
        link_tag = pub_body.find("a", href=True)
        pub_url = link_tag["href"] if link_tag else None

        pub_name = next(pub_body.stripped_strings)
        pubs.append({"name": pub_name, "url": pub_url})
    return pubs

selected_city = type_city()
selected_city_pubs = pubs_from_city(selected_city)

for pub in selected_city_pubs:
    resp_pub = requests.get(pub["url"])
    resp_pub.raise_for_status()
    soup = BeautifulSoup(resp_pub.text, "html.parser")

    pub['beers'] = []

    for beer_div in soup.select("div.col-xl-4.col-lg-4.col-md-4.col-sm-6"):
        panel_body = beer_div.select_one(".panel-body")
        beer_data = panel_body.get_text(separator="#", strip=True).split('#')
        for data in beer_data:
            if data == 'WHALE' or data == 'New':
                beer_data.remove(data)
        beer_data.remove('on tap for')
        panel_footer = beer_div.select_one(".panel-footer")
        beer_price = panel_footer.get_text(separator=" ", strip=True)
        beer = {'tap': beer_data[0], 'brewery': beer_data[1], 'name': beer_data[2], 'details': beer_data[3],
                'time': beer_data[4], 'style': beer_data[5], 'beer_price': beer_price}
        pub['beers'].append(beer)


