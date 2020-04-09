import numpy as np
import matplotlib.pyplot as plt
import so


def _remove_negative(array):
    return np.where(array < 0, 0, array)


def plot_confirmed_case(
        dataset, ax, mask=None, days=1,
        show_info=True, text_left=None, text_right=None,
        show_title=True, text_title=None,
        show_numbers=True, show_hist=True,
        show_legend=True,
        show_diff_numbers=False, show_diff_bar=True):

    slice_data = (
        slice(None, None, days) if mask is None else slice(*mask, days)
    )

    data = dataset[slice_data]
    date_index = data.index
    date_ticks = date_index.strftime('%d\n%b').to_list()
    rows, _ = data.shape

    total_confirmed = data['konfirmasi'].values
    total_recovered = data['sembuh'].values
    total_deaths = data['meninggal'].values
    total_positive = total_confirmed - total_recovered - total_deaths

    # X POSITIONS
    x_pos = np.arange(0, rows*2, 2)
    x_pos_diff = x_pos[:-1] + 1

    # LINE
    ax.plot(
        x_pos, total_confirmed,
        color='blue', linestyle='--',
        marker='o', markerfacecolor='orange')

    # BAR
    # POSITIVE
    ax.bar(
        x_pos, total_positive, bottom=total_deaths+total_recovered,
        color='orange', label='Dalam Perawatan (Positif COVID-19)'
    )

    # RECOVERED
    ax.bar(
        x_pos, total_recovered, bottom=total_deaths,
        color='green', label='Sembuh (Positif COVID-19)'
    )

    # DEATHS
    ax.bar(
        x_pos, total_deaths,
        color='red', label='Meninggal (Positif COVID-19)'
    )

    # DIFF

    diff_confirmed = np.diff(total_confirmed)
    diff_deaths = np.diff(total_deaths)
    diff_recovered = np.diff(total_recovered)
    diff_positive = np.diff(total_positive)

    # BAR (DIFF)
    if show_diff_bar:
        # DEATHS
        ax.bar(
            x_pos_diff, diff_deaths,
            bottom=total_confirmed[:-1],
            color='red', edgecolor='black', alpha=0.5
        )

        # RECOVERED
        ax.bar(
            x_pos_diff, diff_recovered,
            bottom=total_confirmed[:-1]+diff_deaths,
            color='green', edgecolor='black', alpha=0.5
        )

        # POSITIVE
        ax.bar(
            x_pos_diff, diff_positive,
            bottom=total_confirmed[:-1]+diff_deaths+diff_recovered,
            color='orange', edgecolor='black', alpha=0.5
        )

    # ANNOTATION
    ann_space = 70 if show_hist else 10

    if show_numbers:
        for i, val in enumerate(total_confirmed):
            # TOTAL CASE

            if show_hist:

                ax.annotate(
                    f'{total_deaths[i]}', (x_pos[i], val), xytext=(0, 10),
                    textcoords='offset points',
                    ha='center', va='bottom', size=10,  # family='monospace',
                    color='black',
                    bbox=dict(
                        facecolor='white', alpha=1, boxstyle='square',
                        edgecolor='red', linewidth=2
                    )
                )

                ax.annotate(
                    f'{total_recovered[i]}', (x_pos[i], val), xytext=(0, 30),
                    textcoords='offset points',
                    ha='center', va='bottom', size=10,  # family='monospace',
                    color='black',
                    bbox=dict(
                        facecolor='white', alpha=1, boxstyle='square',
                        edgecolor='green', linewidth=2
                    )
                )

                ax.annotate(
                    f'{total_positive[i]}', (x_pos[i], val), xytext=(0, 50),
                    textcoords='offset points',
                    ha='center', va='bottom', size=10,  # family='monospace',
                    color='black',
                    bbox=dict(
                        facecolor='white', alpha=1, boxstyle='square',
                        edgecolor='orange', linewidth=2
                    )
                )

            ax.annotate(
                f'{val}', (x_pos[i], val), xytext=(0, ann_space),
                textcoords='offset points',
                ha='center', va='bottom',
                size=12, color='white', fontweight='bold',
                bbox=dict(
                    facecolor='red', alpha=0.7, boxstyle='round'
                )
            )

            # TEXT DIFF
            if i > 0 and show_diff_numbers:

                if show_hist:

                    ax.annotate(
                        f'{diff_deaths[i-1]:+d}', (x_pos[i]-1, val),
                        xytext=(0, 5),
                        textcoords='offset points',
                        ha='center', va='bottom', size=10,
                        color='black',
                        # bbox=dict(
                        #     facecolor='red', alpha=.3, boxstyle='square',
                        #     edgecolor='red', linewidth=2
                        # )
                    )

                    ax.annotate(
                        f'{diff_recovered[i-1]:+d}', (x_pos[i]-1, val),
                        xytext=(0, 20),
                        textcoords='offset points',
                        ha='center', va='bottom', size=10,
                        color='black',
                        # bbox=dict(
                        #     facecolor='green', alpha=.3, boxstyle='square',
                        #     edgecolor='green', linewidth=2
                        # )
                    )

                    ax.annotate(
                        f'{diff_positive[i-1]:+d}', (x_pos[i]-1, val),
                        xytext=(0, 35),
                        textcoords='offset points',
                        ha='center', va='bottom', size=10,
                        color='black',
                        # bbox=dict(
                        #     facecolor='orange', alpha=.3, boxstyle='square',
                        #     edgecolor='orange', linewidth=2
                        # )
                    )

                ax.annotate(
                    f'{diff_confirmed[i-1]:+d}', (x_pos[i]-1, val),
                    xytext=(0, 50),
                    textcoords='offset points',
                    ha='center', va='bottom',
                    size=12, color='red', fontweight='bold',
                    # bbox=dict(
                    #     facecolor='white', alpha=1, edgecolor=None
                    # )
                )

    # INFO
    if show_info:
        text_right = (
            'Data: Situasi Terkini Perkembangan COVID-19 ' +
            '(infeksiemerging.kemkes.go.id)'
            if text_right is None else
            text_right
        )
        ax.text(
            1, -0.1, text_right,
            horizontalalignment='right',
            verticalalignment='top', style='normal', family='monospace',
            transform=ax.transAxes
        )

        text_left = (
            '' if text_left is None else
            text_left
        )

        ax.text(
            0, -0.1, text_left,
            horizontalalignment='left',
            verticalalignment='top', style='normal', family='serif',
            transform=ax.transAxes
        )

    # LEGEND

    if show_title:
        text_title = (
            'KASUS KONFIRMASI COVID-19 DI INDONESIA'
            if text_title is None else text_title
        )
        ax.set_title(
            text_title,
            fontsize='x-large', fontweight='bold'
        )

    ax.set_xticks(x_pos)
    ax.set_xticklabels(date_ticks, rotation=0)

    ax.set_xlabel('Tanggal', fontsize=14)
    ax.set_ylabel('Kasus Konfirmasi', fontsize=14)

    ax.grid(True, axis='both')

    if show_legend:
        ax.legend(loc='upper left')
    ax.margins(x=0.01, y=0.3)

    plt.tight_layout()


