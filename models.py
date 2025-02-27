import nn

class PerceptronModel(object):
    def __init__(self, dimensions):
        """
        Initialize a new Perceptron instance.

        A perceptron classifies data points as either belonging to a particular
        class (+1) or not (-1). `dimensions` is the dimensionality of the data.
        For example, dimensions=2 would mean that the perceptron must classify
        2D points.
        """
        self.w = nn.Parameter(1, dimensions)

    def get_weights(self):
        """
        Return a Parameter instance with the current weights of the perceptron.
        """
        return self.w

    def run(self, x):
        """
        Calculates the score assigned by the perceptron to a data point x.

        Inputs:
            x: a node with shape (1 x dimensions)
        Returns: a node containing a single number (the score)
        """
        "*** YOUR CODE HERE ***"
        retVal = nn.DotProduct(self.w ,x)

        return retVal

    def get_prediction(self, x):
        """
        Calculates the predicted class for a single data point `x`.

        Returns: 1 or -1
        """
        "*** YOUR CODE HERE ***"
        
        if (nn.as_scalar(self.run(x))) >= 0:
            return 1
        
        return -1

    def train(self, dataset):
        """
        Train the perceptron until convergence.
        """
        "*** YOUR CODE HERE ***"
         
        while True:
            val = True
            for x,y in dataset.iterate_once(1):
                if nn.as_scalar(y) == self.get_prediction(x):
                    continue
                else:
                    val = False
                    nn.Parameter.update(self.w,x,nn.as_scalar(y))

            if val:
                break
            
            
            
            
class RegressionModel(object):
    """
    A neural network model for approximating a function that maps from real
    numbers to real numbers. The network should be sufficiently large to be able
    to approximate sin(x) on the interval [-2pi, 2pi] to reasonable precision.
    """
    def __init__(self):
        # Initialize your model parameters here
        "*** YOUR CODE HERE ***"
        self.batch_size = 200
        self.w1 = nn.Parameter(1, 150)
        self.w2 = nn.Parameter(150, 1)
        self.b1 = nn.Parameter(1,150)
        self.b2 = nn.Parameter(1, 1)
        

    def run(self, x):
        """
        Runs the model for a batch of examples.

        Inputs:
            x: a node with shape (batch_size x 1)
        Returns:
            A node with shape (batch_size x 1) containing predicted y-values
        """
        "*** YOUR CODE HERE ***"
        b_0 = self.b1
        b_1 = self.b2
        w_0 = self.w1
        w_1 = self.w2
        xw1 = nn.Linear(x, w_0)
        r1 = nn.ReLU(nn.AddBias(xw1, b_0))

        xw2 = nn.Linear(r1, w_1)
        val = nn.AddBias(xw2,b_1)

        return val

    def get_loss(self, x, y):
        """
        Computes the loss for a batch of examples.

        Inputs:
            x: a node with shape (batch_size x 1)
            y: a node with shape (batch_size x 1), containing the true y-values
                to be used for training
        Returns: a loss node
        """
        "*** YOUR CODE HERE ***"
        predict = self.run(x)
        retVal = nn.SquareLoss(predict, y)
        return retVal
        

    def train(self, dataset):
        """
        Trains the model.
        """
        "*** YOUR CODE HERE ***"
        loss = 1e10
        
        while loss > .02:
            for x, y in dataset.iterate_once(self.batch_size):
                n_loss = self.get_loss(x,y)
                grad_w1, grad_b1, grad_w2, grad_b2 = nn.gradients(n_loss, [self.w1, self.b1, self.w2, self.b2])
                self.w1.update(grad_w1, -0.005)
                self.b1.update(grad_b1, -0.005)
                self.w2.update(grad_w2, -0.005)
                self.b2.update(grad_b2, -0.005)
                new_loss = self.get_loss(x,y)
                loss = nn.as_scalar(new_loss)
                


