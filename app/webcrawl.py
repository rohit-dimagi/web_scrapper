from bs4 import BeautifulSoup
import multiprocessing as mp
import requests, math,re
import config


# CRAWL PAGES FOR GET INFOR FOR THE APARTMENT
def crawl_webspace(domain_url,city_name,page_num,bedroom=None,bathroom=None):
        props =[]

        page_scrape_url = domain_url + "/"+ city_name +"?page="+str(page_num)
        resp = requests.get(page_scrape_url)
       
        soup = BeautifulSoup(resp.content, 'html.parser')
        containers = soup.findAll('div', attrs={'class': 'search-grid'})

        for container in containers:
                #GET URL FOR EACH APARTMENT
                apartment_url = container.div.a['href']
                resp = requests.get(domain_url+ apartment_url)
                
                soup_apartment = BeautifulSoup(resp.content, 'html.parser')
                details = soup_apartment.find('div', attrs={'class': 'property-headline-details-container'})
                
                #GET PROPERTY NAME
                property_name = details.h1.text
                
                #GET LOCATION DETAILS
                locality =[]
                extra_details = details.find('span', attrs={'itemprop': 'addressLocality'})
                if extra_details:
                    local_json = {}
                    local_json["locality"] = extra_details.text

                extra_details = details.find('span', attrs={'itemprop': 'addressRegion'})
                if extra_details:
                   local_json["region"] = extra_details.text

                extra_details = details.find('span', attrs={'itemprop': 'streetAddress'})
                if extra_details:
                    local_json["street"] = extra_details.text
                
                locality.append(local_json)

                #GET BATHROOM,BEDROOM,SIZE DETAILS
                extra_details = details.find('div', attrs={'class': 'listing-summary-bedrooms'})
                bed_room = (extra_details.div.text).strip()
                
                extra_details = details.find('div', attrs={'class': 'listing-summary-bathrooms'})
                bath_room = (extra_details.div.text).strip()
                
                extra_details = details.find('div', attrs={'class': 'listing-summary-unit-size'})
                unit_size = (extra_details.div.text).strip()
                
                #GET AMENITIES DETAILS
                amenties = soup_apartment.findAll('span', attrs={'class': 'amenity-name'})
                list_amenties =[]
                for item in amenties:
                    list_amenties.append(item.text)
                
                #GET LAT/LONG DETAILS
                location = soup_apartment.find('div', attrs={'id': 'walkscore-map-pane'})
                result = re.search('7C(.*)', location['data-src'])
                if result:
                    map= result.group(1).split(',')
                    latitude = map[0]
                    longitude = map[1]
                else:
                    latitude = None
                    longitude = None
                #GET PROPERTY DETAILS
                property_details = soup_apartment.find('div', attrs={'class': 'shortentext'})
                
                #BUILD A JSON OBJECT
                json ={}
                json["property_name"]= property_name.strip()
                json["latitude"] = latitude
                json["longitude"] = longitude
                json["ameneties"] = list_amenties
                json["address"] = locality
                json["property_size"] = unit_size
                json["property_details"] = property_details.text.strip()
                
                # CHECK IN CASE OF SPECIFIC BATHROOM,BEDROOM SEARCH
                if bathroom and bedroom:
                    try:
                        json["bathroom"] = int(bath_room)
                        json["bedroom"] = int(bed_room)
                        if json["bathroom"] == bathroom and json["bedroom"] == bedroom:
                            props.append(json)
                    except ValueError:
                        pass
                else:
                    json["bathroom"] = bath_room
                    json["bedroom"] = bed_room
                    props.append(json)
                print("checking details for property ==> {}".format(json["property_name"]))
        return props


# READ CONFIG FILE AND START PARALLEL PROCESSES
def calculate_response(city_name, **kwargs):
    app_config = config.read_config()
    query_limit = app_config["result_limit"]
    domain_url = app_config["web_scrape_url"]
    per_page_result = get_page_result_count(domain_url,city_name,page_num=1)
    page_to_crawl = math.ceil(query_limit / per_page_result)

    result = start_parallel_process(domain_url, city_name, page_to_crawl, **kwargs)
    if result:
        return result
    else:
        return None

# START PARALLEL PROCESS
def start_parallel_process(domain_url, city_name, page_to_crawl, **kwargs):
    if kwargs:
        bathroom = kwargs['bathroom']
        bedroom = kwargs['bedroom']
    else:
        bathroom=None
        bedroom=None

    pool = mp.Pool(processes=10)
    results = [pool.apply_async(crawl_webspace, args=(domain_url,city_name,page_num,bathroom,bedroom)) for page_num in range(1,page_to_crawl+1)]
    output = [p.get() for p in results]

    print("Parallel processing finished....")
    return output   
 
# CALCULATE NO OF APARTMENT RESULT IN ONE PAGE
def get_page_result_count(domain_url,city_name,page_num):
    resp = requests.get(domain_url+"/"+city_name+"?page="+str(page_num))

    if resp.status_code == 200:
        soup = BeautifulSoup(resp.content, 'html.parser')
        containers = soup.findAll('div', attrs={'class': 'search-grid'})
        return len(containers)
    else:
        return None