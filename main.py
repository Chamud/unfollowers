import time 
import os
from InstagramAPI import InstagramAPI
import csv
import sys
from datetime import datetime

from dotenv import load_dotenv
load_dotenv('.env')

# datetime object containing current date and time
now = datetime.now()

api = InstagramAPI(os.environ['IGUSERNAME'], os.environ['PASS'])
api.login()
user_id = api.username_id

def getTotalFollowers():
    followers = []
    next_max_id = True
    while next_max_id:
        # first iteration hack
        if next_max_id is True:
            next_max_id = ''

        _ = api.getUserFollowers(user_id, maxid=next_max_id)
        followers.extend(api.LastJson.get('users', []))
        next_max_id = api.LastJson.get('next_max_id', '')
    return followers

def getTotalFollowing():
    followers = []
    next_max_id = True
    while next_max_id:
        # first iteration hack
        if next_max_id is True:
            next_max_id = ''

        _ = api.getUserFollowings(user_id, maxid=next_max_id)
        followers.extend(api.LastJson.get('users', []))
        next_max_id = api.LastJson.get('next_max_id', '')
    return followers

def nonFollowers(followers, following):
    nonFollowers = {}
    dictFollowers = {}
    for follower in followers:
        dictFollowers[follower['username']] = follower['pk']

    for followedUser in following:
        if followedUser['username'] not in dictFollowers:
            nonFollowers[followedUser['username']] = followedUser['pk']

    return nonFollowers

def unFollow():
    followers = getTotalFollowers()
    following = getTotalFollowing()
    nonFollow = nonFollowers(followers, following)
    i = len(nonFollow)
    rounds = 1
    max_rounds = 14
    per_round = 50
    interval = 3
    print('Number of followers:', len(followers))
    print('Number of following:', len(following))
    print('Number of nonFollowers:', i)
    print("")
    choice2 = 'y'
    print('Unfollowing '+str(per_round)+' per each '+str(interval)+' hours for '+str(max_rounds*interval)+' hours!')
    print("")

    while i!=0:
        p = i
        print("")
        time.sleep(3)
        if choice2 == 'y':
            print("Round ", rounds)
            with open('Unfollowed_list.csv', 'a', newline='') as file:
                writer = csv.writer(file)
                while i!=p-per_round:
                    try:
                        i-=1
                        user = list(nonFollow.keys())[len(nonFollow)-1]
                        api.unfollow(nonFollow[user])
                        nonFollow.pop(user)
                        print(datetime.now().strftime("%d/%m/%Y %H:%M:%S") + '  ', str(user))
                        writer.writerow([user])
                    except Exception as e:
                        print("Error While Unfollowing: " + str(user))
                        time.sleep(2)
                        print(str(e))
            print("")
            if rounds==max_rounds:
                choice2 = 'n'
            rounds = rounds+1
            time.sleep(interval*3600)

        elif choice2 == 'n':
            break

    print("")
    print("Remaining NON-FOLLOWERS = ", i)


if __name__ == "__main__":
    filename = "Unfollowing_process_log__" + now.strftime("%Y_%m_%d__%H_%M_%S") + ".txt"
    sys.stdout = open(filename, "w")
    print("Starting...!!")
    print("")
    print("Logged in as the id:", user_id)
    unFollow() 
    print("")
    print("Exiting...!!")
    sys.stdout.close()   