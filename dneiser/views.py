from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from dneiser.models import *
from django.db.models import Q
from django.core.paginator import Paginator
from django.contrib.auth import authenticate, login, get_user_model, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import LoginForm, RegisterForm



def index_index(request):
    return render(request, 'dneiser/index.html')
    
def index_index1(request):
    return render(request, 'dneiser/index1.html')
    
def index_detalles(request):
    return render(request, 'dneiser/detalles.html')
    
def index_maqui_page(request):
    return render(request, 'dneiser/maqui_page.html')
    
def index_papeleria(request):
    return render(request, 'dneiser/papeleria.html')
    
def index_golosina(request):
    return render(request, 'dneiser/golosina.html')
# Create your views here.

class ProductCreateView(LoginRequiredMixin, View):
    template_name= 'dneiser/formulario.html'
    
    def get (self, request, *args, **kwargs):
        categories = Category.objects.all()
        return render(request, self.template_name,{'categories': categories})
        
    def post(self, request, *args, **kwargs):
        name = request.POST.get("name")
        price = request.POST.get("price")
        description = request.POST.get("description","")
        stock = request.POST.get("stock")
        category_id = request.POST.get("category")
        category = Category.objects.filter(id=category_id).first() if category_id else none
        image_file= request.FILES.get('image')
        
        new_product= Product.objects.create(
        name=name,
        price=price,
        description=description,
        stock=stock,
        image=image_file,
        category=category
        )
        
        return redirect('product_list')
        
class ProductListView(LoginRequiredMixin, View):
    template_name = 'dneiser/product_list.html'
    paginate_by =2
    
        
    def get(self, request,*args, **kwargs):
        query= request.GET.get('q')
        products = Product.objects.all()
        
        if query: 
            products =products.filter(
                Q(name__icontains=query) |
                Q(description__icontains=query)
            ).distinct()
            
        paginator= Paginator(products, self.paginate_by)
        page_number = request.GET.get('page')
        page_obj =  paginator.get_page(page_number)
        
        context = {
            'page_obj' : page_obj,
            'products': page_obj.object_list,
            'query': query
        }
            
        return render(request, self.template_name,context)

class ProductDetailView(LoginRequiredMixin,View):
    template_name='dneiser/product_detail.html'

    def get(self,request, id, *args, **kwargs):
        product = get_object_or_404(Product, id=id)
        return render(request, self.template_name,{'product': product})



#-----------------------------------------------------------------
# 
#-----------------------------------------------------------------
class ProductUpdateView(LoginRequiredMixin, View):
    template_name = 'dneiser\product_update.html'

    def get(self, request, id , *args, **kwargs):
        product=get_object_or_404(Product, id=id)
        categories = Category.objects.all()
        return render(request, self.template_name,{'product':product, 'categories': categories})

    def post(self, request, id, *args, **kwargs):
        product = get_object_or_404(Product, id=id)
        
        name = request.POST.get("name")
        price = request.POST.get("price")
        description = request.POST.get("description","")
        available = request.POST.get("available")=="on"
        category_id = request.POST.get("category")
        new_image_file= request.FILES.get('image')
        category = Category.objects.filter(id=category_id).first() if category_id else none

        product.price =price
        product.name = name
        product.description = description
        product.available = available
        product.category = category
        if new_image_file:
            if product.image and product.image.name:
                product.image.delete(save=False)
            product.image = new_image_file
        
        product.save()
    
        return redirect('product_list')
        
        
class ProductDeleteView(LoginRequiredMixin,View):
    template_name ='dneiser\product_confirm_delete.html'
    
    def get(self, request, id, *args, **kwargs):
        product = get_object_or_404(Product, id=id)
        return render(request, self.template_name, {'product': product})
        
    def post(self, request, id, *args, **kwargs):
        product = get_object_or_404(Product, id=id)
        product.delete()
        
        return redirect('product_list')
        
    

class UserLoginView(View):
    template_name= 'dneiser/login.html'
    
    def get(self, request, *args, **kwargs):
        form = LoginForm()
        return render(request, self.template_name, {'form': form})
        
    def post(self, request, *args, **kwargs):
        form =LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            
            
            user=authenticate(request, username=username, password=password)
            
            if user is not None:
                login(request,user)
                return redirect('index')
            else:
                return render(request, self.template_name,{
                    'form':form,
                    'error_message': 'Nombre de ususario o contraseña incorrectos'
                })
        return render(request, self.template_name, {'form':form})  
        
        
        
class UserRegisterView(View):
        template_name= 'dneiser/register.html'
        
        def get(self, request, *args, **kwargs):
            form= RegisterForm()
            return render(request, self.template_name, {'form': form})
            
        def post(self, request, *args, **kwargs):
            form =RegisterForm(request.POST)
            
            if request.user.is_authenticated:
                return redirect('product_list')  
                
            if form.is_valid():
                username = form.cleaned_data['username']
                email= form.cleaned_data['email']
                password= form.cleaned_data['password']
                
                
                User= get_user_model()
                user= User.objects.create_user(username=username, email=email, password=password)
                
                login(request, user)
                
                return redirect('product_list')
                
            return render(request, self.template_name,{'form':form})
            
            

class UserLogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('index')
        
        