def plot_testing_case(
        dataset, ax, mask=None, days=1,
        show_info=True, text_left=None, text_right=None,
        show_title=True, text_title=None,
        show_numbers=True, show_hist=True,
        show_legend=True,
        show_diff_numbers=False, show_diff_bar=True):

    slice_data = (
        slice(None, None, days) if mask is None else slice(*mask, days)
    )

    data = dataset[slice_data]
    date_index = data.index
    date_ticks = date_index.strftime('%d\n%b').to_list()
    rows, _ = data.shape

    total_tests = data['jumlah_periksa'].values
    total_positive = data['konfirmasi'].values
    total_negative = data['negatif'].values
    total_checks = data['proses_periksa'].values

    # X POSITIONS
    x_pos = np.arange(0, rows*2, 2)
    x_pos_diff = x_pos[:-1] + 1

    # LINE
    ax.plot(
        x_pos, total_tests,
        color='blue', linestyle='--',
        marker='o', markerfacecolor='orange'
    )

    # BAR
    # POSITIVE
    ax.bar(
        x_pos, total_positive, bottom=total_negative+total_checks,
        color='red', label='POSITIF COVID-19'
    )

    # NEGATIVE
    ax.bar(
        x_pos, total_negative, bottom=total_checks,
        color='blue', label='NEGATIF COVID-19', alpha=0.7
    )

    # CHECKS
    ax.bar(
        x_pos, total_checks,
        color='yellow', label='PROSES PEMERIKSAAN'
    )

    # DIFF
    diff_tests = np.diff(total_tests)
    diff_positive = np.diff(total_positive)
    diff_negative = np.diff(total_negative)
    diff_checks = np.diff(total_checks)

    # BAR DIFF
    if show_diff_bar:

        # CHECKS
        ax.bar(
            x_pos_diff, diff_checks,
            bottom=total_tests[:-1],
            color='yellow', edgecolor='black', alpha=0.5
        )

        # NEGATIVE
        ax.bar(
            x_pos_diff, diff_negative,
            bottom=total_tests[:-1]+diff_checks,
            color='blue', edgecolor='black', alpha=0.5
        )

        # POSITIVE
        ax.bar(
            x_pos_diff, diff_positive,
            bottom=total_tests[:-1]+diff_checks+diff_negative,
            color='red', edgecolor='black', alpha=0.5
        )

    # ANNOTATION
    ann_space = 70 if show_hist else 10

    if show_numbers:
        for i, val in enumerate(total_tests):

            # TOTAL TESTS
            if show_hist:

                ax.annotate(
                    f'{total_checks[i]}', (x_pos[i], val), xytext=(0, 10),
                    textcoords='offset points',
                    ha='center', va='bottom', size=10,  # family='monospace',
                    color='black',
                    bbox=dict(
                        facecolor='white', alpha=1, boxstyle='square',
                        edgecolor='yellow', linewidth=2
                    )
                )

                ax.annotate(
                    f'{total_negative[i]}', (x_pos[i], val), xytext=(0, 30),
                    textcoords='offset points',
                    ha='center', va='bottom', size=10,  # family='monospace',
                    color='black',
                    bbox=dict(
                        facecolor='white', alpha=1, boxstyle='square',
                        edgecolor='blue', linewidth=2
                    )
                )

                ax.annotate(
                    f'{total_positive[i]}', (x_pos[i], val), xytext=(0, 50),
                    textcoords='offset points',
                    ha='center', va='bottom', size=10,  # family='monospace',
                    color='black',
                    bbox=dict(
                        facecolor='white', alpha=1, boxstyle='square',
                        edgecolor='red', linewidth=2
                    )
                )

            ax.annotate(
                f'{val}', (x_pos[i], val), xytext=(0, ann_space),
                textcoords='offset points',
                ha='center', va='bottom', size=12,
                color='white', fontweight='bold',
                bbox=dict(
                    facecolor='blue', alpha=0.7, boxstyle='round'
                )
            )

            # TEXT DIFF
            if i > 0 and show_diff_numbers:

                y_pos_diff = (
                    val if val > total_tests[i-1] else total_tests[i-1])

                if show_hist:
                    # ax.annotate(
                    #     text_diff,
                    #     (x_pos[i]-1, y_pos_diff), xytext=(0, 10),
                    #     textcoords='offset points',
                    #     ha='center', va='bottom', size=10,
                    #     bbox=dict(
                    #         facecolor='gray', alpha=0.1, boxstyle='square'
                    #     )
                    # )

                    ax.annotate(
                        f'{diff_checks[i-1]:+d}', (x_pos[i]-1, y_pos_diff),
                        xytext=(0, 5),
                        textcoords='offset points',
                        ha='center', va='bottom', size=10,
                        color='black',
                    )

                    ax.annotate(
                        f'{diff_negative[i-1]:+d}', (x_pos[i]-1, y_pos_diff),
                        xytext=(0, 20),
                        textcoords='offset points',
                        ha='center', va='bottom', size=10,
                        color='black',
                    )

                    ax.annotate(
                        f'{diff_positive[i-1]:+d}', (x_pos[i]-1, y_pos_diff),
                        xytext=(0, 35),
                        textcoords='offset points',
                        ha='center', va='bottom', size=10,
                        color='black',
                    )

                ax.annotate(
                    f'{diff_tests[i-1]:+d}', (x_pos[i]-1, y_pos_diff),
                    xytext=(0, 50),
                    textcoords='offset points',
                    ha='center', va='bottom',
                    size=12, color='blue', fontweight='bold',

                )

    # INFO
    if show_info:
        text_right = (
            'Data: Situasi Terkini Perkembangan COVID-19 ' +
            '(infeksiemerging.kemkes.go.id)'
            if text_right is None else
            text_right
        )
        ax.text(
            1, -0.1, text_right,
            horizontalalignment='right',
            verticalalignment='top', style='normal', family='monospace',
            transform=ax.transAxes
        )

        text_left = (
            '' if text_left is None else
            text_left
        )

        ax.text(
            0, -0.1, text_left,
            horizontalalignment='left',
            verticalalignment='top', style='normal', family='serif',
            transform=ax.transAxes
        )

    # LEGEND
    if show_title:
        text_title = (
            'JUMLAH SPESIMEN COVID-19 DI INDONESIA'
            if text_title is None else text_title
        )
        ax.set_title(
            text_title,
            fontsize='x-large', fontweight='bold'
        )

    ax.set_xticks(x_pos)
    ax.set_xticklabels(date_ticks, rotation=0)

    ax.set_xlabel('Tanggal', fontsize=14)
    ax.set_ylabel('Spesimen yang diterima', fontsize=14)

    ax.grid(True, axis='both')

    if show_legend:
        ax.legend(loc='upper left')
    ax.margins(x=0.01, y=0.3)

    plt.tight_layout()

    plt.tight_layout()


