from django.shortcuts import render
from bs4 import BeautifulSoup as bs
import requests, re
from collections import Counter
import csv


from .models import website


from .forms import textField
# Create your views here.

def index(request):
    return render(request, 'counter/index.html')


def frequency(request):
    form = textField()

    context={"form":form}
    return render(request, 'counter/frequency.html', context)


def results(request):

    form = textField()

    if request.method == "POST":
        form = textField(request.POST)
        url_data = request.POST.get('url')
        try:
            data = website.objects.get(url=url_data)
            status = "The results are fetched from the database"
            context = {'url_data':url_data, 'most_occur':data.words, "status":status}

            return render(request, "counter/results.html", context)

        except website.DoesNotExist:
            status = "The results are computed now"

            url=url_data
            page=requests.get(url)
            soup=bs(page.content,'lxml')
            content = soup.get_text(separator=' ')

            getVals = list([val for val in content
                           if val.isalpha() or val.isspace()])

            result = "".join(getVals)


            with open('counter/words.csv') as File:
                reader = csv.reader(File, delimiter=',', quotechar=',',
                                    quoting=csv.QUOTE_MINIMAL)
                count = 0
                common_words = []
                for row in reader:
                    if count<104:
                        common_words.append(row[0].split(';')[1])
                    count += 1


            result = result.lower()
            words=result.split()


            filtered_words = []
            for word in words:
                if word not in common_words:
                    filtered_words.append(word)

            counter = Counter(filtered_words)
            most_occur = counter.most_common(10)


            site_list = website(url=url_data, words=most_occur)
            site_list.save()
            context = {'url_data':url_data, 'result':result, 'most_occur':most_occur, "status":status}
            return render(request, 'counter/results.html', context)
