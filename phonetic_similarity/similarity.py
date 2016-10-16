from libs.phonetic_similarity import data

phone_memory = {}
distance_memory = {}
distance_memory_unweighted = {}


def _get_vector(phones):
    global phone_memory
    try:
        if not phones:
            raise ValueError("No phone passed in")
        if len(phones) == 1:
            return data.phone_features[phones]
        else:
            if phone_memory.get(phones):
                return phone_memory[phones]
            vec = [None] * data.NUM_FEATURES
            # Combine the feature vectors
            mods = []
            for i in range(data.NUM_FEATURES):
                val = None
                for phone in phones:
                    if phone in data.modifiers:
                        mods.append(data.modifiers[phone])
                    else:
                        p_val = data.phone_features[phone][i]
                        if p_val is True:
                            val = True
                            break
                        elif p_val is False:
                            val = False
                vec[i] = val
            for mod in mods:
                for i, v in mod.items():
                    vec[i] = v
            phone_memory = {phones: vec}
            return vec
    except KeyError as e:
        raise ValueError("Unrecognized phone %s" % str(e))


def similarity(phoneA, phoneB, weighted=True):
    global distance_memory
    global distance_memory_unweighted
    mem = distance_memory if weighted else distance_memory_unweighted
    memA = mem.get(phoneA)
    if memA:
        memB = memA.get(phoneB)
        if memB:
            return memB
    else:
        mem[phoneA] = {}
        memA = distance_memory[phoneA]
    vecA = _get_vector(phoneA)
    vecB = _get_vector(phoneB)
    weights = data.feature_weights if weighted else \
        [1 / data.NUM_FEATURES] * data.NUM_FEATURES
    score = 0
    notApplicableRatio = 0
    for i in range(data.NUM_FEATURES):
        if vecA[i] is None and vecB[i] is None:
            notApplicableRatio += weights[i]
        elif vecA[i] == vecB[i]:
            score += weights[i]
    if notApplicableRatio > 0:
        # Enlarge the score by the inverse of the N/A ratio
        score *= 1 / (1 - notApplicableRatio)
    # Floating point errors
    score = min(score, 1)
    memA[phoneB] = score
    return min(score, 1)
