# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/Clumsy/misc/BigDataAssignment1.py
# Compiled at: 2018-11-20 16:23:49
# Size of source mod 2**32: 6417 bytes
from matplotlib import pyplot as plt
import numpy as np, pandas as pd

def load_all_events(MSD_instance):
    """
    Uses the MemorySearchDynamics Class to extract out all event arrays
    as well as a single subject's (LTP093 by default)

    ------
    INPUTS
    MSD_instance: an instance of MemorySearchDynamic class
    """
    all_events = MSD_instance.all_events
    events = all_events[(all_events['subject'] == MSD_instance.subjs[0])]
    return (
     all_events, events)


def get_all_events_d(all_events):
    """
    Returns a dictionary where each key is a subject and each value is
    the event of that subject
    -------
    INPUTS
    all_events: an arr containing all events
    """
    d = {subj:all_events[(all_events['subject'] == subj)] for i, subj in enumerate(np.unique(all_events['subject']))}
    return d


def list_to_df(df_lists):
    """
    Converts a list of DataFrames into one DataFrame,
    averaging across indexes
    -----
    INPUTS
    df_lists: a list of pd.DataFrames
    """
    concat = pd.concat(df_lists)
    concat = concat.groupby(concat.index).mean()
    return concat


def get_good_events(events, sess, trial):
    """
    Takes in events array and returns out one without any intrusions or
    any repeats. Repeats are removed entirely (both) same with intrusions.

    INPUTS
    ------
    events: an events np.recarray
    sess: The session to apply it over
    Trial: The trial to apply it over
    """
    events = events[((events['session'] == sess) & (events['list'] == trial) & (events['type'] == 'REC_WORD') & (events['intrusion'] == 0))]
    d = dict(pd.Series(events['item_name']).value_counts())
    bad_words = [v for k, v in enumerate(d) if d[v] > 1]
    if len(bad_words) > 0:
        events = np.array([event for event in events if event['item_name'] not in bad_words])
    return events


def get_field(events, fields, sess, trial):
    """
    Gets the difference in the field of a single sess/trial of
    inputted events after filtering it using get_good_events

    INPUTS
    -----
    events: an array of beh events
    sess: session number must not be 0 or >23
    trial: number between 1-24
    """
    events = get_good_events(events, sess, trial)
    if len(events) > 1:
        return events[fields]
    return []


def get_field_diff(events, fields, sess, trial):
    """
    Gets the difference in the field of a single sess/trial of
    inputted events after filtering it using get_good_events

    INPUTS
    -----
    events: an array of beh events
    sess: session number must not be 0 or >23
    trial: number between 1-24
    """
    events = get_good_events(events, sess, trial)
    if len(events) > 1:
        diff = np.diff(events[fields])
        k = len(diff)
        if k > 0:
            return diff
    else:
        return []


def get_field_diff_per_sess(events, sess, fieldname):
    """
    Gets all IRT per session of inputted events
    INPUTS
    -----
    events: an array of beh events
    sess: a session
    """
    session = [get_field_diff(events, fieldname, sess, i) for i in range(1, 25)]
    indx = [len(x) for x in session]
    try:
        df = pd.DataFrame(session, index=indx).groupby(indx).mean()
        return df
    except:
        pass


def get_field_per_subj(events, fieldname):
    """
    Gets ALL FIELDS fieldname of a single subject
    --------
    INPUTS
    events: events for a subject
    """
    all_irts = [get_field_diff_per_sess(events, i, fieldname) for i in range(1, 24)]
    return list_to_df(all_irts)


def diff_in_field(events, fields, sess, trial, sp=None):
    """
    Gets the difference in the field of a single sess/trial of
    inputted events after filtering it using get_good_events,
    THIS VERSION WILL BE USED TO INTERACT WITH SERIALPOS SUCH THAT
    WE CAN CONTROL IF WE DO 0, 1, 2, ALL, ETC.

    INPUTS
    -----
    events: an array of beh events
    sess: session number must not be 0 or >23
    trial: number between 1-24
    """
    events = get_good_events(events, sess, trial)
    if len(events) > 1:
        diff = np.diff(events[fields])
        if type(sp) == int:
            try:
                diff = diff[sp]
                return diff
            except:
                return []

        elif type(sp) == str and len(diff) > 0:
            return diff
    else:
        return []


def plot_irt(irt_per_sess, title):
    """
    Plots an IRT curve, one line per len(recall)
    ------
    INPUTS
    irt_per_sess: output of get_irt_per_sess()
    """
    for i in range(len(irt_per_sess)):
        times = irt_per_sess.iloc[i].values
        pos = irt_per_sess.iloc[i].index
        x = times[(~np.isnan(times))]
        pos = pos[:len(x)] + 1
        plt.plot(pos, x, label=('len {}'.format(len(pos))), marker='*')
        plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.0, ncol=2)
        plt.title('Inter-Response Interval ' + title)
        plt.ylabel('Time (ms)')
        plt.xlabel('Recall Serial Position')

    plt.show()


def get_irt_all(all_events_d):
    """
    Gets IRT for all subjects, generates a plot
    ------
    INPUTS
    all_events_d: a dictionary where keys=subj_id, and values=events_subj
    """
    my_list = [get_field_per_subj(all_events_d[subj], 'rectime') for subj in all_events_d.keys()]
    try:
        df = list_to_df(my_list)
        plot_irt(df)
        plt.show()
        return df
    except:
        try:
            return list_to_df(my_list)
        except:
            return my_list