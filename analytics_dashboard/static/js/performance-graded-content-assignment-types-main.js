require(['vendor/domReady!', 'load/init-page'], function (doc, page) {
    'use strict';

    require(['underscore', 'views/data-table-view', 'views/stacked-bar-view'],
        function (_, DataTableView, StackedBarView) {
            var tableColumns,
                model = page.models.courseModel,
                assignmentType = model.get('assignmentType'),
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
                modelAttribute: 'assignments',
                truncateXTicks: true,
                trends: graphSubmissionColumns,
                x: {key: 'id', displayKey: 'name'},
                y: {key: 'count'},
                interactiveTooltipHeaderTemplate: _.template(assignmentType + ': <%=value%>'),
                click: function (d) {document.location.href = d.url;}
            });

            tableColumns = [
                {key: 'index', title: gettext('Order'), type: 'number', className: 'text-right'},
                {key: 'name', title: gettext('Assignment Name')},
                {key: 'num_problems', title: gettext('Problems'), type: 'number', className: 'text-right'}
            ].concat(tableSubmissionColumns);

            new DataTableView({
                el: '[data-role=assignment-table]',
                model: model,
                modelAttribute: 'assignments',
                columns: tableColumns,
                sorting: ['index']
            });
        });
});
