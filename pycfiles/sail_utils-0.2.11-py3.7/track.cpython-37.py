# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\sail_utils\cv\head\deep_sort\track.py
# Compiled at: 2020-04-22 07:16:04
# Size of source mod 2**32: 5441 bytes
"""
module for a single track
"""

class TrackState:
    __doc__ = '\n    Enumeration type for the single target track state. Newly created tracks are\n    classified as `tentative` until enough evidence has been collected. Then,\n    the track state is changed to `confirmed`. Tracks that are no longer alive\n    are classified as `deleted` to mark them for removal from the set of active\n    tracks.\n\n    '
    Tentative = 1
    Confirmed = 2
    Deleted = 3


class Track:
    __doc__ = '\n    A single target track with state space `(x, y, a, h)` and associated\n    velocities, where `(x, y)` is the center of the bounding box, `a` is the\n    aspect ratio and `h` is the height.\n\n    Parameters\n    ----------\n    mean : ndarray\n        Mean vector of the initial state distribution.\n    covariance : ndarray\n        Covariance matrix of the initial state distribution.\n    track_id : int\n        A unique track identifier.\n    n_init : int\n        Number of consecutive detections before the track is confirmed. The\n        track state is set to `Deleted` if a miss occurs within the first\n        `n_init` frames.\n    max_age : int\n        The maximum number of consecutive misses before the track state is\n        set to `Deleted`.\n    feature : Optional[ndarray]\n        Feature vector of the detection this track originates from. If not None,\n        this feature is added to the `features` cache.\n\n    Attributes\n    ----------\n    mean : ndarray\n        Mean vector of the initial state distribution.\n    covariance : ndarray\n        Covariance matrix of the initial state distribution.\n    track_id : int\n        A unique track identifier.\n    hits : int\n        Total number of measurement updates.\n    age : int\n        Total number of frames since first occurance.\n    time_since_update : int\n        Total number of frames since last measurement update.\n    state : TrackState\n        The current track state.\n    features : List[ndarray]\n        A cache of features. On each measurement update, the associated feature\n        vector is added to this list.\n\n    '

    def __init__(self, mean, covariance, track_id, n_init, max_age, feature=None):
        self.mean = mean
        self.covariance = covariance
        self.track_id = track_id
        self.hits = 1
        self.age = 1
        self.time_since_update = 0
        self.state = TrackState.Tentative
        self.features = []
        if feature is not None:
            self.features.append(feature)
        self._n_init = n_init
        self._max_age = max_age

    def to_tlwh(self):
        """
        Get current position in bounding box format `(top left x, top left y,
        width, height)`.

        Returns
        -------
        ndarray
            The bounding box.

        """
        ret = self.mean[:4].copy()
        ret[2] *= ret[3]
        ret[:2] -= ret[2:] / 2
        return ret

    def to_tlbr(self):
        """
        Get current position in bounding box format `(min x, miny, max x,
        max y)`.

        Returns
        -------
        ndarray
            The bounding box.

        """
        ret = self.to_tlwh()
        ret[2:] = ret[:2] + ret[2:]
        return ret

    def predict(self, kalman_filter):
        """
        Propagate the state distribution to the current time step using a
        Kalman filter prediction step.

        Parameters
        ----------
        kalman_filter : KalmanFilter
            The Kalman filter.

        """
        self.mean, self.covariance = kalman_filter.predict(self.mean, self.covariance)
        self.age += 1
        self.time_since_update += 1

    def update(self, kalman_filter, detection):
        """
        Perform Kalman filter measurement update step and update the feature
        cache.

        Parameters
        ----------
        kalman_filter : KalmanFilter
            The Kalman filter.
        detection : Detection
            The associated detection.

        """
        self.mean, self.covariance = kalman_filter.update(self.mean, self.covariance, detection.to_xyah())
        self.features.append(detection.feature)
        self.hits += 1
        self.time_since_update = 0
        if self.state == TrackState.Tentative:
            if self.hits >= self._n_init:
                self.state = TrackState.Confirmed

    def mark_missed(self):
        """
        Mark this track as missed (no association at the current time step).
        """
        if self.state == TrackState.Confirmed:
            self.state = TrackState.Tentative
        if self.state == TrackState.Tentative and self.time_since_update >= 3:
            self.state = TrackState.Deleted
        else:
            if self.time_since_update > self._max_age:
                self.state = TrackState.Deleted

    def is_tentative(self):
        """
        Returns True if this track is tentative (unconfirmed).
        """
        return self.state == TrackState.Tentative

    def is_confirmed(self):
        """
        Returns True if this track is confirmed.
        """
        return self.state == TrackState.Confirmed

    def is_deleted(self):
        """
        Returns True if this track is dead and should be deleted.
        """
        return self.state == TrackState.Deleted