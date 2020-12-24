# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/notekeras/sample/gan/core.py
# Compiled at: 2020-03-29 09:28:39
# Size of source mod 2**32: 95158 bytes
import matplotlib.pyplot as plt
import numpy as np, scipy
import tensorflow.keras.backend as K
from tensorflow.keras.datasets import cifar10, mnist
from tensorflow.keras.layers import BatchNormalization, Activation
from tensorflow.keras.layers import Concatenate
from tensorflow.keras.layers import Embedding, ZeroPadding2D
from tensorflow.keras.layers import Input, Dense, Flatten, Dropout
from tensorflow.keras.layers import LeakyReLU, Reshape, multiply
from tensorflow.keras.layers import UpSampling2D, Conv2D
from tensorflow.keras.layers import concatenate
from tensorflow.keras.models import Sequential, Model
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.utils import to_categorical
from tensorflow.python.keras.layers import merge
from tensorflow_core.python.keras.optimizers import RMSprop
from notekeras.backend import plot_model

def build_generator(img_shape, latent_dim):
    model = Sequential()
    model.add(Dense(256, input_dim=latent_dim))
    model.add(LeakyReLU(alpha=0.2))
    model.add(BatchNormalization(momentum=0.8))
    model.add(Dense(512))
    model.add(LeakyReLU(alpha=0.2))
    model.add(BatchNormalization(momentum=0.8))
    model.add(Dense(1024))
    model.add(LeakyReLU(alpha=0.2))
    model.add(BatchNormalization(momentum=0.8))
    model.add(Dense((np.prod(img_shape)), activation='tanh'))
    model.add(Reshape(img_shape))
    model.summary()
    noise = Input(shape=(latent_dim,))
    img = model(noise)
    return Model(noise, img)


class BaseGAN:

    def __init__(self, name='GAN'):
        self.name = name
        self.generator = None
        self.discriminator = None
        self.combined = None

    def build_generator(self):
        pass

    def build_discriminator(self):
        pass

    def train(self, epochs=30000, batch_size=128, sample_interval=50):
        pass

    def sample_images(self, epoch):
        pass

    def plot(self):
        if self.generator is not None:
            self.generator.summary()
        if self.discriminator is not None:
            self.discriminator.summary()
        if self.combined is not None:
            plot_model((self.combined), ('plot_model/{}.png'.format(self.name)), show_shapes=True, expand_nested=True)


class GAN(BaseGAN):

    def __init__(self):
        super(GAN, self).__init__(name='GAN')
        self.img_rows = 28
        self.img_cols = 28
        self.channels = 1
        self.img_shape = (self.img_rows, self.img_cols, self.channels)
        self.latent_dim = 100
        optimizer = Adam(0.0002, 0.5)
        self.generator = self.build_generator()
        self.discriminator = self.build_discriminator()
        self.discriminator.compile(loss='binary_crossentropy', optimizer=optimizer,
          metrics=[
         'accuracy'])
        self.discriminator.trainable = False
        z = Input(shape=(self.latent_dim,))
        img = self.generator(z)
        validity = self.discriminator(img)
        self.combined = Model(z, validity)
        self.combined.compile(loss='binary_crossentropy', optimizer=optimizer)

    def build_generator(self):
        noise = Input(shape=(self.latent_dim,))
        layer1 = Dense(256, input_dim=(self.latent_dim))(noise)
        layer1 = LeakyReLU(alpha=0.2)(layer1)
        layer1 = BatchNormalization(momentum=0.8)(layer1)
        layer1 = Dense(512)(layer1)
        layer1 = LeakyReLU(alpha=0.2)(layer1)
        layer1 = BatchNormalization(momentum=0.8)(layer1)
        layer1 = Dense(1024)(layer1)
        layer1 = LeakyReLU(alpha=0.2)(layer1)
        layer1 = BatchNormalization(momentum=0.8)(layer1)
        layer1 = Dense((np.prod(self.img_shape)), activation='tanh')(layer1)
        layer1 = Reshape(self.img_shape)(layer1)
        return Model(noise, layer1, name='generator')

    def build_discriminator(self):
        img = Input(shape=(self.img_shape))
        layer1 = Flatten(input_shape=(self.img_shape))(img)
        layer1 = Dense(512)(layer1)
        layer1 = LeakyReLU(alpha=0.2)(layer1)
        layer1 = Dense(256)(layer1)
        layer1 = LeakyReLU(alpha=0.2)(layer1)
        layer1 = Dense(1, activation='sigmoid')(layer1)
        return Model(img, layer1, name='discriminator')

    def train(self, epochs=30000, batch_size=128, sample_interval=50):
        (X_train, _), (_, _) = mnist.load_data()
        X_train = X_train / 127.5 - 1.0
        X_train = np.expand_dims(X_train, axis=3)
        valid = np.ones((batch_size, 1))
        fake = np.zeros((batch_size, 1))
        for epoch in range(epochs):
            idx = np.random.randint(0, X_train.shape[0], batch_size)
            imgs = X_train[idx]
            noise = np.random.normal(0, 1, (batch_size, self.latent_dim))
            gen_imgs = self.generator.predict(noise)
            d_loss_real = self.discriminator.train_on_batch(imgs, valid)
            d_loss_fake = self.discriminator.train_on_batch(gen_imgs, fake)
            d_loss = 0.5 * np.add(d_loss_real, d_loss_fake)
            noise = np.random.normal(0, 1, (batch_size, self.latent_dim))
            g_loss = self.combined.train_on_batch(noise, valid)
            print('%d [D loss: %f, acc.: %.2f%%] [G loss: %f]' % (epoch, d_loss[0], 100 * d_loss[1], g_loss))
            if epoch % sample_interval == 0:
                self.sample_images(epoch)

    def sample_images(self, epoch):
        r, c = (5, 5)
        noise = np.random.normal(0, 1, (r * c, self.latent_dim))
        gen_imgs = self.generator.predict(noise)
        gen_imgs = 0.5 * gen_imgs + 0.5
        fig, axs = plt.subplots(r, c)
        cnt = 0
        for i in range(r):
            for j in range(c):
                axs[(i, j)].imshow((gen_imgs[cnt, :, :, 0]), cmap='gray')
                axs[(i, j)].axis('off')
                cnt += 1

        fig.savefig('images/%d.png' % epoch)
        plt.close()


class ACGAN(BaseGAN):

    def __init__(self):
        super(ACGAN, self).__init__(name='ACGAN')
        self.img_rows = 28
        self.img_cols = 28
        self.channels = 1
        self.img_shape = (self.img_rows, self.img_cols, self.channels)
        self.num_classes = 10
        self.latent_dim = 100
        optimizer = Adam(0.0002, 0.5)
        losses = ['binary_crossentropy', 'sparse_categorical_crossentropy']
        self.generator = self.build_generator()
        self.discriminator = self.build_discriminator()
        self.discriminator.compile(loss=losses, optimizer=optimizer,
          metrics=[
         'accuracy'])
        noise = Input(shape=(self.latent_dim,))
        label = Input(shape=(1, ))
        img = self.generator([noise, label])
        self.discriminator.trainable = False
        valid, target_label = self.discriminator(img)
        self.combined = Model([noise, label], [valid, target_label])
        self.combined.compile(loss=losses, optimizer=optimizer)

    def build_generator(self):
        noise = Input(shape=(self.latent_dim,))
        label = Input(shape=(1, ), dtype='int32')
        label_embedding = Flatten()(Embedding(self.num_classes, self.latent_dim)(label))
        model_input = multiply([noise, label_embedding])
        layer1 = Dense(6272, activation='relu', input_dim=(self.latent_dim))(model_input)
        layer1 = Reshape((7, 7, 128))(layer1)
        layer1 = BatchNormalization(momentum=0.8)(layer1)
        layer1 = UpSampling2D()(layer1)
        layer1 = Conv2D(128, kernel_size=3, padding='same')(layer1)
        layer1 = Activation('relu')(layer1)
        layer1 = BatchNormalization(momentum=0.8)(layer1)
        layer1 = UpSampling2D()(layer1)
        layer1 = Conv2D(64, kernel_size=3, padding='same')(layer1)
        layer1 = Activation('relu')(layer1)
        layer1 = BatchNormalization(momentum=0.8)(layer1)
        layer1 = Conv2D((self.channels), kernel_size=3, padding='same')(layer1)
        layer1 = Activation('tanh')(layer1)
        img = layer1
        return Model([noise, label], img)

    def build_discriminator(self):
        img = Input(shape=(self.img_shape))
        layer1 = Conv2D(16, kernel_size=3, strides=2, input_shape=(self.img_shape), padding='same')(img)
        layer1 = LeakyReLU(alpha=0.2)(layer1)
        layer1 = Dropout(0.25)(layer1)
        layer1 = Conv2D(32, kernel_size=3, strides=2, padding='same')(layer1)
        layer1 = ZeroPadding2D(padding=((0, 1), (0, 1)))(layer1)
        layer1 = LeakyReLU(alpha=0.2)(layer1)
        layer1 = Dropout(0.25)(layer1)
        layer1 = BatchNormalization(momentum=0.8)(layer1)
        layer1 = Conv2D(64, kernel_size=3, strides=2, padding='same')(layer1)
        layer1 = LeakyReLU(alpha=0.2)(layer1)
        layer1 = Dropout(0.25)(layer1)
        layer1 = BatchNormalization(momentum=0.8)(layer1)
        layer1 = Conv2D(128, kernel_size=3, strides=1, padding='same')(layer1)
        layer1 = LeakyReLU(alpha=0.2)(layer1)
        layer1 = Dropout(0.25)(layer1)
        layer1 = Flatten()(layer1)
        features = layer1
        validity = Dense(1, activation='sigmoid')(features)
        label = Dense((self.num_classes), activation='softmax')(features)
        return Model(img, [validity, label])

    def train(self, epochs=14000, batch_size=128, sample_interval=50):
        (X_train, y_train), (_, _) = mnist.load_data()
        X_train = (X_train.astype(np.float32) - 127.5) / 127.5
        X_train = np.expand_dims(X_train, axis=3)
        y_train = y_train.reshape(-1, 1)
        valid = np.ones((batch_size, 1))
        fake = np.zeros((batch_size, 1))
        for epoch in range(epochs):
            idx = np.random.randint(0, X_train.shape[0], batch_size)
            imgs = X_train[idx]
            noise = np.random.normal(0, 1, (batch_size, self.latent_dim))
            sampled_labels = np.random.randint(0, 10, (batch_size, 1))
            gen_imgs = self.generator.predict([noise, sampled_labels])
            img_labels = y_train[idx]
            d_loss_real = self.discriminator.train_on_batch(imgs, [valid, img_labels])
            d_loss_fake = self.discriminator.train_on_batch(gen_imgs, [fake, sampled_labels])
            d_loss = 0.5 * np.add(d_loss_real, d_loss_fake)
            g_loss = self.combined.train_on_batch([noise, sampled_labels], [valid, sampled_labels])
            print('%d [D loss: %f, acc.: %.2f%%, op_acc: %.2f%%] [G loss: %f]' % (
             epoch, d_loss[0], 100 * d_loss[3], 100 * d_loss[4], g_loss[0]))
            if epoch % sample_interval == 0:
                self.save_model()
                self.sample_images(epoch)

    def sample_images(self, epoch):
        r, c = (10, 10)
        noise = np.random.normal(0, 1, (r * c, self.latent_dim))
        sampled_labels = np.array([num for _ in range(r) for num in range(c)])
        gen_imgs = self.generator.predict([noise, sampled_labels])
        gen_imgs = 0.5 * gen_imgs + 0.5
        fig, axs = plt.subplots(r, c)
        cnt = 0
        for i in range(r):
            for j in range(c):
                axs[(i, j)].imshow((gen_imgs[cnt, :, :, 0]), cmap='gray')
                axs[(i, j)].axis('off')
                cnt += 1

        fig.savefig('images/%d.png' % epoch)
        plt.close()

    def save_model(self):

        def save(model, model_name):
            model_path = 'saved_model/%s.json' % model_name
            weights_path = 'saved_model/%s_weights.hdf5' % model_name
            options = {'file_arch':model_path,  'file_weight':weights_path}
            json_string = model.to_json()
            open(options['file_arch'], 'w').write(json_string)
            model.save_weights(options['file_weight'])

        save(self.generator, 'generator')
        save(self.discriminator, 'discriminator')


