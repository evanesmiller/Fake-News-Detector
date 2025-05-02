import pandas as pd #provides tools for data manipulation
from sklearn.model_selection import train_test_split #machine learning 
import re
import string


def text_trim(text):
    #Make text lowercase
    text = text.lower()

    #Trim text for processing
    text = re.sub(r'\[.*?\]', '', text)
    text = re.sub("\\W", " ", text)
    text = re.sub(r'https?://\S+|www\.\S+', '', text)
    text = re.sub('<.*?>+', '', text)
    text = re.sub('[%s]' % re.escape(string.punctuation), '', text)
    text = re.sub('\n', '', text)
    text = re.sub(r'\w*\d\w*', '', text)
    return text





def train_models():
    ds_fake = pd.read_csv('Fake.csv')
    ds_true = pd.read_csv('True.csv')

    ds_fake["class"] = 0
    ds_true["class"] = 1



    ds_merge = pd.concat([ds_fake, ds_true], axis=0)

    ds_true = pd.read_csv('real_news.csv')
    ds_merge = pd.concat([ds_merge, ds_true], axis=0)

    ds = ds_merge.drop(['title', 'subject', 'date'], axis=1)
    print(ds.isnull().sum())
    ds = ds.sample(frac=1)
    ds.reset_index(inplace=True)
    ds.drop(['index'], axis=1, inplace=True)

    ds['text'] = ds['text'].apply(text_trim)
    x = ds['text']
    y = ds['class']

    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.25)

    from sklearn.feature_extraction.text import TfidfVectorizer

    vectorization = TfidfVectorizer()
    xv_train = vectorization.fit_transform(x_train)
    xv_test = vectorization.transform(x_test)

    LR = log_reg(xv_train, y_train)
    DT = dec_tree_class(xv_train, y_train)
    GB = grad_boost_class(xv_train, y_train)
    RF = ran_for_class(xv_train, y_train)

    models = {
        "Logistic Regression":  LR,
        "Decision Tree":        DT,
        "Gradient Boosting":    GB,
        "Random Forest":        RF
    }

    return vectorization, models

def log_reg(xv_train, y_train):
    from sklearn.linear_model import LogisticRegression

    LR = LogisticRegression()
    return LR.fit(xv_train, y_train)


def dec_tree_class(xv_train, y_train):
    from sklearn.tree import DecisionTreeClassifier

    DT = DecisionTreeClassifier()
    return DT.fit(xv_train, y_train)


def grad_boost_class(xv_train, y_train):
    from sklearn.ensemble import GradientBoostingClassifier
    
    GB = GradientBoostingClassifier(random_state=0)
    return GB.fit(xv_train, y_train)


def ran_for_class(xv_train, y_train):
    from sklearn.ensemble import RandomForestClassifier
    
    RF = RandomForestClassifier(random_state=0)
    return RF.fit(xv_train, y_train)


def output(n):
    if n == 0:
        return "Fake news"
    elif n == 1:
        return "Real news"
    
def manual_testing(news, vectorizer, models):
    # Create a DataFrame for the input text
    testing_news = {"text": [news]}
    new_def_test = pd.DataFrame(testing_news)
    
    # Apply the trimming function to the proper column name
    new_def_test["text"] = new_def_test["text"].apply(text_trim)
    
    # Transform the input text using the pre-fitted vectorizer
    new_xv_test = vectorizer.transform(new_def_test["text"])
    
    # Make predictions using each pre-trained model and print the results
    for name, model in models.items():
        prediction = model.predict(new_xv_test)[0]  # get the prediction
        print(f"{name} prediction: {output(prediction)}") #return result


