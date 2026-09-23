import pandas as pd
import openpyxl
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

excel_file = "registro_asistencia_junio.xlsx"

# 1. Leer las hojas del registro de asistencia
df_t1 = pd.read_excel(excel_file, sheet_name='Junio - Asistencia-turno1')
df_t2 = pd.read_excel(excel_file, sheet_name='Junio - Asistencia-turno2')

# Consolidar ambos turnos
df_asistencia = pd.concat([df_t1, df_t2], ignore_index=True)

# 2. Escala salarial por cargo (Leyes laborales peruanas D.L. 728)
SUELDOS_POR_CARGO = {
    'CAJERA': 1300.00,
    'OPERADOR': 1400.00,
    'SEGURIDAD': 1350.00,
    'AZAFATA': 1150.00,
    'ENCARGADO': 2200.00,
    'LIMPIEZA': 1025.00,
    'TECNICO': 1800.00
}

empleados = df_asistencia[['DNI', 'EMPLEADO', 'CARGO']].drop_duplicates()
boletas_data = []

for _, emp in empleados.iterrows():
    dni = emp['DNI']
    nombre = emp['EMPLEADO']
    cargo = emp['CARGO']
    sueldo_basico = SUELDOS_POR_CARGO.get(str(cargo).upper(), 1025.00)

    sub_df = df_asistencia[df_asistencia['DNI'] == dni]

    cant_faltas = (sub_df['ESTADO'] == 'FALTA').sum()
    cant_tardanzas = (sub_df['TARDANZA / FALTA'] == 'TARDANZA').sum()

    minutos_tardanza = cant_tardanzas * 15

    valor_dia = sueldo_basico / 30.0
    valor_hora = valor_dia / 8.0
    valor_minuto = valor_hora / 60.0

    descuento_faltas = (cant_faltas * valor_dia) + (cant_faltas * (valor_dia / 6.0))
    descuento_tardanzas = minutos_tardanza * valor_minuto

    total_descuento_asistencia = descuento_faltas + descuento_tardanzas
    sueldo_imponible = max(0, sueldo_basico - total_descuento_asistencia)

    descuento_afp = sueldo_imponible * 0.1319
    neto_a_pagar = sueldo_imponible - descuento_afp
    aporte_essalud = sueldo_imponible * 0.09

    boletas_data.append({
        'DNI': dni,
        'EMPLEADO': nombre,
        'CARGO': cargo,
        'SUELDO BÁSICO (S/)': round(sueldo_basico, 2),
        'FALTAS (Días)': cant_faltas,
        'TARDANZAS (Nro)': cant_tardanzas,
        'DESC. FALTAS (S/)': round(descuento_faltas, 2),
        'DESC. TARDANZAS (S/)': round(descuento_tardanzas, 2),
        'SUELDO IMPONIBLE (S/)': round(sueldo_imponible, 2),
        'AFP / ONP (13.19%) (S/)': round(descuento_afp, 2),
        'NETO A PAGAR (S/)': round(neto_a_pagar, 2),
        'ESSALUD EMPLEADOR (9%) (S/)': round(aporte_essalud, 2)
    })

df_boletas = pd.DataFrame(boletas_data)

# 3. Guardar o actualizar la 3ra pestaña 'Boletas_de_Pago'
with pd.ExcelWriter(excel_file, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
    df_boletas.to_excel(writer, sheet_name='Boletas_de_Pago', index=False)

print("Pestaña 'Boletas_de_Pago' generada exitosamente.")

# 4. Configuración del Envío de Correo Electrónico
REMITENTE = "deividguett@gmail.com"
PASSWORD_APP = "gomyxkuyuvsrggkq"
DESTINATARIO = "vanjelsin02@gmail.com"

msg = MIMEMultipart()
msg['From'] = REMITENTE
msg['To'] = DESTINATARIO
msg['Subject'] = "Reporte Procesado - Boletas de Pago del Mes (Recursos Humanos)"

cuerpo = """
Estimado Equipo de Recursos Humanos,

Se ha procesado exitosamente la planilla del mes mediante el Pipeline de Jenkins.
Adjunto a este correo encontrarán el archivo Excel actualizado con la pestaña 'Boletas_de_Pago', la cual incluye el detalle de descuentos por tardanzas, faltas, aportes de AFP y neto a pagar por colaborador.

Saludos cordiales,
Sistema Automatizado de Planillas - Jenkins
"""

msg.attach(MIMEText(cuerpo, 'plain'))

# Adjuntar archivo Excel procesado
with open(excel_file, "rb") as attachment:
    part = MIMEBase("application", "octet-stream")
    part.set_payload(attachment.read())

encoders.encode_base64(part)
part.add_header("Content-Disposition", f"attachment; filename={excel_file}")
msg.attach(part)

# Conexión al Servidor SMTP de Gmail
try:
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(REMITENTE, PASSWORD_APP)
    text = msg.as_string()
    server.sendmail(REMITENTE, DESTINATARIO, text)
    server.quit()
    print(f"Correo enviado exitosamente a {DESTINATARIO}")
except Exception as e:
    print(f"Error al enviar el correo: {e}")