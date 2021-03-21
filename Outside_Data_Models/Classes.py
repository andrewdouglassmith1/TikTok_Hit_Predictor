from datetime import timedelta, date
import pandas as pd
from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import f1_score
from sklearn.metrics import precision_score, recall_score, precision_recall_curve,f1_score, fbeta_score, accuracy_score

#Functions to create daily urls

def daterange(end_date):
    start_date = date(2020,6,9)
    for n in range(int((end_date - start_date).days)+1):
        yield end_date - timedelta(n)

def daily_urls(end_date):
        '''
        returns a list of dates in %Y-%m-d% format since the end_date.  End date must also be in datetime format.
        '''
        # Url base
        base = "https://app.chartmetric.com/charts/tiktok_daily?date="
        # Start date
        start_date = date(2020,6,9)
        # Iniate list to store urls
        lst_daily_urls = []
        for dt in daterange(end_date):
            lst_daily_urls.append(base+dt.strftime("%Y=%m-%d"))
        return lst_daily_urls

#Functions to create 7 day rolling average urls

def rolling_daterange(end_date):
    start_date = date(2019,11,28)
    for n in range(int((end_date - start_date).days)+1):
        yield end_date - timedelta(n)

def weekly_rolling_urls(end_date):
        '''
        returns a list of dates in %Y-%m-d% format since the end_date.  End date must also be in datetime format.
        '''
        # Url base
        base = "https://app.chartmetric.com/charts/tiktok_weekly?date="
        # Start date
        start_date = date(2019,11,28)
        # Iniate list to store urls
        lst_weekly_rolling_urls = []
        for dt in rolling_daterange(end_date):
            lst_weekly_rolling_urls.append(base+dt.strftime("%Y=%m-%d"))
        return lst_weekly_rolling_urls

def gnumeric_func (data, columns):
    '''
    Function to factorize a column
    '''
    data[columns] = data[columns].apply(lambda x: pd.factorize(x)[0])
    return data

# Function to create a confusion matrix

# analyze error with confusion matrix

def make_confusion_matrix(model,X_val,y_val, threshold=0.5):
    # Predict class 1 if probability of being in class 1 is greater than threshold
    # (model.predict(X_test) does this automatically with a threshold of 0.5)
    y_predict = (model.predict_proba(X_val)[:, 1] >= threshold)
    success_confusion = confusion_matrix(y_val, y_predict)
    plt.figure(dpi=80)
    sns.heatmap(success_confusion, cmap=plt.cm.Blues, annot=True, square=True, fmt='d',
           xticklabels=['not a success', 'success'],
           yticklabels=['not a success', 'success']);
    plt.xlabel('prediction')
    plt.ylabel('actual')

# Function to return train / test results
def train_scores(model, x_train, y_train):
    """
    Returns training accuracy score
    """
    print("Train Scores")
    print("Accuracy score: {:6.2f}%".format(100*model.score(x_train, y_train)))

def test_scores(y_test, y_predict):
    """
    Returns various test scores
    """
    print("Test Scores")
    print("Score: {:6.2f}%".format(100*accuracy_score(y_test,y_predict)))
    print("F1 score: {:6.2f}%".format(100*f1_score(y_test,y_predict)))
    print("Precision: {:6.2f}%,  Test Recall: {:6.2f}%".format(100*precision_score(y_test,y_predict),
                                                     100*recall_score(y_test,y_predict)))

# Create a get dummies function based on cuttoff point of ranking for top artists
