
import sqlite3
import pandas as pd

# transfer excel data to sql
# name of the xlsx. 
filename = 'workbook'
con = sqlite3.connect(filename+'.db')
wb = pd.read_excel(filename+'.xlsx', sheetname=None)

for sheet in wb:
    wb[sheet].to_sql(sheet, con, index=False)

con.commit()
con.close()


## query the information
## query sql data to python

"""
SELECT
    country
FROM
    Population
WHERE

    population > 500000;
"""

conn = sqlite3.connect('filename'+'.db')
df = pd.read_sql_query(query, conn)

# Load necessary libraries
from pyspark.sql.functions import pandas_udf, PandasUDFType
from pyspark.sql.types import *
import pandas as pd

# Create the schema for the resulting dataframe
schema = StructType([StructField('ID', LongType(), True),
                    StructField('p0', DoubleType(), True),
                    StructField('p1', DoubleType(), True)])

# Define the UDF, input and outputs are Pandas DFs
@pandas_udf(schema, PandasUDFType.GROUPED_MAP)
def analyze_player(sample_pd):
    
    # return empty params in not enough data
    if (len(sample_pd.shots) <= 1):
        return pd.DataFrame({'ID': [sample_pd.player_id[0]], 
                                'p0': [ 0 ], 'p1': [ 0 ]})
    
    # Perform curve fitting     
    result = leastsq(fit, [1, 0], args=(sample_pd.shots, 
                                sample_pd.hits))
    
    # Return the parameters as a Pandas DF 
    return pd.DataFrame({'ID': [sample_pd.player_id[0]], 
                    'p0': [result[0][0]], 'p1': [result[0][1]]})
    
# perform the UDF and show the results 
player_df = stats_df.groupby('player_id').apply(analyze_player)
display(player_df)





import pandas as pd
import numpy as np
from google.oauth2 import service_account
from sklearn.linear_model import LogisticRegression
from datetime import datetime
import pandas_gbq

# fetch the data set and add IDs 
gamesDF = pd.read_csv("https://github.com/bgweber/Twitch/raw/master/Recommendations/games-expand.csv")
gamesDF['User_ID'] = gamesDF.index 
gamesDF['New_User'] = np.floor(np.random.randint(0, 10, gamesDF.shape[0])/9)

# train and test groups 
train = gamesDF[gamesDF['New_User'] == 0]
x_train = train.iloc[:,0:10]
y_train = train['label']
test = gamesDF[gamesDF['New_User'] == 1]
x_test = test.iloc[:,0:10]

# build a model
model = LogisticRegression()
model.fit(x_train, y_train)
y_pred = model.predict_proba(x_test)[:, 1]

# build a predictions dataframe
resultDF = pd.DataFrame({'User_ID':test['User_ID'], 'Pred':y_pred}) 
resultDF['time'] = str(datetime. now())

# save predictions to BigQuery 
table_id = "dsp_demo.user_scores"
project_id = "gameanalytics-123"
credentials = service_account.Credentials.from_service_account_file('dsdemo.json')
pandas_gbq.to_gbq(resultDF, table_id, project_id=project_id, if_exists = 'replace', credentials=credentials)



# load Flask 
import flask
app = flask.Flask(__name__)

# define a predict function as an endpoint 
@app.route("/predict", methods=["GET","POST"])
def predict():
    data = {"success": False}

    # get the request parameters
    params = flask.request.json
    if (params == None):
        params = flask.request.args

    # if parameters are found, echo the msg parameter 
    if (params != None):
        data["response"] = params.get("msg")
        data["success"] = True

    # return a response in json format 
    return flask.jsonify(data)

# start the flask app, allow remote connections
app.run(host='0.0.0.0', port = 80)