def plot_confirmed_growth(
        dataset, ax, mask=None, days=1,
        show_info=True, text_left=None, text_right=None,
        show_title=True, text_title=None,
        show_bar=True,
        show_numbers=True, show_total_numbers=True,
        show_legend=True,
        show_confirmed=False, show_confirmed_numbers=True):

    slice_data = (
        slice(None, None, days) if mask is None else slice(*mask, days)
    )

    data = dataset[slice_data]
    date_index = data.index
    date_ticks = date_index.strftime('%d\n%b').to_list()
    rows, _ = data.shape

    total_confirmed = data['konfirmasi'].values
    total_recovered = data['sembuh'].values
    total_deaths = data['meninggal'].values
    total_positive = total_confirmed - total_recovered - total_deaths

    x_pos = np.arange(0, rows*2, 2)
    x_pos_diff = x_pos[:-1] + 1

    # DIFF
    diff_confirmed = np.diff(total_confirmed)
    diff_deaths = np.diff(total_deaths)
    diff_recovered = np.diff(total_recovered)
    diff_positive = np.diff(total_positive)

    if show_bar:
        # POSITIVE
        ax.bar(
            x_pos_diff, _remove_negative(diff_positive),
            bottom=0, alpha=0.7,
            color='orange',  # edgecolor='black',
            label='Dalam Perawatan (Positif COVID-19)'
        )

        # RECOVERED
        ax.bar(
            x_pos_diff, _remove_negative(diff_recovered),
            bottom=np.absolute(diff_recovered)*-1, alpha=0.7,
            color='green',  # edgecolor='black',
            label='Sembuh (Positif COVID-19)'
        )

        # DEATHS
        ax.bar(
            x_pos_diff, _remove_negative(diff_deaths),
            color='red',  # edgecolor='black', alpha=0.7,
            bottom=(np.absolute(diff_recovered)*-1) + \
            (np.absolute(diff_deaths)*-1),
            label='Meninggal (Positif COVID-19)'
        )

    # ANNOTATION

    if show_numbers:
        for i, val in enumerate(diff_confirmed):

            # POSITIVE CASE
            text = (
                f'{diff_positive[i]:+d}'
            )

            ax.annotate(
                text, (x_pos_diff[i], 0),
                xytext=(0, 50), textcoords='offset points',
                ha='center', va='bottom', size=10, fontweight='bold',
                color='black', family='monospace',
                bbox=dict(
                    facecolor='orange', alpha=1, boxstyle='square'
                )
            )

            # RECOVERED
            rd_pos = np.absolute(diff_recovered) + np.absolute(diff_deaths)
            rd_pos = -rd_pos

            text = (
                f'{diff_recovered[i]:+d}'
            )

            ax.annotate(
                text, (x_pos_diff[i], 0),
                xytext=(0, 30), textcoords='offset points',
                ha='center', va='bottom', size=10, fontweight='bold',
                color='white', family='monospace',
                bbox=dict(
                    facecolor='green', alpha=1, boxstyle='square'
                )
            )

            # DEATHS
            text = (
                f'{diff_deaths[i]:+d}'
            )

            ax.annotate(
                text, (x_pos_diff[i], 0),
                xytext=(0, 10), textcoords='offset points',
                ha='center', va='bottom', size=10, fontweight='bold',
                color='white', family='monospace',
                bbox=dict(
                    facecolor='red', alpha=1, boxstyle='square'
                )
            )

            if show_total_numbers:
                total = np.sum(
                    (diff_deaths[i], diff_recovered[i], diff_positive[i]))
                text = (
                    f'{total:+d}'
                )

                ax.annotate(
                    text, (x_pos_diff[i], 0),
                    xytext=(0, 70), textcoords='offset points',
                    ha='center', va='bottom', size=12, fontweight='bold',
                    color='black',
                )

    if show_confirmed:
        ax2 = ax.twinx()
        ax2.plot(
            x_pos, total_confirmed,
            color='gray', linestyle='--',
            marker='o', markerfacecolor='gray',
            alpha=0.2
        )
        ax2.bar(
            x_pos, total_confirmed,
            alpha=0.3, color='grey',
            label='Kasus Konfirmasi'
        )
        ax2.set_ylabel('Kasus Konfirmasi', fontsize=14)

        if show_confirmed_numbers:
            for i, val in enumerate(total_confirmed):
                text = (
                    f'{val:d}'
                )

                ax2.annotate(
                    text, (x_pos[i], val),
                    xytext=(0, 10), textcoords='offset points',
                    ha='center', va='bottom', size=10, fontweight='bold',
                    color='black', alpha=0.3
                )

        so.align_yaxis_np((ax, ax2))
        ax2.set_yticklabels([f'{abs(x):.0f}' for x in ax2.get_yticks()])

    # INFO

    if show_info:
        text_right = (
            'Data: Situasi Terkini Perkembangan COVID-19 ' +
            '(infeksiemerging.kemkes.go.id)'
            if text_right is None else
            text_right
        )
        ax.text(
            1, -0.1, text_right,
            horizontalalignment='right',
            verticalalignment='top', style='normal', family='monospace',
            transform=ax.transAxes
        )

        text_left = (
            '' if text_left is None else
            text_left
        )

        ax.text(
            0, -0.1, text_left,
            horizontalalignment='left',
            verticalalignment='top', style='normal', family='serif',
            transform=ax.transAxes
        )

    # LEGEND
    ax.set_xticks(x_pos)
    ax.set_xticklabels(date_ticks, rotation=0)
    ax.set_yticklabels([f'{abs(x):.0f}' for x in ax.get_yticks()])

    if show_title:
        text_title = (
            'PERKEMBANGAN KASUS KONFIRMASI COVID-19 DI INDONESIA'
            if text_title is None else text_title
        )
        ax.set_title(
            text_title,
            fontsize='x-large', fontweight='bold'
        )

    ax.set_xlabel('Tanggal', fontsize=14)
    ax.set_ylabel('$(\\pm)$ Kasus', fontsize=14)

    if show_legend:
        if show_confirmed:
            handles1, labels1 = ax.get_legend_handles_labels()
            handles2, labels2 = ax2.get_legend_handles_labels()
            ax.legend((handles1 + handles2),
                      (labels1 + labels2), loc='upper left')
        else:
            ax.legend(loc='upper left')

    ax.set_xlim(min(x_pos)-1, max(x_pos)+1)
    ax.margins(x=0.01)
    ax.axhline(0, linestyle='--', color='grey')

    ax.grid(True, axis='both')
    ax.grid(axis='y', linestyle='-.')

    if show_bar is False:
        ax.set_yticks([], [])

    plt.tight_layout()


