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

                chart
                    // TODO Create a stacked chart that subtracts specific values from the total.
                    //.stacked(true)
                    .showControls(false)
                    .showLegend(true);
            },

            render: function () {
                var self = this;
                var emptyEventHandler = function () {
                };

                DiscreteBarView.prototype.render.call(self);

                // TODO Find a suitable solution that does not cause errors on window resize.
                // Disable clicking on the legend since we don't properly restyle the chart after data changes.
                for (var property in self.chart.legend.dispatch) {
                    if (self.chart.legend.dispatch.hasOwnProperty(property)) {
                        self.chart.legend.dispatch[property] = emptyEventHandler;
                    }
                }
            }

        });

        return StackedBarView;
    });
