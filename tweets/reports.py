import matplotlib.pyplot as plt
from wordcloud import WordCloud


def build_wordcloud(text, filename=None):
    wc = WordCloud(max_font_size=40).generate(text)
    plt.figure()
    plt.imshow(wc, interpolation="bilinear")
    plt.axis("off")

    if filename is not None:
        plt.savefig(filename)
    else:
        plt.show()


def score_piechart(df, field='score', title='', filename=None):
    labels = df.groupby(field).count().index.values
    values = df.groupby(field).size().values

    plt.figure()
    plt.pie(values, labels=labels)
    plt.title(title)

    if filename is not None:
        plt.savefig(filename)
    else:
        plt.show()


def polarity_histogram(df, field='polarity', title='', bins=5, filename=None):

    negative = df[df[field] < 0][field]
    positive = df[df[field] > 0][field].values

    plt.figure()

    plt.hist(negative, bins=bins)
    plt.hist(positive, bins=bins)

    plt.title(title)

    if filename is not None:
        plt.savefig(filename)
    else:
        plt.show()
