def create_urls():
    rooms = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    prices = list(x for x in range(0, 115_000_000, 1_000_000))
    urls = []
    for r in rooms:
        for p in range(len(prices)-1):
                for i in [1, 2]:
                    urls.append(
                        f"https://www.cian.ru/cat.php?currency=2&deal_type=sale&engine_version=2&maxprice={prices[p+1]}"
                        f"&minprice={prices[p]}&object_type%5B0%5D={i}&offer_type=flat&region=1&room{r}=1")
    return urls
