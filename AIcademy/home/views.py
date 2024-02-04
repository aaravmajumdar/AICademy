from django.shortcuts import render, HttpResponse
from .models import studyresource
from django.conf import settings
from transformers import pipeline
# Create your views here.
def index(request):
    return render(request, 'index.html')

def summarizer(request):
    analyzed = ''
    djtext = request.GET.get('text', 'default')
    if djtext == None or djtext == 'default':
        params = {'purpose': 'Summarize', 'analyzed_text':'Please enter the text'}
    else:
        print(djtext)
        summarizer = pipeline('summarization')
        summary = summarizer(djtext, max_length=400, min_length=200, do_sample=False,truncation=True )
        analyzed += summary[0]['summary_text']
        params = {'purpose': 'Summarize', 'analyzed_text': analyzed}
        return render(request,'analyze.html', params)
        # print(summary[0]['summary_text'])
    return render(request,'summarizer.html', params)

from openai import OpenAI

client = OpenAI(
  organization='org-cV3PtBhXu18DYcZYGoa2008H',
  api_key='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'
)

import os 
def chatmax(request):
    analyzed = ''
    file_path = os.path.join(settings.BASE_DIR, 'AIcademy\\templates\\chatlog.txt')
    question = request.GET.get('ChatResponse', 'default')
    if question == '' or question == 'default':
        params = {'purpose': 'ChatResponse', 'analyzed_text':'Please enter the query'}
    else:
        prompt = f"You: {question}\n Max:"
        response = client.completions.create(model="gpt-3.5-turbo-instruct",prompt=prompt)
        answer = response.choices[0].text
        analyzed+=answer
        params = {'purpose':'ChatResponse', 'analyzed_text': analyzed}
        return render(request,'analyze1.html', params)
    return render(request,'chat.html',params)

from django.shortcuts import render

def study_resource_list(request):
    resources = studyresource.objects.filter(subject='English')
    params = {'resources': resources}
    print(resources)
    return render(request, 'study_resource_list.html', params)

def braille(request):
    def text_to_braille(text):
        braille_map = {
            'a': '⠁', 'b': '⠃', 'c': '⠉', 'd': '⠙', 'e': '⠑',
            'f': '⠋', 'g': '⠛', 'h': '⠓', 'i': '⠊', 'j': '⠚',
            'k': '⠅', 'l': '⠇', 'm': '⠍', 'n': '⠝', 'o': '⠕',
            'p': '⠏', 'q': '⠟', 'r': '⠗', 's': '⠎', 't': '⠞',
            'u': '⠥', 'v': '⠧', 'w': '⠺', 'x': '⠭', 'y': '⠽',
            'z': '⠵',
            '1': '⠼⠁', '2': '⠼⠃', '3': '⠼⠉', '4': '⠼⠙', '5': '⠼⠑',
            '6': '⠼⠋', '7': '⠼⠛', '8': '⠼⠓', '9': '⠼⠊', '0': '⠼⠚',
            ',': '⠂', ';': '⠆', ':': '⠒', '.': '⠲', '!': '⠖', '?': '⠦',
            '(': '⠴', ')': '⠶', '[': '⠦', ']': '⠴', '{': '⠐', '}': '⠰',
            '-': '⠤', '_': '⠤', "'": '⠄', '"': '⠐', '/': '⠤'
        }

        braille_result = ''
        for char in text:
            braille_result += braille_map.get(char.lower(), char)

        return braille_result

# Function to convert Braille to text
# Function to convert Braille to text
    def braille_to_text(braille):
        text_map = {
            '⠁': 'a', '⠃': 'b', '⠉': 'c', '⠙': 'd', '⠑': 'e',
            '⠋': 'f', '⠛': 'g', '⠓': 'h', '⠊': 'i', '⠚': 'j',
            '⠅': 'k', '⠇': 'l', '⠍': 'm', '⠝': 'n', '⠕': 'o',
            '⠏': 'p', '⠟': 'q', '⠗': 'r', '⠎': 's', '⠞': 't',
            '⠥': 'u', '⠧': 'v', '⠺': 'w', '⠭': 'x', '⠽': 'y',
            '⠵': 'z',
            '⠼⠁': '1', '⠼⠃': '2', '⠼⠉': '3', '⠼⠙': '4', '⠼⠑': '5',
            '⠼⠋': '6', '⠼⠛': '7', '⠼⠓': '8', '⠼⠊': '9', '⠼⠚': '0',
            '⠂': ',', '⠆': ';', '⠒': ':', '⠲': '.', '⠖': '!', '⠦': '?',
            '⠴': '(', '⠶': ')', '⠦': '[', '⠴': ']', '⠐': '{', '⠰': '}',
            '⠤': '-', '⠄': "'", '⠐': '"', '⠤': '/'
        }

        text_result = ''
        
        for j in braille:
            text_result += text_map.get(j.lower(), j)
            '''while i < len(braille):
            if braille[i:i+2] in text_map:
                text_result += text_map[braille[i:i+2]]
                i += 2
            else:
                text_result += braille[i]
                i += 1'''

        return text_result
    
    question = request.GET.get('BrailleResponse', 'default')

    if question == None or question == 'default':
        params = {'purpose': 'BrailleToText', 'analyzed_text':'Please enter the text'}
    else:
        analyzed = ''
        braille_text = braille_to_text(question)
        analyzed+=braille_text
        params = {'purpose':'BrailleResponse', 'analyzed_text': analyzed}
        return render(request,'analyzebraille.html', params)
    
    return render(request,'braille.html')

    # Example usage
    # text = "Hello, World!"
    # braille_text = text_to_braille(text)
    # print(f"Text to Braille: {braille_text}")


    # converted_text = braille_to_text(braille_text)
    # print(f"Braille to Text: {converted_text}")

def quiz(request):
    return render(request, "quiz.html") 

