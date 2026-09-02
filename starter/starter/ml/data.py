import logging

import numpy as np
from sklearn.preprocessing import LabelBinarizer, OneHotEncoder

logger = logging.getLogger(__name__)


def process_data(
    X, categorical_features=[], label=None, training=True, encoder=None, lb=None
):
    """ Process the data used in the machine learning pipeline.

    Processes the data using one hot encoding for the categorical features and a
    label binarizer for the labels. This can be used in either training or
    inference/validation.

    Note: depending on the type of model used, you may want to add in functionality that
    scales the continuous data.

    Inputs
    ------
    X : pd.DataFrame
        Dataframe containing the features and label. Columns in `categorical_features`
    categorical_features: list[str]
        List containing the names of the categorical features (default=[])
    label : str
        Name of the label column in `X`. If None, then an empty array will be returned
        for y (default=None)
    training : bool
        Indicator if training mode or inference/validation mode.
    encoder : sklearn.preprocessing._encoders.OneHotEncoder
        Trained sklearn OneHotEncoder, only used if training=False.
    lb : sklearn.preprocessing._label.LabelBinarizer
        Trained sklearn LabelBinarizer, only used if training=False.

    Returns
    -------
    X : np.array
        Processed data.
    y : np.array
        Processed labels if labeled=True, otherwise empty np.array.
    encoder : sklearn.preprocessing._encoders.OneHotEncoder
        Trained OneHotEncoder if training is True, otherwise returns the encoder passed
        in.
    lb : sklearn.preprocessing._label.LabelBinarizer
        Trained LabelBinarizer if training is True, otherwise returns the binarizer
        passed in.
    """

    logger.debug(
        "process_data: n_rows=%d training=%s n_categorical=%d",
        len(X), training, len(categorical_features)
    )

    if label is not None:
        y = X[label]
        X = X.drop([label], axis=1)
    else:
        y = np.array([])

    X_categorical = X[categorical_features].values
    X_continuous = X.drop(categorical_features, axis=1)

    if training is True:
        encoder = OneHotEncoder(sparse_output=False, handle_unknown="ignore")
        lb = LabelBinarizer()
        X_categorical = encoder.fit_transform(X_categorical)
        y = lb.fit_transform(y.values).ravel()
    else:
        # handle_unknown="ignore" zero-encodes any category the encoder never
        # saw at fit time, silently degrading the prediction — surface it.
        for i, feature in enumerate(categorical_features):
            unknown = ~np.isin(X_categorical[:, i], encoder.categories_[i])
            n_unknown = int(unknown.sum())
            if n_unknown > 0:
                logger.warning(
                    "process_data: %d value(s) in feature '%s' are outside the "
                    "training vocabulary and will be zero-encoded",
                    n_unknown, feature
                )
                logger.debug(
                    "process_data: unknown values for '%s': %s",
                    feature, np.unique(X_categorical[unknown, i]).tolist()
                )
        X_categorical = encoder.transform(X_categorical)
        try:
            y = lb.transform(y.values).ravel()
        # Catch the case where y is None because we're doing inference.
        except AttributeError:
            pass

    X = np.concatenate([X_continuous, X_categorical], axis=1)
    logger.debug("process_data: output shape=%s", X.shape)
    return X, y, encoder, lb
