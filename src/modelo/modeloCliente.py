from flask import jsonify, request
from modelo.coneccion import db_connection

def buscar_cliente(codigo):
    try:
        conn = db_connection()
        cur = conn.cursor()
        cur.execute("SELECT ci, nombre, direccion, fecha_nac, ciudad FROM cliente WHERE ci = %s", (codigo,))
        datos = cur.fetchone()
        conn.close()
        if datos is not None:
            cliente = {
                'ci': datos[0],
                'nombre': datos[1],
                'direccion': datos[2],
                'fecha_nac': datos[3],
                'ciudad': datos[4]
            }
            return cliente
        else:
            return None
    except Exception as ex:
        raise ex


class ClienteModel:
    @classmethod
    def listar_cliente(cls):
        try:
            conn = db_connection()
            cur = conn.cursor()
            cur.execute("SELECT ci, nombre, direccion, fecha_nac, ciudad FROM cliente")
            datos = cur.fetchall()
            conn.close()
            clientes = []
            for fila in datos:
                cliente = {
                    'ci': fila[0],
                    'nombre': fila[1],
                    'direccion': fila[2],
                    'fecha_nac': fila[3],
                    'ciudad': fila[4]
                }
                clientes.append(cliente)
            
            return jsonify({'clientes': clientes, 'mensaje': "Clientes listados.", 'exito': True})
        except Exception as ex:
            return jsonify({'mensaje': "Error", 'exito': False})

    @classmethod
    def registrar_cliente(cls):
        try:
            cliente = buscar_cliente(request.json['ci'])
            if cliente is not None:
                return jsonify({'mensaje': "El CI ya existe, no se puede duplicar.", 'exito': False})
            else:
                conn = db_connection()
                cur = conn.cursor()
                cur.execute('INSERT INTO cliente (ci, nombre, direccion, fecha_nac, ciudad) VALUES (%s, %s, %s, %s, %s)',
                            (request.json['ci'], request.json['nombre'], request.json['direccion'],
                             request.json['fecha_nac'], request.json['ciudad']))
                conn.commit()
                conn.close()
                return jsonify({'mensaje': "Cliente registrado.", 'exito': True})
        except Exception as ex:
            return jsonify({'mensaje': "Error", 'exito': False})

    @classmethod
    def modificar_cliente(cls):
        try:
            ci = request.json['ci']
            cliente = buscar_cliente(request.json['ci'])
            if cliente is None:
                return jsonify({'mensaje': "El cliente no existe.", 'exito': False})
            else:
                conn = db_connection()
                cur = conn.cursor()
                cur.execute('UPDATE cliente SET nombre = %s, direccion = %s, fecha_nac = %s, ciudad = %s WHERE ci = %s',
                            (request.json['nombre'], request.json['direccion'], request.json['fecha_nac'],
                             request.json['ciudad'], ci))
                conn.commit()
                conn.close()
                return jsonify({'mensaje': "Cliente modificado.", 'exito': True})
        except Exception as ex:
            return jsonify({'mensaje': "Error", 'exito': False})