"""Generate sample PDF docs for testing the pipeline.

Content is based on Python stdlib and scikit-learn documentation topics.
"""

import fitz
from pathlib import Path

DOCS_DIR = Path("data/sample_docs")
DOCS_DIR.mkdir(parents=True, exist_ok=True)

DOCS = {
    "python_collections.pdf": [
        """Python Collections Module

The collections module provides alternatives to Python's general-purpose built-in containers: dict, list, set, and tuple.

namedtuple()
Factory function for creating tuple subclasses with named fields. Named tuples assign meaning to each position in a tuple and allow for more readable, self-documenting code. They can be used wherever regular tuples are used, and they add the ability to access fields by name instead of position index.

from collections import namedtuple
Point = namedtuple('Point', ['x', 'y'])
p = Point(11, y=22)
print(p[0] + p[1])  # 33
print(p.x + p.y)    # 33

Named tuples are especially useful for assigning field names to result tuples returned by the csv or sqlite3 modules.""",

        """deque Objects

class collections.deque([iterable[, maxlen]])
Returns a new deque object initialized left-to-right with data from iterable. If iterable is not specified, the new deque is empty. Deques are a generalization of stacks and queues. Deques support thread-safe, memory efficient appends and pops from either side of the deque with approximately the same O(1) performance in either direction.

If maxlen is not specified or is None, deques may grow to an arbitrary length. Otherwise, the deque is bounded to the specified maximum length. Once a bounded length deque is full, when new items are added, a corresponding number of items are discarded from the opposite end.

deque.append(x): Add x to the right side of the deque.
deque.appendleft(x): Add x to the left side of the deque.
deque.clear(): Remove all elements from the deque.
deque.count(x): Count the number of deque elements equal to x.
deque.extend(iterable): Extend the right side of the deque by appending elements from the iterable.
deque.pop(): Remove and return an element from the right side of the deque. If no elements are present, raises an IndexError.
deque.popleft(): Remove and return an element from the left side of the deque. If no elements are present, raises an IndexError.
deque.rotate(n=1): Rotate the deque n steps to the right. If n is negative, rotate to the left.""",

        """Counter Objects

A Counter is a dict subclass for counting hashable objects. It is a collection where elements are stored as dictionary keys and their counts are stored as dictionary values.

from collections import Counter
cnt = Counter()
for word in ['red', 'blue', 'red', 'green', 'blue', 'blue']:
    cnt[word] += 1
print(cnt)  # Counter({'blue': 3, 'red': 2, 'green': 1})

Elements are counted from an iterable or initialized from another mapping (or counter):
c = Counter('gallahad')      # from an iterable
c = Counter({'red': 4})      # from a mapping
c = Counter(cats=4, dogs=8)  # from keyword args

Counter objects have a dictionary interface except that they return a zero count for missing items instead of raising a KeyError.

most_common([n]): Return a list of the n most common elements and their counts. If n is omitted or None, most_common() returns all elements.

subtract([iterable-or-mapping]): Elements are subtracted from an iterable or from another mapping. Like dict.update() but subtracts counts instead of replacing them.""",

        """OrderedDict Objects

Ordered dictionaries are just like regular dictionaries but have some extra capabilities relating to ordering operations. They have become less important now that the built-in dict class gained the ability to remember insertion order (this new behavior was guaranteed in Python 3.7).

Some differences from dict still remain:
- Regular dict was designed to be very good at mapping operations. Tracking insertion order was secondary.
- The OrderedDict was designed to be good at reordering operations. Space efficiency, iteration speed, and the performance of update operations were secondary.
- The OrderedDict algorithm can handle frequent reorder operations better than dict.

move_to_end(key, last=True): Move an existing key to either end of an ordered dictionary. The item is moved to the right end if last is true (the default) or to the beginning if last is false. Raises KeyError if the key does not exist.

popitem(last=True): Return and remove a (key, value) pair. Pairs are returned in LIFO order if last is true or FIFO order if last is false.""",

        """defaultdict Objects

class collections.defaultdict([default_factory[, ...]])
Returns a new dictionary-like object. defaultdict is a subclass of the built-in dict class. It overrides one method and adds one writable instance variable. The remaining functionality is the same as for the dict class.

The first argument provides the initial value for the default_factory attribute; it defaults to None. All remaining arguments are treated the same as if they were passed to the dict constructor.

defaultdict objects support the following method in addition to the standard dict operations:

__missing__(key): If the default_factory attribute is None, this raises a KeyError exception with the key as argument. If default_factory is not None, it is called without arguments to provide a default value for the given key, this value is inserted in the dictionary for the key, and returned.

Using list as the default_factory:
s = [('yellow', 1), ('blue', 2), ('yellow', 3)]
d = defaultdict(list)
for k, v in s:
    d[k].append(v)
# d = defaultdict(<class 'list'>, {'yellow': [1, 3], 'blue': [2]})""",
    ],
    "python_itertools.pdf": [
        """Python itertools Module

The itertools module standardizes a core set of fast, memory efficient tools that are useful by themselves or in combination. Together, they form an iterator algebra making it possible to construct specialized tools succinctly and efficiently in pure Python.

Infinite Iterators:
count(start=0, step=1): Make an iterator that returns evenly spaced values starting with number start.
cycle(iterable): Make an iterator returning elements from the iterable and saving a copy of each.
repeat(object[, times]): Make an iterator that returns object over and over again.

Iterators terminating on the shortest input sequence:
accumulate(iterable[, func, *, initial=None]): Make an iterator that returns accumulated sums, or accumulated results of other binary functions.
chain(*iterables): Make an iterator that returns elements from the first iterable until it is exhausted, then proceeds to the next iterable.
chain.from_iterable(iterable): Alternate constructor for chain(). Gets chained inputs from a single iterable argument.""",

        """compress(data, selectors): Make an iterator that filters elements from data returning only those that have a corresponding element in selectors that evaluates to True.

dropwhile(predicate, iterable): Make an iterator that drops elements from the iterable as long as the predicate is true; afterwards, returns every element.

filterfalse(predicate, iterable): Make an iterator that filters elements from iterable returning only those for which the predicate is False.

groupby(iterable, key=None): Make an iterator that returns consecutive keys and groups from the iterable. The key is a function computing a key value for each element. If not supplied or is None, key defaults to an identity function.

islice(iterable, stop) or islice(iterable, start, stop[, step]): Make an iterator that returns selected elements from the iterable. Works like slice() but does not support negative values for start, stop, or step.

pairwise(iterable): Return successive overlapping pairs taken from the input iterable. New in Python 3.10.

starmap(function, iterable): Make an iterator that computes the function using arguments obtained from the iterable. Used instead of map() when argument parameters are already grouped in tuples from a single iterable.""",

        """Combinatoric Iterators

product(*iterables, repeat=1): Cartesian product of input iterables. Equivalent to nested for-loops. For example, product(A, B) returns the same as ((x,y) for x in A for y in B).

permutations(iterable, r=None): Return successive r length permutations of elements in the iterable. If r is not specified or is None, then r defaults to the length of the iterable and all possible full-length permutations are generated.

combinations(iterable, r): Return r length subsequences of elements from the input iterable. Combinations are emitted in lexicographic sort order.

combinations_with_replacement(iterable, r): Return r length subsequences of elements from the input iterable allowing individual elements to be repeated more than once.

Example usage:
from itertools import combinations
list(combinations('ABCD', 2))
# [('A', 'B'), ('A', 'C'), ('A', 'D'), ('B', 'C'), ('B', 'D'), ('C', 'D')]

from itertools import permutations
list(permutations('ABC', 2))
# [('A', 'B'), ('A', 'C'), ('B', 'A'), ('B', 'C'), ('C', 'A'), ('C', 'B')]""",
    ],
    "python_functools.pdf": [
        """Python functools Module

The functools module is for higher-order functions: functions that act on or return other functions. In general, any callable object can be treated as a function for the purposes of this module.

functools.cache(user_function)
Simple lightweight unbounded function cache. Sometimes called memoize. Returns the same as lru_cache(maxsize=None), creating a thin wrapper around a dictionary lookup for the function arguments. Because it never needs to evict old values, this is smaller and faster than lru_cache() with a size limit. New in Python 3.9.

@cache
def factorial(n):
    return n * factorial(n-1) if n else 1

factorial(10)      # no previously cached result, makes 11 recursive calls
factorial(5)       # just looks up cached value result
factorial(12)      # makes two new recursive calls, the other 10 are cached""",

        """functools.lru_cache(maxsize=128, typed=False)
Decorator to wrap a function with a memoizing callable that saves up to the maxsize most recent calls. It can save time when an expensive or I/O bound function is periodically called with the same arguments.

Since a dictionary is used to cache results, the positional and keyword arguments to the function must be hashable.

If maxsize is set to None, the LRU feature is disabled and the cache can grow without bound.

If typed is set to true, function arguments of different types will be cached separately. For example, f(3) and f(3.0) will be treated as distinct calls with distinct results.

@lru_cache(maxsize=256)
def count_vowels(sentence):
    return sum(sentence.count(vowel) for vowel in 'aeiou')

The wrapped function is instrumented with a cache_info() function that returns a named tuple showing hits, misses, maxsize and currsize.""",

        """functools.partial(func, /, *args, **keywords)
Return a new partial object which when called will behave like func called with the positional arguments args and keyword arguments keywords. If more arguments are supplied to the call, they are appended to args. If additional keyword arguments are supplied, they extend and override keywords.

from functools import partial
basetwo = partial(int, base=2)
basetwo.__doc__ = 'Convert base 2 string to int.'
basetwo('10010')  # 18

functools.reduce(function, iterable[, initializer])
Apply function of two arguments cumulatively to the items of iterable, from left to right, so as to reduce the iterable to a single value. The left argument, x, is the accumulated value and the right argument, y, is the update value from the iterable.

from functools import reduce
reduce(lambda x, y: x+y, [1, 2, 3, 4, 5])  # 15

functools.wraps(wrapped, assigned=WRAPPER_ASSIGNMENTS, updated=WRAPPER_UPDATES)
This is a convenience function for invoking update_wrapper() as a function decorator when defining a wrapper function. It is equivalent to partial(update_wrapper, wrapped=wrapped, assigned=assigned, updated=updated).""",

        """functools.singledispatch(func)
Transform a function into a single-dispatch generic function. To define a generic function, decorate it with the @singledispatch decorator. When defining a function using @singledispatch, note that the dispatch happens on the type of the first argument.

from functools import singledispatch

@singledispatch
def fun(arg, verbose=False):
    if verbose:
        print("Let me just say,", end=" ")
    print(arg)

@fun.register
def _(arg: int, verbose=False):
    if verbose:
        print("Strength in numbers, eh?", end=" ")
    print(arg)

@fun.register
def _(arg: list, verbose=False):
    if verbose:
        print("Enumerate this:")
    for i, elem in enumerate(arg):
        print(i, elem)

To add overloaded implementations to the function, use the register() attribute of the generic function. It is a decorator. For functions annotated with types, the decorator will infer the type of the first argument automatically.""",
    ],
    "sklearn_preprocessing.pdf": [
        """scikit-learn Preprocessing

The sklearn.preprocessing module includes scaling, centering, normalization, binarization methods.

StandardScaler
Standardize features by removing the mean and scaling to unit variance. The standard score of a sample x is calculated as z = (x - u) / s where u is the mean and s is the standard deviation.

from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

Centering and scaling happen independently on each feature by computing the relevant statistics on the samples in the training set. Mean and standard deviation are then stored to be used on later data using transform.

Important: always fit on training data only, then transform both train and test. Fitting on the full dataset before splitting leads to data leakage.""",

        """MinMaxScaler
Transform features by scaling each feature to a given range, default (0, 1).

The transformation is: X_std = (X - X.min) / (X.max - X.min)
X_scaled = X_std * (max - min) + min

from sklearn.preprocessing import MinMaxScaler
scaler = MinMaxScaler(feature_range=(0, 1))
X_scaled = scaler.fit_transform(X)

This estimator scales and translates each feature individually such that it is in the given range on the training set. This transformation is often used as an alternative to zero mean, unit variance scaling.

RobustScaler
Scale features using statistics that are not influenced by outliers. This Scaler removes the median and scales the data according to the quantile range (defaults to IQR: Interquartile Range). The IQR is the range between the 1st quartile (25th quantile) and the 3rd quartile (75th quantile).

Centering and scaling happen independently on each feature by computing the relevant statistics on the samples in the training set. Median and interquartile range are then stored to be used on later data using the transform method.""",

        """LabelEncoder
Encode target labels with value between 0 and n_classes-1. This transformer should be used to encode target values, i.e. y, and not the input X.

from sklearn.preprocessing import LabelEncoder
le = LabelEncoder()
le.fit([1, 2, 2, 6])
le.transform([1, 1, 2, 6])  # array([0, 0, 1, 2])
le.inverse_transform([0, 0, 1, 2])  # array([1, 1, 2, 6])

OneHotEncoder
Encode categorical features as a one-hot numeric array. The input to this transformer should be an array-like of integers or strings, denoting the values taken on by categorical features. The features are encoded using a one-hot encoding scheme, creating a binary column for each category and returning a sparse matrix or dense array.

from sklearn.preprocessing import OneHotEncoder
enc = OneHotEncoder(handle_unknown='ignore')
X = [['Male', 1], ['Female', 3], ['Female', 2]]
enc.fit(X)
enc.transform([['Female', 1], ['Male', 4]]).toarray()

PolynomialFeatures
Generate polynomial and interaction features. For example, if an input sample is two dimensional and of the form [a, b], the degree-2 polynomial features are [1, a, b, a^2, ab, b^2].""",

        """Normalization
Normalize samples individually to unit norm. Each sample with at least one non-zero component is rescaled independently of other samples so that its norm equals one.

from sklearn.preprocessing import normalize
X_normalized = normalize(X, norm='l2')

The function normalize provides a quick and easy way to perform this operation on a single array-like dataset. Common norms: l1, l2, max.

Binarization
Feature binarization is the process of thresholding numerical features to get boolean values.

from sklearn.preprocessing import Binarizer
binarizer = Binarizer(threshold=1.1)
binarizer.transform(X)

Discretization (KBinsDiscretizer)
Discretization transforms continuous features into discrete values. KBinsDiscretizer discretizes features into k bins. By default, the output is one-hot encoded into a sparse matrix and this can be configured with the encode parameter.

Strategies: uniform (all bins have identical widths), quantile (all bins have the same number of points), kmeans (values in each bin have the same nearest center of a 1D k-means cluster).""",
    ],
    "sklearn_model_selection.pdf": [
        """scikit-learn Model Selection

The sklearn.model_selection module provides tools for model selection, including cross-validation and hyperparameter tuning.

train_test_split
Split arrays or matrices into random train and test subsets. Quick utility that wraps input validation and next(ShuffleSplit().split(X, y)) and application to input data into a single call for splitting (and optionally subsampling) data in a oneliner.

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42
)

Parameters:
- test_size: proportion of the dataset to include in the test split (default 0.25)
- random_state: controls shuffling. Pass an int for reproducible output.
- shuffle: whether to shuffle the data before splitting (default True)
- stratify: if not None, data is split in a stratified fashion using this as the class labels""",

        """Cross-Validation

cross_val_score: Evaluate a score by cross-validation.

from sklearn.model_selection import cross_val_score
scores = cross_val_score(clf, X, y, cv=5, scoring='accuracy')
print(f"Accuracy: {scores.mean():.2f} (+/- {scores.std() * 2:.2f})")

KFold: Provides train/test indices to split data in train/test sets. Split dataset into k consecutive folds (without shuffling by default).

from sklearn.model_selection import KFold
kf = KFold(n_splits=5, shuffle=True, random_state=42)
for train_index, test_index in kf.split(X):
    X_train, X_test = X[train_index], X[test_index]

StratifiedKFold: Stratified K-Folds cross-validator. Provides train/test indices to split data in train/test sets. This cross-validation object is a variation of KFold that returns stratified folds. The folds are made by preserving the percentage of samples for each class.

RepeatedKFold: Repeated K-Fold cross validator. Repeats K-Fold n times with different randomization in each repetition.""",

        """GridSearchCV
Exhaustive search over specified parameter values for an estimator. The parameters of the estimator used to apply these methods are optimized by cross-validated grid-search over a parameter grid.

from sklearn.model_selection import GridSearchCV
param_grid = {'C': [0.1, 1, 10], 'kernel': ['rbf', 'linear']}
grid_search = GridSearchCV(SVC(), param_grid, cv=5, scoring='accuracy')
grid_search.fit(X_train, y_train)
print(grid_search.best_params_)
print(grid_search.best_score_)

RandomizedSearchCV
Randomized search on hyper parameters. In contrast to GridSearchCV, not all parameter values are tried out, but rather a fixed number of parameter settings is sampled from the specified distributions.

from sklearn.model_selection import RandomizedSearchCV
from scipy.stats import uniform, randint
param_dist = {'C': uniform(0.1, 10), 'kernel': ['rbf', 'linear']}
random_search = RandomizedSearchCV(SVC(), param_dist, n_iter=20, cv=5)
random_search.fit(X_train, y_train)

The number of parameter settings that are tried is given by n_iter. This is more efficient than GridSearchCV when the parameter space is large.""",

        """Learning Curves

learning_curve: Determine cross-validated training and test scores for different training set sizes.

from sklearn.model_selection import learning_curve
train_sizes, train_scores, test_scores = learning_curve(
    estimator, X, y, cv=5, n_jobs=-1,
    train_sizes=np.linspace(0.1, 1.0, 10)
)

This is useful to determine:
- How much the estimator benefits from more data (bias/variance tradeoff)
- Whether the estimator suffers from underfitting or overfitting

validation_curve: Determine training and test scores for varying parameter values. Compute scores for an estimator with different values of a single hyperparameter.

from sklearn.model_selection import validation_curve
param_range = np.logspace(-6, -1, 5)
train_scores, test_scores = validation_curve(
    SVC(), X, y, param_name="gamma", param_range=param_range, cv=5
)

TimeSeriesSplit: Time Series cross-validator. Provides train/test indices to split time series data samples in a fixed way. Each fold keeps the temporal order.""",
    ],
    "sklearn_metrics.pdf": [
        """scikit-learn Metrics

The sklearn.metrics module includes score functions, performance metrics and pairwise metrics and distance computations.

Classification Metrics

accuracy_score: Accuracy classification score. In multilabel classification, this function computes subset accuracy: the set of labels predicted for a sample must exactly match the corresponding set of labels in y_true.

from sklearn.metrics import accuracy_score
y_pred = [0, 2, 1, 3]
y_true = [0, 1, 2, 3]
accuracy_score(y_true, y_pred)  # 0.5

precision_score, recall_score, f1_score: Compute the precision, recall, and F1 score respectively.

from sklearn.metrics import precision_score, recall_score, f1_score
precision_score(y_true, y_pred, average='weighted')
recall_score(y_true, y_pred, average='weighted')
f1_score(y_true, y_pred, average='weighted')

The average parameter is required for multiclass/multilabel targets: 'micro', 'macro', 'weighted', 'samples'.""",

        """confusion_matrix: Compute confusion matrix to evaluate the accuracy of a classification.

from sklearn.metrics import confusion_matrix
y_true = [2, 0, 2, 2, 0, 1]
y_pred = [0, 0, 2, 2, 0, 2]
confusion_matrix(y_true, y_pred)
# array([[2, 0, 0],
#        [0, 0, 1],
#        [1, 0, 2]])

classification_report: Build a text report showing the main classification metrics.

from sklearn.metrics import classification_report
print(classification_report(y_true, y_pred, target_names=['class 0', 'class 1', 'class 2']))

roc_auc_score: Compute Area Under the Receiver Operating Characteristic Curve (ROC AUC) from prediction scores.

from sklearn.metrics import roc_auc_score
roc_auc_score(y_true, y_scores)

The ROC curve is created by plotting the true positive rate (TPR) against the false positive rate (FPR) at various threshold settings. AUC provides an aggregate measure of performance across all possible classification thresholds.""",

        """Regression Metrics

mean_squared_error: Mean squared error regression loss.

from sklearn.metrics import mean_squared_error
y_true = [3, -0.5, 2, 7]
y_pred = [2.5, 0.0, 2, 8]
mean_squared_error(y_true, y_pred)  # 0.375

mean_absolute_error: Mean absolute error regression loss.
r2_score: R-squared (coefficient of determination) regression score function. Best possible score is 1.0. It can be negative if the model is worse than predicting the mean.

from sklearn.metrics import r2_score
r2_score(y_true, y_pred)  # 0.948...

mean_absolute_percentage_error: Mean absolute percentage error regression loss. Note: MAPE output is non-negative floating point, with best value 0.0. Undefined when y_true contains zeros.

Clustering Metrics

adjusted_rand_score: Rand index adjusted for chance. The Rand Index computes a similarity measure between two clusterings by considering all pairs of samples.

silhouette_score: Compute the mean Silhouette Coefficient of all samples. Composed of two scores: a (mean intra-cluster distance) and b (mean nearest-cluster distance). The Silhouette Coefficient for a sample is (b - a) / max(a, b). Best value is 1, worst is -1. Values near 0 indicate overlapping clusters.""",
    ],
}


def create_pdf(filename: str, pages: list[str]):
    doc = fitz.open()
    for text in pages:
        page = doc.new_page(width=595, height=842)  # A4
        # insert text
        rect = fitz.Rect(50, 50, 545, 792)
        page.insert_textbox(
            rect,
            text,
            fontsize=10,
            fontname="helv",
        )
    doc.save(str(DOCS_DIR / filename))
    doc.close()
    print(f"created {filename} ({len(pages)} pages)")


if __name__ == "__main__":
    for fname, pages in DOCS.items():
        create_pdf(fname, pages)
    print("done")
