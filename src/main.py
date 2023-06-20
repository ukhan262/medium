"""Upload articles to medium."""
import argparse
import os

import requests

# If not github actions, use dotenv
if not os.environ.get("GITHUB_ACTIONS"):
    from dotenv import load_dotenv

    load_dotenv()

api_token = os.environ.get("MEDIUM_TOKEN")

# Get file to upload from argparse
parser = argparse.ArgumentParser(description="Upload articles to medium")
parser.add_argument(
    "-f",
    "--file",
    type=str,
    help="File to upload",
    required=True,
)

args = parser.parse_args()


# Get medium user info from api
def get_user_info():
    """
    Get user details from Medium API.

    Returns:
         user_detail
    """
    my_details = requests.get(
        url=f"https://api.medium.com/v1/me?accessToken={api_token}", timeout=10
    ).json()

    return my_details


def post_article(contents, state="draft"):
    """
    Post article on Medium API.

    Args:
        contents: Markdown formatted content to be published onto medium.
        state: The state of the article, defaults to draft.

    Returns:
        True if successful
    """
    print("Posting article")
    try:
        headers = {"Authorization": f"Bearer {api_token}"}

        article_metadata = {
            "title": "Hello World",
            "contentFormat": "markdown",
            "content": contents,
            "tags": ["helloworld", "testing"],
            "publishStatus": state,
        }

        response = requests.post(
            url=f'https://api.medium.com/v1/users/{get_user_info()["data"]["id"]}/posts',
            headers=headers,
            timeout=10,
            data=article_metadata,
        )
    except Exception as error_message:
        print(error_message)
        return False

    print(f'New article URL: {response.json()["data"]["url"]}')
    return True


def read_file(filename):
    """
    Read file from given path.

    Args:
        filename: Path to file to be read

    Returns:
        contents of file
    """
    try:
        with open(filename, "r", encoding="UTF-8") as file_contents:
            contents = file_contents.read()
    except FileNotFoundError:
        print("File not found")
        return None
    except Exception as error_message:
        print(error_message)
        return None

    return contents


def main():
    """Execute function."""
    filename = args.file
    if filename.endswith(".md"):
        contents = read_file(filename)
        if contents:
            post_article(contents, state="draft")
        else:
            print("No contents found")


if __name__ == "__main__":
    main()
