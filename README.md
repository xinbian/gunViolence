# Predicting Gun Violence and the Effectiveness of Laws

This is a breif summmury. More info can be found in the PDF format report.



## Introduction

Gun violence in the United States is a substantial public health concern. As best as we know, the literatures studying gun-control laws didn’t consider enough variables that might affect gun violence. In this project, we are aiming to analyze the problem using the firearm death data along with factors including unemployment rate, education level, crime rate, poverty rate, median household income and the strictness of law regulations at county level. The techniques used are Naive Bayes, Random Forest, and Neural Network. We first build regression models to predict firearm death rate, then try to find the relation, if any, between the strictness of law regulations and firearm death rate.


## Methodology

The goal is to design a model which can be used to predict firearm death rate  and to study the influence of laws on the firearm death rate. The data sets are collected in U.S at county level.  

### Approaches
1.  Collecting county level data.
2.  Data cleaning and  selection of attributes
3. Algorithm implementation, such as k-NN, k-means, Naive Bayes, Random Forest, Neural Network, for predicting the firearm death rate

### Algorithm and Tools
1. Tools: Weka, Tableau, Exploratory, scikit-learn
2. Languages: python 2.7
3. Algorithms: PCA, k-NN, k-Means, Naïve Bayes, Neural Network, Random Forest
4. Verification: 10-fold cross validation


## Main Results
### Random Forest and Neural Network Results

We build two regression models, random forest and neural network to predict firearm death rate. The RandomForestRegressor and MLPRgressor of scikit-learn are used to build the model.  


For random forest, the default parameters are used. 5 attributes: Income, Unemployment, Education, Poverty and Law are used  to predict Fire Rate.  The following figure shows precentage error of random forest regression model on test data.

![error of rf](http://d.pr/i/ifNDHs+)

For neural network, relu is used as activation function. The neural network has two hidden layers. Each hidden layer has 100 neurons. The input layer has 5 attributes: Income, Unemployment, Education, Poverty and Law, while the output is Fire Rate. The following figure shows precentage error of nueral network regression model on test data.

![error of nn](http://d.pr/i/zouIHz+)

We conducted 10-fold cross validation on the two models by measuring the mean absolute error. The two models have similar errors. Random forest and Neural Network have mean absolute error of 0.0488  and 0.0425, respectively. This is about 5% error or about 95% accuracy on average. The following figure shows PDF of errors.

![error pdf](http://d.pr/i/HT9EVF+)

### Analysis of Law Effectiveness by Selecting Neighbors 

   We apply k-means clustering method and k-NN to find similar counties. For example, Monroe county, NY is selected and the nearest 250 neighbors of Monroe county is found. Using this method, we assume that we obtained 250 similar data points with respective to Income, Unemployment, Education, and Poverty.  
   
 
With 250 similar data points in Income, Unemployment rate, Education, and Poverty, we move to the stage of exploring the relation between law and firearm death rate. The results are shown in figure 12. As we can see, the curved score for laws and firearm death rate have negative correlation with correlation coefficient about -0.27. The pink line shows linear regression results. It should be noted that linear regression doesn’t accurately capture the relation between the two. Thus, at this stage, we would like to leave the regression for future improvement and just focusing the observation of the data. Based on our observation, we found that if we choose a column of the data point with same score of law, for example, 0.1, normalized firearm death rate is ranging from 0 to 0.3. It indicates two possibilities: First one is there still other factors that we failed to consider that affect the firearm death rate. Second one is that effect of law is not significant. Both of the possibilities are worth further studying in the future.

The following figure shows PCA and k-means results.


![kmeans](http://d.pr/i/LCW49A+)


### Analysis of Law Effectiveness by Regression Models
The regression models can be used to predict the effects of gun control laws. We use the real data for Income, Unemployment, Education, Poverty of each county and vary the curved score for law from 0  to 1 to predict the firearm death rate. Then we calculate the mean of firearm death rate for all available counties. The results are shown in Figure 13. By increasing the curved score for laws from 0 to 1, the average firearm death rate can be lowered about 60%. The two models have almost the same results. This is not surprising, since the prediction is an average of about 1500 counties. 


![kmeans](http://d.pr/i/HCYNNb+)