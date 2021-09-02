from django.contrib.messages.api import success
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth import authenticate, login, logout

# from django.contrib.messages import constants as messages
from django.contrib import messages

from django.contrib.auth.decorators import login_required

from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.authtoken.models import Token

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import Customer
from .serializers import *
from .forms import CreateUserForm


# Create your views here.

@api_view(['POST',])      # Это открывает внешний доступ!!!!
def registerPageRest(request):

    if request.method == 'POST':
        serializer = RegistrationSerializer(data=request.data)
        data = {}

        if serializer.is_valid():
            account = serializer.save()
            data['response'] = 'success of register'
            data['username'] = account.username
            data['email'] = account.email
            token = Token.objects.get(user=account).key
            data['token'] = token
        else:
            data = serializer.errors
        return Response(data)

# Это как и первый, только через Форму
# @api_view(['POST',])      # Это открывает внешний доступ!!!!
# def registerPageRest(request):

#     if request.method == 'POST':
#         form = CreateUserForm()
#         data = {}

#         if form.is_valid():
#             account = form.save()
#             data['response'] = 'success of register'
#             data['username'] = form.cleaned_data.get('username')
#             data['email'] = account.email
#             # token = Token.objects.get(user=account).key
#             # data['token'] = token
#         else:
#             data = form.errors
#         return Response(data)


# Authorization
# def registerPage(request):
#     if request.user.is_authenticated:
#         return redirect("testpage")
#     else:
#         form = CreateUserForm()
#         # form = UserCreationForm()

#         if request.method == 'POST':
#             form = CreateUserForm(request.POST)
#             # form = UserCreationForm(request.POST)
#             if form.is_valid():
#                 form.save()
#                 user = form.cleaned_data.get('username')
#                 messages.success(request, 'Created user ' + user)

#                 return redirect('login')

#         context = {'form' : form}    # Это информация, которую мы передаем ввиде словаря в наш шаблон
#         return render(request, 'accounts/register.html', context)     

# def loginPage(request):
#     if request.user.is_authenticated:
#         return redirect("testpage")
#     else:
#         if request.method == 'POST':
#             username = request.POST.get('username')
#             password = request.POST.get('password')

#             user = authenticate(request, username=username, password=password)

#             if user is not None:
#                 login(request, user)
#                 return redirect('testpage')
#             else:
#                 messages.info(request, 'Username or password is incorrect')

#         context = {}            
#         return render(request, 'accounts/login.html', context)

@login_required(login_url = 'login')
def testPage(request):
    context = {}
    return render(request, 'accounts/testpage.html', context)

def logoutUser(request):
    logout(request)
    return redirect('login')

@api_view(['GET', 'POST'])
# @login_required(login_url = 'login')
@permission_classes((IsAuthenticated,))
def customers_list(request):
    """
    List  customers, or create a new customer.
    """
    if request.method == 'GET':
        data = []
        nextPage = 1
        previousPage = 1
        customers = Customer.objects.all()
        page = request.GET.get('page', 1)
        paginator = Paginator(customers, 10)
        try:
            data = paginator.page(page)
        except PageNotAnInteger:
            data = paginator.page(1)
        except EmptyPage:
            data = paginator.page(paginator.num_pages)

        serializer = CustomerSerializer(data,context={'request': request} ,many=True)
        if data.has_next():
            nextPage = data.next_page_number()
        if data.has_previous():
            previousPage = data.previous_page_number()

        return Response({'data': serializer.data , 'count': paginator.count, 'numpages' : paginator.num_pages, 'nextlink': '/api/customers/?page=' + str(nextPage), 'prevlink': '/api/customers/?page=' + str(previousPage)})

    elif request.method == 'POST':

        # 5:50 ????
        # Таким образом в поле telegram_id передается имя пользователя
        account = request.user
        user_customer = Customer(telegram_id=account)
        print(user_customer)

        serializer = CustomerSerializer(user_customer, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# The User which is created customer, only can do this operations
# For this I need to add User/Author to table of Customers
# And this is Telegram_id !!!!!!!
# The same I need to do with Telega
@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes((IsAuthenticated,))
def customers_detail(request, pk):
    """
    Retrieve, update or delete a customer by id/pk.
    """
    try:
        customer = Customer.objects.get(pk=pk)
    except Customer.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)



    if request.method == 'GET':
        serializer = CustomerSerializer(customer,context={'request': request})
        return Response(serializer.data)

    user = request.user
    # print(type(str(user)))
    # print(type(customer.telegram_id))
    if customer.telegram_id != str(user):
        return Response({'response': "You don't have permissions to edit that."})
    # Do I need to do elif lower ????
    
    elif request.method == 'PUT':
        serializer = CustomerSerializer(customer, data=request.data,context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        customer.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

