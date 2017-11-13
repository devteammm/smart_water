from main.fusioncharts import FusionCharts
from main.models import *
from main.apis import *

def revenue_chart(company=None,r = 12):
    times = Month.objects.all()

    top_12_time = times[:12]
    top_12_time =  top_12_time.reverse()
    month_label = [{'label': '%s / %s'%(time.month,time.year)} for time in top_12_time]

    total_money_top_12 = [{'value':
        '%s'% get_total_money(company,month=time.month,year=time.year)}
        for time in top_12_time
        ]

    paid_money_top_12 = [{'value':
        '%s'%get_total_money(company,month=time.month,year=time.year)}
        for time in top_12_time
        ]

    revenue_source = {}
    revenue_source["chart"] = {
        "caption": 'Thong ke doanh thu',
        "subcaption": '12 thang gan nhat',
        "xaxisname": "Thang",
        "yaxisname": "So tien (VND)",
        "numberprefix": "VND",
        "theme": "ocean"
    }
    revenue_source["categories"] = [{
        "category": month_label
    }]


    revenue_source["dataset"] = [{
            "seriesname": "Tong so tien can thu",
            "data": total_money_top_12
        }, {
            "seriesname": "Tong so tien thu duoc",
            "showvalues": "0",
            "data": paid_money_top_12
        }
    ]

    # Create an object for the mscombi2d chart using the FusionCharts class constructor
    chart = FusionCharts("mscombi2d", "ex3", "100%", 400, "revenue_chart", "json", revenue_source)

    return chart

def used_chart(company=None,r = 12):
    times = Month.objects.all()

    top_12_time = times[:12]
    top_12_time = top_12_time.reverse()
    month_label = [{'label': '%s / %s'%(time.month,time.year)} for time in top_12_time]

    total_used_top_12 = [{'value':
        '%s'% get_total_used(company,month=time.month,year=time.year)}
        for time in top_12_time
        ]

    revenue_source = {}
    revenue_source["chart"] = {
        "caption": 'Thong ke su dung nuoc',
        "subcaption": '12 thang gan nhat',
        "xaxisname": "Thang",
        "yaxisname": "So nuoc",
        # "numberprefix": "VND",
        "theme": "ocean"
    }
    revenue_source["categories"] = [{
        "category": month_label
    }]

    revenue_source["dataset"] = [{
            "seriesname": "Tong so nuoc da su dung",
            "data": total_used_top_12
        }
    ]

    # Create an object for the mscombi2d chart using the FusionCharts class constructor
    chart = FusionCharts("mscombi2d", "total_used_chart", "100%", 400, "used_chart", "json", revenue_source)

    return chart
