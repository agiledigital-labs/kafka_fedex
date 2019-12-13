import os
import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from confluent_kafka import Producer

def downloadFiles(soup):
    data_source = []
    for link in soup.select("a[href$='.pdf']"):
        try:
            file_url = urljoin(url,link['href'])
            response = requests.get(file_url)
            if response.status_code == 200:
                data_source.append(file_url)
                print("writing: "+str(file_url))
            else:
                print("An error occured with the following status code: "+str(response.status_code))
        except Exception as e:
            print(e)
    return data_source

def delivery_report(err, msg):
    print("in delivery report")
    """ Called once for each message produced to indicate delivery result.
        Triggered by poll() or flush(). """
    if err is not None:
        print('Message delivery failed: {}'.format(err))
    else:
        print('Message delivered to {} [{}]'.format(msg.topic(), msg.partition()))

def collect_data(url):
    data_source = []
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup= BeautifulSoup(response.text, "html.parser")
            data_source = downloadFiles(soup)
        else:
            print("An error occured with the following status code: "+str(response.status_code))
    except Exception as e:
        print(e)

    return data_source

def send_kafka(data_source):
    p = Producer({'bootstrap.servers': 'localhost:9092'})
    for data in data_source:
        print("doing stuff with source")
        # Trigger any available delivery report callbacks from previous produce() calls
        p.poll(0)

        # Asynchronously produce a message, the delivery report callback
        # will be triggered from poll() above, or flush() below, when the message has
        # been successfully delivered or failed permanently.
        p.produce('fedex', data, callback=delivery_report)
    p.flush()

url = "https://www.afp.gov.au/about-us/information-publication-scheme/routinely-requested-information-and-disclosure-log"
data_source = collect_data(url)
send_kafka(data_source)
