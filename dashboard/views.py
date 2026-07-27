import json
import pandas as pd
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Cliente

def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
        
    if request.method == 'POST':
        username_input = request.POST.get('username')
        password_input = request.POST.get('password')
        
        user = authenticate(request, username=username_input, password=password_input)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, "ACCESO DENEGADO: Credenciales de Morales Analítica no válidas.")
            
    return render(request, 'dashboard/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def dashboard_view(request):
    clientes = Cliente.objects.all()
    total_clientes = clientes.count()
    
    avg_o = avg_c = avg_e = avg_a = avg_n = 0
    if total_clientes > 0:
        avg_o = sum(c.ocean_o for c in clientes) // total_clientes
        avg_c = sum(c.ocean_c for c in clientes) // total_clientes
        avg_e = sum(c.ocean_e for c in clientes) // total_clientes
        avg_a = sum(c.ocean_a for c in clientes) // total_clientes
        avg_n = sum(c.ocean_n for c in clientes) // total_clientes

    context = {
        'total_clientes': total_clientes,
        'avg_o': avg_o,
        'avg_c': avg_c,
        'avg_e': avg_e,
        'avg_a': avg_a,
        'avg_n': avg_n,
    }
    return render(request, 'dashboard/dashboard.html', context)

@login_required
def api_clientes(request):
    """Devuelve la lista completa de clientes para renderizar en el mapa y la tabla."""
    clientes = Cliente.objects.all()
    data = []
    for c in clientes:
        data.append({
            'id': c.id,
            'nombre': c.nombre,
            'empresa': c.empresa or '',
            'telefono': c.telefono or '',
            'direccion': c.direccion or '',
            'latitud': c.latitud,
            'longitud': c.longitud,
            'ocean_o': c.ocean_o,
            'ocean_c': c.ocean_c,
            'ocean_e': c.ocean_e,
            'ocean_a': c.ocean_a,
            'ocean_n': c.ocean_n,
            'comportamiento_compra': c.comportamiento_compra,
            'estilo_decision': c.estilo_decision,
            'disparadores_compra': c.disparadores_compra or '',
            'intereses': c.intereses or '',
        })
    return JsonResponse({'status': 'success', 'data': data})

@login_required
def crear_cliente(request):
    """Guarda un nuevo cliente o actualiza un cliente existente."""
    if request.method == 'POST':
        try:
            if request.content_type == 'application/json':
                data_source = json.loads(request.body)
            else:
                data_source = request.POST
                
            cliente_id = data_source.get('id')
            nombre = data_source.get('nombre')
            
            if not nombre or str(nombre).strip() == '':
                return JsonResponse({'status': 'error', 'message': 'El campo Nombre es obligatorio.'}, status=400)
                
            # Procesar coordenadas de forma segura
            def parse_float(val, default=0.0):
                try:
                    return float(val) if val not in [None, ''] else default
                except (ValueError, TypeError):
                    return default

            # Procesar valores OCEAN de forma segura
            def parse_int(val, default=50):
                try:
                    return int(float(val)) if val not in [None, ''] else default
                except (ValueError, TypeError):
                    return default

            latitud = parse_float(data_source.get('latitud'))
            longitud = parse_float(data_source.get('longitud'))
            
            # Crear o buscar cliente
            if cliente_id:
                cliente = Cliente.objects.get(id=cliente_id)
                cliente.nombre = str(nombre).strip()
            else:
                cliente = Cliente(nombre=str(nombre).strip())

            cliente.empresa = str(data_source.get('empresa', '')).strip()
            cliente.telefono = str(data_source.get('telefono', '')).strip()
            cliente.direccion = str(data_source.get('direccion', '')).strip()
            cliente.latitud = latitud
            cliente.longitud = longitud
            cliente.ocean_o = parse_int(data_source.get('ocean_o'))
            cliente.ocean_c = parse_int(data_source.get('ocean_c'))
            cliente.ocean_e = parse_int(data_source.get('ocean_e'))
            cliente.ocean_a = parse_int(data_source.get('ocean_a'))
            cliente.ocean_n = parse_int(data_source.get('ocean_n'))
            cliente.intereses = str(data_source.get('intereses', '')).strip()

            cliente.save()
            
            return JsonResponse({
                'status': 'success', 
                'message': 'Cliente guardado exitosamente.',
                'cliente': {
                    'id': cliente.id,
                    'nombre': cliente.nombre,
                    'comportamiento': cliente.comportamiento_compra,
                    'decision': cliente.estilo_decision
                }
            })
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': f'Error al procesar los datos: {str(e)}'}, status=400)
            
    return JsonResponse({'status': 'error', 'message': 'Método no permitido.'}, status=405)

# Alias para evitar problemas de compatibilidad en plantillas
registrar_cliente = crear_cliente

@login_required
def exportar_excel(request):
    try:
        clientes = Cliente.objects.all()
        data = []
        for c in clientes:
            data.append({
                'ID': c.id,
                'Nombre': c.nombre,
                'Empresa': c.empresa or '',
                'Teléfono': c.telefono or '',
                'Dirección': c.direccion or '',
                'Latitud': c.latitud,
                'Longitud': c.longitud,
                'Apertura (O)': c.ocean_o,
                'Responsabilidad (C)': c.ocean_c,
                'Extraversión (E)': c.ocean_e,
                'Amabilidad (A)': c.ocean_a,
                'Neuroticismo (N)': c.ocean_n,
                'Comportamiento Compra': c.comportamiento_compra,
                'Estilo Decisión': c.estilo_decision,
                'Disparadores Venta': c.disparadores_compra or '',
                'Intereses': c.intereses or '',
                'Fecha Registro': c.created_at.strftime('%Y-%m-%d %H:%M:%S') if c.created_at else ''
            })
            
        df = pd.DataFrame(data)
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename="morales_analitica_clientes.xlsx"'
        
        with pd.ExcelWriter(response, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Clientes')
            
        return response
    except Exception as e:
        messages.error(request, f"Error al exportar la base de datos: {str(e)}")
        return redirect('dashboard')

@login_required
def importar_excel(request):
    if request.method == 'POST':
        file = request.FILES.get('excel_file')
        if not file:
            messages.error(request, "No se seleccionó ningún archivo.")
            return redirect('dashboard')
            
        try:
            if file.name.endswith('.xlsx') or file.name.endswith('.xls'):
                df = pd.read_excel(file)
            elif file.name.endswith('.csv'):
                df = pd.read_csv(file)
            else:
                messages.error(request, "Formato invalido. Formatos soportados: .xlsx o .csv")
                return redirect('dashboard')
                
            df.columns = [col.strip().lower() for col in df.columns]
            
            col_mappings = {
                'nombre': ['nombre', 'name', 'nombre completo', 'fullname'],
                'empresa': ['empresa', 'company', 'rubro', 'organization'],
                'telefono': ['telefono', 'teléfono', 'phone', 'telephone', 'celular'],
                'direccion': ['direccion', 'dirección', 'address'],
                'latitud': ['latitud', 'lat', 'latitude'],
                'longitud': ['longitud', 'long', 'lng', 'lon', 'longitude'],
                'ocean_o': ['apertura (o)', 'apertura', 'openness', 'ocean_o', 'o'],
                'ocean_c': ['responsabilidad (c)', 'responsabilidad', 'conscientiousness', 'ocean_c', 'c'],
                'ocean_e': ['extraversión (e)', 'extraversión', 'extraversion', 'ocean_e', 'e'],
                'ocean_a': ['amabilidad (a)', 'amabilidad', 'agreeableness', 'ocean_a', 'a'],
                'ocean_n': ['neuroticismo (n)', 'neuroticismo', 'neuroticism', 'ocean_n', 'n'],
                'intereses': ['intereses', 'interests', 'intereses clave'],
                'comportamiento_compra': ['comportamiento compra', 'comportamiento_compra', 'behavior'],
                'estilo_decision': ['estilo decisión', 'estilo_decision', 'decision_style'],
                'disparadores_compra': ['disparadores venta', 'disparadores_compra', 'triggers']
            }
            
            created_count = 0
            for index, row in df.iterrows():
                def get_val(field_name, default=None):
                    for option in col_mappings[field_name]:
                        if option in df.columns:
                            val = row[option]
                            if pd.isna(val):
                                return default
                            return val
                    return default
                
                nombre = get_val('nombre')
                if not nombre:
                    continue
                    
                lat_val = get_val('latitud')
                lng_val = get_val('longitud')
                try:
                    latitud = float(lat_val) if lat_val is not None else 0.0
                    longitud = float(lng_val) if lng_val is not None else 0.0
                except ValueError:
                    latitud = 0.0
                    longitud = 0.0
                    
                def get_ocean_score(field):
                    val = get_val(field, 50)
                    try:
                        return int(float(val))
                    except ValueError:
                        return 50
                
                cliente = Cliente(
                    nombre=str(nombre),
                    empresa=str(get_val('empresa', '')) if get_val('empresa') else '',
                    telefono=str(get_val('telefono', '')) if get_val('telefono') else '',
                    direccion=str(get_val('direccion', '')) if get_val('direccion') else '',
                    latitud=latitud,
                    longitud=longitud,
                    ocean_o=get_ocean_score('ocean_o'),
                    ocean_c=get_ocean_score('ocean_c'),
                    ocean_e=get_ocean_score('ocean_e'),
                    ocean_a=get_ocean_score('ocean_a'),
                    ocean_n=get_ocean_score('ocean_n'),
                    intereses=str(get_val('intereses', '')) if get_val('intereses') else ''
                )
                cliente.save()
                created_count += 1
                
            messages.success(request, f"Carga masiva exitosa: {created_count} clientes procesados.")
        except Exception as e:
            messages.error(request, f"Error al leer el archivo: {str(e)}")
            
    return redirect('dashboard')

@login_required
def eliminar_clientes(request):
    """Procesa la eliminación individual o múltiple de prospectos."""
    if request.method == 'POST':
        try:
            if request.content_type == 'application/json':
                body = json.loads(request.body)
                ids = body.get('ids', [])
            else:
                ids_str = request.POST.get('ids', '')
                ids = [int(i) for i in ids_str.split(',') if i.strip()]
                
            if not ids:
                return JsonResponse({'status': 'error', 'message': 'Seleccione al menos un registro para eliminar.'}, status=400)
                
            deleted_count, _ = Cliente.objects.filter(id__in=ids).delete()
            return JsonResponse({
                'status': 'success', 
                'message': f'Se eliminaron {deleted_count} cliente(s) exitosamente.',
                'deleted_count': deleted_count
            })
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
            
    return JsonResponse({'status': 'error', 'message': 'Método no permitido.'}, status=405)
