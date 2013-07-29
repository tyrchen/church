// state column chart
function state_distribution_chart(url_or_raw_data, subtitle, transform) {
    var name = "chart-state-distribution";
    var url = '';
    var raw_data = null;

    var container = $('<div id="' + name + '" style="width: 100%; height: 400px; margin: 0 auto"></div>')
        .appendTo('#tab-charts');

    if (typeof url_or_raw_data == 'string' || url_or_raw_data instanceof String) {
        url = url_or_raw_data;
    } else {
        raw_data = url_or_raw_data;
    }

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
                text: 'PR numbers'
            }
        },
        url: url,
        raw_data: raw_data,
        transform: transform
    }
    chart(config);
}

// open/resolve line chart
function catchup_chart(url_or_raw_data, subtitle, transform) {
    var name = "chart-catchup";
    var url = '';
    var raw_data = null;

    var container = $('<div id="' + name + '" style="width: 100%; height: 500px; margin: 0 auto"></div>')
        .appendTo('#tab-charts');

    if (typeof url_or_raw_data == 'string' || url_or_raw_data instanceof String) {
        url = url_or_raw_data;
    } else {
        raw_data = url_or_raw_data;
    }

    var config = {
        container: container,
        type: 'line',
        title: 'PR created/closed Catchup',
        subtitle: subtitle,
        xAxis: {
            tickInterval: 2,
            title: {
                text: 'Weeks'
            }
        },
        yAxis: {
            min: 0,
            title: {
                text: 'PR numbers'
            },
            plotLines: [{
                value: 0,
                width: 1,
                color: '#808080'
            }]
        },
        url: url,
        raw_data: raw_data,
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

    return series;
}

function transform_date_daily(data) {
    return generate_date_stats(data, 'daily', true);
}


function transform_date_weekly(data) {
    return generate_date_stats(data, 'weekly', true);
}

function transform_date_monthly(data) {
    return generate_date_stats(data, 'monthly', true);
}