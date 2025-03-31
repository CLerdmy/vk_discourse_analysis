import vk_api
from vk_api import VkApiError
import pandas as pd
import time

def get_total_posts_count(group_url, start_date, end_date, token):
    vk_session = vk_api.VkApi(token=token)
    vk = vk_session.get_api()

    try:
        group_id = vk.utils.resolveScreenName(screen_name=group_url.split('/')[-1])['object_id']
    except VkApiError as e:
        print("Error:", e)
        return -1

    total_posts_count = 0
    offset = 0
    step = 100

    while True:
        try:
            posts = vk.wall.get(owner_id=-group_id, count=step, offset=offset)
        except VkApiError as e:
            print("Error:", e)
            break

        if not posts['items']:
            break

        for post in posts['items']:
            if start_date <= post['date'] <= end_date:
                total_posts_count += 1

        offset += step

    return total_posts_count

def get_all_posts(group_url, start_date, end_date, token, stop=None):
    vk_session = vk_api.VkApi(token=token)
    vk = vk_session.get_api()

    try:
        group_id = vk.utils.resolveScreenName(screen_name=group_url.split('/')[-1])['object_id']
    except VkApiError as e:
        print("Error:", e)
        return []

    all_posts = []
    offset = 0
    step = 100
    total_posts = get_total_posts_count(group_url, start_date, end_date, token)

    if total_posts == -1:
        print("Error.")
        return []

    print("Общее количество постов:", total_posts)

    while True:
        try:
            posts = vk.wall.get(owner_id=-group_id, count=step, offset=offset)
        except VkApiError as e:
            print("Error:", e)
            break

        if not posts['items']:
            break

        for post in posts['items']:
            if start_date <= post['date'] <= end_date:
                post_info = {
                    'Дата': pd.to_datetime(post['date'], unit='s'),
                    'Текст': post['text'],
                    'Лайки': post['likes']['count'],
                    'Комментарии': post['comments']['count'],
                    'Репосты': post['reposts']['count']
                }

                try:
                    comments = vk.wall.getComments(owner_id=-group_id, post_id=post['id'], count=100)
                    post_comments = [comment['text'] for comment in comments['items']]
                    post_info['Комментарии к посту'] = "\n".join(post_comments)
                except VkApiError as e:
                    print("Error:", e)
                    post_info['Комментарии к посту'] = ""

                all_posts.append(post_info)

                # Progress info
                print(f"Loaded {len(all_posts)} from {total_posts}")

                if stop is not None and len(all_posts) >= stop:
                    return all_posts

        offset += step
        time.sleep(3)
    return all_posts

# Input data (API_KEY, URL, OUTPUT_PATH)
token = 'TOKEN'
group_url = 'GROUP_URL'
path = 'PATH'

# Date
start_date = pd.Timestamp('2023-04-26').timestamp()
end_date = pd.Timestamp('2024-04-26').timestamp()

# Limit
stop_number = None

posts = get_all_posts(group_url, start_date, end_date, token, stop=stop_number)

df = pd.DataFrame(posts)

df.to_excel(path, index=False)