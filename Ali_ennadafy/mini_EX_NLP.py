import collections
import re
import matplotlib.pyplot as plt
import nltk
import numpy as np
import pandas as pd
from tensorflow.keras.preprocessing.text import Tokenizer  # type: ignore
from nltk.corpus import stopwords
from sklearn.model_selection import train_test_split

nltk.download('stopwords')

NB_WORDS = 10000
NB_START_EPOCHS = 20
BATCH_SIZE = 512
MAX_LEN = 20


def deep_model(model, X_train, y_train, X_valid, y_valid):
    model.compile(
        optimizer='rmsprop',
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )
    history = model.fit(
        X_train, y_train,
        epochs=NB_START_EPOCHS,
        batch_size=BATCH_SIZE,
        validation_data=(X_valid, y_valid),
        verbose=0
    )
    return history


def eval_metric(model, history, metric_name):
    metric = history.history[metric_name]
    val_metric = history.history['val_' + metric_name]
    e = range(1, NB_START_EPOCHS + 1)
    plt.plot(e, metric, 'bo', label='Apprentissage ' + metric_name)
    plt.plot(e, val_metric, 'b', label='Validation ' + metric_name)
    plt.xlabel('Epoch number')
    plt.ylabel(metric_name)
    plt.title('Comparaison entre apprentissage et validation ' + metric_name + ' for ' + model.name)
    plt.legend()
    plt.show()


def test_model(model, X_train, y_train, X_test, y_test, epoch_stop):
    model.fit(
        X_train, y_train,
        epochs=epoch_stop,
        batch_size=BATCH_SIZE,
        verbose=0
    )
    results = model.evaluate(X_test, y_test)
    print()
    print('Test accuracy: {0:.2f}%'.format(results[1] * 100))
    return results


def compare_models_by_metric(model_1, model_2, model_hist_1, model_hist_2, metric):
    metric_model_1 = model_hist_1.history[metric]
    metric_model_2 = model_hist_2.history[metric]
    e = range(1, NB_START_EPOCHS + 1)
    metrics_dict = {
        'acc': 'Accuracy Apprentissage',
        'loss': 'Loss Apprentissage',
        'val_acc': 'Accuracy Validation',
        'val_loss': 'Loss Validation'
    }
    metric_label = metrics_dict[metric]
    plt.plot(e, metric_model_1, 'ro', label=model_1.name)
    plt.plot(e, metric_model_2, 'r', label=model_2.name)
    plt.xlabel('Nombre Epoques')
    plt.ylabel(metric_label)
    plt.title('Comparaison de ' + metric_label + ' entre les modèles')
    plt.legend()
    plt.show()


def optimal_epoch(model_hist):
    min_epoch = np.argmin(model_hist.history['val_loss']) + 1
    print("Perte de validation minimale atteinte à l'époque {}".format(min_epoch))
    return min_epoch


def remove_stopwords(input_text):
    stopwords_list = stopwords.words('english')
    whitelist = ["n't", "not", "no"]
    words = input_text.split()
    clean_words = [word for word in words if (word not in stopwords_list or word in whitelist) and len(word) > 1]
    return " ".join(clean_words)


def remove_mentions(input_text):
    return re.sub(r'@\w+', '', input_text)


df = pd.read_csv('Tweets.csv')

print("Les colonnes disponibles dans le fichier CSV :", df.columns.tolist())

target_col = None
for col in df.columns:
    if 'sentiment' in col.lower() or 'target' in col.lower():
        target_col = col
        break

if target_col is None:
    target_col = df.columns[1]

print("La colonne cible utilisée est :", target_col)

df = df[['text', target_col]]

df = df.dropna(subset=['text', target_col])

df['text'] = df['text'].astype(str).apply(remove_mentions)
df['text'] = df['text'].apply(remove_stopwords)

df = df.reindex(np.random.permutation(df.index))

X = df['text']
y = df[target_col]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=42)

print("Taille de X_train:", len(X_train))
print("Taille de X_test:", len(X_test))

tk = Tokenizer(
    num_words=NB_WORDS,
    filters='!"#$%&()*+,-./:;<=>?@[\\]^_`{|}~\t\n',
    lower=True,
    char_level=False,
    split=' '
)
tk.fit_on_texts(X_train)

print('Ajustement du tokenizer sur {} documents'.format(tk.document_count))
print('{} mots du dictionnaire'.format(tk.num_words))