class BGAN(BaseGAN):
    __doc__ = 'Reference: https://wiseodd.github.io/techblog/2017/03/07/boundary-seeking-gan/'

    def __init__(self):
        super(BGAN, self).__init__(name='BGAN')
        self.img_rows = 28
        self.img_cols = 28
        self.channels = 1
        self.img_shape = (self.img_rows, self.img_cols, self.channels)
        self.latent_dim = 100
        optimizer = Adam(0.0002, 0.5)
        self.discriminator = self.build_discriminator()
        self.discriminator.compile(loss='binary_crossentropy', optimizer=optimizer,
          metrics=[
         'accuracy'])
        self.generator = self.build_generator()
        z = Input(shape=(self.latent_dim,))
        img = self.generator(z)
        self.discriminator.trainable = False
        valid = self.discriminator(img)
        self.combined = Model(z, valid)
        self.combined.compile(loss=(self.boundary_loss), optimizer=optimizer)

    def build_generator(self):
        noise = Input(shape=(self.latent_dim,))
        layer1 = Dense(256, input_dim=(self.latent_dim))(noise)
        layer1 = LeakyReLU(alpha=0.2)(layer1)
        layer1 = BatchNormalization(momentum=0.8)(layer1)
        layer1 = Dense(512)(layer1)
        layer1 = LeakyReLU(alpha=0.2)(layer1)
        layer1 = BatchNormalization(momentum=0.8)(layer1)
        layer1 = Dense(1024)(layer1)
        layer1 = LeakyReLU(alpha=0.2)(layer1)
        layer1 = BatchNormalization(momentum=0.8)(layer1)
        layer1 = Dense((np.prod(self.img_shape)), activation='tanh')(layer1)
        layer1 = Reshape(self.img_shape)(layer1)
        return Model(noise, layer1)

    def build_discriminator(self):
        img = Input(shape=(self.img_shape))
        output = Flatten(input_shape=(self.img_shape))(img)
        output = Dense(512)(output)
        output = LeakyReLU(alpha=0.2)(output)
        output = Dense(256)(output)
        output = LeakyReLU(alpha=0.2)(output)
        output = Dense(1, activation='sigmoid')(output)
        return Model(img, output)

    def boundary_loss(self, y_true, y_pred):
        """
        Boundary seeking loss.
        Reference: https://wiseodd.github.io/techblog/2017/03/07/boundary-seeking-gan/
        """
        return 0.5 * K.mean((K.log(y_pred) - K.log(1 - y_pred)) ** 2)

    def train(self, epochs=30000, batch_size=128, sample_interval=50):
        (X_train, _), (_, _) = mnist.load_data()
        X_train = X_train / 127.5 - 1.0
        X_train = np.expand_dims(X_train, axis=3)
        valid = np.ones((batch_size, 1))
        fake = np.zeros((batch_size, 1))
        for epoch in range(epochs):
            idx = np.random.randint(0, X_train.shape[0], batch_size)
            imgs = X_train[idx]
            noise = np.random.normal(0, 1, (batch_size, self.latent_dim))
            gen_imgs = self.generator.predict(noise)
            d_loss_real = self.discriminator.train_on_batch(imgs, valid)
            d_loss_fake = self.discriminator.train_on_batch(gen_imgs, fake)
            d_loss = 0.5 * np.add(d_loss_real, d_loss_fake)
            g_loss = self.combined.train_on_batch(noise, valid)
            print('%d [D loss: %f, acc.: %.2f%%] [G loss: %f]' % (epoch, d_loss[0], 100 * d_loss[1], g_loss))
            if epoch % sample_interval == 0:
                self.sample_images(epoch)

    def sample_images(self, epoch):
        r, c = (5, 5)
        noise = np.random.normal(0, 1, (r * c, self.latent_dim))
        gen_imgs = self.generator.predict(noise)
        gen_imgs = 0.5 * gen_imgs + 0.5
        fig, axs = plt.subplots(r, c)
        cnt = 0
        for i in range(r):
            for j in range(c):
                axs[(i, j)].imshow((gen_imgs[cnt, :, :, 0]), cmap='gray')
                axs[(i, j)].axis('off')
                cnt += 1

        fig.savefig('images/mnist_%d.png' % epoch)
        plt.close()


class AdversarialAutoEncoder:

    def __init__(self):
        self.img_rows = 28
        self.img_cols = 28
        self.channels = 1
        self.img_shape = (self.img_rows, self.img_cols, self.channels)
        self.latent_dim = 10
        optimizer = Adam(0.0002, 0.5)
        self.discriminator = self.build_discriminator()
        self.discriminator.compile(loss='binary_crossentropy', optimizer=optimizer,
          metrics=[
         'accuracy'])
        self.encoder = self.build_encoder()
        self.decoder = self.build_decoder()
        img = Input(shape=(self.img_shape))
        encoded_repr = self.encoder(img)
        reconstructed_img = self.decoder(encoded_repr)
        self.discriminator.trainable = False
        validity = self.discriminator(encoded_repr)
        self.adversarial_autoencoder = Model(img, [reconstructed_img, validity])
        self.adversarial_autoencoder.compile(loss=['mse', 'binary_crossentropy'], loss_weights=[
         0.999, 0.001],
          optimizer=optimizer)

    def build_encoder(self):
        img = Input(shape=(self.img_shape))
        h = Flatten()(img)
        h = Dense(512)(h)
        h = LeakyReLU(alpha=0.2)(h)
        h = Dense(512)(h)
        h = LeakyReLU(alpha=0.2)(h)
        mu = Dense(self.latent_dim)(h)
        log_var = Dense(self.latent_dim)(h)
        latent_repr = merge([mu, log_var], mode=(lambda p: p[0] + K.random_normal(K.shape(p[0])) * K.exp(p[1] / 2)),
          output_shape=(lambda p: p[0]))
        return Model(img, latent_repr)

    def build_decoder(self):
        model = Sequential()
        model.add(Dense(512, input_dim=(self.latent_dim)))
        model.add(LeakyReLU(alpha=0.2))
        model.add(Dense(512))
        model.add(LeakyReLU(alpha=0.2))
        model.add(Dense((np.prod(self.img_shape)), activation='tanh'))
        model.add(Reshape(self.img_shape))
        model.summary()
        z = Input(shape=(self.latent_dim,))
        img = model(z)
        return Model(z, img)

    def build_discriminator(self):
        model = Sequential()
        model.add(Dense(512, input_dim=(self.latent_dim)))
        model.add(LeakyReLU(alpha=0.2))
        model.add(Dense(256))
        model.add(LeakyReLU(alpha=0.2))
        model.add(Dense(1, activation='sigmoid'))
        model.summary()
        encoded_repr = Input(shape=(self.latent_dim,))
        validity = model(encoded_repr)
        return Model(encoded_repr, validity)

    def train(self, epochs=20000, batch_size=128, sample_interval=50):
        (X_train, _), (_, _) = mnist.load_data()
        X_train = (X_train.astype(np.float32) - 127.5) / 127.5
        X_train = np.expand_dims(X_train, axis=3)
        valid = np.ones((batch_size, 1))
        fake = np.zeros((batch_size, 1))
        for epoch in range(epochs):
            idx = np.random.randint(0, X_train.shape[0], batch_size)
            imgs = X_train[idx]
            latent_fake = self.encoder.predict(imgs)
            latent_real = np.random.normal(size=(batch_size, self.latent_dim))
            d_loss_real = self.discriminator.train_on_batch(latent_real, valid)
            d_loss_fake = self.discriminator.train_on_batch(latent_fake, fake)
            d_loss = 0.5 * np.add(d_loss_real, d_loss_fake)
            g_loss = self.adversarial_autoencoder.train_on_batch(imgs, [imgs, valid])
            print('%d [D loss: %f, acc: %.2f%%] [G loss: %f, mse: %f]' % (
             epoch, d_loss[0], 100 * d_loss[1], g_loss[0], g_loss[1]))
            if epoch % sample_interval == 0:
                self.sample_images(epoch)

    def sample_images(self, epoch):
        r, c = (5, 5)
        z = np.random.normal(size=(r * c, self.latent_dim))
        gen_imgs = self.decoder.predict(z)
        gen_imgs = 0.5 * gen_imgs + 0.5
        fig, axs = plt.subplots(r, c)
        cnt = 0
        for i in range(r):
            for j in range(c):
                axs[(i, j)].imshow((gen_imgs[cnt, :, :, 0]), cmap='gray')
                axs[(i, j)].axis('off')
                cnt += 1

        fig.savefig('images/mnist_%d.png' % epoch)
        plt.close()

    def save_model(self):

        def save(model, model_name):
            model_path = 'saved_model/%s.json' % model_name
            weights_path = 'saved_model/%s_weights.hdf5' % model_name
            options = {'file_arch':model_path,  'file_weight':weights_path}
            json_string = model.to_json()
            open(options['file_arch'], 'w').write(json_string)
            model.save_weights(options['file_weight'])

        save(self.generator, 'aae_generator')
        save(self.discriminator, 'aae_discriminator')


