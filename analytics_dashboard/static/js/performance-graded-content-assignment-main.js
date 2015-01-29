require(['vendor/domReady!', 'load/init-page'], function (doc, page) {
    'use strict';

    require(['underscore', 'views/data-table-view', 'views/stacked-bar-view'],
        function (_, DataTableView, StackedBarView) {
            var tableColumns,
                model = page.models.courseModel,
                graphSubmissionColumns = [
                    {
                        key: 'correct_submissions',
                        title: gettext('Correct Submissions'),
                        className: 'text-right',
                        type: 'number',
                        color: '#4BB4FB'
                    },
                    {
                        key: 'incorrect_submissions',
                        title: gettext('Incorrect Submissions'),
                        className: 'text-right',
                        type: 'number',
                        color: '#CA0061'
                    }
                ],
                tableSubmissionColumns = [{
                    key: 'total_submissions',
                    title: gettext('Total Submissions'),
                    className: 'text-right',
                    type: 'number',
                    color: '#4BB4FB'
                }].concat(graphSubmissionColumns);

            new StackedBarView({
                el: '#chart-view',
                model: model,
                modelAttribute: 'problems',
                truncateXTicks: true,
                trends: graphSubmissionColumns,
                x: {key: 'name'},
                y: {key: 'count'},
                /* Translators: This string is used for a tooltip heading (e.g. Problem: What is 2+2?).
                 Do NOT translate the word "value". */
                interactiveTooltipHeaderTemplate: _.template(gettext('Problem: <%=value%>'))
            });

            tableColumns = [
                {key: 'index', title: gettext('Order'), type: 'number', className: 'text-right'},
                {key: 'name', title: gettext('Problem Name')}
            ].concat(tableSubmissionColumns);

            new DataTableView({
                el: '[data-role=problem-table]',
                model: model,
                modelAttribute: 'problems',
                columns: tableColumns,
                sorting: ['index']
            });
        });
});
