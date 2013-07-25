
function chart(config) {
    function render(series) {
        config.container.highcharts({
            chart: {
                type: config.type
            },
            title: {
                text: config.title
            },
            subtitle: {
                text: config.subtitle
            },
            xAxis: config.xAxis,
            yAxis: config.yAxis,
            tooltip: {
                headerFormat: '<span style="font-size:10px">{point.key}</span><table>',
                pointFormat: '<tr><td style="color:{series.color};padding:0">{series.name}: </td>' +
                    '<td style="padding:0"><b>{point.y}</b></td></tr>',
                footerFormat: '</table>',
                shared: true,
                useHTML: true
            },
            plotOptions: {
                column: {
                    pointPadding: 0.2,
                    borderWidth: 0
                }
            },
            series: series
        });
    }
    if (config.url) {
        $.getJSON(config.url, function(items) {
            var series = config.transform(items);
            render(series);
        })
    } else {
        render(config.series);
    }

}

function state_distribution(url, subtitle, transform) {
    var name = "chart-state-distribution";
    var container = $('<div id="' + name + '" style="width: 100%; height: 400px; margin: 0 auto"></div>')
        .appendTo('#tab-charts');

    var config = {
        container: container,
        type: 'column',
        title: 'PR State Distribution',
        subtitle: subtitle,
        xAxis: {
            categories: ['open', 'analyzed', 'info', 'feedback', 'monitored', 'suspended', 'closed']
        },
        yAxis: {
            min: 0,
            title: {
                text: 'PR number'
            }
        },
        url: url,
        transform: transform
    }
    chart(config);
}

// transforms

function transform_level_state(data) {
    var series = [{
        name: "High",
        data: [0, 0, 0, 0, 0, 0, 0]
    }, {
        name: "Medium",
        data: [0, 0, 0, 0, 0, 0, 0]
    }, {
        name: "Low",
        data: [0, 0, 0, 0, 0, 0, 0]
    }]
    var categories = {
        'open': 0,
        'analyzed': 1,
        'info': 2,
        'feedback': 3,
        'monitored': 4,
        'suspended': 5,
        'closed': 6
    }

    _.each(data, function(item) {
        var level = parseInt(item.level.split('-')[0]);
        var state = item.state;
        var pos;
        if (level <=2) {
            pos = 0;
        } else if (level <= 4) {
            pos = 1;
        } else {
            pos = 2;
        }
        series[pos].data[categories[state]]++;
    })

    console.log(series);
    return series;
}