class BIGAN:

    def __init__(self):
        self.img_rows = 28
        self.img_cols = 28
        self.channels = 1
        self.img_shape = (self.img_rows, self.img_cols, self.channels)
        self.latent_dim = 100
        optimizer = Adam(0.0002, 0.5)
        self.discriminator = self.build_discriminator()
        self.discriminator.compile(loss=['binary_crossentropy'], optimizer=optimizer,
          metrics=[
         'accuracy'])
        self.generator = self.build_generator()
        self.encoder = self.build_encoder()
        self.discriminator.trainable = False
        z = Input(shape=(self.latent_dim,))
        img_ = self.generator(z)
        img = Input(shape=(self.img_shape))
        z_ = self.encoder(img)
        fake = self.discriminator([z, img_])
        valid = self.discriminator([z_, img])
        self.bigan_generator = Model([z, img], [fake, valid])
        self.bigan_generator.compile(loss=['binary_crossentropy', 'binary_crossentropy'], optimizer=optimizer)

    def build_encoder(self):
        model = Sequential()
        model.add(Flatten(input_shape=(self.img_shape)))
        model.add(Dense(512))
        model.add(LeakyReLU(alpha=0.2))
        model.add(BatchNormalization(momentum=0.8))
        model.add(Dense(512))
        model.add(LeakyReLU(alpha=0.2))
        model.add(BatchNormalization(momentum=0.8))
        model.add(Dense(self.latent_dim))
        model.summary()
        img = Input(shape=(self.img_shape))
        z = model(img)
        return Model(img, z)

    def build_generator(self):
        inputs = Input(shape=(self.latent_dim,))
        output = Dense(512, input_dim=(self.latent_dim))(inputs)
        output = LeakyReLU(alpha=0.2)(output)
        output = BatchNormalization(momentum=0.8)(output)
        output = Dense(512)(output)
        output = LeakyReLU(alpha=0.2)(output)
        output = BatchNormalization(momentum=0.8)(output)
        output = Dense((np.prod(self.img_shape)), activation='tanh')(output)
        output = Reshape(self.img_shape)(output)
        return Model(inputs, output)

    def build_discriminator(self):
        z = Input(shape=(self.latent_dim,))
        img = Input(shape=(self.img_shape))
        d_in = concatenate([z, Flatten()(img)])
        model = Dense(1024)(d_in)
        model = LeakyReLU(alpha=0.2)(model)
        model = Dropout(0.5)(model)
        model = Dense(1024)(model)
        model = LeakyReLU(alpha=0.2)(model)
        model = Dropout(0.5)(model)
        model = Dense(1024)(model)
        model = LeakyReLU(alpha=0.2)(model)
        model = Dropout(0.5)(model)
        validity = Dense(1, activation='sigmoid')(model)
        return Model([z, img], validity)

    def train(self, epochs=40000, batch_size=128, sample_interval=50):
        (X_train, _), (_, _) = mnist.load_data()
        X_train = (X_train.astype(np.float32) - 127.5) / 127.5
        X_train = np.expand_dims(X_train, axis=3)
        valid = np.ones((batch_size, 1))
        fake = np.zeros((batch_size, 1))
        for epoch in range(epochs):
            z = np.random.normal(size=(batch_size, self.latent_dim))
            imgs_ = self.generator.predict(z)
            idx = np.random.randint(0, X_train.shape[0], batch_size)
            imgs = X_train[idx]
            z_ = self.encoder.predict(imgs)
            d_loss_real = self.discriminator.train_on_batch([z_, imgs], valid)
            d_loss_fake = self.discriminator.train_on_batch([z, imgs_], fake)
            d_loss = 0.5 * np.add(d_loss_real, d_loss_fake)
            g_loss = self.bigan_generator.train_on_batch([z, imgs], [valid, fake])
            print('%d [D loss: %f, acc: %.2f%%] [G loss: %f]' % (epoch, d_loss[0], 100 * d_loss[1], g_loss[0]))
            if epoch % sample_interval == 0:
                self.sample_interval(epoch)

    def sample_interval(self, epoch):
        r, c = (5, 5)
        z = np.random.normal(size=(25, self.latent_dim))
        gen_imgs = self.generator.predict(z)
        gen_imgs = 0.5 * gen_imgs + 0.5
        fig, axs = plt.subplots(r, c)
        cnt = 0
        for i in range(r):
            for j in range(c):
                axs[(i, j)].imshow((gen_imgs[cnt, :, :, 0]), cmap='gray')
                axs[(i, j)].axis('off')
                cnt += 1

        fig.savefig('images/mnist_%d.png' % epoch)
        plt.close()


class CCGAN:

    def __init__(self):
        self.img_rows = 32
        self.img_cols = 32
        self.channels = 1
        self.img_shape = (self.img_rows, self.img_cols, self.channels)
        self.mask_height = 10
        self.mask_width = 10
        self.num_classes = 10
        self.gf = 32
        self.df = 32
        optimizer = Adam(0.0002, 0.5)
        self.discriminator = self.build_discriminator()
        self.discriminator.compile(loss=['mse', 'categorical_crossentropy'], loss_weights=[
         0.5, 0.5],
          optimizer=optimizer,
          metrics=[
         'accuracy'])
        self.generator = self.build_generator()
        masked_img = Input(shape=(self.img_shape))
        gen_img = self.generator(masked_img)
        self.discriminator.trainable = False
        valid, _ = self.discriminator(gen_img)
        self.combined = Model(masked_img, valid)
        self.combined.compile(loss=['mse'], optimizer=optimizer)

    def build_generator(self):
        """U-Net Generator"""

        def conv2d(layer_input, filters, f_size=4, bn=True):
            """Layers used during downsampling"""
            d = Conv2D(filters, kernel_size=f_size, strides=2, padding='same')(layer_input)
            d = LeakyReLU(alpha=0.2)(d)
            if bn:
                d = BatchNormalization(momentum=0.8)(d)
            return d

        def deconv2d(layer_input, skip_input, filters, f_size=4, dropout_rate=0):
            """Layers used during upsampling"""
            u = UpSampling2D(size=2)(layer_input)
            u = Conv2D(filters, kernel_size=f_size, strides=1, padding='same', activation='relu')(u)
            if dropout_rate:
                u = Dropout(dropout_rate)(u)
            u = BatchNormalization(momentum=0.8)(u)
            u = Concatenate()([u, skip_input])
            return u

        img = Input(shape=(self.img_shape))
        d1 = conv2d(img, (self.gf), bn=False)
        d2 = conv2d(d1, self.gf * 2)
        d3 = conv2d(d2, self.gf * 4)
        d4 = conv2d(d3, self.gf * 8)
        u1 = deconv2d(d4, d3, self.gf * 4)
        u2 = deconv2d(u1, d2, self.gf * 2)
        u3 = deconv2d(u2, d1, self.gf)
        u4 = UpSampling2D(size=2)(u3)
        output_img = Conv2D((self.channels), kernel_size=4, strides=1, padding='same', activation='tanh')(u4)
        return Model(img, output_img)

    def build_discriminator(self):
        img = Input(shape=(self.img_shape))
        model = Sequential()
        model.add(Conv2D(64, kernel_size=4, strides=2, padding='same', input_shape=(self.img_shape)))
        model.add(LeakyReLU(alpha=0.8))
        model.add(Conv2D(128, kernel_size=4, strides=2, padding='same'))
        model.add(LeakyReLU(alpha=0.2))
        model.add(BatchNormalization())
        model.add(Conv2D(256, kernel_size=4, strides=2, padding='same'))
        model.add(LeakyReLU(alpha=0.2))
        model.add(BatchNormalization())
        model.summary()
        img = Input(shape=(self.img_shape))
        features = model(img)
        validity = Conv2D(1, kernel_size=4, strides=1, padding='same')(features)
        label = Flatten()(features)
        label = Dense((self.num_classes + 1), activation='softmax')(label)
        return Model(img, [validity, label])

    def mask_randomly(self, imgs):
        y1 = np.random.randint(0, self.img_rows - self.mask_height, imgs.shape[0])
        y2 = y1 + self.mask_height
        x1 = np.random.randint(0, self.img_rows - self.mask_width, imgs.shape[0])
        x2 = x1 + self.mask_width
        masked_imgs = np.empty_like(imgs)
        for i, img in enumerate(imgs):
            masked_img = img.copy()
            _y1, _y2, _x1, _x2 = (y1[i], y2[i], x1[i], x2[i])
            masked_img[_y1:_y2, _x1:_x2, :] = 0
            masked_imgs[i] = masked_img

        return masked_imgs

    def train(self, epochs, batch_size=128, sample_interval=50):
        (X_train, y_train), (_, _) = mnist.load_data()
        X_train = np.array([scipy.misc.imresize(x, [self.img_rows, self.img_cols]) for x in X_train])
        X_train = (X_train.astype(np.float32) - 127.5) / 127.5
        X_train = np.expand_dims(X_train, axis=3)
        y_train = y_train.reshape(-1, 1)
        valid = np.ones((batch_size, 4, 4, 1))
        fake = np.zeros((batch_size, 4, 4, 1))
        for epoch in range(epochs):
            idx = np.random.randint(0, X_train.shape[0], batch_size)
            imgs = X_train[idx]
            labels = y_train[idx]
            masked_imgs = self.mask_randomly(imgs)
            gen_imgs = self.generator.predict(masked_imgs)
            labels = to_categorical(labels, num_classes=(self.num_classes + 1))
            fake_labels = to_categorical((np.full((batch_size, 1), self.num_classes)), num_classes=(self.num_classes + 1))
            d_loss_real = self.discriminator.train_on_batch(imgs, [valid, labels])
            d_loss_fake = self.discriminator.train_on_batch(gen_imgs, [fake, fake_labels])
            d_loss = 0.5 * np.add(d_loss_real, d_loss_fake)
            g_loss = self.combined.train_on_batch(masked_imgs, valid)
            print('%d [D loss: %f, op_acc: %.2f%%] [G loss: %f]' % (epoch, d_loss[0], 100 * d_loss[4], g_loss))
            if epoch % sample_interval == 0:
                idx = np.random.randint(0, X_train.shape[0], 6)
                imgs = X_train[idx]
                self.sample_images(epoch, imgs)
                self.save_model()

    def sample_images(self, epoch, imgs):
        r, c = (3, 6)
        masked_imgs = self.mask_randomly(imgs)
        gen_imgs = self.generator.predict(masked_imgs)
        imgs = (imgs + 1.0) * 0.5
        masked_imgs = (masked_imgs + 1.0) * 0.5
        gen_imgs = (gen_imgs + 1.0) * 0.5
        gen_imgs = np.where(gen_imgs < 0, 0, gen_imgs)
        fig, axs = plt.subplots(r, c)
        for i in range(c):
            axs[(0, i)].imshow((imgs[i, :, :, 0]), cmap='gray')
            axs[(0, i)].axis('off')
            axs[(1, i)].imshow((masked_imgs[i, :, :, 0]), cmap='gray')
            axs[(1, i)].axis('off')
            axs[(2, i)].imshow((gen_imgs[i, :, :, 0]), cmap='gray')
            axs[(2, i)].axis('off')

        fig.savefig('images/%d.png' % epoch)
        plt.close()

    def save_model(self):

        def save(model, model_name):
            model_path = 'saved_model/%s.json' % model_name
            weights_path = 'saved_model/%s_weights.hdf5' % model_name
            options = {'file_arch':model_path,  'file_weight':weights_path}
            json_string = model.to_json()
            open(options['file_arch'], 'w').write(json_string)
            model.save_weights(options['file_weight'])

        save(self.generator, 'ccgan_generator')
        save(self.discriminator, 'ccgan_discriminator')


