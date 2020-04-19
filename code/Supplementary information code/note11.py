#! python3
# -*- coding: utf-8 -*-
"""

@author: Qian Pan
@e-mail: qianpan_93@163.com
"""


from configure import *


lat_path = os.path.join('../data', 'note11', 'Lattice model')
rand_path = os.path.join('../data', '1000 equivalent random networks')
sw_path = os.path.join('../data', 'note11')


def cal_rand_c_l():
    list_l_rand = []
    list_c_latt = []
    for rt in range(1, iters+1):
        rand = pd.read_csv(rand_path + '/' + str(rt) + '.csv', header=None)
        rand.columns = ['source', 'target']
        g_rand = nx.from_pandas_edgelist(rand, 'source', 'target', create_using=nx.Graph())
        list_l_rand.append(nx.average_shortest_path_length(g_rand))

        lat = pd.read_csv(lat_path + '/' + str(rt) + '.csv', header=None)
        lat.columns = ['source', 'target']
        lat_g = nx.from_pandas_edgelist(lat, 'source', 'target', create_using=nx.Graph())
        list_c_latt.append(nx.average_clustering(lat_g))
    l_rand = np.mean(list_l_rand)
    c_latt = np.mean(list_c_latt)
    return l_rand, c_latt


def plot_res(l_rand, c_latt):
    df_c_spl = pd.DataFrame()
    for i in range(1, 5):
        df = pd.read_csv('output/sw_process/sw_' + str(i) + '.csv')
        df_c_spl = pd.concat([df_c_spl, df], axis=0)

    df_c_spl['omega'] = (l_rand / df_c_spl['L']) - (df_c_spl['C'] / c_latt)
    data = df_c_spl.groupby('p', as_index=False).apply(np.mean)
    omega_empirical = round((l_rand / 2.671) - (0.713 / c_latt), 4)

    fig = plt.figure(figsize=(6, 5))
    ax = fig.add_subplot(111)

    ax.plot(data['p'], data['omega'], 'bo', ms=10)
    ax.plot(0.04, omega_empirical, 'ro', fillstyle='none', mew=3, ms=22, alpha=1, label='')

    ax.set_ylabel(r'$\omega$', fontsize=40, color='b', rotation='horizontal', labelpad=15)
    ax.set_ylim(-1.1, 1.1)
    ax.set_yticks(np.arange(-1, 1.01, 0.2))
    ax.set_xscale('log')

    ax.set_xlabel(r"Rewiring Probability ($p$)", fontsize=29)

    ax2 = ax.twinx()
    ax2.plot(data['p'], data['C(p)/C(0)'], 'ks', fillstyle='none', mew=1.8, ms=13, label='')
    ax2.plot(data['p'], data['L(p)/L(0)'], 'ko', ms=10, alpha=0.85, label='')

    ax2.set_yticks(np.arange(0, 1.01, 0.2))
    yminorlocator = MultipleLocator(0.05)
    ax2.yaxis.set_minor_locator(yminorlocator)

    ax2.set_ylabel(r'$C(p)/C(0)$'+'\n'+'$L(p)/L(0)$', fontsize=32, rotation=270, labelpad=75)
    pltstyle.axes_style(ax)
    pltstyle.axes_style(ax2)

    for label in ax.xaxis.get_ticklabels():
        label.set_weight('bold')

    ax.tick_params(axis='y', direction='in', top=True, right=False, which='major',
                   width=2.5, color='b', length=10.5, pad=8, labelsize=24, labelcolor='b')
    ax.tick_params(axis='x', direction='in', top=True, right=False, which='major',
                   width=2.5, length=10.5, pad=8, labelsize=22)
    ax.tick_params(axis='both', direction='in', top=True, right=False, which='minor',
                   width=2, length=7.5)
    ax.spines['left'].set_color('b')

    t = plt.title('Note: The number of iterations of the experiment:' + '\n' +
                  'in your test, {}; in the manuscript, 1000.'.format(iters), color='red', style='italic',
                  fontsize=20, pad=30)
    t.set_bbox(dict(facecolor='gray', alpha=0.3, edgecolor=None))

    if SAVE_RESULT:
        save_path = os.path.join('output', 'Supplementary note 11')
        if os.path.exists(save_path):
            pass
        else:
            os.makedirs(save_path)
        filename = 'Supplementary Fig. 26 Small-world networks generated by adoption of the Watts-Strogatz...(b).png'
        plt.savefig(save_path + '/' + filename, bbox_inches='tight')
        print()
        print('The result file "{}" saved at: "{}"'.format(filename, save_path))
        print()
    else:
        plt.show()
    plt.close('all')


