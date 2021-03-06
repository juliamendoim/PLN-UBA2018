"""Evaulate a Sentiment Analysis model.

Usage:
  eval.py -i <file> [-f]
  eval.py -h | --help

Options:
  -i <file>     Trained model file.
  -f --final    Use final test set instead of development.
  -h --help     Show this screen.
"""
from docopt import docopt
import pickle
from pprint import pprint
from collections import defaultdict

from sentiment.evaluator import Evaluator
from sentiment.tass import InterTASSReader

if __name__ == '__main__':
    opts = docopt(__doc__)

    # load model
    filename = opts['-i']
    f = open(filename, 'rb')
    model = pickle.load(f)
    f.close()

    # load corpus
    if not opts['--final']:
        reader = InterTASSReader('TASS/InterTASS/TASS2017_T1_development.xml')
    else:
        reader = InterTASSReader(
            'TASS/InterTASS/TASS2017_T1_test.xml',
            'TASS/InterTASS/TASS2017_T1_test_res.qrel')
    X, y_true = list(reader.X()), list(reader.y())

    # classify
    y_pred = model.predict(X)

    # evaluate and print
    evaluator = Evaluator()
    evaluator.evaluate(y_true, y_pred)
    evaluator.print_results()
    evaluator.print_confusion_matrix()

    # detailed confusion matrix, for result analysis
    cm_items = defaultdict(list)
    for i, (true, pred) in enumerate(zip(y_true, y_pred)):
        cm_items[true, pred] += [i]