class CGAN:

    def __init__(self):
        self.img_rows = 28
        self.img_cols = 28
        self.channels = 1
        self.img_shape = (self.img_rows, self.img_cols, self.channels)
        self.num_classes = 10
        self.latent_dim = 100
        optimizer = Adam(0.0002, 0.5)
        self.discriminator = self.build_discriminator()
        self.discriminator.compile(loss=['binary_crossentropy'], optimizer=optimizer,
          metrics=[
         'accuracy'])
        self.generator = self.build_generator()
        noise = Input(shape=(self.latent_dim,))
        label = Input(shape=(1, ))
        img = self.generator([noise, label])
        self.discriminator.trainable = False
        valid = self.discriminator([img, label])
        self.combined = Model([noise, label], valid)
        self.combined.compile(loss=['binary_crossentropy'], optimizer=optimizer)

    def build_generator(self):
        model = Sequential()
        model.add(Dense(256, input_dim=(self.latent_dim)))
        model.add(LeakyReLU(alpha=0.2))
        model.add(BatchNormalization(momentum=0.8))
        model.add(Dense(512))
        model.add(LeakyReLU(alpha=0.2))
        model.add(BatchNormalization(momentum=0.8))
        model.add(Dense(1024))
        model.add(LeakyReLU(alpha=0.2))
        model.add(BatchNormalization(momentum=0.8))
        model.add(Dense((np.prod(self.img_shape)), activation='tanh'))
        model.add(Reshape(self.img_shape))
        model.summary()
        noise = Input(shape=(self.latent_dim,))
        label = Input(shape=(1, ), dtype='int32')
        label_embedding = Flatten()(Embedding(self.num_classes, self.latent_dim)(label))
        model_input = multiply([noise, label_embedding])
        img = model(model_input)
        return Model([noise, label], img)

    def build_discriminator(self):
        model = Sequential()
        model.add(Dense(512, input_dim=(np.prod(self.img_shape))))
        model.add(LeakyReLU(alpha=0.2))
        model.add(Dense(512))
        model.add(LeakyReLU(alpha=0.2))
        model.add(Dropout(0.4))
        model.add(Dense(512))
        model.add(LeakyReLU(alpha=0.2))
        model.add(Dropout(0.4))
        model.add(Dense(1, activation='sigmoid'))
        model.summary()
        img = Input(shape=(self.img_shape))
        label = Input(shape=(1, ), dtype='int32')
        label_embedding = Flatten()(Embedding(self.num_classes, np.prod(self.img_shape))(label))
        flat_img = Flatten()(img)
        model_input = multiply([flat_img, label_embedding])
        validity = model(model_input)
        return Model([img, label], validity)

    def train(self, epochs, batch_size=128, sample_interval=50):
        (X_train, y_train), (_, _) = mnist.load_data()
        X_train = (X_train.astype(np.float32) - 127.5) / 127.5
        X_train = np.expand_dims(X_train, axis=3)
        y_train = y_train.reshape(-1, 1)
        valid = np.ones((batch_size, 1))
        fake = np.zeros((batch_size, 1))
        for epoch in range(epochs):
            idx = np.random.randint(0, X_train.shape[0], batch_size)
            imgs, labels = X_train[idx], y_train[idx]
            noise = np.random.normal(0, 1, (batch_size, 100))
            gen_imgs = self.generator.predict([noise, labels])
            d_loss_real = self.discriminator.train_on_batch([imgs, labels], valid)
            d_loss_fake = self.discriminator.train_on_batch([gen_imgs, labels], fake)
            d_loss = 0.5 * np.add(d_loss_real, d_loss_fake)
            sampled_labels = np.random.randint(0, 10, batch_size).reshape(-1, 1)
            g_loss = self.combined.train_on_batch([noise, sampled_labels], valid)
            print('%d [D loss: %f, acc.: %.2f%%] [G loss: %f]' % (epoch, d_loss[0], 100 * d_loss[1], g_loss))
            if epoch % sample_interval == 0:
                self.sample_images(epoch)

    def sample_images(self, epoch):
        r, c = (2, 5)
        noise = np.random.normal(0, 1, (r * c, 100))
        sampled_labels = np.arange(0, 10).reshape(-1, 1)
        gen_imgs = self.generator.predict([noise, sampled_labels])
        gen_imgs = 0.5 * gen_imgs + 0.5
        fig, axs = plt.subplots(r, c)
        cnt = 0
        for i in range(r):
            for j in range(c):
                axs[(i, j)].imshow((gen_imgs[cnt, :, :, 0]), cmap='gray')
                axs[(i, j)].set_title('Digit: %d' % sampled_labels[cnt])
                axs[(i, j)].axis('off')
                cnt += 1

        fig.savefig('images/%d.png' % epoch)
        plt.close()


class COGAN:
    __doc__ = 'Reference: https://wiseodd.github.io/techblog/2017/02/18/coupled_gan/'

    def __init__(self):
        self.img_rows = 28
        self.img_cols = 28
        self.channels = 1
        self.img_shape = (self.img_rows, self.img_cols, self.channels)
        self.latent_dim = 100
        optimizer = Adam(0.0002, 0.5)
        self.d1, self.d2 = self.build_discriminators()
        self.d1.compile(loss='binary_crossentropy', optimizer=optimizer,
          metrics=[
         'accuracy'])
        self.d2.compile(loss='binary_crossentropy', optimizer=optimizer,
          metrics=[
         'accuracy'])
        self.g1, self.g2 = self.build_generators()
        z = Input(shape=(self.latent_dim,))
        img1 = self.g1(z)
        img2 = self.g2(z)
        self.d1.trainable = False
        self.d2.trainable = False
        valid1 = self.d1(img1)
        valid2 = self.d2(img2)
        self.combined = Model(z, [valid1, valid2])
        self.combined.compile(loss=['binary_crossentropy', 'binary_crossentropy'], optimizer=optimizer)

    def build_generators(self):
        model = Sequential()
        model.add(Dense(256, input_dim=(self.latent_dim)))
        model.add(LeakyReLU(alpha=0.2))
        model.add(BatchNormalization(momentum=0.8))
        model.add(Dense(512))
        model.add(LeakyReLU(alpha=0.2))
        model.add(BatchNormalization(momentum=0.8))
        noise = Input(shape=(self.latent_dim,))
        feature_repr = model(noise)
        g1 = Dense(1024)(feature_repr)
        g1 = LeakyReLU(alpha=0.2)(g1)
        g1 = BatchNormalization(momentum=0.8)(g1)
        g1 = Dense((np.prod(self.img_shape)), activation='tanh')(g1)
        img1 = Reshape(self.img_shape)(g1)
        g2 = Dense(1024)(feature_repr)
        g2 = LeakyReLU(alpha=0.2)(g2)
        g2 = BatchNormalization(momentum=0.8)(g2)
        g2 = Dense((np.prod(self.img_shape)), activation='tanh')(g2)
        img2 = Reshape(self.img_shape)(g2)
        model.summary()
        return (
         Model(noise, img1), Model(noise, img2))

    def build_discriminators(self):
        img1 = Input(shape=(self.img_shape))
        img2 = Input(shape=(self.img_shape))
        model = Sequential()
        model.add(Flatten(input_shape=(self.img_shape)))
        model.add(Dense(512))
        model.add(LeakyReLU(alpha=0.2))
        model.add(Dense(256))
        model.add(LeakyReLU(alpha=0.2))
        img1_embedding = model(img1)
        img2_embedding = model(img2)
        validity1 = Dense(1, activation='sigmoid')(img1_embedding)
        validity2 = Dense(1, activation='sigmoid')(img2_embedding)
        return (
         Model(img1, validity1), Model(img2, validity2))

    def train(self, epochs, batch_size=128, sample_interval=50):
        (X_train, _), (_, _) = mnist.load_data()
        X_train = (X_train.astype(np.float32) - 127.5) / 127.5
        X_train = np.expand_dims(X_train, axis=3)
        X1 = X_train[:int(X_train.shape[0] / 2)]
        X2 = X_train[int(X_train.shape[0] / 2):]
        X2 = scipy.ndimage.interpolation.rotate(X2, 90, axes=(1, 2))
        valid = np.ones((batch_size, 1))
        fake = np.zeros((batch_size, 1))
        for epoch in range(epochs):
            idx = np.random.randint(0, X1.shape[0], batch_size)
            imgs1 = X1[idx]
            imgs2 = X2[idx]
            noise = np.random.normal(0, 1, (batch_size, 100))
            gen_imgs1 = self.g1.predict(noise)
            gen_imgs2 = self.g2.predict(noise)
            d1_loss_real = self.d1.train_on_batch(imgs1, valid)
            d2_loss_real = self.d2.train_on_batch(imgs2, valid)
            d1_loss_fake = self.d1.train_on_batch(gen_imgs1, fake)
            d2_loss_fake = self.d2.train_on_batch(gen_imgs2, fake)
            d1_loss = 0.5 * np.add(d1_loss_real, d1_loss_fake)
            d2_loss = 0.5 * np.add(d2_loss_real, d2_loss_fake)
            g_loss = self.combined.train_on_batch(noise, [valid, valid])
            print('%d [D1 loss: %f, acc.: %.2f%%] [D2 loss: %f, acc.: %.2f%%] [G loss: %f]' % (
             epoch, d1_loss[0], 100 * d1_loss[1], d2_loss[0], 100 * d2_loss[1], g_loss[0]))
            if epoch % sample_interval == 0:
                self.sample_images(epoch)

    def sample_images(self, epoch):
        r, c = (4, 4)
        noise = np.random.normal(0, 1, (r * int(c / 2), 100))
        gen_imgs1 = self.g1.predict(noise)
        gen_imgs2 = self.g2.predict(noise)
        gen_imgs = np.concatenate([gen_imgs1, gen_imgs2])
        gen_imgs = 0.5 * gen_imgs + 0.5
        fig, axs = plt.subplots(r, c)
        cnt = 0
        for i in range(r):
            for j in range(c):
                axs[(i, j)].imshow((gen_imgs[cnt, :, :, 0]), cmap='gray')
                axs[(i, j)].axis('off')
                cnt += 1

        fig.savefig('images/mnist_%d.png' % epoch)
        plt.close()


