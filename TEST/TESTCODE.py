
from imports import *
from generalhandler import Handler
from Models import *


class ScrapeFriends(Handler):
    def get(self):
        #Check if we want to scrape this person right now
        logging.info("Passed")
        token = self.request.get("token")
        id = self.request.get("id")
        id_search = db.GqlQuery("SELECT * FROM Users WHERE id= :str", str=id)
        last_scraped = datetime.datetime(2013,1,1)
        old_entry = False
        person = False
        #Even though this is a for loop, there should really be just one person
        try:
            person = id_search.fetch(1)
            last_scraped = person.friends_scraped
        except:
            pass
        now = datetime.datetime.now()
        timedelta = now - last_scraped
        print("This is a test to see what happens with newlines \n")

        #TODO test#1

        #TODO determine if we really want to scrape the person
        if timedelta.total_seconds() > 0:
            request_string = 'https://graph.facebook.com/' + id + '/friends?access_token=' + token
            request = url.urlopen(request_string)
            request = request.read()
            json_obj = json.loads(request)
            hashlist = {}
            while len(json_obj['data']) > 0:
                friendlist = json_obj['data']
                for friend in friendlist:
                    hashlist[friend['name']]=friend['id']
                next_pg = json_obj["paging"]["next"]
                new_request = url.urlopen(next_pg)
                new_request = new_request.read()
                json_obj = json.loads(new_request)

            logging.info(hashlist)

            #Assemble the total database
            database = db.GqlQuery("SELECT * From SearchBase order by quantity asc")
            database = database.fetch(None)
            database_dict={}
            to_append = {}
            lowest_dict = {}
            lowest_length = 100000000
