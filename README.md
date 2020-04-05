# My Emotion Text Insights API
The My Emotion Text Insights API is a ML model API for predicting the score 
of an Instrument review in three diccerent category `satisfied`, `moderate`, 
`not-satisfied` (Labels: 2, 1, 0). The model is trained on top of Amazon 
Musical Instrument Review data set.

## Project Structure
```
root
|__api (api server has not been build)
|__datalake (data storage for raw, parsed and processed data for modeling)
|__etl (package for data preprocessing)
|__modelboy (API for model training and serving)
|__modellake (storage for trained model pkl file)
|__prototype (Experiment Notebooks)
|__test (testing the dataio and model pipeline)
```

## Project History
The project has been taken as 8 (strictly) hours hackathon which involve: 
Building a ML model pipeline from scratch and Deploy the final model in to API 
separately. Here is the planned vs reality:

The plan was:
- Experiment over bunch of classifiers such as Logistic, SVM, Random Forest
- Try out a RNN model with Tensorflow
- Preprocess-Load-Train-Test-validation-Save ML pipeline
- Deploy the model in Server
- Create a Package Distribution `.whl` of the ML Pipeline Interface

In reality it has been shortned in to following:
- Experiment only with Logistic and SVM
- Preparing semi-automated ML Pipeline

Because of not having enough time the project is narrowed down to following steps.

## Prototyping the Model
The prototyping for data tranformation and modeling can be found in the 
`prototype` directory. Jupyter notebook has been used to experiment when 
building proto type. 

### Data Preprocessing
When trying out on raw data it has been found:
- The 5 (converted to 3) scores in the sample is highly imbalanced
- There is no null value in the text
- There is review with zero length

The review length with zero has been removed from the data. To fix imbalanced 
data the up-sample technique has been applied the data set. First the 5 score 
has been converted to 3 scores where 1 and 2 represent 0, 3 represent 1, 
and 4 and 5 represent 2. Then the up sample has been done to raise the score 
0 and 1 to the same size of score 3. Which has been added to the data 
preprocessing pipeline later in the production version.

Caution: __Now up-sampling created a potential bug which has been found out 
later. As the data is up-sampled and the split to train test it might happen 
there is small percentage of train data replicated into test, in 
real life the API might not provide that high accuracy. In future version it 
can be fixed.__

### Model Architecture Selection
Using Grid Search a `logistic` and a `support-vector-machine` model has been 
fitted with different parameter set to find out the best classifier 
which should pass to production pipeline. The following parameter has been 
considered for grid search:

- General
    - Regularization
    - Different Tokenizer
    - Regularization Parameter (C)
    - Stop word
 - SVM
    - Linear and Non-Linear Kernel 



It took more than 12 hours to run a test on grid search. The detail can be 
found on `02-prototype.ipynb` in the `prototype` directory. Based on the 
harmonic mean of precision and recall which is considered as f1 score the 
decision was to go with <SVC/Logistic> model. But the SVC models looks bit over
fitted and having not enough time to inspect the Logistic model has been 
selected.

When comparing the macro F1 score to select a model the SVC model looks over 
fitted as it gives almost 1. Hence also having score very close logistic 
model has been selected. In case of multi-class the the PRE micro can be 
calculated as follows:
 
PRE = (TP1 + TP2 + TP2)/(TP1 + TP2 + ... + FP3)

TP: True positive, FP: False positive

### Training the Production Model
Later a pipeline has been build based the model we have got using Gridsearch 
and added to the ML-Flow pipeline. The `modelboy` is the pipeline with the 
following feature. Upon giving a data location `datalake` and the `modelboy`
class from `modelboy.flow` will be able to train a and save a model.

## Pipeline: ModelBoy
ModelBoy provide a final API interface to 
preprocess-train-test-validation-save-load a model lifecycle. 
As it also save some accuracy and few other metadata along with the model with 
a specific version.

The ModelBoy class from modelboy accepts a directory of textfile and will do 
the upsampling and provide and profivide a fit on top. After the fittend model 
it can store the test and validation accuracy along with other metadata in the 
a specific directory with each version. the first model we have trained and 
saved can by found in the models directory and also can be load any time using 
ModelBoyLoader.

Sample:

Sample:
```python
from modelboy.flow import ModelBoy
from modelboy.utils import version_by_date

latest_data = version_by_date("./datalake/feed/", "csv")
model_files = "./modellake"

# Create a Instance of the Class
mboy = ModelBoy(latest_data, model_files)

# Read the Latest Data
main_df = mboy.data_reader()

# Split the Data
X_train, y_train, X_test, y_test = mboy.train_test_split(main_df, 0.7)

# Train A Classifier
classifier = mboy.trainer(X_train, y_train)

# Check Accuracy on Test Set
classifier.score(X_test, y_test)

# Save the model
mboy.saver(classifier)
```

Due to maintaining strictly 8 hours time constrain the test and validation 
part has not been automated.

Model Boy also provide a `loader` function which can be used to load a model:
```python
from modelboy.flow import loader
model_files = "./modellake"

# load the model when not providing any
latest_classifier = loader(model_files)
```

The `modelboy.utils` provide has some external function like `tokenizer`, 
searching directory and versioning models and data.

### Getting Prediction from the model
Sample:
```python

from modelboy.flow import loader

### loading latest model
classifier = loader("../modellake/")
a_text_list = ["update 15 july 2013i still really love how these assist in quick tuning but man are they flimsy all of my other musician friends who also love this tuner s ability to grab the right pitch also have"]

classifier.predict(a_text_list)   
```
Though it has been noticed, providing small un-satisfactory review is most of
the time miss-classified as satisfactory.

# Conclusion
Well in industry situation some industry grade pipeline builder such as
Apache Airflow, Apache Beam, Tensorflow Extended, Kubeflow should be used. But
they are more tedious to configure in local machine and also I never had any 
opportunity to used them in some of my projects. By following the strict time
limit thats what I came up with but there is a lot room for improvements. such
as fully automated pipeline, testing and validation in automation. More 
elaborate use of Precision, Recall instead of  average F1-score from Grid 
Search.

__Thanks,__ 