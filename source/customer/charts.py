from main.fusioncharts import FusionCharts
from main.models import *
from main.apis import get_customer_used,get_customer_money

def customer_used_chart(customer=None,r = 12):
    times = Month.objects.all()
    top_times = times[:r]
    top_times = top_times.reverse()

    labels = [{'label': '%s / %s'%(time.month,time.year)} for time in top_times]

    top_useds = [{'value': get_customer_used(customer=customer,month=time.month,year=time.year)}
        for time in top_times
        ]

    source = {}
    source["chart"] = {
        "caption": 'Thong ke su dung nuoc',
        "subcaption": '12 thang gan nhat',
        "xaxisname": "Thang",
        "yaxisname": "So nuoc",
        # "numberprefix": "VND",
        "theme": "ocean"
    }
    source["categories"] = [{
        "category": labels
    }]

    source["dataset"] = [{
            "seriesname": "Tong so nuoc da su dung",
            "data": top_useds
        }
    ]

    chart = FusionCharts("mscombi2d", "customer_used_chart", "100%", 400, "used_chart", "json", source)

    return chart

def customer_money_chart(customer=None,r = 12):
    times = Month.objects.all()
    top_times = times[:r]
    top_times = top_times.reverse()

    labels = [{'label': '%s / %s'%(time.month,time.year)} for time in top_times]

    top_useds = [{'value': get_customer_money(customer=customer,month=time.month,year=time.year)}
        for time in top_times
        ]

    source = {}
    source["chart"] = {
        "caption": 'Thong ke tien nuoc',
        "subcaption": '12 thang gan nhat',
        "xaxisname": "Thang",
        "yaxisname": "Tien nuoc",
        # "numberprefix": "VND",
        "theme": "ocean"
    }
    source["categories"] = [{
        "category": labels
    }]

    source["dataset"] = [{
            "seriesname": "So tien phai chi tra",
            "data": top_useds
        }
    ]

    chart = FusionCharts("mscombi2d", "customer_money_chart", "100%", 400, "money_chart", "json", source)

    return chart