class ContextEncoder:

    def __init__(self):
        self.img_rows = 32
        self.img_cols = 32
        self.mask_height = 8
        self.mask_width = 8
        self.channels = 3
        self.num_classes = 2
        self.img_shape = (self.img_rows, self.img_cols, self.channels)
        self.missing_shape = (self.mask_height, self.mask_width, self.channels)
        optimizer = Adam(0.0002, 0.5)
        self.discriminator = self.build_discriminator()
        self.discriminator.compile(loss='binary_crossentropy', optimizer=optimizer,
          metrics=[
         'accuracy'])
        self.generator = self.build_generator()
        masked_img = Input(shape=(self.img_shape))
        gen_missing = self.generator(masked_img)
        self.discriminator.trainable = False
        valid = self.discriminator(gen_missing)
        self.combined = Model(masked_img, [gen_missing, valid])
        self.combined.compile(loss=['mse', 'binary_crossentropy'], loss_weights=[
         0.999, 0.001],
          optimizer=optimizer)

    def build_generator(self):
        model = Sequential()
        model.add(Conv2D(32, kernel_size=3, strides=2, input_shape=(self.img_shape), padding='same'))
        model.add(LeakyReLU(alpha=0.2))
        model.add(BatchNormalization(momentum=0.8))
        model.add(Conv2D(64, kernel_size=3, strides=2, padding='same'))
        model.add(LeakyReLU(alpha=0.2))
        model.add(BatchNormalization(momentum=0.8))
        model.add(Conv2D(128, kernel_size=3, strides=2, padding='same'))
        model.add(LeakyReLU(alpha=0.2))
        model.add(BatchNormalization(momentum=0.8))
        model.add(Conv2D(512, kernel_size=1, strides=2, padding='same'))
        model.add(LeakyReLU(alpha=0.2))
        model.add(Dropout(0.5))
        model.add(UpSampling2D())
        model.add(Conv2D(128, kernel_size=3, padding='same'))
        model.add(Activation('relu'))
        model.add(BatchNormalization(momentum=0.8))
        model.add(UpSampling2D())
        model.add(Conv2D(64, kernel_size=3, padding='same'))
        model.add(Activation('relu'))
        model.add(BatchNormalization(momentum=0.8))
        model.add(Conv2D((self.channels), kernel_size=3, padding='same'))
        model.add(Activation('tanh'))
        model.summary()
        masked_img = Input(shape=(self.img_shape))
        gen_missing = model(masked_img)
        return Model(masked_img, gen_missing)

    def build_discriminator(self):
        model = Sequential()
        model.add(Conv2D(64, kernel_size=3, strides=2, input_shape=(self.missing_shape), padding='same'))
        model.add(LeakyReLU(alpha=0.2))
        model.add(BatchNormalization(momentum=0.8))
        model.add(Conv2D(128, kernel_size=3, strides=2, padding='same'))
        model.add(LeakyReLU(alpha=0.2))
        model.add(BatchNormalization(momentum=0.8))
        model.add(Conv2D(256, kernel_size=3, padding='same'))
        model.add(LeakyReLU(alpha=0.2))
        model.add(BatchNormalization(momentum=0.8))
        model.add(Flatten())
        model.add(Dense(1, activation='sigmoid'))
        model.summary()
        img = Input(shape=(self.missing_shape))
        validity = model(img)
        return Model(img, validity)

    def mask_randomly(self, imgs):
        y1 = np.random.randint(0, self.img_rows - self.mask_height, imgs.shape[0])
        y2 = y1 + self.mask_height
        x1 = np.random.randint(0, self.img_rows - self.mask_width, imgs.shape[0])
        x2 = x1 + self.mask_width
        masked_imgs = np.empty_like(imgs)
        missing_parts = np.empty((imgs.shape[0], self.mask_height, self.mask_width, self.channels))
        for i, img in enumerate(imgs):
            masked_img = img.copy()
            _y1, _y2, _x1, _x2 = (y1[i], y2[i], x1[i], x2[i])
            missing_parts[i] = masked_img[_y1:_y2, _x1:_x2, :].copy()
            masked_img[_y1:_y2, _x1:_x2, :] = 0
            masked_imgs[i] = masked_img

        return (masked_imgs, missing_parts, (y1, y2, x1, x2))

    def train(self, epochs, batch_size=128, sample_interval=50):
        (X_train, y_train), (_, _) = cifar10.load_data()
        X_cats = X_train[(y_train == 3).flatten()]
        X_dogs = X_train[(y_train == 5).flatten()]
        X_train = np.vstack((X_cats, X_dogs))
        X_train = X_train / 127.5 - 1.0
        y_train = y_train.reshape(-1, 1)
        valid = np.ones((batch_size, 1))
        fake = np.zeros((batch_size, 1))
        for epoch in range(epochs):
            idx = np.random.randint(0, X_train.shape[0], batch_size)
            imgs = X_train[idx]
            masked_imgs, missing_parts, _ = self.mask_randomly(imgs)
            gen_missing = self.generator.predict(masked_imgs)
            d_loss_real = self.discriminator.train_on_batch(missing_parts, valid)
            d_loss_fake = self.discriminator.train_on_batch(gen_missing, fake)
            d_loss = 0.5 * np.add(d_loss_real, d_loss_fake)
            g_loss = self.combined.train_on_batch(masked_imgs, [missing_parts, valid])
            print('%d [D loss: %f, acc: %.2f%%] [G loss: %f, mse: %f]' % (
             epoch, d_loss[0], 100 * d_loss[1], g_loss[0], g_loss[1]))
            if epoch % sample_interval == 0:
                idx = np.random.randint(0, X_train.shape[0], 6)
                imgs = X_train[idx]
                self.sample_images(epoch, imgs)

    def sample_images(self, epoch, imgs):
        r, c = (3, 6)
        masked_imgs, missing_parts, (y1, y2, x1, x2) = self.mask_randomly(imgs)
        gen_missing = self.generator.predict(masked_imgs)
        imgs = 0.5 * imgs + 0.5
        masked_imgs = 0.5 * masked_imgs + 0.5
        gen_missing = 0.5 * gen_missing + 0.5
        fig, axs = plt.subplots(r, c)
        for i in range(c):
            axs[(0, i)].imshow(imgs[i, :, :])
            axs[(0, i)].axis('off')
            axs[(1, i)].imshow(masked_imgs[i, :, :])
            axs[(1, i)].axis('off')
            filled_in = imgs[i].copy()
            filled_in[y1[i]:y2[i], x1[i]:x2[i], :] = gen_missing[i]
            axs[(2, i)].imshow(filled_in)
            axs[(2, i)].axis('off')

        fig.savefig('images/%d.png' % epoch)
        plt.close()

    def save_model(self):

        def save(model, model_name):
            model_path = 'saved_model/%s.json' % model_name
            weights_path = 'saved_model/%s_weights.hdf5' % model_name
            options = {'file_arch':model_path,  'file_weight':weights_path}
            json_string = model.to_json()
            open(options['file_arch'], 'w').write(json_string)
            model.save_weights(options['file_weight'])

        save(self.generator, 'generator')
        save(self.discriminator, 'discriminator')


