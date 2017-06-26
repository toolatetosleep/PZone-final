from django.test import TestCase
from django.shortcuts import render
from django.template import Context
from django.http import HttpResponse


# Create your tests here.

def test(req):
    return render(req, 'test.html', Context({'1': 1}))
