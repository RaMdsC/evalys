# coding: utf-8

import matplotlib.gridspec

from . import core
from . import gantt
from . import lifecycle
from . import series
from .. import utils


class DetailsLayout(core.EvalysLayout):
    def __init__(self, *, wtitle='Workload overview'):
        super().__init__(wtitle=wtitle)

        gs = matplotlib.gridspec.GridSpec(nrows=4, ncols=1)

        visualizations = 'utilization', 'queue', 'lifecycle', 'gantt'
        for idx, visu in enumerate(visualizations):
            self.sps[visu] = gs[idx, :]

    def show(self):
        # hacky way to enforce sharing of axes
        axes = self.fig.get_axes()
        axes[0].get_shared_x_axes().join(*axes)

        super().show()


def plot_details(jobset, *, title='Workload overview', **kwargs):
    visualizations = {
        'gantt': gantt.GanttVisualization,
        'lifecycle': lifecycle.LifecycleVisualization,
        'queue': series.QueueSeriesVisualization,
        'utilization': series.UtilizationSeriesVisualization,
    }

    layout = DetailsLayout(wtitle=title)
    for spskey, visu_cls in visualizations.items():
        plot = layout.inject(visu_cls, spskey=spskey)
        utils.bulksetattr(plot, **kwargs)
        plot.build(jobset)
    layout.show()
