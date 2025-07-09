import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor, as_completed
import time
import random

# install the above dependencies if you havent, this wont work without any of them!

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

LOG_PATH = r"C:\Users\youruseriguess\Documents\UsernameLog.txt" # where you want to send the output, id recommend having it in documents or something, **you also have to make the text file first** then copy it as path and add it here

def fetch_username(user_id):
    url = f"https://www.roblox.com/users/{user_id}/profile"
    print(f"Fetching: {url}")
    time.sleep(random.uniform(1.5, 2.5))
    try:
        res = requests.get(url, headers=HEADERS, timeout=10)
        print(f"Status Code: {res.status_code}")

        if res.status_code == 429:
            print("You might wanna slow it down a bit, you just got rate limited. Sleeping for 10 seconds.")
            time.sleep(10)
            return None
        elif res.status_code != 200:
            return None

        soup = BeautifulSoup(res.text, "html.parser")

        title = soup.title.string if soup.title else None
        if title and " - Roblox" in title:
            username = title.replace(" - Roblox", "").strip()
            print(f"Found username: {username}")
            return username

     #   print("username not found error, close enough HTML:")
        print(res.text[:500])

    except Exception as e:
        print(f"error fetching user id {user_id}: {e}")
    return None

def log_username(username):
    with open(LOG_PATH, "a", encoding="utf-8") as f:
        f.write(username + "\n")

def get_usernames(start_id, count, max_workers):
    usernames = set()
    batch_size = 20
    current_id = start_id

    open(LOG_PATH, "w").close()

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        while len(usernames) < count:
            ids = [current_id + i * 3 for i in range(batch_size)] # goes up in threes idk i thought it would be better for variation, change the 3 if you want

            futures = {
                executor.submit(fetch_username, uid): uid
                for uid in ids
            }
            for future in as_completed(futures):
                result = future.result()
                if result and result not in usernames:
                    usernames.add(result)
                    log_username(result)
                    print(f"[{len(usernames)}/{count}] Logged: {result}")
                if len(usernames) >= count:
                    break

            current_id += batch_size * 3

            time.sleep(random.uniform(3.0, 5.0))

    return list(usernames)

if __name__ == "__main__":
    get_usernames(start_id= random.randint(100000, 5000000000), count=int(input("How many usernames do you want to log? I would recommend 1000.")), max_workers=2) # dont change the workers or youll get rate limited by roblox, tweak it slightly if you must but not more than about 5 and thats pushing it
