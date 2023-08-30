"""
Key changes and optimizations:

1. Moved the load_dotenv call to a dedicated function for better clarity.
2. Added error handling using raise_for_status() for API requests to handle potential errors more gracefully.
3. Changed the way API request data is sent from using the data parameter to sending JSON data directly using the json parameter.
4. Improved error handling in the read_file function to print errors and return early.
5. Moved the argparse setup into the main function for better encapsulation.
6. Wrapped the article posting process in a try-except block to handle potential exceptions during the API request.
7. Consolidated the process of getting user information and posting an article into their respective functions for better separation of concerns.
8. Allowed arguments for the title and tags of the article.

"""
"""Upload articles to medium."""
import argparse
import os
import requests

from dotenv import load_dotenv

API_TOKEN = os.environ.get("MEDIUM_TOKEN")

def load_env():
    if not os.environ.get("GITHUB_ACTIONS"):
        load_dotenv()

def get_user_info(api_token):
    response = requests.get(
        f"https://api.medium.com/v1/me?accessToken={api_token}", timeout=10
    )
    response.raise_for_status()
    return response.json()

def post_article(api_token, title, contents, tags, state="draft"):
    headers = {"Authorization": f"Bearer {api_token}"}
    article_metadata = {
        "title": title,
        "contentFormat": "markdown",
        "content": contents,
        "tags": tags,
        "publishStatus": state,
    }

    response = requests.post(
        f'https://api.medium.com/v1/users/{get_user_info(api_token)["data"]["id"]}/posts',
        headers=headers,
        timeout=10,
        json=article_metadata,
    )
    response.raise_for_status()
    return response.json()["data"]["url"]

def read_file(filename):
    try:
        with open(filename, "r", encoding="UTF-8") as file_contents:
            return file_contents.read()
    except FileNotFoundError:
        print("File not found")
    except Exception as error_message:
        print(error_message)

def main():
    parser = argparse.ArgumentParser(description="Upload articles to Medium")
    parser.add_argument(
        "-f",
        "--file",
        type=str,
        help="File to upload",
        required=True,
    )
    parser.add_argument(
        "-t",
        "--title",
        type=str,
        help="Title of the article",
        required=True,
    )
    parser.add_argument(
        "--tags",
        type=str,
        help="Comma-separated list of tags",
        required=True,
    )
    args = parser.parse_args()

    load_env()

    filename = args.file
    if filename.endswith(".md"):
        contents = read_file(filename)
        if contents:
            try:
                tags = args.tags.split(",")  # Convert comma-separated tags to a list
                article_url = post_article(API_TOKEN, args.title, contents, tags, state="draft")
                print(f'New article URL: {article_url}')
            except requests.exceptions.RequestException as e:
                print(f"An error occurred while posting the article: {e}")
        else:
            print("No contents found")

if __name__ == "__main__":
    main()