def plot_testing_growth(
        dataset, ax, mask=None, days=1,
        show_info=True, text_left=None, text_right=None,
        show_title=True, text_title=None,
        show_bar=True,
        show_numbers=True, show_total_numbers=True,
        show_legend=True,
        show_confirmed=False, show_confirmed_numbers=True):

    slice_data = (
        slice(None, None, days) if mask is None else slice(*mask, days)
    )

    data = dataset[slice_data]
    date_index = data.index
    date_ticks = date_index.strftime('%d\n%b').to_list()
    rows, _ = data.shape

    total_tests = data['jumlah_periksa'].values
    total_positive = data['konfirmasi'].values
    total_negative = data['negatif'].values
    total_checks = data['proses_periksa'].values

    x_pos = np.arange(0, rows*2, 2)
    x_pos_diff = x_pos[:-1] + 1

    # DIFF
    diff_tests = np.diff(total_tests)
    diff_positive = np.diff(total_positive)
    diff_negative = np.diff(total_negative)
    diff_checks = np.diff(total_checks)

    if show_bar:

        # NEGATIVE
        ax.bar(
            x_pos_diff, _remove_negative(diff_negative),
            color='blue',  alpha=0.5,  # edgecolor='black', alpha=0.7,
            bottom=_remove_negative(diff_checks),
            label='Negatif COVID-19'
        )

        # CHECKS
        ax.bar(
            x_pos_diff, _remove_negative(diff_checks),
            bottom=0, alpha=0.5,
            color='yellow',  # edgecolor='black',
            label='Proses Pemeriksaan'
        )

        # POSITIVE
        ax.bar(
            x_pos_diff, _remove_negative(diff_positive)*-1,
            bottom=0, alpha=0.5,
            color='red',  # edgecolor='black',
            label='Kasus Konfirmasi Positif COVID-19'
        )

    # ANNOTATION
    if show_numbers:
        for i, val in enumerate(diff_tests):

            # NEGATIVE
            text = (
                f'{diff_negative[i]:+d}'
            )

            ax.annotate(
                text, (x_pos_diff[i], 0),
                xytext=(0, 50), textcoords='offset points',
                ha='center', va='bottom', size=10, fontweight='bold',
                color='white', family='monospace',
                bbox=dict(
                    facecolor='blue', alpha=1, boxstyle='square'
                )
            )

            # CHECKS
            text = (
                f'{diff_checks[i]:+d}'
            )

            ax.annotate(
                text, (x_pos_diff[i], 0),
                xytext=(0, 30), textcoords='offset points',
                ha='center', va='bottom', size=10, fontweight='bold',
                color='black', family='monospace',
                bbox=dict(
                    facecolor='yellow', alpha=1, boxstyle='square'
                )
            )

            # POSITIVE CASE
            text = (
                f'{diff_positive[i]:+d}'
            )

            ax.annotate(
                text, (x_pos_diff[i], 0),
                xytext=(0, 10), textcoords='offset points',
                ha='center', va='bottom', size=10, fontweight='bold',
                color='white', family='monospace',
                bbox=dict(
                    facecolor='red', alpha=1, boxstyle='square'
                )
            )

            if show_total_numbers:
                total = np.sum(
                    (diff_positive[i], diff_negative[i], diff_checks[i]))
                text = (
                    f'{total:+d}'
                )

                ax.annotate(
                    text, (x_pos_diff[i], 0),
                    xytext=(0, 70), textcoords='offset points',
                    ha='center', va='bottom', size=12, fontweight='bold',
                    color='black',
                )

    if show_confirmed:
        ax2 = ax.twinx()
        ax2.plot(
            x_pos, total_tests,
            color='gray', linestyle='--',
            marker='o', markerfacecolor='gray',
            alpha=0.2
        )
        ax2.bar(
            x_pos, total_tests,
            alpha=0.3, color='grey',
            label='Jumlah Spesimen'
        )
        ax2.set_ylabel('Jumlah Spesimen', fontsize=14)

        if show_confirmed_numbers:
            for i, val in enumerate(total_tests):
                text = (
                    f'{val:d}'
                )

                ax2.annotate(
                    text, (x_pos[i], val),
                    xytext=(0, 10), textcoords='offset points',
                    ha='center', va='top', size=10, fontweight='bold',
                    color='black', alpha=0.3
                )

        so.align_yaxis_np((ax, ax2))
        ax2.set_yticklabels([f'{abs(x):.0f}' for x in ax2.get_yticks()])

    # INFO

    if show_info:
        text_right = (
            'Data: Situasi Terkini Perkembangan COVID-19 ' +
            '(infeksiemerging.kemkes.go.id)'
            if text_right is None else
            text_right
        )
        ax.text(
            1, -0.1, text_right,
            horizontalalignment='right',
            verticalalignment='top', style='normal', family='monospace',
            transform=ax.transAxes
        )

        text_left = (
            '' if text_left is None else
            text_left
        )

        ax.text(
            0, -0.1, text_left,
            horizontalalignment='left',
            verticalalignment='top', style='normal', family='serif',
            transform=ax.transAxes
        )

    # LEGEND

    ax.set_xticks(x_pos)
    ax.set_xticklabels(date_ticks, rotation=0)
    ax.set_yticklabels([f'{abs(x):.0f}' for x in ax.get_yticks()])

    if show_title:
        text_title = (
            'PERKEMBANGAN JUMLAH SPESIMEN COVID-19 DI INDONESIA'
            if text_title is None else text_title
        )
        ax.set_title(
            text_title,
            fontsize='x-large', fontweight='bold'
        )

    ax.set_xlabel('Tanggal', fontsize=14)
    ax.set_ylabel('$(\\pm)$ Spesimen', fontsize=14)

    if show_legend:
        if show_confirmed:
            handles1, labels1 = ax.get_legend_handles_labels()
            handles2, labels2 = ax2.get_legend_handles_labels()
            ax.legend((handles1 + handles2),
                      (labels1 + labels2), loc='upper left')
        else:
            ax.legend(loc='upper left')

    ax.set_xlim(min(x_pos)-1, max(x_pos)+1)
    ax.margins(x=0.01)
    ax.axhline(0, linestyle='--', color='grey')

    ax.grid(True, axis='both')
    ax.grid(axis='y', linestyle='-.')

    if show_bar is False:
        ax.set_yticks([], [])

    plt.tight_layout()


