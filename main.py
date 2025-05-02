import os
import pickle
import requests
from bs4 import BeautifulSoup
from fnd import train_models, manual_testing, text_trim

# point to where you’ll store your models
MODEL_DIR    = "models"
VECT_FILE    = os.path.join(MODEL_DIR, "vectorizer.pkl")
MODELS_FILE  = os.path.join(MODEL_DIR, "models.pkl")

def ensure_models():
    """
    If saved models exist, load them.
    Otherwise train once and save to disk.
    Returns: (vectorizer, models_dict)
    """
    # make sure the folder exists
    os.makedirs(MODEL_DIR, exist_ok=True)

    if os.path.exists(VECT_FILE) and os.path.exists(MODELS_FILE):
        # load pre‑trained objects
        with open(VECT_FILE, "rb") as vf:
            vectorizer = pickle.load(vf)
        with open(MODELS_FILE, "rb") as mf:
            models = pickle.load(mf)
    else:
        # train from scratch (this will take time only once)
        vectorizer, models = train_models()  
        # save them to disk
        with open(VECT_FILE, "wb") as vf:
            pickle.dump(vectorizer, vf)
        with open(MODELS_FILE, "wb") as mf:
            pickle.dump(models, mf)

    return vectorizer, models


def extract_info(url):
    try:
        #open url as user in web browser
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        #check for errors (invalid url)
        response.raise_for_status()

        '''
        soup = BeautifulSoup(response.text, "html.parser")
        Parses the html file (reformats the file data into easily accessible text)
        
        e.g.

        <html>
            <body>
                <h1>Hello World</h1>
                <p>
                    fadjasdlkf afdkas
                </p>
            </body>
        </html>    
        
        Parsing allows for individual tags and the text between them to be accessed easily
        '''
        soup = BeautifulSoup(response.text, "html.parser")

        #collect title of article
        if soup.title:
            title = soup.title.text
        else:
            title = "No title found"     

        #collect date of article
        date = None
        date_tag = soup.find("time")
        if date_tag:
            date = date_tag.text
        else:
            date_tags = [   
                            {"property": "article:published_time"}, 
                            {"name": "date"},
                            {"name": "publish_date"},
                            {"name": "article_date"},
                            {"name": "publication_date"}
                        ]

            for tag in date_tags:
                meta_tag = soup.find("meta", tag)
                if meta_tag and meta_tag.get("content"):
                    date = meta_tag["content"]
                    break

        if not date:
            date = "No date found"

        #collect text of article
        paragraphs = soup.find_all("p")
        text = "\n".join(p.get_text() for p in paragraphs)

        return {"title": title, "date": date, "text": text if text else "No text found"}
    
    #handle errors when trying URL
    except requests.exceptions.RequestException as e:
        return {"error": f'Error fetching the url: {e}'}

if __name__ == "__main__":
    vectorizer, models = ensure_models()
    url = ""
    while url != "DONE":
        url = input("Enter the article URL (or DONE): ")
        if url == "DONE":
            break
        details = extract_info(url)  
        if "error" in details:
            print("Invalid input. Please enter either a link or DONE\n")
            continue

        manual_testing(details["text"], vectorizer, models)
        print("\n")



