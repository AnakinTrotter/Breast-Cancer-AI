import sklearn
from sklearn import datasets
from sklearn import svm
from sklearn import metrics
import pickle
import pandas as pd


# gets the user input (train, predict, quit)
def run():
    should_run = True
    while should_run:
        print("Menu:")
        print("1. Train a model")
        print("2. Make a prediction")
        selection = input("Please type 1 or 2 to make a selection or anything else to quit.\n")
        if selection == "1":
            train()
        elif selection == "2":
            predict()
        else:
            should_run = False
    print("Thank you for using Breast Cancer AI!")


# prints at start of program
def welcome():
    print("\n\n\n")
    print("Welcome to Breast Cancer AI!")
    print("This program can predict it a tumor is malignant or benign based on")
    print("inputs such as the mean radius and texture.\n")


# trains SVM model saving 20% of data for testing then saves the model
def train():
    print("Training...")
    cancer = datasets.load_breast_cancer()
    # if can write to data.csv then save the training set for testing
    try:
        pd.DataFrame(data=cancer['data'], columns=cancer['feature_names']).to_csv("data.csv", sep=",", index=False)
    except PermissionError:
        pass

    print("\nFeature names:")
    print(cancer.feature_names)
    print("Target names:")
    print(cancer.target_names, "\n")

    x = cancer.data
    y = cancer.target

    x_train, x_test, y_train, y_test = sklearn.model_selection.train_test_split(x, y, test_size=0.2)

    clf = svm.SVC(kernel="linear")
    clf.fit(x_train, y_train)

    y_pred = clf.predict(x_test)

    acc = metrics.accuracy_score(y_test, y_pred)
    with open("model.pickle", "wb") as f:
        pickle.dump(clf, f)
    print("Done!")
    print("Accuracy: ", acc * 100, "%\n")


# loads model from pickle then outputs predictions to a file
def predict():
    try:
        clf = pickle.load(open("model.pickle", "rb"))
    except FileNotFoundError:
        print("No model found.")
        return

    try:
        path = input("Please enter the name of your input file (csv).\n")
        data = pd.read_csv(path)
    except FileNotFoundError:
        print("Invalid input.")
        return

    predictions = clf.predict(data)
    output = open("results.txt", "w")
    for a in predictions:
        line = "Benign"
        if a == 1:
            line = "Malignant"
        output.write(line + "\n")
    output.close()
    print("Predictions saved to results.txt file.\n")


if __name__ == '__main__':
    welcome()
    run()
