from mastodon import Mastodon
import json

#create hashtag pool and empty lists to store posts
hashtags = ['climatechange', 'globalwarming', 'climatecrisis', 'climateaction', 'climatehoax', 'climatechangeisreal', 'gretathunberg', 'climate', 'sustainability', 'recycling', 'cleanenergy', 'ecofriendly', 'solar', 'environment', 'earthday', 'cleanenergy']
climatePosts = []

#create list of seed users found through searching app and empty list to store them
seedUsers = ['@climateactapp', '@greenpeace', '@ed_hawkins', '@gretathunberg', '@climate', '@green', '@coveringclimate', '@MichaelEmann', '@fff', '@climatenewsnow']
climateUsers = []

#iterate through tags
for tag in hashtags:
    print(f"Getting posts for hashtag: #{tag}")
    #gather posts that contain specific hashtag
    taggedPosts = mastodon.timeline_hashtag(tag, limit=200)
    #create node to be stored in json that stores specific info about the post
    for node in taggedPosts:
        post_info = {
            'user': node['account']['username'],
            'content': node['content'],
            'created_at': node['created_at'].isoformat(), #create to string or error
            'replies_count': node['replies_count'],
            'reblogs_count': node['reblogs_count'],
            'favourites_count': node['favourites_count'],
            'in_reply_to_id': node['in_reply_to_id'],
            'boosted_post_id': node['reblog']['id'] if node['reblog'] else None 
        }
        climatePosts.append(post_info)

#save to file
with open('climate_change_posts.json', 'w') as f:
    json.dump(climatePosts, f, indent=4)
#output total number
print(f"Collected {len(climatePosts)} climate change posts")


#Repeat similar process for seed users
for user in seedUsers:
    print(f"Getting followers and following list for user: {user}")
    
    user_info = mastodon.account_search(user)
    if user_info:
        user_id = user_info[0]['id']
        #get follower and following lists
        user_followers = mastodon.account_followers(user_id)
        user_following = mastodon.account_following(user_id)
        
        #iterate through followers list and store to climate users list
        for follower in user_followers:
            follower_data = {
                'username': follower['username'],
                'display_name': follower['display_name'],
                'followers_count': follower['followers_count'],
                'following_count': follower['following_count'],
                'follows': []
            }
            climateUsers.append(follower_data)

        #create following list  and go through it, append to climate users list as well
        following_list = []
        for following in user_following:
            following_list.append(following['username'])
            
            following_data = {
                'username': following['username'],
                'display_name': following['display_name'],
                'followers_count': following['followers_count'],
                'following_count': following['following_count'],
                'follows': [] 
            }
            climateUsers.append(following_data)
        
        #finally append root user to the list as well
        user_data = {
            'username': user_info[0]['username'],
            'display_name': user_info[0]['display_name'],
            'followers_count': user_info[0]['followers_count'],
            'following_count': user_info[0]['following_count'],
            'follows': following_list 
        }
        climateUsers.append(user_data)

#save to user json file 
#later to be used for friendship network
with open('climate_change_users.json', 'w') as f:
    json.dump(climateUsers, f, indent=4)

print(f"Collected data on {len(climateUsers)} climate users")
