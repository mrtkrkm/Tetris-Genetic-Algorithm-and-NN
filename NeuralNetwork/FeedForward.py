import numpy as np



class NN(object):
    def __init__(self, input_number, hidden_number, hidden1_number, output1_number, output2_number):
        self.input_number = input_number
        self.hidden_number = hidden_number
        self.hidden1_number = hidden1_number
        self.output1_number = output1_number
        self.output2_number = output2_number

    def extract_weights(self,chromosome):
        W1_m=(self.hidden_number,self.input_number)
        W1_m = (self.hidden1_number, self.hidden_number)
        W2_1_m=(self.output1_number,self.hidden_number)
        W3_1_m=(self.output2_number,self.hidden_number)

        W1_end=self.hidden_number*self.input_number
        W2_end = W1_end+(self.hidden1_number*self.hidden_number)
        W2_Rot_end=W2_end+(self.output1_number*self.hidden_number)
        W2_X_end=W2_Rot_end+(self.output2_number*self.hidden_number)

        W1=chromosome[:W1_end]
        W2=chromosome[W1_end:W2_end]
        W2_Rot=chromosome[W2_end:W2_Rot_end]
        W2_X=chromosome[W2_Rot_end:W2_X_end]

        return W1.reshape(self.hidden_number,self.input_number), W2.reshape(self.hidden1_number, self.hidden_number), W2_Rot.reshape(self.output1_number, self.hidden_number), \
               W2_X.reshape(self.output2_number, self.hidden_number)

    def sigmoid(self,z):
        return 1/(1+np.exp(-z))

    def softmax(self,z):
        return np.exp(z.T) / np.sum(np.exp(z.T), axis=1).reshape(-1, 1)

    def forward(self,chromosome, input):
        W1, W2, W2_rot, W2_X=self.extract_weights(chromosome)

        Z=np.matmul(W1,input.T)
        A=self.sigmoid(Z)
        Z2=np.matmul(W2,A)
        A2=self.sigmoid(Z2)
        Rot_Z=np.matmul(W2_rot, A2)
        Rot_A=self.sigmoid(Rot_Z)
        Rot=self.softmax(Rot_A)
        X_Z=np.matmul(W2_X, A)
        X_A=self.sigmoid(X_Z)
        X=self.softmax(X_A)

        return Rot, X