class DCGAN:

    def __init__(self):
        self.img_rows = 28
        self.img_cols = 28
        self.channels = 1
        self.img_shape = (self.img_rows, self.img_cols, self.channels)
        self.latent_dim = 100
        optimizer = Adam(0.0002, 0.5)
        self.discriminator = self.build_discriminator()
        self.discriminator.compile(loss='binary_crossentropy', optimizer=optimizer,
          metrics=[
         'accuracy'])
        self.generator = self.build_generator()
        z = Input(shape=(self.latent_dim,))
        img = self.generator(z)
        self.discriminator.trainable = False
        valid = self.discriminator(img)
        self.combined = Model(z, valid)
        self.combined.compile(loss='binary_crossentropy', optimizer=optimizer)

    def build_generator(self):
        model = Sequential()
        model.add(Dense(6272, activation='relu', input_dim=(self.latent_dim)))
        model.add(Reshape((7, 7, 128)))
        model.add(UpSampling2D())
        model.add(Conv2D(128, kernel_size=3, padding='same'))
        model.add(BatchNormalization(momentum=0.8))
        model.add(Activation('relu'))
        model.add(UpSampling2D())
        model.add(Conv2D(64, kernel_size=3, padding='same'))
        model.add(BatchNormalization(momentum=0.8))
        model.add(Activation('relu'))
        model.add(Conv2D((self.channels), kernel_size=3, padding='same'))
        model.add(Activation('tanh'))
        model.summary()
        noise = Input(shape=(self.latent_dim,))
        img = model(noise)
        return Model(noise, img)

    def build_discriminator(self):
        model = Sequential()
        model.add(Conv2D(32, kernel_size=3, strides=2, input_shape=(self.img_shape), padding='same'))
        model.add(LeakyReLU(alpha=0.2))
        model.add(Dropout(0.25))
        model.add(Conv2D(64, kernel_size=3, strides=2, padding='same'))
        model.add(ZeroPadding2D(padding=((0, 1), (0, 1))))
        model.add(BatchNormalization(momentum=0.8))
        model.add(LeakyReLU(alpha=0.2))
        model.add(Dropout(0.25))
        model.add(Conv2D(128, kernel_size=3, strides=2, padding='same'))
        model.add(BatchNormalization(momentum=0.8))
        model.add(LeakyReLU(alpha=0.2))
        model.add(Dropout(0.25))
        model.add(Conv2D(256, kernel_size=3, strides=1, padding='same'))
        model.add(BatchNormalization(momentum=0.8))
        model.add(LeakyReLU(alpha=0.2))
        model.add(Dropout(0.25))
        model.add(Flatten())
        model.add(Dense(1, activation='sigmoid'))
        model.summary()
        img = Input(shape=(self.img_shape))
        validity = model(img)
        return Model(img, validity)

    def train(self, epochs, batch_size=128, save_interval=50):
        (X_train, _), (_, _) = mnist.load_data()
        X_train = X_train / 127.5 - 1.0
        X_train = np.expand_dims(X_train, axis=3)
        valid = np.ones((batch_size, 1))
        fake = np.zeros((batch_size, 1))
        for epoch in range(epochs):
            idx = np.random.randint(0, X_train.shape[0], batch_size)
            imgs = X_train[idx]
            noise = np.random.normal(0, 1, (batch_size, self.latent_dim))
            gen_imgs = self.generator.predict(noise)
            d_loss_real = self.discriminator.train_on_batch(imgs, valid)
            d_loss_fake = self.discriminator.train_on_batch(gen_imgs, fake)
            d_loss = 0.5 * np.add(d_loss_real, d_loss_fake)
            g_loss = self.combined.train_on_batch(noise, valid)
            print('%d [D loss: %f, acc.: %.2f%%] [G loss: %f]' % (epoch, d_loss[0], 100 * d_loss[1], g_loss))
            if epoch % save_interval == 0:
                self.save_imgs(epoch)

    def save_imgs(self, epoch):
        r, c = (5, 5)
        noise = np.random.normal(0, 1, (r * c, self.latent_dim))
        gen_imgs = self.generator.predict(noise)
        gen_imgs = 0.5 * gen_imgs + 0.5
        fig, axs = plt.subplots(r, c)
        cnt = 0
        for i in range(r):
            for j in range(c):
                axs[(i, j)].imshow((gen_imgs[cnt, :, :, 0]), cmap='gray')
                axs[(i, j)].axis('off')
                cnt += 1

        fig.savefig('images/mnist_%d.png' % epoch)
        plt.close()


class DUALGAN:

    def __init__(self):
        self.img_rows = 28
        self.img_cols = 28
        self.channels = 1
        self.img_dim = self.img_rows * self.img_cols
        optimizer = Adam(0.0002, 0.5)
        self.D_A = self.build_discriminator()
        self.D_A.compile(loss=(self.wasserstein_loss), optimizer=optimizer,
          metrics=[
         'accuracy'])
        self.D_B = self.build_discriminator()
        self.D_B.compile(loss=(self.wasserstein_loss), optimizer=optimizer,
          metrics=[
         'accuracy'])
        self.G_AB = self.build_generator()
        self.G_BA = self.build_generator()
        self.D_A.trainable = False
        self.D_B.trainable = False
        imgs_A = Input(shape=(self.img_dim,))
        imgs_B = Input(shape=(self.img_dim,))
        fake_B = self.G_AB(imgs_A)
        fake_A = self.G_BA(imgs_B)
        valid_A = self.D_A(fake_A)
        valid_B = self.D_B(fake_B)
        recov_A = self.G_BA(fake_B)
        recov_B = self.G_AB(fake_A)
        self.combined = Model(inputs=[imgs_A, imgs_B], outputs=[valid_A, valid_B, recov_A, recov_B])
        self.combined.compile(loss=[self.wasserstein_loss, self.wasserstein_loss, 'mae', 'mae'], optimizer=optimizer,
          loss_weights=[
         1, 1, 100, 100])

    def build_generator(self):
        X = Input(shape=(self.img_dim,))
        model = Sequential()
        model.add(Dense(256, input_dim=(self.img_dim)))
        model.add(LeakyReLU(alpha=0.2))
        model.add(BatchNormalization(momentum=0.8))
        model.add(Dropout(0.4))
        model.add(Dense(512))
        model.add(LeakyReLU(alpha=0.2))
        model.add(BatchNormalization(momentum=0.8))
        model.add(Dropout(0.4))
        model.add(Dense(1024))
        model.add(LeakyReLU(alpha=0.2))
        model.add(BatchNormalization(momentum=0.8))
        model.add(Dropout(0.4))
        model.add(Dense((self.img_dim), activation='tanh'))
        X_translated = model(X)
        return Model(X, X_translated)

    def build_discriminator(self):
        img = Input(shape=(self.img_dim,))
        model = Sequential()
        model.add(Dense(512, input_dim=(self.img_dim)))
        model.add(LeakyReLU(alpha=0.2))
        model.add(Dense(256))
        model.add(LeakyReLU(alpha=0.2))
        model.add(BatchNormalization(momentum=0.8))
        model.add(Dense(1))
        validity = model(img)
        return Model(img, validity)

    def sample_generator_input(self, X, batch_size):
        idx = np.random.randint(0, X.shape[0], batch_size)
        return X[idx]

    def wasserstein_loss(self, y_true, y_pred):
        return K.mean(y_true * y_pred)

    def train(self, epochs, batch_size=128, sample_interval=50):
        (X_train, _), (_, _) = mnist.load_data()
        X_train = (X_train.astype(np.float32) - 127.5) / 127.5
        X_A = X_train[:int(X_train.shape[0] / 2)]
        X_B = scipy.ndimage.interpolation.rotate((X_train[int(X_train.shape[0] / 2):]), 90, axes=(1,
                                                                                                  2))
        X_A = X_A.reshape(X_A.shape[0], self.img_dim)
        X_B = X_B.reshape(X_B.shape[0], self.img_dim)
        clip_value = 0.01
        n_critic = 4
        valid = -np.ones((batch_size, 1))
        fake = np.ones((batch_size, 1))
        for epoch in range(epochs):
            for _ in range(n_critic):
                imgs_A = self.sample_generator_input(X_A, batch_size)
                imgs_B = self.sample_generator_input(X_B, batch_size)
                fake_B = self.G_AB.predict(imgs_A)
                fake_A = self.G_BA.predict(imgs_B)
                D_A_loss_real = self.D_A.train_on_batch(imgs_A, valid)
                D_A_loss_fake = self.D_A.train_on_batch(fake_A, fake)
                D_B_loss_real = self.D_B.train_on_batch(imgs_B, valid)
                D_B_loss_fake = self.D_B.train_on_batch(fake_B, fake)
                D_A_loss = 0.5 * np.add(D_A_loss_real, D_A_loss_fake)
                D_B_loss = 0.5 * np.add(D_B_loss_real, D_B_loss_fake)
                for d in [self.D_A, self.D_B]:
                    for l in d.layers:
                        weights = l.get_weights()
                        weights = [np.clip(w, -clip_value, clip_value) for w in weights]
                        l.set_weights(weights)

            g_loss = self.combined.train_on_batch([imgs_A, imgs_B], [valid, valid, imgs_A, imgs_B])
            print('%d [D1 loss: %f] [D2 loss: %f] [G loss: %f]' % (
             epoch, D_A_loss[0], D_B_loss[0], g_loss[0]))
            if epoch % sample_interval == 0:
                self.save_imgs(epoch, X_A, X_B)

    def save_imgs(self, epoch, X_A, X_B):
        r, c = (4, 4)
        imgs_A = self.sample_generator_input(X_A, c)
        imgs_B = self.sample_generator_input(X_B, c)
        fake_B = self.G_AB.predict(imgs_A)
        fake_A = self.G_BA.predict(imgs_B)
        gen_imgs = np.concatenate([imgs_A, fake_B, imgs_B, fake_A])
        gen_imgs = gen_imgs.reshape((r, c, self.img_rows, self.img_cols, 1))
        gen_imgs = 0.5 * gen_imgs + 0.5
        fig, axs = plt.subplots(r, c)
        cnt = 0
        for i in range(r):
            for j in range(c):
                axs[(i, j)].imshow((gen_imgs[i, j, :, :, 0]), cmap='gray')
                axs[(i, j)].axis('off')
                cnt += 1

        fig.savefig('images/mnist_%d.png' % epoch)
        plt.close()


