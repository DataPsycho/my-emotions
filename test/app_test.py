from modelboy.flow import ModelBoy
from modelboy.utils import version_by_date, tokenizer
from modelboy.flow import loader

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

# load the model when not providing any
latest_classifier = loader(model_files)
