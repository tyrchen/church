function list_accum(l) {
    var new_list = [];
    _.each(l, function(item, i) {
        if(i > 0) {
            new_list.push(item + new_list[i-1]);
        } else {
            new_list.push(item)
        }
    });
    return new_list;
}

function generate_date_stats(data, type, accumulate) {
    var TYPES = {
        'daily': {
            len: moment().dayOfYear() + 1,
            fun: function(x) {return moment(x).dayOfYear();}
        },
        'weekly': {
            len: moment().week() + 1,
            fun: function(x) {return moment(x).week();}
        },
        'monthly': {
            len: moment().month() + 1 + 1,
            fun: function(x) {return moment(x).month() + 1;}
        }
    }

    var series = [{
        name: 'Opened',
        data: []
    }, {
        name: 'Resolved',
        data: []
    }];

    // initialize the data
    for(var i=0;i<TYPES[type].len;i++) {
        series[0].data.push(0);
        series[1].data.push(0);
    }

    _.each(data, function(item) {
        if (moment().year() != moment(item.arrived_at).year()) return;
        var pos_opened = TYPES[type].fun(item.arrived_at);
        if (pos_opened == 50) {
            console.log(item.arrived_at);
        }


        series[0].data[pos_opened]++;

        if (_.indexOf(['feedback', 'monitored', 'suspended', 'closed'], item.state) >= 0) {
            var pos_resolved = TYPES[type].fun(item.modified_at);
            series[1].data[pos_resolved]++;
        }
    });

    if (accumulate) {
        series[0].data = list_accum(series[0].data);
        series[1].data = list_accum(series[1].data);
    }


    return series;
}

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
        if (config.raw_data) {
            var series = config.transform(config.raw_data);
            render(series);
        } else {
            render(config.series);
        }
    }

}