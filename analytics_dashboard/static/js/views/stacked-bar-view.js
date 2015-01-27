define(['nvd3', 'underscore', 'views/discrete-bar-view'],
    function (nvd3, _, DiscreteBarView) {
        'use strict';

        var StackedBarView = DiscreteBarView.extend({
            getChart: function () {
                return nvd3.models.multiBarChart();
            },

            initChart: function (chart) {
                var self = this;
                DiscreteBarView.prototype.initChart.call(self, chart);

                chart.stacked(true)
                    .showControls(false)
                    .showLegend(false);
            }

        });

        return StackedBarView;
    });
