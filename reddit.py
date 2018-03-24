
from my_constants import Auth
import praw

client_id, client_secret, user_agent, password, username = Auth.reddit()

reddit = praw.Reddit(
                    client_id=client_id, 
                    client_secret=client_secret, 
                    user_agent=user_agent,
                    password=password,
                    username=username
                    )
#
# print(reddit.user.me())
submission = reddit.submission(url='https://www.reddit.com/r/Bitcoin/comments/86sdic/how_bitcoin_became_popular_in_my_company_because/')
for top_level_comment in submission.comments:
    print(top_level_comment.body)