import requests
from bs4 import BeautifulSoup
import json
import data


# * Get search keyword 
keyword = data.name

esg = None

try:
    # * Get company and IID variable from MSCI
    url_json = f"https://www.msci.com/our-solutions/esg-investing/esg-ratings/esg-ratings-corporate-search-tool?p_p_id=esgratingsprofile&p_p_lifecycle=2&p_p_state=normal&p_p_mode=view&p_p_resource_id=searchEsgRatingsProfiles&p_p_cacheability=cacheLevelPage&_esgratingsprofile_keywords={keyword}"
        
    response_json = requests.get(url_json)

    keys = json.loads(response_json.text)[0]

    company = keys['encodedTitle']
    iid = keys['url']


    # * Get html from MSCI rating for specific company
    url = f"https://www.msci.com/our-solutions/esg-investing/esg-ratings/esg-ratings-corporate-search-tool?p_p_id=esgratingsprofile&p_p_lifecycle=2&p_p_state=normal&p_p_mode=view&p_p_resource_id=showEsgRatingsProfile&p_p_cacheability=cacheLevelPage&_esgratingsprofile_issuerId={iid}"
        
    payload = {}
        
    headers = {
        'Accept': '*/*',
        'Accept-Language': 'en-us',
        'Host': 'www.msci.com',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Safari/605.1.15',
        'Referer': f'https://www.msci.com/our-solutions/esg-investing/esg-ratings/esg-ratings-corporate-search-tool/issuer/{company}/{iid}',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'X-Requested-With': 'XMLHttpRequest'
        }

    response = requests.request("GET", url, headers=headers, data=payload)


    # * Extracting the rating
    soup = BeautifulSoup(response.content, "html.parser")

    esg_raw = soup.find("div", {"class": "ratingdata-company-rating"})['class']
        
    if "esg-rating-circle-aaa" in esg_raw:
        esg = 'AAA'
    elif "esg-rating-circle-aa" in esg_raw:
        esg = 'AA'
    elif "esg-rating-circle-a" in esg_raw:
        esg = 'A'
    elif "esg-rating-circle-bbb" in esg_raw:
        esg = 'BBB'
    elif "esg-rating-circle-bb" in esg_raw:
        esg = 'BB'
    elif "esg-rating-circle-b" in esg_raw:
        esg = 'B'
    elif "esg-rating-circle-ccc" in esg_raw:
        esg = 'CCC'
    else:
        esg = 'no rating'  
        
except:
    esg = "no rating" 

