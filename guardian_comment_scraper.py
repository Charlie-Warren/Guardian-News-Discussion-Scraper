import requests
import json
import os
from pathlib import Path
import pandas as pd
import re
import string

def get_discussion_id(url:str) -> str:
    """
    Find discussion ID from url
    """
    response = requests.get(url)
    response.raise_for_status()
    x = str(response.content)
    mylist = x.split('\"shortUrlId\":', maxsplit=1)
    bl = mylist[1].split(',', maxsplit=1)
    id = bl[0].strip('\"')
    return id

def save_json(data, title) -> None:
    """
    Saves json file
    """
    try:
        script_dir = Path(os.path.dirname(os.path.realpath(__file__)))
        data_folder = script_dir / str(title)
        # Create data folder
        data_folder.mkdir(parents=True, exist_ok=True)
        with open(data_folder / 'discussion.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        print(f"Saved JSON file to {(data_folder / 'discussion.json')}")
    except:
        print("Failed to save JSON file")

def remove_html_tags(text:str) -> str:
    """Remove html tags from a string"""
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)

def maxqda_format(all_data, title:str, save:bool):
    """Creates a dataframe from the input data. Formats the dataframe for use with MAXQDA, and optionally saves."""
    # number, , name, date and time, likes, pinned, comment
    data_df = pd.DataFrame(all_data)
    rows = list(range(1, len(data_df)+1))
    data_df.index = rows
    print(data_df)
    if save:
        try:
            script_dir = Path(os.path.dirname(os.path.realpath(__file__)))
            try:
                # Create data folder
                data_folder = script_dir / str(title)
                data_folder.mkdir(parents=True, exist_ok=True)
            except OSError:
                data_folder = script_dir / 'article'
                data_folder.mkdir(parents=True, exist_ok=True)
            save_path = data_folder / 'guardian_comments.csv'
            data_df.to_csv(save_path)
            print(f'Saved data to {save_path}')
        except:
            print('Failed to save csv file')

def main():
    ### CHANGE THESE ###
    url = 'https://www.theguardian.com/sport/2022/sep/11/jon-rahms-stunning-62-puts-him-in-contention-at-pga-championship'
    save = False
    ####################


    #comments_and_responses = []
    p = 'http://discussion.theguardian.com/discussion-api/discussion/' + get_discussion_id(url)
    response = requests.get(p)
    data_dict = response.json()
    
    x = data_dict['discussion']
    data_rows = []
    for comment in x['comments']:
        # Add thread comment entry
        df_row = {
            'Name': comment['userProfile']['displayName'],
            'Date': comment['date'],
            'Likes': comment['numRecommends'],
            'isPinned': comment['isHighlighted'],
            'Comment': remove_html_tags(comment['body']).strip()
            }
        data_rows.append(df_row)
        # Check for responses
        if 'responses' in comment:
            # Add responses as comment entries
            for response in comment['responses']:
                df_row = {
                    'Name': response['userProfile']['displayName'],
                    'Date': response['date'],
                    'Likes': response['numRecommends'],
                    'isPinned': response['isHighlighted'],
                    'Comment': remove_html_tags(response['body']).strip()
                    }
                data_rows.append(df_row)
    
    title = x['title']
    print(f"Title: {title}")
    cleaned_title = title.translate(str.maketrans('', '', string.punctuation))

    maxqda_format(data_rows, cleaned_title, save)
    if save:
        save_json(data_dict, cleaned_title)

if __name__ == '__main__':
    main()