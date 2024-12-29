from django.db import models, transaction
from django.db.models import Q


class Editorial(models.Model):
    nombre_editorial = models.CharField(max_length=100, unique=True)
    direccion = models.CharField(max_length=200)
    telefono = models.CharField(max_length=20)
    
    class Meta:
        db_table = 'editoriales'
        verbose_name_plural = 'editoriales'
    
    def __str__(self):
        return self.nombre_editorial

    @classmethod
    def find_duplicates(cls):
        return cls.objects.values('nombre_editorial').annotate(count=models.Count('id')).filter(count__gt=1)

    @classmethod
    @transaction.atomic
    def merge_duplicates(cls, primary_id, duplicate_ids):
        primary = cls.objects.get(id=primary_id)
        duplicates = cls.objects.filter(id__in=duplicate_ids)
        
        # Excluir la editorial principal de la lista de duplicados
        duplicates = duplicates.exclude(id=primary_id)
        
        for duplicate in duplicates:
            # Obtener todos los productos asociados a la editorial duplicada
            productos = Producto.objects.filter(editorial=duplicate)
            
            # Actualizar cada producto para que use la editorial principal
            for producto in productos:
                producto.editorial = primary
                producto.save()
            
            # Eliminar la editorial duplicada
            duplicate.delete()
        
        return primary

class Autor(models.Model):
    nombre_autor = models.CharField(max_length=100)
    nacionalidad = models.CharField(max_length=50)
    
    class Meta:
        db_table = 'autores'
        verbose_name_plural = 'autores'
    
    def __str__(self):
        return self.nombre_autor

    @classmethod
    def find_duplicates(cls):
        return cls.objects.values('nombre_autor').annotate(count=models.Count('id')).filter(count__gt=1)

    @classmethod
    @transaction.atomic
    def merge_duplicates(cls, primary_id, duplicate_ids):
        primary = cls.objects.get(id=primary_id)
        duplicates = cls.objects.filter(id__in=duplicate_ids)
        
        # Excluir el autor principal de la lista de duplicados
        duplicates = duplicates.exclude(id=primary_id)
        
        for duplicate in duplicates:
            # Obtener todos los productos asociados al autor duplicado
            productos = duplicate.productos.all()
            
            # Agregar cada producto al autor principal
            for producto in productos:
                producto.autores.add(primary)
                producto.autores.remove(duplicate)
            
            # Eliminar el autor duplicado
            duplicate.delete()
        
        return primary

class Producto(models.Model):
    TIPOS = (
        ('libro', 'Libro'),
        ('revista', 'Revista'),
        ('periodico', 'Periódico'),
        ('otro', 'Otro'),
    )
    
    nombre = models.CharField(max_length=200)
    tipo = models.CharField(max_length=20, choices=TIPOS)
    editorial = models.ForeignKey(Editorial, on_delete=models.PROTECT)
    autores = models.ManyToManyField(Autor, related_name='productos')
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    
    class Meta:
        db_table = 'productos'
        ordering = ['nombre']
    
    def __str__(self):
        return self.nombre