def plot_net():
    num_nodes = 20
    ave_k = 6
    G1 = nx.connected_watts_strogatz_graph(n=num_nodes, k=ave_k, p=0, tries=100, seed=None)
    G2 = nx.connected_watts_strogatz_graph(n=num_nodes, k=ave_k, p=0.1, tries=100, seed=None)
    G3 = nx.connected_watts_strogatz_graph(n=num_nodes, k=ave_k, p=1, tries=100, seed=None)

    fig = plt.figure(figsize=(14, 5))
    ax1 = fig.add_subplot(131)
    ax2 = fig.add_subplot(132)
    ax3 = fig.add_subplot(133)

    nx.draw_circular(G1, ax=ax1, node_size=220, node_color='k', edgecolors='white', edge_color='gray', width=1.5)
    nx.draw_circular(G2, ax=ax2, node_size=220, node_color='k', edgecolors='white', edge_color='gray', width=1.6)
    nx.draw_circular(G3, ax=ax3, node_size=220, node_color='k', edgecolors='white', edge_color='gray', width=1.6)

    plt.tight_layout(w_pad=-3.5)
    if SAVE_RESULT:
        save_path = os.path.join('output', 'Supplementary note 11')
        if os.path.exists(save_path):
            pass
        else:
            os.makedirs(save_path)
        filename = 'Supplementary Fig. 26 Small-world networks generated by adoption of the Watts-Strogatz...(a).png'
        plt.savefig(save_path + '/' + filename, bbox_inches='tight')
        print()
        print('The result file "{}" saved at: "{}"'.format(filename, save_path))
        print()
    else:
        plt.show()
    plt.close('all')


def startup():
    if os.path.exists(lat_path) and os.path.exists(rand_path) and os.path.exists(sw_path):
        print('*********************************')
        print("Location in the manuscript text: ")
        print('Section titled "Supplementary note 11: Existence of a structural core of the GLSN is not '
              'the same as small-world distance scaling"')
        print('*********************************')
        print()
        print('***************************RUN TIME WARNING***************************')
        print('It needs 2 days for 1000 iterations of the corresponding experiments.')
        print()
        print('---------------------------------------------------------------------------------------------------')
        print('Output:')
        print()
        print('**********************************************************************************************')
        print('Note: The number of iterations of the experiment: in your test, {}; in '
              'the manuscript, 1000.'.format(iters))
        print('**********************************************************************************************')
        print()

        from src import note11_1
        from src import note11_2
        from src import note11_3
        from src import note11_4
        p1 = mp.Process(target=note11_1.startup, args=(iters, ))
        p2 = mp.Process(target=note11_2.startup, args=(iters, ))
        p3 = mp.Process(target=note11_3.startup, args=(iters, ))
        p4 = mp.Process(target=note11_4.startup, args=(iters, ))
        p1.start()
        p2.start()
        p3.start()
        p4.start()
        p1.join()
        p2.join()
        p3.join()
        p4.join()

        l_rand, c_latt = cal_rand_c_l()
        plot_res(l_rand, c_latt)
        plot_net()

        del_path = 'output/sw_process'
        if os.path.exists(del_path):
            shutil.rmtree(del_path)
        else:
            pass

    else:
        print()
        print('Please download (in this link: https://doi.org/10.6084/m9.figshare.12136236.v1) zip files first!')
        sys.exit()