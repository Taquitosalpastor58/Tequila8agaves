# Importaciones necesarias
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser, VentaBarra, Inventario, Categoria, Proveedor, NotaProveedor, MensajeCocina

# Formulario de creación de usuario personalizado
class CustomUserCreationForm(UserCreationForm):
    """
    Formulario para la creación de usuarios personalizados.
    Extiende el formulario de creación de usuarios de Django.
    """
    class Meta:
        # Especifica el modelo que se utilizará para crear el formulario
        model = CustomUser
        # Campos que se incluirán en el formulario
        fields = ('username', 'role', 'password1', 'password2')

# Formulario de autenticación (inicio de sesión)
class LoginForm(AuthenticationForm):
    """
    Formulario de autenticación para el inicio de sesión.
    Extiende el formulario de autenticación de Django.
    """
    pass

# Formulario para registrar ventas en barra
class VentaBarraForm(forms.ModelForm):
    """
    Formulario para registrar ventas en la barra.
    Utiliza el modelo VentaBarra.
    """
    class Meta:
        model = VentaBarra
        # Campos que se incluirán en el formulario
        fields = ['producto', 'cantidad_vendida']

# Formulario para agregar productos al inventario
class InventarioForm(forms.ModelForm):
    class Meta:
        model = Inventario
        fields = ['nombre_producto', 'cantidad', 'unidad', 'categoria', 'proveedor', 'limite_stock', 'para_barra', 'para_cocina']
        widgets = {
            'nombre_producto': forms.TextInput(attrs={'class': 'form-control'}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control'}),
            'unidad': forms.Select(attrs={'class': 'form-control'}),  # Select para las unidades
            'categoria': forms.Select(attrs={'class': 'form-control'}),
            'proveedor': forms.Select(attrs={'class': 'form-control'}),
            'limite_stock': forms.NumberInput(attrs={'class': 'form-control'}),
            'para_barra': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'para_cocina': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

# Formulario para agregar categorías
class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nombre_categoria']
        widgets = {
            'nombre_categoria': forms.TextInput(attrs={'class': 'form-control', 'id': 'id_nombre_categoria'}),
        }

# Formulario para agregar proveedores
class ProveedorForm(forms.ModelForm):
    class Meta:
        model = Proveedor
        fields = ['nombre_proveedor']
        widgets = {
            'nombre_proveedor': forms.TextInput(attrs={'class': 'form-control', 'id': 'id_nombre_proveedor'}),
        }

# Formulario para subir notas o facturas de proveedores
class NotaProveedorForm(forms.ModelForm):
    class Meta:
        model = NotaProveedor
        fields = ['proveedor', 'archivo']
        widgets = {
            'proveedor': forms.Select(attrs={'class': 'form-control'}),
            'archivo': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

# Formulario para agregar mensajes especiales al dashboard de cocina
class MensajeCocinaForm(forms.ModelForm):
    class Meta:
        model = MensajeCocina
        fields = ['titulo', 'contenido']
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'contenido': forms.Textarea(attrs={'class': 'form-control'}),
        }