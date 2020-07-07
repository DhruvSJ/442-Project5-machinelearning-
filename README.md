# 442 Project5 Machine Learning
This project will be an introduction to machine learning to build a neural network to classify digits, and more!

Installation
For this project, you will need to install the following two libraries:

numpy, which provides support for large multi-dimensional arrays 
matplotlib, a 2D plotting library 

To test that everything has been installed, run:

python autograder.py --check-dependencies

If numpy and matplotlib are installed correctly, you should see a window pop up where a line segment spins in a circle:

Question 1 (6 points): Perceptron
Before starting this part, be sure you have numpy and matplotlib installed!

In this part, you will implement a binary perceptron. Your task will be to complete the implementation of the PerceptronModel class in models.py.

For the perceptron, the output labels will be either 
1
 or 
−
1
, meaning that data points (x, y) from the dataset will have y be a nn.Constant node that contains either 
1
 or 
−
1
 as its entries.

We have already initialized the perceptron weights self.w to be a 
1
×
dimensions
 parameter node. The provided code will include a bias feature inside x when needed, so you will not need a separate parameter for the bias.

Your tasks are to:

Implement the run(self, x) method. This should compute the dot product of the stored weight vector and the given input, returning an nn.DotProduct object.
Implement get_prediction(self, x), which should return 
1
 if the dot product is non-negative or 
−
1
 otherwise. You should use nn.as_scalar to convert a scalar Node into a Python floating-point number.
Write the train(self) method. This should repeatedly loop over the data set and make updates on examples that are misclassified. Use the update method of the nn.Parameter class to update the weights. When an entire pass over the data set is completed without making any mistakes, 100% training accuracy has been achieved, and training can terminate.
In this project, the only way to change the value of a parameter is by calling parameter.update(direction, multiplier), which will perform the update to the weights:
weights
←
weights
+
direction
⋅
multiplier
The direction argument is a Node with the same shape as the parameter, and the multiplier argument is a Python scalar.

To test your implementation, run the autograder:

python autograder.py -q q1
