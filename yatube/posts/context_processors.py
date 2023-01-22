from datetime import datetime


def year(request):
    years = datetime.now().year
    return {'year': years}