

def get_address(meta: dict, soup):
    address = soup.find_all('span', {'itemprop': 'name'})
    #print(address)
    for a in address:
        if a and a.get('content'):
            return a['content']
    return None
