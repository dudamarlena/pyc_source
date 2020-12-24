# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/examples/python/generate_visuals.py
# Compiled at: 2018-10-21 08:35:10
# Size of source mod 2**32: 8853 bytes
import matplotlib as mpl, matplotlib.patches as patches, matplotlib.pyplot as plt, numpy as np, pandas as pd, transitionMatrix as tm
from transitionMatrix import source_path
from transitionMatrix.estimators import cohort_estimator as es
dataset_path = source_path + 'datasets/'
example = 6
if example == 1:
    cohort_data = pd.read_csv(dataset_path + 'synthetic_data1.csv')
    sorted_data = cohort_data.sort_values(['ID', 'Time'], ascending=[True, True])
    unique_states = sorted_data['State'].unique()
    x = sorted_data.as_matrix(columns=['Time'])
    y = sorted_data.as_matrix(columns=['State'])
    summary = 'Unique States: ' + str(len(unique_states)) + '. ' + 'Observed Transitions: ' + str(len(x))
    fig = plt.figure()
    plt.style.use(['dark_background', 'ggplot'])
    fig.suptitle(summary)
    plt.ylabel('State')
    plt.xlabel('Time')
    plt.step(x, y, marker='o', label='post', where='post', linewidth=1)
    plt.yticks(range(len(unique_states)))
    plt.grid(True)
    plt.margins(y=0.1, x=0.05)
    plt.show()