# def plot_confirmed_percent(
#         dataset, ax, mask=None, days=1,
#         show_info=True, text_left=None, text_right=None,
#         show_title=True, text_title=None,
#         show_numbers=True, show_hist=True,
#         show_legend=True,
#         show_diff_numbers=False, show_diff_bar=True):

#     slice_data = (
#         slice(None, None, days) if mask is None else slice(*mask, days)
#     )

#     data = dataset[slice_data]
#     date_index = data.index
#     date_ticks = date_index.strftime('%d\n%b').to_list()
#     rows, _ = data.shape

#     total_confirmed = data['konfirmasi'].values
#     total_recovered = data['sembuh'].values
#     total_deaths = data['meninggal'].values
#     total_positive = total_confirmed - total_recovered - total_deaths

#     percent_recovered = total_recovered / total_confirmed * 100
#     percent_deaths = total_deaths / total_confirmed * 100
#     percent_positive = total_positive / total_confirmed * 100

#     # Y POSITIONS
#     y_pos = np.arange(0, rows*2, 2)
#     y_pos_diff = y_pos[:-1] + 1

#     y_pos = -y_pos
#     y_pos_diff

#     # BAR
#     # POSITIVE
#     ax.barh(
#         y_pos, total_positive, left=0,
#         color='orange', label='Dalam Perawatan'
#     )

