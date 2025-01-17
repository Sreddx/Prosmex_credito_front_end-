from app.models import Accion, Permiso, Rol, Grupo, Ruta, TipoPrestamo, Usuario
from app.services import BonoService
from app import db

def populate_bonos():
    servicio_bono = BonoService()
    bonos = [
        {'monto': 150, 'entrega_min': 5000, 'entrega_max': 5999, 'fallas': 0},
        {'monto': 200, 'entrega_min': 6000, 'entrega_max': 7499, 'fallas': 0},
        {'monto': 250, 'entrega_min': 7500, 'entrega_max': 8499, 'fallas': 1},
        {'monto': 300, 'entrega_min': 8500, 'entrega_max': 9999, 'fallas': 2},
        {'monto': 400, 'entrega_min': 10000, 'entrega_max': 13500, 'fallas': 2}
    ]
    try:
        for bono_data in bonos:
            servicio_bono.create_bono(bono_data)
        return True
    except ValueError as e:
        print(f"Error al crear bonos: {str(e)}")
        return False
    except Exception as e:
        print(f"Error inesperado al crear bonos: {str(e)}")
        return False

def populate_data():
    if Accion.query.first() is not None:
        return "Initial data already exists."

    try:
        # Definir y cargar acciones
        acciones = [
            'Alta de cliente/aval', 'Creación de préstamo', 'Registro de pagos de cobranzas a nivel grupo',
            'Realizar corte con superior', 'Registro pagos de préstamos a nivel grupo', 'Visualizar reportes de rutas',
            'Visualizar reportes generales', 'Editar información', 'Crear usuario', 'Dar de baja usuario',
            'Creación de préstamo mayor a $5000', 'Eliminar crédito', 'Asignar titular a grupo', 'Asignar grupo a ruta'
        ]
        accion_objects = []
        for accion_desc in acciones:
            accion = Accion(descripcion=accion_desc)
            db.session.add(accion)
            accion_objects.append(accion)
        db.session.commit()

        # Definir y cargar roles
        roles = ['Gestor de cobranza', 'Titular', 'Supervisor', 'Gerente', 'Director', 'Admin']
        role_objects = []
        for role_name in roles:
            role = Rol(nombre=role_name)
            db.session.add(role)
            role_objects.append(role)
        db.session.commit()

        # Asignar permisos a roles
        roles_permisos = {
            'Gestor de cobranza': [3, 4],
            'Titular': [1, 2, 3, 4],
            'Supervisor': [1, 2, 3, 4, 5, 6],
            'Gerente': [1, 2, 3, 4, 5, 6],
            'Director': [1, 2, 3, 4, 5, 6, 7],
            'Admin': list(range(1, 15))
        }
        for role_name, permiso_indices in roles_permisos.items():
            role = next((r for r in role_objects if r.nombre == role_name), None)
            if role:
                for index in permiso_indices:
                    accion = accion_objects[index - 1]
                    permiso = Permiso(rol_id=role.rol_id, accion_id=accion.accion_id)
                    db.session.add(permiso)
        db.session.commit()

        # Crear datos dummy para Rutas
        rutas = [
            {'nombre_ruta': 'Ruta 1: zapopan'},
            {'nombre_ruta': 'Ruta 2: Guadalajara'},
            {'nombre_ruta': 'Ruta 3: Tlaquepaque'}
        ]
        ruta_objects = []
        for ruta in rutas:
            new_ruta = Ruta(nombre_ruta=ruta['nombre_ruta'])
            db.session.add(new_ruta)
            ruta_objects.append(new_ruta)
        db.session.commit()

        # Crear un usuario líder de grupo dummy
        leader_user = Usuario(
            nombre="Gestor Cobranza",
            apellido_paterno="Default",
            apellido_materno="One",
            usuario="Cobranza.user@example.com",
            contrasena="cobranza123",
            rol_id=1  
        )
        db.session.add(leader_user)
        db.session.commit()

        # Crear un usuario titular dummy
        titular_user = Usuario(
            nombre="Titular",
            apellido_paterno="Default",
            apellido_materno="One",
            usuario="titular.user@example.com",
            contrasena="titular123",
            rol_id=2  
        )
        db.session.add(titular_user)
        db.session.commit()

        # Crear datos dummy para Grupos
        grupos = [
            {'nombre_grupo': 'Grupo 1 - Nuevo Mexico', 'ruta_id': ruta_objects[0].ruta_id},
            {'nombre_grupo': 'Grupo 2 - Chapultepec', 'ruta_id': ruta_objects[1].ruta_id},
            {'nombre_grupo': 'Grupo 3 - Las Huertas', 'ruta_id': ruta_objects[2].ruta_id}
        ]
        for grupo in grupos:
            new_grupo = Grupo(
                nombre_grupo=grupo['nombre_grupo'],
                ruta_id=grupo['ruta_id'],
                usuario_id_titular=titular_user.id
            )
            db.session.add(new_grupo)
        db.session.commit()

        # Crear datos predeterminados para Tipos de Préstamo
        tipos_prestamo = [
            {'tipo_prestamo_id': 1, 'nombre': 'Préstamo Tipo 14 semanas', 'numero_semanas': 14, 'porcentaje_semanal': 0.1, 'incumplimientos_tolerados': 1, 'pena_incumplimiento': 1.0, 'limite_penalizaciones': 1, 'interes': 0.4},
            {'tipo_prestamo_id': 34, 'nombre': 'Préstamo Tipo 20 semanas', 'numero_semanas': 20, 'porcentaje_semanal': 0.07, 'incumplimientos_tolerados': 1, 'pena_incumplimiento': 1.0, 'limite_penalizaciones': 4, 'interes': 0.4},
            {'tipo_prestamo_id': 35, 'nombre': 'Préstamo Tipo 30 semanas', 'numero_semanas': 30, 'porcentaje_semanal': 0.05, 'incumplimientos_tolerados': 1, 'pena_incumplimiento': 2.0, 'limite_penalizaciones': 4, 'interes': 0.5},
            {'tipo_prestamo_id': 36, 'nombre': 'Préstamo Tipo 11 semanas', 'numero_semanas': 11, 'porcentaje_semanal': 0.1, 'incumplimientos_tolerados': 1, 'pena_incumplimiento': 1.0, 'limite_penalizaciones': 4, 'interes': 0.1},
            {'tipo_prestamo_id': 37, 'nombre': 'Préstamo Tipo 13 semanas', 'numero_semanas': 13, 'porcentaje_semanal': 0.1, 'incumplimientos_tolerados': 1, 'pena_incumplimiento': 1.0, 'limite_penalizaciones': 4, 'interes': 0.3}
        ]
        for tipo in tipos_prestamo:
            new_tipo = TipoPrestamo(
                tipo_prestamo_id=tipo['tipo_prestamo_id'],
                nombre=tipo['nombre'],
                numero_semanas=tipo['numero_semanas'],
                porcentaje_semanal=tipo['porcentaje_semanal'],
                incumplimientos_tolerados=tipo['incumplimientos_tolerados'],
                pena_incumplimiento=tipo['pena_incumplimiento'],
                limite_penalizaciones=tipo['limite_penalizaciones'],
                interes=tipo['interes']
            )
            db.session.add(new_tipo)
        db.session.commit()

        # Llamar a la función populate_bonos para cargar los bonos
        if not populate_bonos():
            print("Error al crear bonos.")
        
        return "Datos iniciales cargados con éxito."

    except Exception as e:
        db.session.rollback()
        print(f"Error al cargar los datos iniciales: {str(e)}")
