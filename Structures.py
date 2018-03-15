import numpy
from keras.models import Sequential, Model
from keras.layers import Dense, RepeatVector, Activation,Convolution2D
from keras.layers import TimeDistributed,MaxPooling2D, Flatten, Input, Permute
from keras.layers import Dropout, merge, Lambda
from keras.layers import LSTM
from keras.callbacks import ModelCheckpoint
from keras.utils import np_utils
from keras.optimizers import RMSprop
from keras.layers.convolutional import Conv1D
from keras.layers.convolutional import MaxPooling1D
from keras.regularizers import l2
from keras.callbacks import *
# from visualizer import *
from keras.models import *
from keras.optimizers import *
from keras.utils.np_utils import to_categorical
from keras.layers.core import *
from keras.layers import Input, Embedding, LSTM, Dense, merge, TimeDistributed
import theano
    

    
class Structures:

   
    def __init__(self, CONTEXT_LENGTH,embedding_size, Labs, NEURONS):
            self.model = Sequential()
            self.CONTEXT_LENGTH = CONTEXT_LENGTH
            self.NEURONS = NEURONS
            self.embedding_size = embedding_size
            self.Labels_one_hot_len = Labs
    
    #For attention model

    def get_H_n(self,X):
        ans = X[:, -1, :]  # get last element from time dim
        return ans


    def get_Y(self,X, xmaxlen):
        return X[:, :xmaxlen, :]  # get first xmaxlen elem from time dim


    def get_R(self,X):
        Y, alpha = X[0], X[1]
        ans = K.T.batched_dot(Y, alpha)
        return ans
    

    
   
    def structure_11_simple_attention_dot(self):
        #keras.layers.merge.Dot(axes, normalize=False)
        L = self.CONTEXT_LENGTH
        NEURONS = self.NEURONS
        encoding_input = Input(shape=(L,self.embedding_size))
        drop_out = Dropout(0.1, name='dropout')(encoding_input)
        lstm_fwd = LSTM(NEURONS, return_sequences=True, name='lstm_fwd')(drop_out)
        lstm_bwd = LSTM(NEURONS, return_sequences=True, go_backwards=True, name='lstm_bwd')(drop_out)
        bilstm = merge([lstm_fwd, lstm_bwd], name='bilstm', mode='concat')
        drop_out = Dropout(0.1)(bilstm)
        #
        # compute importance for each step
        attention = Dense(1, activation='tanh')(drop_out)
        attention = Flatten()(attention)
        attention = Activation('softmax')(attention)
        #attention = RepeatVector(NEURONS*2)(attention) #bidirectional attention model
        #attention = Permute([2, 1])(attention)#what is this step doing?
        sent_representation = merge([attention,drop_out], dot_axes=1, mode='dot')
        #sent_representation = Lambda(lambda xin: K.sum(xin, axis=-2), output_shape=(NEURONS*2,))(sent_representation)
        out_relu =  Dense(NEURONS, activation = "relu")(sent_representation)
        out = Dense(self.Labels_one_hot_len, activation='softmax')(out_relu)
        output = out
        model = Model(input=[encoding_input], output=output)
        return model
    
        
    
   
    def structure_11_cnn_attention_dot(self):
        #keras.layers.merge.Dot(axes, normalize=False)
        L = self.CONTEXT_LENGTH
        NEURONS = self.NEURONS
        encoding_input = Input(shape=(L,self.embedding_size))
        drop_out = Dropout(0.1, name='dropout')(encoding_input)
        modconv = Conv1D(filters=32, kernel_size=3, padding='same', activation='relu')(drop_out)
        maxp = MaxPooling1D(pool_size=2)(modconv)
        lstm_fwd = LSTM(NEURONS, return_sequences=True, name='lstm_fwd')(modconv)
        lstm_bwd = LSTM(NEURONS, return_sequences=True, go_backwards=True, name='lstm_bwd')(modconv)
        bilstm = merge([lstm_fwd, lstm_bwd], name='bilstm', mode='concat')
        drop_out = Dropout(0.1)(bilstm)
        #
        # compute importance for each step
        attention = Dense(1, activation='tanh')(drop_out)
        attention = Flatten()(attention)
        attention = Activation('softmax')(attention)
        #attention = RepeatVector(NEURONS*2)(attention) #bidirectional attention model
        #attention = Permute([2, 1])(attention)#what is this step doing?
        sent_representation = merge([attention,drop_out], dot_axes=1, mode='dot')
        #sent_representation = Lambda(lambda xin: K.sum(xin, axis=-2), output_shape=(NEURONS*2,))(sent_representation)
        out_relu =  Dense(NEURONS, activation = "relu")(sent_representation)
        out = Dense(self.Labels_one_hot_len, activation='softmax')(out_relu)
        output = out
        model = Model(input=[encoding_input], output=output)
        return model
    
        
       
    
    
    
    def structrue_11_simple_attention(self):
        L = self.CONTEXT_LENGTH
        NEURONS = self.NEURONS
        encoding_input = Input(shape=(L,self.embedding_size))
        drop_out = Dropout(0.1, name='dropout')(encoding_input)
        lstm_fwd = LSTM(NEURONS, return_sequences=True, name='lstm_fwd')(drop_out)
        lstm_bwd = LSTM(NEURONS, return_sequences=True, go_backwards=True, name='lstm_bwd')(drop_out)
        bilstm = merge([lstm_fwd, lstm_bwd], name='bilstm', mode='concat')
        drop_out = Dropout(0.1)(bilstm)
    
        # compute importance for each step
        attention = Dense(1, activation='tanh')(drop_out)
        attention = Flatten()(attention)
        attention = Activation('softmax')(attention)
        attention = RepeatVector(NEURONS*2)(attention) #bidirectional attention model
        attention = Permute([2, 1])(attention)#what is this step doing?
        sent_representation = merge([drop_out, attention], mode='mul')
        sent_representation = Lambda(lambda xin: K.sum(xin, axis=-2), output_shape=(NEURONS*2,))(sent_representation)

        out = Dense(self.Labels_one_hot_len, activation='softmax')(sent_representation)
        output = out
        model = Model(input=[encoding_input], output=output)
        return model
    
    


    #simple bidirectional model.    
    def structrue_11_no_attention(self):
        L = self.CONTEXT_LENGTH
        NEURONS = self.NEURONS
        encoding_input = Input(shape=(L,self.embedding_size))
        drop_out = Dropout(0.1, name='dropout')(encoding_input)
        lstm_fwd = LSTM(NEURONS, return_sequences=True, name='lstm_fwd')(drop_out)
        lstm_bwd = LSTM(NEURONS, return_sequences=True, go_backwards=True, name='lstm_bwd')(drop_out)
        bilstm = merge([lstm_fwd, lstm_bwd], name='bilstm', mode='concat')
        drop_out = Dropout(0.1)(bilstm)

        encoded_text2 = Flatten()(drop_out)

        out = Dense(self.Labels_one_hot_len, activation='softmax')(encoded_text2)
        output = out
        model = Model(input=[encoding_input], output=output)
        return model
    
    
    
    def structrue_11_simple_attention_topic(self, topic):
        L = self.CONTEXT_LENGTH
        NEURONS = self.NEURONS
        encoding_input = Input(shape=(L,self.embedding_size))
        drop_out = Dropout(0.1, name='dropout')(encoding_input)
        lstm_fwd = LSTM(NEURONS, return_sequences=True, name='lstm_fwd')(drop_out)
        lstm_bwd = LSTM(NEURONS, return_sequences=True, go_backwards=True, name='lstm_bwd')(drop_out)
        bilstm = merge([lstm_fwd, lstm_bwd], name='bilstm', mode='concat')
        drop_out = Dropout(0.1)(bilstm)

        topic_input = Input(shape=(topic,))
        attention_topic = Dense(1, activation='tanh')(topic_input)
        attention_topic =  RepeatVector(L)(attention_topic) #bidirectional attention model
        attention_topic = Flatten()(attention_topic)



        # compute importance for each step
        attention = Dense(1, activation='tanh')(drop_out)
        attention = Flatten()(attention)

        attention = merge([attention,attention_topic], mode="mul")


        attention = Activation('softmax')(attention)
        attention = RepeatVector(NEURONS*2)(attention) #bidirectional attention model
        attention = Permute([2, 1])(attention)#what is this step doing?
        sent_representation = merge([drop_out, attention], mode='mul')
        sent_representation = Lambda(lambda xin: K.sum(xin, axis=-2), output_shape=(NEURONS*2,))(sent_representation)

        out = Dense(self.Labels_one_hot_len, activation='softmax')(sent_representation)
        #out2 = Dense(expected_length, activation='softmax')(sent_representation)
        #output = [out,out2]
        model = Model(input=[encoding_input,topic_input], output=out)

        return model    


    def structrue_11_simple_attention_topic_2(self, topic):
        L = self.CONTEXT_LENGTH
        NEURONS = self.NEURONS
        encoding_input = Input(shape=(L,self.embedding_size))
        drop_out = Dropout(0.1, name='dropout')(encoding_input)
        lstm_fwd = LSTM(NEURONS, return_sequences=True, name='lstm_fwd')(drop_out)
        lstm_bwd = LSTM(NEURONS, return_sequences=True, go_backwards=True, name='lstm_bwd')(drop_out)
        bilstm = merge([lstm_fwd, lstm_bwd], name='bilstm', mode='concat')
        drop_out = Dropout(0.1)(bilstm)
        
        topic_input = Input(shape=(topic,))
        attention_topic = Dense(NEURONS, activation='linear')(topic_input)
        attention_topic =  RepeatVector(L)(attention_topic) #bidirectional attention model
        #attention_topic = Flatten()(attention_topic)
        
        
        # compute importance for each step
        attention = Dense(NEURONS, activation='linear')(drop_out)
        #attention = Flatten()(attention)
        
        attention = merge([attention,attention_topic], mode="sum")
        
        
        attention = Dense(1, activation='tanh')(attention) # sequence + topic
        attention = Flatten()(attention)
        
        attention = Activation('softmax')(attention)
        attention = RepeatVector(NEURONS*2)(attention) #bidirectional attention model
        attention = Permute([2, 1])(attention)#what is this step doing?
        sent_representation = merge([drop_out, attention], mode='mul')
        sent_representation = Lambda(lambda xin: K.sum(xin, axis=-2), output_shape=(NEURONS*2,))(sent_representation)
        out = Dense(self.Labels_one_hot_len, activation='softmax')(sent_representation)
        #out2 = Dense(expected_length, activation='softmax')(sent_representation)
        #output = [out,out2]
        model = Model(input=[encoding_input,topic_input], output=out)
        
        return model  
    
    #this outputs topics -> for the next publication.
    def structrue_11_simple_attention_double(self):
        L = self.CONTEXT_LENGTH
        NEURONS = self.NEURONS
        encoding_input = Input(shape=(L,self.embedding_size))
        drop_out = Dropout(0.1, name='dropout')(encoding_input)
        lstm_fwd = LSTM(NEURONS, return_sequences=True, name='lstm_fwd')(drop_out)
        lstm_bwd = LSTM(NEURONS, return_sequences=True, go_backwards=True, name='lstm_bwd')(drop_out)
        bilstm = merge([lstm_fwd, lstm_bwd], name='bilstm', mode='concat')
        drop_out = Dropout(0.1)(bilstm)
    
        # compute importance for each step
        attention = Dense(1, activation='tanh')(drop_out)
        attention = Flatten()(attention)
        attention = Activation('softmax')(attention)
        attention = RepeatVector(NEURONS*2)(attention) #bidirectional attention model
        attention = Permute([2, 1])(attention)#what is this step doing?
        sent_representation = merge([drop_out, attention], mode='mul')
        sent_representation = Lambda(lambda xin: K.sum(xin, axis=-2), output_shape=(NEURONS*2,))(sent_representation)

        out = Dense(self.Labels_one_hot_len, activation='softmax')(sent_representation)
        out2 = Dense(self.ONE_HOT_LEN, activation='softmax')(sent_representation)
        output = [out,out2]
        model = Model(input=[encoding_input], output=output)
        return model
    
    
    
    def structure_11(self):
        k = 256
        L = self.CONTEXT_LENGTH
        encoding_input = Input(shape=(self.CONTEXT_LENGTH-1,self.embedding_size))
        drop_out = Dropout(0.1, name='dropout')(encoding_input)
        lstm_fwd = LSTM(128, return_sequences=True, name='lstm_fwd')(drop_out)
        lstm_bwd = LSTM(128, return_sequences=True, go_backwards=True, name='lstm_bwd')(drop_out)
        bilstm = merge([lstm_fwd, lstm_bwd], name='bilstm', mode='concat')
        drop_out = Dropout(0.1)(bilstm)
        h_n = Lambda(self.get_H_n, output_shape=(k,), name="h_n")(drop_out)
        Y = Lambda(self.get_Y, arguments={"xmaxlen": L}, name="Y", output_shape=(L, k))(drop_out)
        Whn = Dense(k, W_regularizer=l2(0.01), name="Wh_n")(h_n)
        Whn_x_e = RepeatVector(L, name="Wh_n_x_e")(Whn)
        WY = TimeDistributed(Dense(k, W_regularizer=l2(0.01)), name="WY")(Y)
        merged = merge([Whn_x_e, WY], name="merged", mode='sum')
        M = Activation('tanh', name="M")(merged)

        alpha_ = TimeDistributed(Dense(1, activation='linear'), name="alpha_")(M)
        flat_alpha = Flatten(name="flat_alpha")(alpha_)
        alpha = Dense(L, activation='softmax', name="alpha")(flat_alpha)

        Y_trans = Permute((2, 1), name="y_trans")(Y)  # of shape (None,300,20)

        r_ = merge([Y_trans, alpha], output_shape=(k, 1), name="r_", mode=self.get_R)

        r = Reshape((k,), name="r")(r_)

        Wr = Dense(k, W_regularizer=l2(0.01))(r)
        Wh = Dense(k, W_regularizer=l2(0.01))(h_n)
        merged = merge([Wr, Wh], mode='sum')
        h_star = Activation('tanh')(merged)
        #out = Dense(ONE_HOT_LEN, activation='softmax')(h_star)
        out = Dense(self.Labels_one_hot_len, activation='softmax')(h_star)

        output = out
        model = Model(input=[encoding_input], output=output)
        return model

    
    def structure_11_double(self, Neurons):
        k = Neurons*2
        L = self.CONTEXT_LENGTH-1
        encoding_input = Input(shape=(self.CONTEXT_LENGTH-1,self.embedding_size))
        drop_out = Dropout(0.1, name='dropout')(encoding_input)
        lstm_fwd = LSTM(Neurons, return_sequences=True, name='lstm_fwd')(drop_out)
        lstm_bwd = LSTM(Neurons, return_sequences=True, go_backwards=True, name='lstm_bwd')(drop_out)
        bilstm = merge([lstm_fwd, lstm_bwd], name='bilstm', mode='concat')
        drop_out = Dropout(0.1)(bilstm)
        h_n = Lambda(self.get_H_n, output_shape=(k,), name="h_n")(drop_out)
        Y = Lambda(self.get_Y, arguments={"xmaxlen": L}, name="Y", output_shape=(L, k))(drop_out)
        Whn = Dense(k, W_regularizer=l2(0.01), name="Wh_n")(h_n)
        Whn_x_e = RepeatVector(L, name="Wh_n_x_e")(Whn)
        WY = TimeDistributed(Dense(k, W_regularizer=l2(0.01)), name="WY")(Y)
        merged = merge([Whn_x_e, WY], name="merged", mode='sum')
        M = Activation('tanh', name="M")(merged)

        alpha_ = TimeDistributed(Dense(1, activation='linear'), name="alpha_")(M)
        flat_alpha = Flatten(name="flat_alpha")(alpha_)
        alpha = Dense(L, activation='softmax', name="alpha")(flat_alpha)

        Y_trans = Permute((2, 1), name="y_trans")(Y)  # of shape (None,300,20)

        r_ = merge([Y_trans, alpha], output_shape=(k, 1), name="r_", mode=self.get_R)

        r = Reshape((k,), name="r")(r_)

        Wr = Dense(k, W_regularizer=l2(0.01))(r)
        Wh = Dense(k, W_regularizer=l2(0.01))(h_n)
        merged = merge([Wr, Wh], mode='sum')
        h_star = Activation('tanh')(merged)
        #
        out = Dense(self.Labels_one_hot_len, activation='softmax')(h_star)
        out2 = Dense(self.ONE_HOT_LEN, activation='softmax')(h_star)
       
        output = [out,out2]
        model = Model(input=[encoding_input], output=output)
        return model


    
    
    def structure_13(self):

        context_model = Sequential()
        context_model.add(Convolution2D(32, 2, 2, activation='relu', border_mode='same', input_shape=(1, self.CONTEXT_LENGTH-1, self.CONTEXT_LENGTH-1)))
        context_model.add(MaxPooling2D((2, 2)))
        context_model.add(Convolution2D(32, 2, 2, activation='relu', border_mode='same'))
        context_model.add(Convolution2D(32, 2, 2, activation='relu'))
        context_model.add(MaxPooling2D((2, 2)))
        context_model.add(Flatten())

        # now let's get a tensor with the output of our vision model:
        image_input = Input(shape=(1, self.CONTEXT_LENGTH-1, self.CONTEXT_LENGTH-1))
        encoded_context = context_model(image_input)

        k = 256
        L = self.CONTEXT_LENGTH-1
        encoding_input = Input(shape=(self.CONTEXT_LENGTH-1,self.embedding_size))
        drop_out = Dropout(0.1, name='dropout')(encoding_input)
        lstm_fwd = LSTM(128, return_sequences=True, name='lstm_fwd')(drop_out)
        lstm_bwd = LSTM(128, return_sequences=True, go_backwards=True, name='lstm_bwd')(drop_out)
        bilstm = merge([lstm_fwd, lstm_bwd], name='bilstm', mode='concat')
        drop_out = Dropout(0.1)(bilstm)
        h_n = Lambda(self.get_H_n, output_shape=(k,), name="h_n")(drop_out)
        Y = Lambda(self.get_Y, arguments={"xmaxlen": L}, name="Y", output_shape=(L, k))(drop_out)
        Whn = Dense(k, W_regularizer=l2(0.01), name="Wh_n")(h_n)
        Whn_x_e = RepeatVector(L, name="Wh_n_x_e")(Whn)
        WY = TimeDistributed(Dense(k, W_regularizer=l2(0.01)), name="WY")(Y)
        merged = merge([Whn_x_e, WY], name="merged", mode='sum')
        M = Activation('tanh', name="M")(merged)

        alpha_ = TimeDistributed(Dense(1, activation='linear'), name="alpha_")(M)
        flat_alpha = Flatten(name="flat_alpha")(alpha_)

        flat_beta  = merge([flat_alpha, encoded_context], name='m2', mode='concat')

        alpha = Dense(L, activation='softmax', name="alpha")(flat_beta)

        Y_trans = Permute((2, 1), name="y_trans")(Y)  # of shape (None,300,20)

        r_ = merge([Y_trans, alpha], output_shape=(k, 1), name="r_", mode=self.get_R)

        r = Reshape((k,), name="r")(r_)

        Wr = Dense(k, W_regularizer=l2(0.01))(r)
        Wh = Dense(k, W_regularizer=l2(0.01))(h_n)
        merged = merge([Wr, Wh], mode='sum')
        h_star = Activation('tanh')(merged)


        #out = Dense(ONE_HOT_LEN, activation='softmax')(h_star)
        #variation below
        out = Dense(self.Labels_one_hot_len, activation='softmax')(h_star)

        output = out
        self.model = Model(input=[encoding_input,image_input], output=output)
        return self.model   
    
    
    
   
    def structure_14(self):

        context_model = Sequential()
        context_model.add(Convolution2D(32, 2, 2, activation='relu', border_mode='same', input_shape=(1, 13, 13)))
        context_model.add(MaxPooling2D((2, 2)))
        context_model.add(Convolution2D(32, 2, 2, activation='relu', border_mode='same'))
        context_model.add(Convolution2D(32, 2, 2, activation='relu'))
        context_model.add(MaxPooling2D((2, 2)))
        context_model.add(Flatten())

        # now let's get a tensor with the output of our vision model:
        image_input = Input(shape=(1, self.CONTEXT_LENGTH-1, self.CONTEXT_LENGTH-1))
        encoded_context = context_model(image_input)
        repeated_context = RepeatVector(self.CONTEXT_LENGTH-1)(encoded_context)


        k = 256
        L = self.CONTEXT_LENGTH-1
        encoding_input = Input(shape=(self.CONTEXT_LENGTH-1,self.embedding_size))
        drop_out = Dropout(0.1, name='dropout')(encoding_input)



        flat_beta  = merge([drop_out, repeated_context], name='m2', mode='concat')


        lstm_fwd = LSTM(128, return_sequences=True, name='lstm_fwd')(flat_beta)
        lstm_bwd = LSTM(128, return_sequences=True, go_backwards=True, name='lstm_bwd')(flat_beta)
        bilstm = merge([lstm_fwd, lstm_bwd], name='bilstm', mode='concat')
        drop_out = Dropout(0.1)(bilstm)
        h_n = Lambda(self.get_H_n, output_shape=(k,), name="h_n")(drop_out)
        Y = Lambda(self.get_Y, arguments={"xmaxlen": L}, name="Y", output_shape=(L, k))(drop_out)
        Whn = Dense(k, W_regularizer=l2(0.01), name="Wh_n")(h_n)
        Whn_x_e = RepeatVector(L, name="Wh_n_x_e")(Whn)
        WY = TimeDistributed(Dense(k, W_regularizer=l2(0.01)), name="WY")(Y)
        merged = merge([Whn_x_e, WY], name="merged", mode='sum')
        M = Activation('tanh', name="M")(merged)

        alpha_ = TimeDistributed(Dense(1, activation='linear'), name="alpha_")(M)
        flat_alpha = Flatten(name="flat_alpha")(alpha_)

        alpha = Dense(L, activation='softmax', name="alpha")(flat_alpha)

        Y_trans = Permute((2, 1), name="y_trans")(Y)  # of shape (None,300,20)

        r_ = merge([Y_trans, alpha], output_shape=(k, 1), name="r_", mode=self.get_R)

        r = Reshape((k,), name="r")(r_)

        Wr = Dense(k, W_regularizer=l2(0.01))(r)
        Wh = Dense(k, W_regularizer=l2(0.01))(h_n)
        merged = merge([Wr, Wh], mode='sum')
        h_star = Activation('tanh')(merged)

        #out = Dense(ONE_HOT_LEN, activation='softmax')(h_star)
        #variation below
        out = Dense(self.Labels_one_hot_len, activation='softmax')(h_star)

        output = out
        model = Model(input=[encoding_input,image_input], output=output)
        return model    
    

    
    
    
    
    def structure_15(self,batch_size):
        k = 256
        L = self.CONTEXT_LENGTH-1
        encoding_input = Input(batch_shape=(batch_size,self.CONTEXT_LENGTH-1,self.embedding_size))
        drop_out = Dropout(0.5, name='dropout')(encoding_input)
        lstm_fwd = LSTM(128, batch_input_shape=(batch_size,self.CONTEXT_LENGTH-1, self.embedding_size), return_sequences=True, name='lstm_fwd', stateful=True)(drop_out)
        lstm_bwd = LSTM(128, batch_input_shape=(batch_size,self.CONTEXT_LENGTH-1, self.embedding_size), return_sequences=True, go_backwards=True, name='lstm_bwd', stateful=True)(drop_out)
        bilstm = merge([lstm_fwd, lstm_bwd], name='bilstm', mode='concat')
        drop_out = Dropout(0.5)(bilstm)
        h_n = Lambda(self.get_H_n, output_shape=(k,), name="h_n")(drop_out)
        Y = Lambda(self.get_Y, arguments={"xmaxlen": L}, name="Y", output_shape=(L, k))(drop_out)
        Whn = Dense(k, W_regularizer=l2(0.01), name="Wh_n")(h_n)
        Whn_x_e = RepeatVector(L, name="Wh_n_x_e")(Whn)
        WY = TimeDistributed(Dense(k, W_regularizer=l2(0.01)), name="WY")(Y)
        merged = merge([Whn_x_e, WY], name="merged", mode='sum')
        M = Activation('tanh', name="M")(merged)

        alpha_ = TimeDistributed(Dense(1, activation='linear'), name="alpha_")(M)
        flat_alpha = Flatten(name="flat_alpha")(alpha_)

        alpha = Dense(L, activation='softmax', name="alpha")(flat_alpha)

        Y_trans = Permute((2, 1), name="y_trans")(Y)  # of shape (None,300,20)

        r_ = merge([Y_trans, alpha], output_shape=(k, 1), name="r_", mode=self.get_R)

        r = Reshape((k,), name="r")(r_)

        Wr = Dense(k, W_regularizer=l2(0.01))(r)
        Wh = Dense(k, W_regularizer=l2(0.01))(h_n)
        merged = merge([Wr, Wh], mode='sum')
        h_star = Activation('tanh')(merged)

        #out = Dense(ONE_HOT_LEN, activation='softmax')(h_star)
        #variation below
        out = Dense(self.Labels_one_hot_len, activation='softmax')(h_star)

        output = out
        model = Model(input=[encoding_input], output=output)
        return model    
