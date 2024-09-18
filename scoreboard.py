import pickle


def get_persistent_storage():
    scores = {}
    try:
        scores = pickle.load(open('high_score.pk', 'rb'))
    except Exception as ex:
        print('Scores not found. Ex = ', ex)
    return scores


def load_high_score(level):
    return get_persistent_storage().get(level, 0)


def dump_high_score(level, score):
    scores = get_persistent_storage()
    scores[level] = max(scores.get(level, 0), score)
    try:
        pickle.dump(scores, open('high_score.pk', 'wb'))
    except Exception as ex:
        print('Scores could not be saved. Ex = ', ex)