class DigitClassificationModel(object):
    """
    A model for handwritten digit classification using the MNIST dataset.

    Each handwritten digit is a 28x28 pixel grayscale image, which is flattened
    into a 784-dimensional vector for the purposes of this model. Each entry in
    the vector is a floating point number between 0 and 1.

    The goal is to sort each digit into one of 10 classes (number 0 through 9).

    (See RegressionModel for more information about the APIs of different
    methods here. We recommend that you implement the RegressionModel before
    working on this part of the project.)
    """
    def __init__(self):
        # Initialize your model parameters here
        "*** YOUR CODE HERE ***"
        self.batch_size = 1
        self.w1 = nn.Parameter(784, 500)
        self.b1 = nn.Parameter(1, 500)
        self.w2 = nn.Parameter(500, 10)
        self.b2 = nn.Parameter(1, 10)

    def run(self, x):
        """
        Runs the model for a batch of examples.

        Your model should predict a node with shape (batch_size x 10),
        containing scores. Higher scores correspond to greater probability of
        the image belonging to a particular class.

        Inputs:
            x: a node with shape (batch_size x 784)
        Output:
            A node with shape (batch_size x 10) containing predicted scores
                (also called logits)
        """
        "*** YOUR CODE HERE ***"
        b_0 = self.b1
        b_1 = self.b2
        w_0 = self.w1
        w_1 = self.w2
        xw1 = nn.Linear(x, w_0)
        r1 = nn.ReLU(nn.AddBias(xw1, b_0))

        xw2 = nn.Linear(r1, w_1)
        val = nn.AddBias(xw2,b_1)

        return val
    
    def get_loss(self, x, y):
        """
        Computes the loss for a batch of examples.

        The correct labels `y` are represented as a node with shape
        (batch_size x 10). Each row is a one-hot vector encoding the correct
        digit class (0-9).

        Inputs:
            x: a node with shape (batch_size x 784)
            y: a node with shape (batch_size x 10)
        Returns: a loss node
        """
        "*** YOUR CODE HERE ***"
        x = self.run(x)
        val = nn.SoftmaxLoss(x, y)

        return val
        

    def train(self, dataset):
        """
        Trains the model.
        """
        "*** YOUR CODE HERE ***"
        loss = 1e10
        
        while loss > .02:
            for x, y in dataset.iterate_once(self.batch_size):
                n_loss = self.get_loss(x,y)
                grad_w1, grad_b1, grad_w2, grad_b2 = nn.gradients(n_loss, [self.w1, self.b1, self.w2, self.b2])
                self.w1.update(grad_w1, -0.002)
                self.b1.update(grad_b1, -0.002)
                self.w2.update(grad_w2, -0.002)
                self.b2.update(grad_b2, -0.002)
                new_loss = self.get_loss(x,y)
                loss = nn.as_scalar(new_loss)
        