#     # RECOVERED
#     ax.barh(
#         y_pos, -total_recovered, left=0,
#         color='green', label='Sembuh'
#     )

#     # DEATHS
#     ax.barh(
#         y_pos, -total_deaths, left=-total_recovered,
#         color='red', label='Meninggal'
#     )

#     # DIFF

#     diff_confirmed = np.diff(total_confirmed)
#     diff_deaths = np.diff(total_deaths)
#     diff_recovered = np.diff(total_recovered)
#     diff_positive = np.diff(total_positive)

#     # ANNOTATION

#     y_rd = total_recovered + total_deaths

#     if show_numbers:
#         for i, val in enumerate(total_confirmed):

#             if show_hist:

#                 ax.annotate(
#                     f'{percent_positive[i]:.1f}%', (
#                         0, y_pos[i]),
#                     xytext=(10, 0), textcoords='offset points',
#                     ha='left', va='center', size=10,  family='monospace',
#                     color='black',
#                     bbox=dict(
#                         facecolor='white', alpha=1, boxstyle='square',
#                         edgecolor='orange', linewidth=2
#                     )
#                 )

#                 ax.annotate(
#                     f'{percent_recovered[i]:.1f}%', (
#                         0, y_pos[i]),
#                     xytext=(-10, 0), textcoords='offset points',
#                     ha='right', va='center', size=10, family='monospace',
#                     color='black',
#                     bbox=dict(
#                         facecolor='white', alpha=1, boxstyle='square',
#                         edgecolor='green', linewidth=2
#                     )
#                 )

#                 ax.annotate(
#                     f'{percent_deaths[i]:.1f}%', (
#                         0, y_pos[i]),
#                     xytext=(-50, 0), textcoords='offset points',
#                     ha='right', va='center', size=10, family='monospace',
#                     color='black',
#                     bbox=dict(
#                         facecolor='white', alpha=1, boxstyle='square',
#                         edgecolor='red', linewidth=2
#                     )
#                 )

#                 pass

#     # LEGEND

#     if show_title:
#         text_title = (
#             'KASUS KONFIRMASI COVID-19 DI INDONESIA'
#             if text_title is None else text_title
#         )
#         ax.set_title(
#             text_title,
#             fontsize='x-large', fontweight='bold'
#         )

#     ax.set_yticks(y_pos)
#     ax.set_yticklabels(date_ticks, rotation=0)

#     ax.set_ylabel('Tanggal', fontsize=14)
#     ax.set_xlabel('Kasus Konfirmasi', fontsize=14)

#     ax.grid(True, axis='both')

#     if show_legend:
#         ax.legend(loc='upper right')
#     # ax.margins(x=0.01, y=0.3)

#     ax.axvline(0, linestyle='-', color='grey')
#     ax.margins(x=0.3)

#     plt.tight_layout()
