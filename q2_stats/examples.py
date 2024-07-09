# ----------------------------------------------------------------------------
# Copyright (c) 2022-2023, QIIME 2 development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------

import os
import pkg_resources

import qiime2


def _get_data_from_tests(path):
    return pkg_resources.resource_filename('q2_stats.tests',
                                           os.path.join('data', path))


def faithpd_timedist_factory():
    return qiime2.Artifact.import_data(
        'Dist1D[Ordered, Matched]', _get_data_from_tests('faithpd_timedist')
    )


def faithpd_refdist_factory():
    return qiime2.Artifact.import_data(
        'Dist1D[Unordered, Independent]',
        _get_data_from_tests('faithpd_refdist')
    )


def stats_table_factory():
    return qiime2.Artifact.import_data(
        'StatsTable[Pairwise]', _get_data_from_tests('stats_table')
    )


def wilcoxon_baseline0(use):
    timedist = use.init_artifact('timedist', faithpd_timedist_factory)

    stats_table, = use.action(
        use.UsageAction('stats', 'wilcoxon_srt'),
        use.UsageInputs(
            distribution=timedist,
            compare='baseline',
            baseline_group='0',
            p_val_approx='asymptotic',
        ),
        use.UsageOutputNames(
            stats='stats'
        )
    )

    stats_table.assert_output_type('StatsTable[Pairwise]')


def mann_whitney_pairwise(use):
    timedist = use.init_artifact('timedist', faithpd_timedist_factory)
    refdist = use.init_artifact('refdist', faithpd_refdist_factory)

    stats_table, = use.action(
        use.UsageAction('stats', 'mann_whitney_u'),
        use.UsageInputs(
            distribution=refdist,
            compare='all-pairwise',
            against_each=timedist,
            p_val_approx='asymptotic',
        ),
        use.UsageOutputNames(
            stats='stats'
        )
    )

    stats_table.assert_output_type('StatsTable[Pairwise]')


def plot_rainclouds(use):
    timedist = use.init_artifact('timedist', faithpd_timedist_factory)
    stats_table = use.init_artifact('stats_table', stats_table_factory)

    _, raincloud = use.action(
        use.UsageAction('stats', 'plot_rainclouds'),
        use.UsageInputs(
            data=timedist,
            stats=stats_table,
        ),
        use.UsageOutputNames(
            raincloud_plot='raincloud_plot'
        )
    )

    raincloud.assert_output_type('Visualization')