else:
    if example == 2:
        data = pd.read_csv(dataset_path + 'synthetic_data4.csv')
        unique_states = data['State'].unique()
        unique_ids = data['ID'].unique()
        n = len(unique_ids)
        m = 5
        sample_ids = np.random.choice(unique_ids, min(5, m))
        viz_data = []
        summary = 'Sampled Entities IDs: '
        for identity in sample_ids:
            summary += str(identity) + ' '
            entity_data = data[(data['ID'] == identity)]
            entity_data = entity_data[['Timestep', 'State']]
            sorted_data = entity_data.sort_values(['Timestep'], ascending=[True])
            raw_data = sorted_data.as_matrix()
            viz_data.append(raw_data)

        plt.close('all')
        plt.style.use(['ggplot'])
        f, axarr = plt.subplots(m, 1)
        plt.setp([a.get_xticklabels() for a in f.axes[:-1]], visible=False)
        for axi in range(m):
            x = viz_data[axi][:, 0]
            y = viz_data[axi][:, 1]
            axarr[axi].step(x, y, marker='o', label='post', where='post')
            axarr[axi].set_title('ID: ' + str(sample_ids[axi]), fontsize=10)
            axarr[axi].set_yticks(range(len(unique_states)), minor=False)
            axarr[axi].yaxis.grid(True, which='major')
            axarr[axi].margins(y=0.1, x=0.01)

        f.subplots_adjust(left=0.125, bottom=0.1, right=0.9, top=0.9, wspace=0, hspace=0.4)
        f.suptitle(summary, fontsize=12)
        plt.show()
    else:
        if example == 3:
            data = pd.read_csv(dataset_path + 'synthetic_data5.csv', dtype={'State': str})
            sorted_data = data.sort_values(['ID', 'Timestep'], ascending=[True, True])
            description = [('0', 'Stage 1'), ('1', 'Stage 2'), ('2', 'Stage 3')]
            myState = tm.StateSpace(description)
            myState.describe()
            myEstimator = es.CohortEstimator(states=myState, ci={'method': 'goodman',  'alpha': 0.05})
            result = myEstimator.fit(sorted_data)
            viz_data = []
            for k in range(len(result)):
                for s in range(len(myState.get_states())):
                    raw_data = result[k][s, :]
                    viz_data.append(raw_data)

            n = myState.cardinality
            m = len(result)
            plt.close('all')
            labels = myState.get_state_labels()
            f, axarr = plt.subplots(m, n)
            f.subplots_adjust(left=0.125, bottom=0.1, right=0.9, top=0.9, wspace=0.2, hspace=0.2)
            plt.style.use(['ggplot'])
            for axj in range(m):
                for axi in range(n):
                    x = [s for s in range(len(myState.get_states()))]
                    ii = axi + axj * n
                    y = list(viz_data[ii])
                    axarr[(axj, axi)].bar(x, y, 1)
                    if axj == 0:
                        axarr[(axj, axi)].set_title('From ' + labels[axi], fontsize=12)
                    if axi == 0:
                        axarr[(axj, axi)].set_ylabel('Cohort ' + str(axj), fontsize=12)
                    axarr[(axj, axi)].set_xticks(range(n), minor=False)
                    axarr[(axj, axi)].yaxis.grid(True, which='major')
                    axarr[(axj, axi)].margins(y=0.1, x=0.01)

            plt.show()
        else:
            if example == 4:
                data = pd.read_csv(dataset_path + 'synthetic_data3.csv')
                print(data.head())
                unique_states = data['State'].unique()
                unique_ids = data['ID'].unique()
                x = []
                y = []
                colors = []
                mymap = plt.get_cmap('RdYlGn')
                for row in data.itertuples():
                    x.append(row[2])
                    y.append(row[1])
                    colors.append(row[3] / len(unique_states))

                my_colors = mymap(colors)
                fig = plt.figure()
                plt.style.use(['ggplot'])
                plt.ylabel('Entity')
                plt.xlabel('Time')
                fig.suptitle('Entity Transitions Plot')
                plt.scatter(x, y, marker='o', c=my_colors)
                plt.margins(y=0.1, x=0.05)
                plt.show()
            else:
                if example == 5:
                    data = pd.read_csv(dataset_path + 'scenario_data.csv')
                    data = data.sort_values(['ID', 'State'], ascending=[True, True])
                    unique_states = data['State'].unique()
                    unique_ids = data['ID'].unique()
                    x = []
                    y = []
                    colors = []
                    mymap = plt.get_cmap('seismic')
                    mymap = plt.get_cmap('RdYlGn')
                    for row in data.itertuples():
                        x.append(row[2])
                        y.append(row[1])
                        colors.append(1.1 - row[3] / 7)

                    my_colors = mymap(colors)
                    print(colors)
                    fig = plt.figure()
                    plt.style.use(['ggplot'])
                    plt.ylabel('Entity')
                    plt.xlabel('Time')
                    fig.suptitle('Entity Transitions Plot')
                    plt.scatter(x, y, marker='o', c=my_colors)
                    plt.margins(y=0.1, x=0.05)
                    plt.savefig('scatterplot2.png')
                    plt.show()
                elif example == 6:
                    filename = dataset_path + 'JLT.json'
                    myMatrix = tm.TransitionMatrix(json_file=filename)
                    fig = plt.figure()
                    ax = fig.add_subplot(111, aspect='equal')
                    plt.style.use(['ggplot'])
                    plt.ylabel('From State')
                    plt.xlabel('To State')
                    mymap = plt.get_cmap('RdYlGn')
                    mymap = plt.get_cmap('Reds')
                    normalize = mpl.colors.LogNorm(vmin=0.0001, vmax=1)
                    matrix_size = myMatrix.shape[0]
                    square_size = 1.0 / matrix_size
                    diagonal = myMatrix.diagonal()
                    ax.set_xticklabels(range(0, matrix_size))
                    ax.set_yticklabels(range(0, matrix_size))
                    ax.xaxis.set_ticks(np.arange(0 + 0.5 * square_size, 1 + 0.5 * square_size, square_size))
                    ax.yaxis.set_ticks(np.arange(0 + 0.5 * square_size, 1 + 0.5 * square_size, square_size))
                    for i in range(0, matrix_size):
                        for j in range(0, matrix_size):
                            if myMatrix[(i, j)] > 0:
                                rect_size = np.sqrt(myMatrix[(i, j)]) * square_size
                            else:
                                rect_size = 0
                            dx = 0.5 * (square_size - rect_size)
                            dy = 0.5 * (square_size - rect_size)
                            p = patches.Rectangle((
                             i * square_size + dx, j * square_size + dy), rect_size, rect_size, fill=True, color=mymap(normalize(myMatrix[(i, j)])))
                            ax.add_patch(p)

                    cbax = fig.add_axes([0.85, 0.12, 0.05, 0.78])
                    cb = mpl.colorbar.ColorbarBase(cbax, cmap=mymap, norm=normalize, orientation='vertical')
                    cb.set_label('Transition Prabability', rotation=270, labelpad=15)
                    plt.show(block=True)
                    plt.interactive(False)