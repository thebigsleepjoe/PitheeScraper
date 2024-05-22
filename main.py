
from requests import post
import sys # for parsing args
import time # for sleeping
import database as db

if not __name__ == "__main__":
    print("This script is not meant to be imported.")
    sys.exit(1)

if len(sys.argv) < 4:
    print("Error: missing args. Please include all necessary arguments.")
    print("E.g., python main.py <token> <num_winners> <num_posts>")
    sys.exit(1)

NUM_WINNERS = int(sys.argv[2])
NUM_POSTS = int(sys.argv[3])

# assert NUM_WINNERS > 0, "Number of winners must be greater than 0."
# assert NUM_POSTS > 0, "Number of posts must be greater than 0."

# Dislcaimer for end users
print("----------------------------------")
print("I am not responsible for the possible (though unlikely) invalidation/banning of your API key. Use responsibly and at your own risk.")
print("By continuing, you agree to these facts.")
print("Also, please note that your provided bearer token may be invalidated during execution due to naturally expiring. (typically lasts <=1hr)")
print(f"We will try to fetch {NUM_WINNERS} winners and {NUM_POSTS} posts. The winners will take a very long time to fetch, but it does not require your personal token.")
print("----------------------------------")

print("You have 10 seconds to cancel with CTRL+C or closing the terminal if you do not agree.")
time.sleep(10)

# I believe this is static. If it starts having auth issues then I will work on a proper API key resolver,
# as the (anonymous) api key is immediately shared with anyone connecting to the main page w/o sign in.
apiKey = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im9xdXRqYXh4eHp6Ymp0eXJmb2thIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MDg4ODU3OTIsImV4cCI6MjAyNDQ2MTc5Mn0.FOLioyIMlswKlxTDjyTylkIpm1MRYMGm1lvLakH-oyE"

# For getting winner archive:
# curl --request POST \
#  --url https://oqutjaxxxzzbjtyrfoka.supabase.co/rest/v1/rpc/get_win_archive \
#  --header 'apikey: <public key>' \
#  --data '{}'

print("Creating ./data directory if it does not exist.")
db.createDataDir()


USER_BEARER = "Bearer " + sys.argv[1]

def fetchWinnerArchive():
    """
    Fetch the winner archive in the form of a JSON object.
    This does not require prior authentication.
    """
    url = "https://oqutjaxxxzzbjtyrfoka.supabase.co/rest/v1/rpc/get_win_archive"
    headers = {
        "apikey": apiKey
    }
    response = post(url, headers=headers, json={})

    # Typically this is a list of dictionaries as such:
    # {
    #     won_at: string
    #     player_name: string
    #     post_text: string
    # }

    dictList = response.json()
    result = [] # list of post_texts

    for d in dictList:
        result.append(d["post_text"])
    
    return result




# For getting all posts:
# curl --request POST \
#   --url https://oqutjaxxxzzbjtyrfoka.supabase.co/rest/v1/rpc/get_posts \
#   --header 'apikey: <api key>' \
#   --header 'authorization: <bearer token>' \
#   --data '{"post_quantity":20}'

def fetchAllPosts():
    """
    Fetch all posts from the Supabase database.
    This requires authentication.
    """
    url = "https://oqutjaxxxzzbjtyrfoka.supabase.co/rest/v1/rpc/get_posts"
    headers = {
        "apikey": apiKey,
        "authorization": USER_BEARER
    }
    response = post(url, headers=headers, json={"post_quantity": 20})

    # Typically this is a list of dictionaries as such:
    # {
    #     post_id
    #     post_text
    # }

    dictList = response.json()
    result = [] # list of post_texts

    for d in dictList:
        result.append(d["post_text"])

    return result

print("Now fetching posts. This may take a few minutes.")
while True:
    num_posts = db.countRecordedPosts()

    if num_posts >= NUM_POSTS:
        print("Done fetching posts!")
        break

    # Fetch all posts
    all_posts = fetchAllPosts()
    
    # Add the posts to the all.yaml file
    db.addToAllPosts(all_posts)

    # sleep for a bit to not overload the server
    time.sleep(3)

    print(f"We have recorded {db.countRecordedPosts()} posts total, of the desired {NUM_POSTS}.")

print("")
print("Now moving on to fetching winners. This will take a LONG time depending on the desired number (potentially hours).")
while True:
    # Count the number of recorded winners and posts
    totalWinnersCount = db.countRecordedWinners()

    if totalWinnersCount >= NUM_WINNERS:
        break
    
    fetchedWinnerArchive = fetchWinnerArchive()

    # Add the winners to the winners.yaml file
    db.addToWinners(fetchedWinnerArchive)

    numRecordedWinners = db.countRecordedWinners()
    # Print the number of recorded winners and posts
    print(f"We have recorded {numRecordedWinners} winners total.")

    if numRecordedWinners >= NUM_WINNERS:
        break

    time.sleep(600) # Since Pithee only updates winners once per 10 minutes, let's just wait that long.


print("Done fetching winners!")