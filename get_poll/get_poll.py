import requests
import reddit_oauth as auth
from datetime import date
import csv

headers = auth.get_headers()

if headers == None:
    raise RuntimeError("Could not obtain headers to access Reddit. Check your login info.")

res = requests.get("https://oauth.reddit.com/r/ThePiratesDen/new", headers=headers)

# look at a list of post titles
for post in res.json()['data']['children']:
    
    post_title = post['data']['title']
    
    # the titles seem to be listed by new
    # look for posts that start with "The Den Votes"
    if post_title.startswith('The Den Votes'):
        
        # data we are trying to retrieve
        # post_date_str
        vote_counts = [] # [up, flat, down, kanga]
        # Because vote option text is subject to change,
        # I'm assuming it will always be in that order.
        # If that does change, the analysis code will need to be updated accordingly
        
        # record the date of the post
        
        # start by pulling it from the title in the form MM/DD
        post_date_str = post_title[14:].split(' ')[0]
        
        # format the date in the iso format YYYY-MM-DD
        date_iso_str = str(date.today().year) + "-" + post_date_str.replace('/', '-')
        print(post_title, " (", date_iso_str, ")")
        
        try:
        
            # get the vote data
            for choice in post['data']['poll_data']['options']:
            
                # get the vote counts
                vote_counts.append(choice['vote_count'])
                print(choice, "(", choice['vote_count'], ")")
        
            # because we only want the newest one
            break
            
        except KeyError:
            print("ERROR: Could not get vote counts")

# export to a file in the data folder
# again assuming choices are [up, flat, down, kanga] in that order
filename = '../data/' + date_iso_str + '.csv'
with open(filename, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile, delimiter=' ', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    writer.writerow(vote_counts)