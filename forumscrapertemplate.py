import requests
import json
import pprint
import pickle
from bs4 import BeautifulSoup

def cleans_dictionary(raw_dictionary):
    #get all the slugs and topic_id's out of this dictionary (make sure the parameters are string)
    #and make a new dictionary with the 30 topics just the id's and slugs
    #new_submissions = [{'topic_id': 23124,'slug':'debit-cards'},{'topic_id': 846283,'slug':'credit-card'}]
    topics = raw_dictionary['topic_list']['topics']
    list_of_topics = []
    for i in topics:
        list_of_topics.append([i['id'],i['slug']])
    return list_of_topics

i = 0
new_submissions = []
crawler_condition = True
while crawler_condition == True:
    print(i)
    #Change the url below to reflect the discourse forum you're scraping
    url = "https://onehack.us/latest.json?no_definitions=true&page="+str(i)
    r = (requests.get(url)).text
    raw_dictionary = json.loads(r)
    if len(raw_dictionary['topic_list']['topics']) <= 0:
        crawler_condition = False
        break
    else:
        clean_dictionary = cleans_dictionary(raw_dictionary)
        new_submissions.extend(clean_dictionary)
        i += 1

with open("topic_names_1hack.pickle", "wb") as output_file:
     pickle.dump(new_submissions, output_file)

# this can also be done with scrapy where I only scrape a certain xpath. 
# To do that use: xpath = '/html/body/div/div[2]'

def get_forum_message(message):
    soup = BeautifulSoup(message,features="lxml")
    div = soup.find("div", {"itemprop": "articleBody"})
    ht = div.findAll('p')
    submission_text = ''
    for i in ht:
        submission_text += i.get_text() 
    return submission_text.strip()

with open("topic_names_1hack.pickle", "rb") as input_file:
    new_submissions = pickle.load(input_file)

dic = []
breaker = len(new_submissions)
for i in range(3):
    print((i/breaker)*100)
    submission = new_submissions[i]
    #Change the url below to reflect the forum you're scraping
    topic_url = ("https://onehack.us/t/" + submission[1] + '/' + str(submission[0]))
    response = requests.get(topic_url)
    message = response.text
    dic.append([topic_url,get_forum_message(message)])

with open("/content/text_submissions_1hack.pickle", "wb") as output_file:
    pickle.dump(dic, output_file)
