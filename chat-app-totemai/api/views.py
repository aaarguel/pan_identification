from django.shortcuts import render

from rest_framework import viewsets,status
from rest_framework.decorators import api_view

from rest_framework.response import Response


from .serializers import ThreadSerializer
from chat.models import Thread

#TF
import pandas as pd
import numpy as np
import string
import nltk
from nltk.corpus import stopwords
import joblib
from nltk.stem import WordNetLemmatizer
import os
from num2words import num2words
import json






def function_analize(texto):
    df = pd.Series(data = [texto], index = [0])

    df_conv = df.apply(lambda x: x.lower().replace('|', ' '))
    #print(df_conv)

    df_conv = df_conv.apply(lambda x: ' '.join([num2words(word) if word.isnumeric() and int(word)<1000000000 else word for message in x.split('|') for word in message.split(' ')]))
    #print(df_conv)

    df_conv = df_conv.apply(lambda x: x.translate(str.maketrans('', '', string.punctuation)))
    #print(df_conv)

    with open('abbreviations.json', 'r') as fp:
        abbr_dict = json.load(fp)

    df_conv = df_conv.apply(lambda x: ' '.join([abbr_dict[word] if word in abbr_dict.keys() else word for word in x.split(' ') ]))

    stop = stopwords.words('english')
    df_conv = df_conv.apply(lambda x: ' '.join([word for word in x.split() if word not in (stop)]))

    df_conv = df_conv.apply(lambda x: x.translate(str.maketrans('', '', string.punctuation)))

    df_conv = df_conv.apply(lambda x: ' '.join([word for word in x.split(' ') if word.isalpha()]))
    wordnet_lemmatizer = WordNetLemmatizer()
    df_conv = df_conv.apply(lambda x: ' '.join([wordnet_lemmatizer.lemmatize(word, pos='v') for word in x.split(' ')]))

    vectorizer = joblib.load(os.path.join(os.getcwd(), "vectorizer.joblib"))
    model = joblib.load(os.path.join(os.getcwd(), "modeloOG.joblib"))

    Xtest = vectorizer.transform(df_conv)
    prediction = model.predict(Xtest)
    if prediction == 1:
        return True
        
    else:
        return  False
        

@api_view(['GET', 'POST'])
def verify_chats(request):
    """
    List all messages to verify
    """
    if request.method == 'GET':
        objs = []
        threads = Thread.objects.prefetch_related('chatmessage_thread').order_by('timestamp')  
        for e in threads:            
            serializer = ThreadSerializer(e)
            conversation=""
            for message in serializer.data['chatmessage_thread']:
                conversation += message['message'] + "|"
            #objs.append(serializer.data['chatmessage_thread'])
            
            response = {}
            response['is_depredator'] = function_analize(conversation)
            response['first_person'] = serializer.data['first_person']
            response['second_person'] = serializer.data['second_person']
            response['conversation'] = conversation
            print("Is depredator: " + str(response['is_depredator']))
            print(conversation)
            #response['data'] = serializer.data
            objs.append(response)
        return Response(objs)

    elif request.method == 'POST':
        #serializer = SnippetSerializer(data=request.data)
        #if serializer.is_valid():
        #    serializer.save()
        #    return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response('Error', status=status.HTTP_400_BAD_REQUEST)



class ThreadViewSet(viewsets.ModelViewSet):
    queryset = Thread.objects.prefetch_related('chatmessage_thread').order_by('timestamp')
    serializer_class = ThreadSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = Thread.objects.all()
    serializer_class = ThreadSerializer