class INFOGAN:

    def __init__(self):
        self.img_rows = 28
        self.img_cols = 28
        self.channels = 1
        self.num_classes = 10
        self.img_shape = (self.img_rows, self.img_cols, self.channels)
        self.latent_dim = 72
        optimizer = Adam(0.0002, 0.5)
        losses = ['binary_crossentropy', self.mutual_info_loss]
        self.discriminator, self.auxilliary = self.build_disk_and_q_net()
        self.discriminator.compile(loss=['binary_crossentropy'], optimizer=optimizer,
          metrics=[
         'accuracy'])
        self.auxilliary.compile(loss=[self.mutual_info_loss], optimizer=optimizer,
          metrics=[
         'accuracy'])
        self.generator = self.build_generator()
        gen_input = Input(shape=(self.latent_dim,))
        img = self.generator(gen_input)
        self.discriminator.trainable = False
        valid = self.discriminator(img)
        target_label = self.auxilliary(img)
        self.combined = Model(gen_input, [valid, target_label])
        self.combined.compile(loss=losses, optimizer=optimizer)

    def build_generator(self):
        model = Sequential()
        model.add(Dense(6272, activation='relu', input_dim=(self.latent_dim)))
        model.add(Reshape((7, 7, 128)))
        model.add(BatchNormalization(momentum=0.8))
        model.add(UpSampling2D())
        model.add(Conv2D(128, kernel_size=3, padding='same'))
        model.add(Activation('relu'))
        model.add(BatchNormalization(momentum=0.8))
        model.add(UpSampling2D())
        model.add(Conv2D(64, kernel_size=3, padding='same'))
        model.add(Activation('relu'))
        model.add(BatchNormalization(momentum=0.8))
        model.add(Conv2D((self.channels), kernel_size=3, padding='same'))
        model.add(Activation('tanh'))
        gen_input = Input(shape=(self.latent_dim,))
        img = model(gen_input)
        model.summary()
        return Model(gen_input, img)

    def build_disk_and_q_net(self):
        img = Input(shape=(self.img_shape))
        model = Sequential()
        model.add(Conv2D(64, kernel_size=3, strides=2, input_shape=(self.img_shape), padding='same'))
        model.add(LeakyReLU(alpha=0.2))
        model.add(Dropout(0.25))
        model.add(Conv2D(128, kernel_size=3, strides=2, padding='same'))
        model.add(ZeroPadding2D(padding=((0, 1), (0, 1))))
        model.add(LeakyReLU(alpha=0.2))
        model.add(Dropout(0.25))
        model.add(BatchNormalization(momentum=0.8))
        model.add(Conv2D(256, kernel_size=3, strides=2, padding='same'))
        model.add(LeakyReLU(alpha=0.2))
        model.add(Dropout(0.25))
        model.add(BatchNormalization(momentum=0.8))
        model.add(Conv2D(512, kernel_size=3, strides=2, padding='same'))
        model.add(LeakyReLU(alpha=0.2))
        model.add(Dropout(0.25))
        model.add(BatchNormalization(momentum=0.8))
        model.add(Flatten())
        img_embedding = model(img)
        validity = Dense(1, activation='sigmoid')(img_embedding)
        q_net = Dense(128, activation='relu')(img_embedding)
        label = Dense((self.num_classes), activation='softmax')(q_net)
        return (
         Model(img, validity), Model(img, label))

    def mutual_info_loss(self, c, c_given_x):
        """The mutual information metric we aim to minimize"""
        eps = 1e-08
        conditional_entropy = K.mean(-K.sum((K.log(c_given_x + eps) * c), axis=1))
        entropy = K.mean(-K.sum((K.log(c + eps) * c), axis=1))
        return conditional_entropy + entropy

    def sample_generator_input(self, batch_size):
        sampled_noise = np.random.normal(0, 1, (batch_size, 62))
        sampled_labels = np.random.randint(0, self.num_classes, batch_size).reshape(-1, 1)
        sampled_labels = to_categorical(sampled_labels, num_classes=(self.num_classes))
        return (
         sampled_noise, sampled_labels)

    def train(self, epochs, batch_size=128, sample_interval=50):
        (X_train, y_train), (_, _) = mnist.load_data()
        X_train = (X_train.astype(np.float32) - 127.5) / 127.5
        X_train = np.expand_dims(X_train, axis=3)
        y_train = y_train.reshape(-1, 1)
        valid = np.ones((batch_size, 1))
        fake = np.zeros((batch_size, 1))
        for epoch in range(epochs):
            idx = np.random.randint(0, X_train.shape[0], batch_size)
            imgs = X_train[idx]
            sampled_noise, sampled_labels = self.sample_generator_input(batch_size)
            gen_input = np.concatenate((sampled_noise, sampled_labels), axis=1)
            gen_imgs = self.generator.predict(gen_input)
            d_loss_real = self.discriminator.train_on_batch(imgs, valid)
            d_loss_fake = self.discriminator.train_on_batch(gen_imgs, fake)
            d_loss = 0.5 * np.add(d_loss_real, d_loss_fake)
            g_loss = self.combined.train_on_batch(gen_input, [valid, sampled_labels])
            print('%d [D loss: %.2f, acc.: %.2f%%] [Q loss: %.2f] [G loss: %.2f]' % (
             epoch, d_loss[0], 100 * d_loss[1], g_loss[1], g_loss[2]))
            if epoch % sample_interval == 0:
                self.sample_images(epoch)

    def sample_images(self, epoch):
        r, c = (10, 10)
        fig, axs = plt.subplots(r, c)
        for i in range(c):
            sampled_noise, _ = self.sample_generator_input(c)
            label = to_categorical(np.full(fill_value=i, shape=(r, 1)), num_classes=(self.num_classes))
            gen_input = np.concatenate((sampled_noise, label), axis=1)
            gen_imgs = self.generator.predict(gen_input)
            gen_imgs = 0.5 * gen_imgs + 0.5
            for j in range(r):
                axs[(j, i)].imshow((gen_imgs[j, :, :, 0]), cmap='gray')
                axs[(j, i)].axis('off')

        fig.savefig('images/%d.png' % epoch)
        plt.close()

    def save_model(self):

        def save(model, model_name):
            model_path = 'saved_model/%s.json' % model_name
            weights_path = 'saved_model/%s_weights.hdf5' % model_name
            options = {'file_arch':model_path,  'file_weight':weights_path}
            json_string = model.to_json()
            open(options['file_arch'], 'w').write(json_string)
            model.save_weights(options['file_weight'])

        save(self.generator, 'generator')
        save(self.discriminator, 'discriminator')


class LSGAN:

    def __init__(self):
        self.img_rows = 28
        self.img_cols = 28
        self.channels = 1
        self.img_shape = (self.img_rows, self.img_cols, self.channels)
        self.latent_dim = 100
        optimizer = Adam(0.0002, 0.5)
        self.discriminator = self.build_discriminator()
        self.discriminator.compile(loss='mse', optimizer=optimizer,
          metrics=[
         'accuracy'])
        self.generator = self.build_generator()
        z = Input(shape=(self.latent_dim,))
        img = self.generator(z)
        self.discriminator.trainable = False
        valid = self.discriminator(img)
        self.combined = Model(z, valid)
        self.combined.compile(loss='mse', optimizer=optimizer)

    def build_generator(self):
        model = Sequential()
        model.add(Dense(256, input_dim=(self.latent_dim)))
        model.add(LeakyReLU(alpha=0.2))
        model.add(BatchNormalization(momentum=0.8))
        model.add(Dense(512))
        model.add(LeakyReLU(alpha=0.2))
        model.add(BatchNormalization(momentum=0.8))
        model.add(Dense(1024))
        model.add(LeakyReLU(alpha=0.2))
        model.add(BatchNormalization(momentum=0.8))
        model.add(Dense((np.prod(self.img_shape)), activation='tanh'))
        model.add(Reshape(self.img_shape))
        model.summary()
        noise = Input(shape=(self.latent_dim,))
        img = model(noise)
        return Model(noise, img)

    def build_discriminator(self):
        model = Sequential()
        model.add(Flatten(input_shape=(self.img_shape)))
        model.add(Dense(512))
        model.add(LeakyReLU(alpha=0.2))
        model.add(Dense(256))
        model.add(LeakyReLU(alpha=0.2))
        model.add(Dense(1))
        model.summary()
        img = Input(shape=(self.img_shape))
        validity = model(img)
        return Model(img, validity)

    def train(self, epochs, batch_size=128, sample_interval=50):
        (X_train, _), (_, _) = mnist.load_data()
        X_train = (X_train.astype(np.float32) - 127.5) / 127.5
        X_train = np.expand_dims(X_train, axis=3)
        valid = np.ones((batch_size, 1))
        fake = np.zeros((batch_size, 1))
        for epoch in range(epochs):
            idx = np.random.randint(0, X_train.shape[0], batch_size)
            imgs = X_train[idx]
            noise = np.random.normal(0, 1, (batch_size, self.latent_dim))
            gen_imgs = self.generator.predict(noise)
            d_loss_real = self.discriminator.train_on_batch(imgs, valid)
            d_loss_fake = self.discriminator.train_on_batch(gen_imgs, fake)
            d_loss = 0.5 * np.add(d_loss_real, d_loss_fake)
            g_loss = self.combined.train_on_batch(noise, valid)
            print('%d [D loss: %f, acc.: %.2f%%] [G loss: %f]' % (epoch, d_loss[0], 100 * d_loss[1], g_loss))
            if epoch % sample_interval == 0:
                self.sample_images(epoch)

    def sample_images(self, epoch):
        r, c = (5, 5)
        noise = np.random.normal(0, 1, (r * c, self.latent_dim))
        gen_imgs = self.generator.predict(noise)
        gen_imgs = 0.5 * gen_imgs + 0.5
        fig, axs = plt.subplots(r, c)
        cnt = 0
        for i in range(r):
            for j in range(c):
                axs[(i, j)].imshow((gen_imgs[cnt, :, :, 0]), cmap='gray')
                axs[(i, j)].axis('off')
                cnt += 1

        fig.savefig('images/mnist_%d.png' % epoch)
        plt.close()


