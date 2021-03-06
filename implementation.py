import os 
import pandas as pd 
import matplotlib.pyplot as plt
import numpy as np
from BasicAlgorithms.perceptron import Perceptron
from matplotlib.colors import ListedColormap
from BasicAlgorithms.perceptronV2 import Perceptron2 as per2
from BasicAlgorithms.adalinegd import Adaline
from BasicAlgorithms.adalinesgd import AdalineSGD
from LogisticRegression.Logisticregressionclassifier import LogisticRegressionGD as Logisticregressionclassifier
from sklearn.datasets import load_iris
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split


s = 'https://archive.ics.uci.edu/ml/machine-learning-databases/iris/iris.data'
df = pd.read_csv(s,header=None, encoding='utf-8')

y = df.iloc[0:100,4].values
y = np.where(y=="Iris-setosa",-1,1)
X = df.iloc[0:100 , [0,2]].values


ppn = Perceptron(eta=0.1,n_iter=10)
ada = Adaline(eta=0.0001,n_iter=10)
adasgd = AdalineSGD(n_iter=15,eta=0.01,random_state=1)
lrgd = Logisticregressionclassifier(eta=0.05,n_iter=1000,random_state=1)

ada.fit(X,y)
ppn.fit(X,y)


def plotting_data():
    plt.scatter(X[:50,0], X[:50,1] , color = "red",marker="o",label="setosa")
    plt.scatter(X[50:100,0],X[50:100,1],color ="green",marker="*",label="versicolor")
    plt.xlabel("sepal length")
    plt.ylabel("petal length")
    plt.legend(loc="upper left")

def perceptron():
    plt.plot(range(1,len(ppn.errors_)+1),ppn.errors_,marker="o")
    plt.xlabel("Epochs")
    plt.ylabel("Number of updates")
    plt.show()

def plot_decision_regions(X,y,classifier,resolution=0.02):
    markers = ("s","x","o","*","^")
    colors = ("red","blue","lightgreen","gray","cyan")
    cmap = ListedColormap(colors[:len(np.unique(y))])
    x1_min,x1_max = X[:,0].min() -1 , X[:,0].max() +1
    x2_min,x2_max = X[:,1].min() -1 , X[:,1].max() +1
    xx1,xx2 = np.meshgrid(np.arange(x1_min,x1_max,resolution),np.arange(x2_min,x2_max,resolution))
    Z = classifier.predict(np.array([xx1.ravel(),xx2.ravel()]).T)
    Z = Z.reshape(xx1.shape)
    plt.contourf(xx1,xx2,Z,alpha=0.3,cmap=cmap)
    plt.xlim(xx1.min(),xx1.max())
    plt.ylim(xx2.min(),xx2.max())
    for idx,cl in enumerate(np.unique(y)):
        plt.scatter(x=X[y==cl,0],y=X[y==cl,1],alpha=0.8,c=colors[idx],marker=markers[idx],label=cl,edgecolor="black")
    plt.xlabel("sepal length")
    plt.ylabel("petal length")
    plt.legend(loc="upper left")
    

def adaline():
    fig,axes = plt.subplots(nrows=1,ncols=3,figsize=(10,4))
    ada1 = Adaline(n_iter=10,eta=0.01).fit(X,y)
    axes[0].plot(range(1,len(ada1.cost_)+1),np.log10(ada1.cost_),marker="o")
    axes[0].set_xlabel("epochs")
    axes[0].set_ylabel("cost")
    axes[0].set_title("0.01 learning rate")

    ada2 = Adaline(n_iter=10,eta=0.001).fit(X,y)
    axes[1].plot(range(1,len(ada2.cost_)+1),np.log10(ada2.cost_),marker="o")
    axes[1].set_xlabel("epochs")
    axes[1].set_ylabel("cost")
    axes[1].set_title("0.001 learning rate")

    ada3 = Adaline(n_iter=10,eta=0.0001).fit(X,y)
    axes[2].plot(range(1,len(ada3.cost_)+1),np.log10(ada3.cost_),marker="o")
    axes[2].set_xlabel("epochs")
    axes[2].set_ylabel("cost")
    axes[2].set_title("0.0001 learning rate")
    plt.show()

X_std = np.copy(X)
X_std[:,0] =(X[:,0] - X[:,0].mean()) / X[:,0].std()
X_std[:,1] = (X[:,1] - X[:,1].mean()) / X[:,1].std()    



def logistic_reg():
    iris = load_iris()
    X_ = iris.data[: , [2,3]]
    y_ = iris.target

    X_train, X_test, y_train , y_test = train_test_split(X_,y_,test_size=0.3,random_state=1)

    std = StandardScaler()
    std.fit(X_train)
    std.fit(X_test)
    X_train_std = std.transform(X_train)
    X_test_std = std.transform(X_test)
    X_train_subset = X_train_std[(y_train == 0) | (y_train ==1)]
    y_train_subset = y_train[(y_train == 0) | (y_train == 1)]
    lrgd.fit(X_train_subset,y_train_subset)
    plot_decision_regions(X=X_train_subset, y=y_train_subset, classifier=lrgd)
    plt.xlabel("petal length")
    plt.ylabel("petal width")
    plt.legend(loc="best")
    plt.tight_layout()
    plt.show()