class LanguageIDModel(object):
    """
    A model for language identification at a single-word granularity.

    (See RegressionModel for more information about the APIs of different
    methods here. We recommend that you implement the RegressionModel before
    working on this part of the project.)
    """
    def __init__(self):
        # Our dataset contains words from five different languages, and the
        # combined alphabets of the five languages contain a total of 47 unique
        # characters.
        # You can refer to self.num_chars or len(self.languages) in your code
        self.num_chars = 47
        self.languages = ["English", "Spanish", "Finnish", "Dutch", "Polish"]

        # Initialize your model parameters here
        "*** YOUR CODE HERE ***"
        self.batch_size = 1
        self.w1 = nn.Parameter(47, 200)
        self.w2 = nn.Parameter(200, 100)
        self.w3 = nn.Parameter(100, 10)
        self.w4 = nn.Parameter(10, 200)
        self.w5 = nn.Parameter(10,20)
        self.w6 = nn.Parameter(20,5)
        
        self.b1 = nn.Parameter(1,200)
        self.b2 = nn.Parameter(1, 100)
        self.b3 = nn.Parameter(1,10)
        self.b4 = nn.Parameter(1,40)
        self.b5 = nn.Parameter(1,20)
        self.b6 = nn.Parameter(1,5)

    def run(self, xs):
        """
        Runs the model for a batch of examples.

        Although words have different lengths, our data processing guarantees
        that within a single batch, all words will be of the same length (L).

        Here `xs` will be a list of length L. Each element of `xs` will be a
        node with shape (batch_size x self.num_chars), where every row in the
        array is a one-hot vector encoding of a character. For example, if we
        have a batch of 8 three-letter words where the last word is "cat", then
        xs[1] will be a node that contains a 1 at position (7, 0). Here the
        index 7 reflects the fact that "cat" is the last word in the batch, and
        the index 0 reflects the fact that the letter "a" is the inital (0th)
        letter of our combined alphabet for this task.

        Your model should use a Recurrent Neural Network to summarize the list
        `xs` into a single node of shape (batch_size x hidden_size), for your
        choice of hidden_size. It should then calculate a node of shape
        (batch_size x 5) containing scores, where higher scores correspond to
        greater probability of the word originating from a particular language.

        Inputs:
            xs: a list with L elements (one per character), where each element
                is a node with shape (batch_size x self.num_chars)
        Returns:
            A node with shape (batch_size x 5) containing predicted scores
                (also called logits)
        """
        "*** YOUR CODE HERE ***"
        w1x = nn.Linear(xs[0],self.w1)
        w1x_b1 = nn.AddBias(w1x,self.b1)
        relu = nn.ReLU(w1x_b1)
        w2x = nn.Linear(relu,self.w2)
        fl_x = nn.AddBias(w2x,self.b2)
        relu2 = nn.ReLU(fl_x)
        w3x = nn.Linear(relu2,self.w3)
        h1 = nn.AddBias(w3x, self.b3)

        for i in range(1,len(xs)):
            w1x = nn.Add(nn.Linear(xs[i],self.w1), nn.Linear(h1,self.w4))
            w1x_b1 = nn.AddBias(w1x,self.b1)
            relu = nn.ReLU(w1x_b1)
            w2x = nn.Linear(relu,self.w2)
            fl_x = nn.AddBias(w2x,self.b2)
            relu2 = nn.ReLU(fl_x)
            w3x = nn.Linear(relu2,self.w3)
            h1 = nn.AddBias(w3x, self.b3)
        return nn.AddBias(nn.Linear(nn.ReLU(nn.AddBias(nn.Linear(h1,self.w5),self.b5)),self.w6),self.b6)
        

    def get_loss(self, xs, y):
        """
        Computes the loss for a batch of examples.

        The correct labels `y` are represented as a node with shape
        (batch_size x 5). Each row is a one-hot vector encoding the correct
        language.

        Inputs:
            xs: a list with L elements (one per character), where each element
                is a node with shape (batch_size x self.num_chars)
            y: a node with shape (batch_size x 5)
        Returns: a loss node
        """
        "*** YOUR CODE HERE ***"
        predict = self.run(xs)
        val = nn.SoftmaxLoss(predict,y)
        return val 

    def train(self, dataset):
        """
        Trains the model.
        """
        "*** YOUR CODE HERE ***"
        
        while dataset.get_validation_accuracy() < .9:
            for x, y in dataset.iterate_once(self.batch_size):
                loss = self.get_loss(x,y)
                grad_w1, grad_b1, grad_w2, grad_b2, grad_w3, grad_b3, grad_w4, grad_w5, grad_b5, grad_w6, grad_b6 = nn.gradients(loss, [self.w1, self.b1, self.w2, self.b2, self.w3, self.b3, self.w4, self. w5, self.b5, self.w6, self.b6])
                self.w1.update(grad_w1, -0.002)
                self.w2.update(grad_w2, -0.002)
                self.w3.update(grad_w3, -0.002)
                self.w4.update(grad_w4, -0.002)
                self.w5.update(grad_w5, -0.002)
                self.w6.update(grad_w6, -0.002)
                self.b1.update(grad_b1, -0.002)
                self.b2.update(grad_b2, -0.002)
                self.b3.update(grad_b3, -0.002)
                self.b5.update(grad_b5, -0.002)
                self.b6.update(grad_b6, -0.002)
                nloss = self.get_loss(x,y)
                losss = nn.as_scalar(nloss)
