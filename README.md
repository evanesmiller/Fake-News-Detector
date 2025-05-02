# Fake-News-Detector

### How to run program

#### Step 1:
Download other fake.csv and real.csv files from the link below
```
https://www.kaggle.com/datasets/clmentbisaillon/fake-and-real-news-dataset
```
Move them into folder with Python files

#### Step 2:
Download required dependencies via terminal
```
pip install feedparser 
pip install requests           
pip install beautifulsoup4    
pip install pandas             
pip install scikit-learn
```

#### Step 3:
Run program with the following command
```
python3 main.py
```
*** NOTES ***
- First run will take a while to complete while models are being trained
- article_extract.py was used to generate more real_news.csv (unnecessary for running main.py)
- Models may not be entirely accurate due to inaccuracy of datasets
- Kaggle datasets and pretrained models were too large in size to be included on GitHub