class SGAN:

    def __init__(self):
        self.img_rows = 28
        self.img_cols = 28
        self.channels = 1
        self.img_shape = (self.img_rows, self.img_cols, self.channels)
        self.num_classes = 10
        self.latent_dim = 100
        optimizer = Adam(0.0002, 0.5)
        self.discriminator = self.build_discriminator()
        self.discriminator.compile(loss=[
         'binary_crossentropy', 'categorical_crossentropy'],
          loss_weights=[
         0.5, 0.5],
          optimizer=optimizer,
          metrics=[
         'accuracy'])
        self.generator = self.build_generator()
        noise = Input(shape=(100, ))
        img = self.generator(noise)
        self.discriminator.trainable = False
        valid, _ = self.discriminator(img)
        self.combined = Model(noise, valid)
        self.combined.compile(loss=['binary_crossentropy'], optimizer=optimizer)

    def build_generator(self):
        model = Sequential()
        model.add(Dense(6272, activation='relu', input_dim=(self.latent_dim)))
        model.add(Reshape((7, 7, 128)))
        model.add(BatchNormalization(momentum=0.8))
        model.add(UpSampling2D())
        model.add(Conv2D(128, kernel_size=3, padding='same'))
        model.add(Activation('relu'))
        model.add(BatchNormalization(momentum=0.8))
        model.add(UpSampling2D())
        model.add(Conv2D(64, kernel_size=3, padding='same'))
        model.add(Activation('relu'))
        model.add(BatchNormalization(momentum=0.8))
        model.add(Conv2D(1, kernel_size=3, padding='same'))
        model.add(Activation('tanh'))
        model.summary()
        noise = Input(shape=(self.latent_dim,))
        img = model(noise)
        return Model(noise, img)

    def build_discriminator(self):
        model = Sequential()
        model.add(Conv2D(32, kernel_size=3, strides=2, input_shape=(self.img_shape), padding='same'))
        model.add(LeakyReLU(alpha=0.2))
        model.add(Dropout(0.25))
        model.add(Conv2D(64, kernel_size=3, strides=2, padding='same'))
        model.add(ZeroPadding2D(padding=((0, 1), (0, 1))))
        model.add(LeakyReLU(alpha=0.2))
        model.add(Dropout(0.25))
        model.add(BatchNormalization(momentum=0.8))
        model.add(Conv2D(128, kernel_size=3, strides=2, padding='same'))
        model.add(LeakyReLU(alpha=0.2))
        model.add(Dropout(0.25))
        model.add(BatchNormalization(momentum=0.8))
        model.add(Conv2D(256, kernel_size=3, strides=1, padding='same'))
        model.add(LeakyReLU(alpha=0.2))
        model.add(Dropout(0.25))
        model.add(Flatten())
        model.summary()
        img = Input(shape=(self.img_shape))
        features = model(img)
        valid = Dense(1, activation='sigmoid')(features)
        label = Dense((self.num_classes + 1), activation='softmax')(features)
        return Model(img, [valid, label])

    def train(self, epochs, batch_size=128, sample_interval=50):
        (X_train, y_train), (_, _) = mnist.load_data()
        X_train = (X_train.astype(np.float32) - 127.5) / 127.5
        X_train = np.expand_dims(X_train, axis=3)
        y_train = y_train.reshape(-1, 1)
        half_batch = batch_size // 2
        cw1 = {0:1,  1:1}
        cw2 = {i:self.num_classes / half_batch for i in range(self.num_classes)}
        cw2[self.num_classes] = 1 / half_batch
        valid = np.ones((batch_size, 1))
        fake = np.zeros((batch_size, 1))
        for epoch in range(epochs):
            idx = np.random.randint(0, X_train.shape[0], batch_size)
            imgs = X_train[idx]
            noise = np.random.normal(0, 1, (batch_size, self.latent_dim))
            gen_imgs = self.generator.predict(noise)
            labels = to_categorical((y_train[idx]), num_classes=(self.num_classes + 1))
            fake_labels = to_categorical((np.full((batch_size, 1), self.num_classes)), num_classes=(self.num_classes + 1))
            d_loss_real = self.discriminator.train_on_batch(imgs, [valid, labels], class_weight=[cw1, cw2])
            d_loss_fake = self.discriminator.train_on_batch(gen_imgs, [fake, fake_labels], class_weight=[cw1, cw2])
            d_loss = 0.5 * np.add(d_loss_real, d_loss_fake)
            g_loss = self.combined.train_on_batch(noise, valid, class_weight=[cw1, cw2])
            print('%d [D loss: %f, acc: %.2f%%, op_acc: %.2f%%] [G loss: %f]' % (
             epoch, d_loss[0], 100 * d_loss[3], 100 * d_loss[4], g_loss))
            if epoch % sample_interval == 0:
                self.sample_images(epoch)

    def sample_images(self, epoch):
        r, c = (5, 5)
        noise = np.random.normal(0, 1, (r * c, self.latent_dim))
        gen_imgs = self.generator.predict(noise)
        gen_imgs = 0.5 * gen_imgs + 0.5
        fig, axs = plt.subplots(r, c)
        cnt = 0
        for i in range(r):
            for j in range(c):
                axs[(i, j)].imshow((gen_imgs[cnt, :, :, 0]), cmap='gray')
                axs[(i, j)].axis('off')
                cnt += 1

        fig.savefig('images/mnist_%d.png' % epoch)
        plt.close()

    def save_model(self):

        def save(model, model_name):
            model_path = 'saved_model/%s.json' % model_name
            weights_path = 'saved_model/%s_weights.hdf5' % model_name
            options = {'file_arch':model_path,  'file_weight':weights_path}
            json_string = model.to_json()
            open(options['file_arch'], 'w').write(json_string)
            model.save_weights(options['file_weight'])

        save(self.generator, 'mnist_sgan_generator')
        save(self.discriminator, 'mnist_sgan_discriminator')
        save(self.combined, 'mnist_sgan_adversarial')


class WGAN:

    def __init__(self):
        self.img_rows = 28
        self.img_cols = 28
        self.channels = 1
        self.img_shape = (self.img_rows, self.img_cols, self.channels)
        self.latent_dim = 100
        self.n_critic = 5
        self.clip_value = 0.01
        optimizer = RMSprop(lr=5e-05)
        self.critic = self.build_critic()
        self.critic.compile(loss=(self.wasserstein_loss), optimizer=optimizer,
          metrics=[
         'accuracy'])
        self.generator = self.build_generator()
        z = Input(shape=(self.latent_dim,))
        img = self.generator(z)
        self.critic.trainable = False
        valid = self.critic(img)
        self.combined = Model(z, valid)
        self.combined.compile(loss=(self.wasserstein_loss), optimizer=optimizer,
          metrics=[
         'accuracy'])

    def wasserstein_loss(self, y_true, y_pred):
        return K.mean(y_true * y_pred)

    def build_generator(self):
        model = Sequential()
        model.add(Dense(6272, activation='relu', input_dim=(self.latent_dim)))
        model.add(Reshape((7, 7, 128)))
        model.add(UpSampling2D())
        model.add(Conv2D(128, kernel_size=4, padding='same'))
        model.add(BatchNormalization(momentum=0.8))
        model.add(Activation('relu'))
        model.add(UpSampling2D())
        model.add(Conv2D(64, kernel_size=4, padding='same'))
        model.add(BatchNormalization(momentum=0.8))
        model.add(Activation('relu'))
        model.add(Conv2D((self.channels), kernel_size=4, padding='same'))
        model.add(Activation('tanh'))
        model.summary()
        noise = Input(shape=(self.latent_dim,))
        img = model(noise)
        return Model(noise, img)

    def build_critic(self):
        model = Sequential()
        model.add(Conv2D(16, kernel_size=3, strides=2, input_shape=(self.img_shape), padding='same'))
        model.add(LeakyReLU(alpha=0.2))
        model.add(Dropout(0.25))
        model.add(Conv2D(32, kernel_size=3, strides=2, padding='same'))
        model.add(ZeroPadding2D(padding=((0, 1), (0, 1))))
        model.add(BatchNormalization(momentum=0.8))
        model.add(LeakyReLU(alpha=0.2))
        model.add(Dropout(0.25))
        model.add(Conv2D(64, kernel_size=3, strides=2, padding='same'))
        model.add(BatchNormalization(momentum=0.8))
        model.add(LeakyReLU(alpha=0.2))
        model.add(Dropout(0.25))
        model.add(Conv2D(128, kernel_size=3, strides=1, padding='same'))
        model.add(BatchNormalization(momentum=0.8))
        model.add(LeakyReLU(alpha=0.2))
        model.add(Dropout(0.25))
        model.add(Flatten())
        model.add(Dense(1))
        model.summary()
        img = Input(shape=(self.img_shape))
        validity = model(img)
        return Model(img, validity)

    def train(self, epochs, batch_size=128, sample_interval=50):
        (X_train, _), (_, _) = mnist.load_data()
        X_train = (X_train.astype(np.float32) - 127.5) / 127.5
        X_train = np.expand_dims(X_train, axis=3)
        valid = -np.ones((batch_size, 1))
        fake = np.ones((batch_size, 1))
        for epoch in range(epochs):
            for _ in range(self.n_critic):
                idx = np.random.randint(0, X_train.shape[0], batch_size)
                imgs = X_train[idx]
                noise = np.random.normal(0, 1, (batch_size, self.latent_dim))
                gen_imgs = self.generator.predict(noise)
                d_loss_real = self.critic.train_on_batch(imgs, valid)
                d_loss_fake = self.critic.train_on_batch(gen_imgs, fake)
                d_loss = 0.5 * np.add(d_loss_fake, d_loss_real)
                for l in self.critic.layers:
                    weights = l.get_weights()
                    weights = [np.clip(w, -self.clip_value, self.clip_value) for w in weights]
                    l.set_weights(weights)

            g_loss = self.combined.train_on_batch(noise, valid)
            print('%d [D loss: %f] [G loss: %f]' % (epoch, 1 - d_loss[0], 1 - g_loss[0]))
            if epoch % sample_interval == 0:
                self.sample_images(epoch)

    def sample_images(self, epoch):
        r, c = (5, 5)
        noise = np.random.normal(0, 1, (r * c, self.latent_dim))
        gen_imgs = self.generator.predict(noise)
        gen_imgs = 0.5 * gen_imgs + 0.5
        fig, axs = plt.subplots(r, c)
        cnt = 0
        for i in range(r):
            for j in range(c):
                axs[(i, j)].imshow((gen_imgs[cnt, :, :, 0]), cmap='gray')
                axs[(i, j)].axis('off')
                cnt += 1

        fig.savefig('images/mnist_%d.png' % epoch)
        plt.close()