from instagram_private_api import Client, ClientCompatPatch


def unofficial(user_name, password, LIMIT_IMAGE_COUNT, HASHTAG):
    api = Client(user_name, password)

    all_hash_image_posts_urls = []
    next_max_id = None
    while (api.feed_tag(HASHTAG, api.generate_uuid())["more_available"] == True) and (
            len([item for sublist in all_hash_image_posts_urls for item in sublist]) <= LIMIT_IMAGE_COUNT):
        if next_max_id == None:
            # Gets the first 12 posts
            posts = api.feed_tag(HASHTAG, api.generate_uuid())
            len(posts['items'])
            image_urls = []
            for i in range(len(posts['items'])):
                try:
                    url = posts['items'][i]['image_versions2']['candidates'][0][
                        'url']  # some posts do not have 'image_version2', they are overlooked in that case
                    image_urls.append(url)
                except:
                    pass
                    # Extract the value *next_max_id* from the above response, this is needed to load the next 12 posts
            next_max_id = posts["next_max_id"]
            all_hash_image_posts_urls.append(image_urls)
        else:
            next_page_posts = api.feed_tag(HASHTAG, api.generate_uuid())
            len(next_page_posts['items'])
            # get image urls
            next_image_urls = []
            for i in range(len(next_page_posts['items'])):
                try:
                    url = next_page_posts['items'][i]['image_versions2']['candidates'][0]['url']
                    next_image_urls.append(url)
                except:
                    pass
            # Extract the value *next_max_id*
            next_max_id = next_page_posts["next_max_id"]
            all_hash_image_posts_urls.append(next_image_urls)

    else:
        flat_hash_image_posts_urls = [item for sublist in all_hash_image_posts_urls for item in sublist]
        print(f"A total of {len(flat_hash_image_posts_urls)} image post urls were retrieved from the Instagram page.")

    return flat_hash_image_posts_urls




def official(user_name, password, LIMIT_IMAGE_COUNT, USERNAME):
    api = Client(user_name, password)

    all_image_posts_urls = []
    next_max_id = None
    while (api.username_feed(USERNAME, max_id=next_max_id)["more_available"] == True) and (
            len([item for sublist in all_image_posts_urls for item in sublist]) <= LIMIT_IMAGE_COUNT):
        if next_max_id == None:
            # Gets the first 12 posts
            posts = api.username_feed(USERNAME)
            #print('posts: {}'.format(posts))
            len(posts['items'])
            image_urls = []
            for i in range(len(posts['items'])):
                #print('posts[items]: {}'.format(posts['items']))
                url = posts['items'][i]['image_versions2']['candidates'][0]['url']
                image_urls.append(url)
            # Extract the value *next_max_id* from the above response, this is needed to load the next 12 posts
            next_max_id = posts["next_max_id"]
            all_image_posts_urls.append(image_urls)
        else:
            next_page_posts = api.username_feed(USERNAME, max_id=next_max_id)
            len(next_page_posts['items'])
            # get image urls
            next_image_urls = []
            for i in range(len(next_page_posts['items'])):
                try:
                    url = next_page_posts['items'][i]['image_versions2']['candidates'][0]['url']
                    next_image_urls.append(url)
                except:
                    pass
            # Extract the value *next_max_id*
            next_max_id = next_page_posts["next_max_id"]
            all_image_posts_urls.append(next_image_urls)

    else:
        flat_image_posts_urls = [item for sublist in all_image_posts_urls for item in sublist]
        print(f"A total of {len(flat_image_posts_urls)} image post urls were retrieved from the Instagram page.")

    return flat_image_posts_urls
