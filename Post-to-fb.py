import os
import openai
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
PAGE_ID = os.getenv("FACEBOOK_PAGE_ID")
ACCESS_TOKEN = os.getenv("FACEBOOK_ACCESS_TOKEN")

# === Generate Post with OpenAI ===

def generate_post(topic, post_type, tone, audience, max_words, use_emojis, use_hashtags, use_quote):
    prompt = f"""Generate a {post_type} type social media post on the topic "{topic}".
Tone: {tone}
Target audience: {audience}
Word limit: {max_words}
Include emojis: {"Yes" if use_emojis else "No"}
Include hashtags: {"Yes" if use_hashtags else "No"}
Include a quote: {"Yes" if use_quote else "No"}

Write the post as if it's going to be published on a Facebook business page.
"""
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.8,
        max_tokens=400
    )
    return response['choices'][0]['message']['content'].strip()

# === Facebook Post Function ===

def post_to_facebook(text):
    url = f"https://graph.facebook.com/{PAGE_ID}/feed"
    params = {"message": text, "access_token": ACCESS_TOKEN}
    r = requests.post(url, params=params)
    if r.status_code == 200:
        return f"Post successful! ID: {r.json().get('id')}"
    else:
        return f"Failed to post: {r.json()}"

# === Example Interactive Flow ===

if __name__ == "__main__":
    print("Auto Social Media Post Generator & Publisher\n")

    # User Inputs
    topic = input("Enter the topic: ")
    post_type = input("Type of post (tip, story, announcement, quote, promo): ")
    tone = input("Tone (professional, casual, witty, inspiring): ")
    audience = input("Target audience (e.g., entrepreneurs, teens, parents): ")
    max_words = int(input("Maximum number of words: "))
    use_emojis = input("Include emojis? (y/n): ").lower() == 'y'
    use_hashtags = input("Include hashtags? (y/n): ").lower() == 'y'
    use_quote = input("Include a quote? (y/n): ").lower() == 'y'

    # Generate content
    print("\nGenerating post...")
    post_text = generate_post(topic, post_type, tone, audience, max_words, use_emojis, use_hashtags, use_quote)
    print("\nGenerated Post:\n" + "-"*40)
    print(post_text)
    print("-"*40)

    # Confirm and post
    confirm = input("\nDo you want to post this to Facebook? (y/n): ").lower()
    if confirm == 'y':
        result = post_to_facebook(post_text)
        print(result)
    else:
        print("Post was not sent.")

