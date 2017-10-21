import os
import math
import pickle
import string
from config import DATA_PATH
import language_check


tool = language_check.LanguageTool('en-US')
model_data = pickle.load(open(os.path.join(DATA_PATH, "gib_model.pki"), "rb"))
accepted_chars = 'abcdefghijklmnopqrstuvwxyz '
pos = dict([(char, idx) for idx, char in enumerate(accepted_chars)])


def normalize(line):
    """ Return only the subset of chars from accepted_chars.
    This helps keep the  model relatively small by ignoring punctuation,
    infrequenty symbols, etc. """
    return [c.lower() for c in line if c.lower() in accepted_chars]


def ngram(n, l):
    """Return all n grams from l after normalizing."""
    filtered = normalize(l)
    for start in range(0, len(filtered) - n + 1):
        yield ''.join(filtered[start:start + n])


def avg_transition_prob(l, log_prob_mat):
    """ Return the average transition prob from l through log_prob_mat. """
    log_prob = 0.0
    transition_ct = 0
    for a, b in ngram(2, l):
        log_prob += log_prob_mat[pos[a]][pos[b]]
        transition_ct += 1
    # The exponentiation translates from log probs to probs.
    return math.exp(log_prob / (transition_ct or 1))


def check_all_errors(actual_resp, expected_resp):
    model_mat = model_data['mat']
    threshold = model_data['thresh']
    if actual_resp == "" or actual_resp is None:
        return "Nothing entered"
    if "\n" in actual_resp:
        actual_resp = actual_resp.replace('\n', ' ')
    error = False
    text = ""
    if (avg_transition_prob(actual_resp, model_mat) < threshold):
        text += "The sentence is Gibberish.\n"
        error = True
    # check for puntuation
    # 1. ensure that the response is not empty
    # 2. only check puntation for responses longer than 1 word
    # 3. check the end of the response to see if it has a puntation
    if len(actual_resp) > 0 and len(actual_resp.split()) > 1 and actual_resp[-1] not in string.punctuation:
        text += "The sentence is not properly punctuated.\n"
        error = True
    matches = tool.check(actual_resp)
    if len(matches) > 0:
        for m in matches:
            msg = bytes(m.msg, 'utf-8').decode('utf-8', 'ignore')
            if msg == "This sentence does not start with an uppercase letter" and expected_resp[0].islower():
                continue
            text += msg + "\n"
            error = True
    if not error:
        text = "NO ERRORS!!"
    return text.strip('\n')
