import os
import hashlib
from datetime import datetime
from flask import Flask, render_template, jsonify, request, send_from_directory, abort

app = Flask(__name__)
PDF_FOLDER = os.path.join(app.root_path, "static", "pdfs")

# ==============================================================================
# EXPEDIENTE N° 00530-2023-0-2101-JR-CI-03 (DATOS REALES INDEXADOS)
# ==============================================================================
EXPEDIENTE_DATA = {
    "codigo_expediente": "00530-2023-0-2101-JR-CI-03",
    "distrito_judicial": "PUNO",
    "instancia": "JUZGADO ESPECIALIZADO",
    "especialidad": "CIVIL",
    "anio": "2023",
    "numero": "00530",
    "organo_jurisdiccional": "3° JUZGADO CIVIL - SEDE CENTRAL PUNO",
    "organo_segunda_instancia": "1° SALA CIVIL - SEDE CENTRAL PUNO (ORALIDAD - EJE)",
    "juez": "CHEVARRIA TISNADO, GUIDO ARMANDO",
    "especialista_legal": "TAPIA SANCHEZ, MARY ELENIA",
    "colegiado_superior": "MAMANI COAQUIRA, OSWALDO / MONZÓN MAMANI, PÁNFILO / NUÑEZ VILLAR, MILAGROS",
    "materia": "OBLIGACIÓN DE DAR SUMA DE DINERO",
    "proceso": "PROCESO ÚNICO DE EJECUCIÓN",
    "fecha_inicio": "05/10/2023",
    "fecha_conclusion": "24/07/2025",
    "estado_actual": "ARCHIVO DEFINITIVO — CONCLUIDO POR PAGO (ART. 322 INC. 1 CPC)",
    "cuantia_demandada": "S/ 128,961.12",
    "monto_transado": "S/ 66,448.36 (60 cuotas) — Cancelado íntegramente por S/ 45,000.00 (15/07/2025)",
    "titulo_ejecutivo": "Pagaré Incompleto N° 0011-0229-9600419563-20 (Reactiva Perú - Emitido 18/06/2020, Vencido 07/08/2023)",
    "ubicacion_fisica": "ARCHIVO CENTRAL DE EXPEDIENTES - SEDE ANEXA PUNO (JR. CUSCO N° 232)",
    "folios_totales": 335,
    "resumen_ia_general": (
        "Proceso Único de Ejecución iniciado el 05/10/2023 por Banco BBVA Perú S.A. contra Intiqa Hotel E.I.R.L. "
        "y sus fiadores solidarios Francisco Gerardo Aquise Aquise y Juliana Judhy Gonzales Aza, reclamando S/ 128,961.12 "
        "derivados de un pagaré Reactiva Perú. En primera instancia (Res. N° 07), el 3° Juzgado Civil de Puno declaró fundada "
        "la contradicción por llenado contrario a acuerdos; sin embargo, la 1° Sala Civil mediante Auto de Vista N° 249-2024 "
        "(Res. N° 14) revocó dicha decisión y declaró infundada la contradicción, ordenando llevar adelante la ejecución (Res. N° 16). "
        "Posteriormente, las partes suscribieron un acuerdo extrajudicial de pago (Art. 339 CPC) y, tras acreditarse la cancelación "
        "total de S/ 45,000.00 mediante Constancia de No Adeudo del 16/07/2025, el Juzgado emitió la Resolución N° 20 (24/07/2025) "
        "declarando la conclusión definitiva del proceso sin declaración sobre el fondo, el levantamiento de embargos y su archivo definitivo."
    ),
    "partes": [
        {
            "rol": "DEMANDANTE / EJECUTANTE",
            "tipo_persona": "JURÍDICA",
            "nombre": "BANCO BBVA PERÚ S.A.",
            "nombre_anon": "ENTIDAD FINANCIERA EJECUTANTE (RUC 20100130204)",
            "documento": "RUC N° 20100130204",
            "representante": "Elizabeth Patricia Flores Ortiz (Apoderada / Abogada CAP N° 755)",
            "domicilio_procesal": "Jr. Independencia N° 105 - Of. A-204, Puno",
            "casilla_sinoe": "Casilla SINOE N° 107520 / CUD: cud@peru.gob.pe"
        },
        {
            "rol": "DEMANDADO / OBLIGADO PRINCIPAL",
            "tipo_persona": "JURÍDICA",
            "nombre": "INTIQA HOTEL E.I.R.L.",
            "nombre_anon": "PERSONA JURÍDICA EJECUTADA N° 01 (P.E. 11052346)",
            "documento": "Partida Electrónica N° 11052346 - SUNARP Puno",
            "representante": "Francisco Gerardo Aquise Aquise (Titular Gerente)",
            "domicilio_procesal": "Jr. Tarapacá N° 272, Puno / Abog. Germán A. Salinas Machaca (CAP 5980)",
            "casilla_sinoe": "Casilla Electrónica SINOE (Defensa Técnica)"
        },
        {
            "rol": "DEMANDADO / FIADOR SOLIDARIO",
            "tipo_persona": "NATURAL",
            "nombre": "AQUISE AQUISE, FRANCISCO GERARDO",
            "nombre_anon": "F. G. A. A. (PERSONA NATURAL EJECUTADA N° 02)",
            "documento": "DNI N° 01285695",
            "representante": "En nombre propio / Abog. Germán A. Salinas Machaca",
            "domicilio_procesal": "Jr. Tarapacá N° 272, Puno",
            "casilla_sinoe": "Casilla Electrónica SINOE (Defensa Técnica)"
        },
        {
            "rol": "DEMANDADO / FIADORA SOLIDARIA",
            "tipo_persona": "NATURAL",
            "nombre": "GONZALES AZA, JULIANA JUDHY",
            "nombre_anon": "J. J. G. A. (PERSONA NATURAL EJECUTADA N° 03)",
            "documento": "DNI N° 01287042",
            "representante": "En nombre propio",
            "domicilio_procesal": "Jr. Tarapacá N° 272, Puno",
            "casilla_sinoe": "Sin casilla electrónica registrada en Sala"
        }
    ]
}

# ==============================================================================
# LOS 41 ACTUADOS PROCESALES REALES (CON METADATOS ARCHIVÍSTICOS ART. 49.3)
# ==============================================================================
ACTUADOS = [
    {"id": 1, "archivo": "01_demanda.pdf.pdf", "paginas": 20, "fojas": "01 - 20", "fecha": "05/10/2023", "hora": "11:14:22", "instancia": "1° Instancia - 3° Juzgado Civil", "tipo": "ESCRITO / DEMANDA", "titulo": "Escrito N° 01 — Demanda de Obligación de Dar Suma de Dinero", "sumilla": "Interpone demanda en Proceso Único de Ejecución por S/ 128,961.12 derivada de Pagaré Reactiva Perú.", "detalle": "Presentada por Elizabeth Patricia Flores Ortiz en representación del Banco BBVA Perú. Adjunta Testimonio Notarial de poderes, copia de Pagaré N° 0011-0229-9600419563-20 y tasa Págalo.pe Ticket 230006307687.", "estado_firma": "Firmado Digitalmente — Abog. Elizabeth Patricia Flores Ortiz (CAP 755)", "cvd": "CVD-2023-00530-001", "hito": True},
    {"id": 2, "archivo": "02_resolucion_1.pdf.pdf", "paginas": 2, "fojas": "21 - 22", "fecha": "16/10/2023", "hora": "15:30:10", "instancia": "1° Instancia - 3° Juzgado Civil", "tipo": "RESOLUCIÓN JUDICIAL", "titulo": "Resolución N° 01 — Auto de Inadmisibilidad", "sumilla": "Declara inadmisible la demanda y otorga plazo de 3 días para subsanar.", "detalle": "El Juez Guido Armando Chevarría Tisnado requiere adjuntar el título valor (Pagaré) en original y juegos de copias suficientes.", "estado_firma": "Firma Digital SINOE — Juez Chevarría Tisnado / Esp. Cruz Asencio", "cvd": "CVD-2023-00530-002", "hito": False},
    {"id": 3, "archivo": "03_cumple_requerimiento.pdf.pdf", "paginas": 2, "fojas": "23 - 24", "fecha": "20/10/2023", "hora": "10:05:40", "instancia": "1° Instancia - 3° Juzgado Civil", "tipo": "ESCRITO", "titulo": "Escrito N° 02 — Cumple Mandato y Adjunta Título Valor Original", "sumilla": "Subsanación de demanda (Reg. 16812-2023).", "detalle": "Banco BBVA Perú cumple requerimiento de la Resolución N° 01 adjuntando el Pagaré original para custodia en caja fuerte del Juzgado.", "estado_firma": "Firmado Digitalmente — Abog. Elizabeth Patricia Flores Ortiz", "cvd": "CVD-2023-00530-003", "hito": False},
    {"id": 4, "archivo": "04_resolucion_2.pdf.pdf", "paginas": 2, "fojas": "25 - 26", "fecha": "25/10/2023", "hora": "16:12:05", "instancia": "1° Instancia - 3° Juzgado Civil", "tipo": "RESOLUCIÓN JUDICIAL", "titulo": "Resolución N° 02 — Auto Admisorio y Mandato Ejecutivo", "sumilla": "Admite demanda en Proceso Único de Ejecución y ordena pago en 5 días.", "detalle": "Notificada el 26/10/2023. Ordena que los ejecutados paguen S/ 128,961.12 más intereses, costas y costos bajo apercibimiento de ejecución forzada.", "estado_firma": "Firma Digital SINOE — Juez Chevarría Tisnado", "cvd": "CVD-2023-00530-004", "hito": True},
    {"id": 5, "archivo": "05_contradiccion.pdf.pdf", "paginas": 44, "fojas": "27 - 70", "fecha": "09/11/2023", "hora": "14:48:19", "instancia": "1° Instancia - 3° Juzgado Civil", "tipo": "ESCRITO / CONTRADICCIÓN", "titulo": "Escrito N° 01 (Ejecutado) — Excepción y Contradicción al Mandato Ejecutivo", "sumilla": "Deduce Excepción de Falta de Legitimidad para Obrar y Contradicción (Reg. 17978-2023).", "detalle": "Presentado por Francisco Gerardo Aquise Aquise con Abog. Germán A. Salinas Machaca (CAP 5980). Alega llenado contrario a acuerdos (art. 690-D inc. 2 CPC).", "estado_firma": "Firmado Digitalmente — Abog. Germán A. Salinas Machaca (CAP 5980)", "cvd": "CVD-2023-00530-005", "hito": True},
    {"id": 6, "archivo": "06_resolucion_3.pdf.pdf", "paginas": 2, "fojas": "71 - 72", "fecha": "15/11/2023", "hora": "12:20:00", "instancia": "1° Instancia - 3° Juzgado Civil", "tipo": "RESOLUCIÓN JUDICIAL", "titulo": "Resolución N° 03 — Inadmisibilidad de Excepción y Contradicción", "sumilla": "Concede 2 días para adjuntar aranceles judiciales; declara no ha lugar devolución de cédula.", "detalle": "Notificada el 16/11/2023. Advierte omisión de tasas judiciales por excepción procesal y contradicción.", "estado_firma": "Firma Digital SINOE — Juez Chevarría Tisnado / Esp. Huaquisto Miranda", "cvd": "CVD-2023-00530-006", "hito": False},
    {"id": 7, "archivo": "07_subsana_observaciones.pdf.pdf", "paginas": 2, "fojas": "73 - 74", "fecha": "21/11/2023", "hora": "09:33:11", "instancia": "1° Instancia - 3° Juzgado Civil", "tipo": "ESCRITO", "titulo": "Escrito N° 02 (Ejecutado) — Subsana Observaciones de Aranceles", "sumilla": "Adjunta aranceles judiciales por excepción y contradicción.", "detalle": "Francisco Gerardo Aquise Aquise presenta los comprobantes de pago requeridos mediante Resolución N° 03.", "estado_firma": "Firmado Digitalmente — Abog. Germán A. Salinas Machaca (CAP 5980)", "cvd": "CVD-2023-00530-007", "hito": False},
    {"id": 8, "archivo": "08_resolucion_4.pdf.pdf", "paginas": 2, "fojas": "75 - 76", "fecha": "27/11/2023", "hora": "15:45:30", "instancia": "1° Instancia - 3° Juzgado Civil", "tipo": "RESOLUCIÓN JUDICIAL", "titulo": "Resolución N° 04 — Admite a Trámite Excepción y Contradicción", "sumilla": "Corre traslado al ejecutante Banco BBVA Perú por el plazo de 3 días.", "detalle": "Notificada el 28/11/2023. Tiene por subsanadas las observaciones y admite a trámite la excepción y contradicción.", "estado_firma": "Firma Digital SINOE — Juez Chevarría Tisnado", "cvd": "CVD-2023-00530-008", "hito": False},
    {"id": 9, "archivo": "09_absuelve_traslado_de_contradiccion.pdf.pdf", "paginas": 5, "fojas": "77 - 81", "fecha": "05/12/2023", "hora": "16:02:44", "instancia": "1° Instancia - 3° Juzgado Civil", "tipo": "ESCRITO", "titulo": "Escrito N° 03 — Absuelve Traslado de Excepción y Contradicción", "sumilla": "Solicita se declaren infundadas la excepción y la contradicción (Reg. 20528-2023).", "detalle": "Banco BBVA Perú invoca la Cláusula Décimo Primera del Contrato de Crédito Comercial y el VI Pleno Casatorio Civil.", "estado_firma": "Firmado Digitalmente — Abog. Elizabeth Patricia Flores Ortiz", "cvd": "CVD-2023-00530-009", "hito": False},
    {"id": 10, "archivo": "10_resolucion_5.pdf.pdf", "paginas": 1, "fojas": "82", "fecha": "11/12/2023", "hora": "11:50:12", "instancia": "1° Instancia - 3° Juzgado Civil", "tipo": "RESOLUCIÓN JUDICIAL", "titulo": "Resolución N° 05 — Requerimiento de Aranceles de Notificación", "sumilla": "Requiere al ejecutante adjuntar aranceles en el plazo de 2 días.", "detalle": "Notificada el 12/12/2023. Previene al Banco BBVA Perú bajo apercibimiento de tenerse por no presentado su escrito.", "estado_firma": "Firma Digital SINOE — Juez Chevarría Tisnado", "cvd": "CVD-2023-00530-010", "hito": False},
    {"id": 11, "archivo": "11_cumple_requerimiento.pdf.pdf", "paginas": 1, "fojas": "83", "fecha": "15/12/2023", "hora": "10:18:05", "instancia": "1° Instancia - 3° Juzgado Civil", "tipo": "ESCRITO", "titulo": "Escrito N° 04 — Cumple Requerimiento de Aranceles", "sumilla": "Adjunta 4 aranceles por derecho de notificación (Reg. 21157-2023).", "detalle": "Banco BBVA Perú cumple con el mandato de la Resolución N° 05 dentro del plazo concedido.", "estado_firma": "Firmado Digitalmente — Abog. Elizabeth Patricia Flores Ortiz", "cvd": "CVD-2023-00530-011", "hito": False},
    {"id": 12, "archivo": "12_resolucion_6.pdf.pdf", "paginas": 2, "fojas": "84 - 85", "fecha": "20/12/2023", "hora": "14:22:09", "instancia": "1° Instancia - 3° Juzgado Civil", "tipo": "RESOLUCIÓN JUDICIAL", "titulo": "Resolución N° 06 — Tiene por Absuelto Traslado", "sumilla": "Da por absuelta la excepción de falta de legitimidad y la contradicción.", "detalle": "Notificada el 21/12/2023. Califica positivamente la absolución formulada por el Banco BBVA Perú conforme al art. 690-D del CPC.", "estado_firma": "Firma Digital SINOE — Juez Chevarría Tisnado / Esp. Huaquisto Miranda", "cvd": "CVD-2023-00530-012", "hito": False},
    {"id": 13, "archivo": "13_resolucion_7.pdf.pdf", "paginas": 6, "fojas": "86 - 91", "fecha": "28/12/2023", "hora": "17:05:40", "instancia": "1° Instancia - 3° Juzgado Civil", "tipo": "AUTO FINAL (1° INSTANCIA)", "titulo": "Resolución N° 07 — Auto Final (Funda Contradicción / Improcedente Demanda)", "sumilla": "Declara infundada excepción, fundada contradicción e improcedente la demanda sin costas ni costos.", "detalle": "Notificada el 29/12/2023. El Juzgado estima llenado contrario a las Cláusulas 8° y 11° del contrato respecto a la fecha de vencimiento.", "estado_firma": "Firma Digital SINOE — Juez Chevarría Tisnado", "cvd": "CVD-2023-00530-013", "hito": True},
    {"id": 14, "archivo": "14_apelacion.pdf.pdf", "paginas": 4, "fojas": "92 - 95", "fecha": "09/01/2024", "hora": "15:11:28", "instancia": "1° Instancia - 3° Juzgado Civil", "tipo": "RECURSO IMPUGNATORIO", "titulo": "Escrito N° 05 — Recurso de Apelación contra Auto Final", "sumilla": "Solicita revocatoria de Resolución N° 07 y que se ordene llevar adelante la ejecución (Reg. 438-2024).", "detalle": "Banco BBVA Perú sustenta que el vencimiento anticipado (Cláusula 7°) y llenado del pagaré (Cláusula 11°) son autónomos.", "estado_firma": "Firmado Digitalmente — Abog. Elizabeth Patricia Flores Ortiz", "cvd": "CVD-2024-00530-014", "hito": True},
    {"id": 15, "archivo": "15_resolucion_8.pdf.pdf", "paginas": 2, "fojas": "96 - 97", "fecha": "16/01/2024", "hora": "12:40:15", "instancia": "1° Instancia - 3° Juzgado Civil", "tipo": "RESOLUCIÓN JUDICIAL", "titulo": "Resolución N° 08 — Concesorio de Apelación con Efecto Suspensivo", "sumilla": "Concede apelación contra Resolución N° 07 y ordena elevar autos al superior jerárquico.", "detalle": "Al amparo de los arts. 691° y 371° del CPC, concede el recurso con efecto suspensivo contra los extremos II y III de la Resolución N° 07.", "estado_firma": "Firma Digital SINOE — Juez Chevarría Tisnado", "cvd": "CVD-2024-00530-015", "hito": False},
    {"id": 16, "archivo": "16_se_eleva_actuado.pdf.pdf", "paginas": 3, "fojas": "98 - 100", "fecha": "08/03/2024", "hora": "11:09:50", "instancia": "1° Instancia - 3° Juzgado Civil", "tipo": "ESCRITO", "titulo": "Escrito N° 07 — Solicita Elevación de Actuados al Superior", "sumilla": "Impulsa remisión del expediente a la Sala Civil (Reg. 2975-2024).", "detalle": "Banco BBVA Perú solicita cumplimiento efectivo del concesorio conforme al art. 376° del CPC.", "estado_firma": "Firmado Digitalmente — Abog. Elizabeth Patricia Flores Ortiz", "cvd": "CVD-2024-00530-016", "hito": False},
    {"id": 17, "archivo": "17_resolucion_9.pdf.pdf", "paginas": 1, "fojas": "101", "fecha": "19/03/2024", "hora": "16:00:02", "instancia": "1° Instancia - 3° Juzgado Civil", "tipo": "RESOLUCIÓN JUDICIAL", "titulo": "Resolución N° 09 — Ordena Elevación Inmediata", "sumilla": "Dispone elevar el expediente sin más trámite a la Sala Civil.", "detalle": "Provee el escrito con cargo N° 2975-2024 ordenando la remisión inmediata del expediente principal.", "estado_firma": "Firma Digital SINOE — Juez Chevarría Tisnado / Esp. Gómez Maydana", "cvd": "CVD-2024-00530-017", "hito": False},
    {"id": 18, "archivo": "18_oficio_de_elevacion.pdf.pdf", "paginas": 2, "fojas": "102 - 103", "fecha": "25/03/2024", "hora": "09:45:00", "instancia": "1° Instancia -> 2° Instancia", "tipo": "OFICIO / TRÁMITE EJE", "titulo": "Oficio de Elevación a la 1° Sala Civil de Puno", "sumilla": "Remite expediente principal en apelación con efecto suspensivo (143 fojas).", "detalle": "El 3° Juzgado Civil remite electrónicamente los autos a la 1° Sala Civil - Sede Central Puno.", "estado_firma": "Firma Digital — 3° Juzgado Civil Sede Central Puno", "cvd": "CVD-2024-00530-018", "hito": False},
    {"id": 19, "archivo": "19_resolucion_10.pdf.pdf", "paginas": 1, "fojas": "104", "fecha": "03/06/2024", "hora": "14:15:33", "instancia": "2° Instancia - 1° Sala Civil", "tipo": "RESOLUCIÓN DE SALA", "titulo": "Resolución N° 010 — Avocamiento y Lineamientos de Oralidad Civil", "sumilla": "Pone el expediente EJE a conocimiento del Colegiado Superior.", "detalle": "Notificada el 04/06/2024 por el Secretario de Sala Jhon Alfonse Chaina Vilca.", "estado_firma": "Firma Digital SINOE — 1° Sala Civil Puno", "cvd": "CVD-2024-00530-019", "hito": False},
    {"id": 20, "archivo": "20_constancia.pdf.pdf", "paginas": 1, "fojas": "105", "fecha": "10/06/2024", "hora": "10:30:18", "instancia": "2° Instancia - 1° Sala Civil", "tipo": "CONSTANCIA JUDICIAL", "titulo": "Constancia de Notificación en Segunda Instancia", "sumilla": "Deja constancia de falta de domicilio procesal y casilla electrónica de codemandados.", "detalle": "Suscrita por la Asistente Judicial Jaqueline Edith Inofuente Peñaloza.", "estado_firma": "Firma Digital SINOE — Asistente Judicial Inofuente Peñaloza", "cvd": "CVD-2024-00530-020", "hito": False},
    {"id": 21, "archivo": "21_resolucion_11.pdf.pdf", "paginas": 3, "fojas": "106 - 108", "fecha": "08/07/2024", "hora": "15:20:45", "instancia": "2° Instancia - 1° Sala Civil", "tipo": "RESOLUCIÓN DE SALA", "titulo": "Resolución N° 011-2024 — Fija Cuestiones Controvertidas y Vista de Causa", "sumilla": "Señala audiencia pública virtual (Google Meet) para el 16/07/2024 a las 10:35 a.m.", "detalle": "Notificada el 09/07/2024. El Colegiado delimita los tres puntos controvertidos sobre la causal del art. 690-D inc. 2 CPC.", "estado_firma": "Firma Digital SINOE — Vocales Mamani, Monzón y Núñez", "cvd": "CVD-2024-00530-021", "hito": True},
    {"id": 22, "archivo": "22_constancia_2.pdf.pdf", "paginas": 1, "fojas": "109", "fecha": "10/06/2024", "hora": "10:32:00", "instancia": "2° Instancia - 1° Sala Civil", "tipo": "CONSTANCIA JUDICIAL", "titulo": "Constancia de Notificación (Duplicado EJE)", "sumilla": "Registro digital de constancia de notificación en cuaderno de Sala.", "detalle": "Constancia incorporada al expediente judicial electrónico sobre domicilios procesales.", "estado_firma": "Firma Digital SINOE — Asistente Judicial Inofuente Peñaloza", "cvd": "CVD-2024-00530-022", "hito": False},
    {"id": 23, "archivo": "23_solicita_uso_de_palabra.pdf.pdf", "paginas": 2, "fojas": "110 - 111", "fecha": "10/07/2024", "hora": "14:55:10", "instancia": "2° Instancia - 1° Sala Civil", "tipo": "ESCRITO", "titulo": "Escrito N° 08 (Ejecutante) — Solicita Uso de la Palabra", "sumilla": "Pide informe oral para Vista de Causa del 16/07/2024 (Reg. 4865-2024).", "detalle": "Banco BBVA Perú solicita intervención oral de su abogada patrocinante.", "estado_firma": "Firmado Digitalmente — Abog. Elizabeth Patricia Flores Ortiz", "cvd": "CVD-2024-00530-023", "hito": False},
    {"id": 24, "archivo": "24_solicito_uso_de_la_palabra2.pdf.pdf", "paginas": 2, "fojas": "112 - 113", "fecha": "12/07/2024", "hora": "11:40:22", "instancia": "2° Instancia - 1° Sala Civil", "tipo": "ESCRITO", "titulo": "Escrito N° 04 (Ejecutado) — Solicita Uso de la Palabra", "sumilla": "Pide informe oral conforme al art. 375 del CPC (Reg. 4984-2024).", "detalle": "Francisco Gerardo Aquise Aquise solicita uso de la palabra para su defensa técnica Abog. Germán A. Salinas Machaca.", "estado_firma": "Firmado Digitalmente — Abog. Germán A. Salinas Machaca", "cvd": "CVD-2024-00530-024", "hito": False},
    {"id": 25, "archivo": "25_resolucion_12.pdf.pdf", "paginas": 2, "fojas": "114 - 115", "fecha": "15/07/2024", "hora": "16:30:00", "instancia": "2° Instancia - 1° Sala Civil", "tipo": "RESOLUCIÓN DE SALA", "titulo": "Resolución N° 012 — Concede Uso de la Palabra por 5 Minutos", "sumilla": "Autoriza informe oral a ambas partes y requiere aranceles al demandado en 2 días.", "detalle": "Suscrita por el Secretario de Sala Ronald Gómez Gutiérrez con visto bueno de Presidencia.", "estado_firma": "Firma Digital SINOE — Secretario de Sala Ronald Gómez Gutiérrez", "cvd": "CVD-2024-00530-025", "hito": False},
    {"id": 26, "archivo": "26_resolucion_13.pdf.pdf", "paginas": 1, "fojas": "116", "fecha": "16/07/2024", "hora": "12:15:40", "instancia": "2° Instancia - 1° Sala Civil", "tipo": "RESOLUCIÓN DE SALA", "titulo": "Resolución N° 013 — Tiene por Cumplido Mandato de Aranceles", "sumilla": "Agrega aranceles presentados por el demandado (Reg. 5021-2024).", "detalle": "Notificada el 18/07/2024. Da por subsanado el requerimiento de la Resolución N° 012.", "estado_firma": "Firma Digital SINOE — Secretario de Sala Ronald Gómez Gutiérrez", "cvd": "CVD-2024-00530-026", "hito": False},
    {"id": 27, "archivo": "27_resolucion_14.pdf.pdf", "paginas": 12, "fojas": "117 - 128", "fecha": "25/07/2024", "hora": "17:45:19", "instancia": "2° Instancia - 1° Sala Civil", "tipo": "AUTO DE VISTA (2° INSTANCIA)", "titulo": "Resolución N° 014-2024 / Auto de Vista N° 249-2024 — Revoca y Reforma", "sumilla": "Revoca Resolución N° 07 y reformándola declara INFUNDADA la contradicción.", "detalle": "Notificada el 31/07/2024. La 1° Sala Civil determina que el llenado del pagaré al amparo de las Cláusulas 7° y 11° es válido y autónomo.", "estado_firma": "Firma Digital SINOE — Vocales Mamani, Monzón y Núñez", "cvd": "CVD-2024-00530-027", "hito": True},
    {"id": 28, "archivo": "28_constancia_no_domicilio.pdf.pdf", "paginas": 1, "fojas": "129", "fecha": "31/10/2024", "hora": "11:10:05", "instancia": "2° Instancia -> 1° Instancia", "tipo": "OFICIO DE DEVOLUCIÓN", "titulo": "Oficio de Devolución de Expediente de Sala Civil a Juzgado", "sumilla": "Devuelve expediente en 185 páginas en mérito al Auto de Vista N° 249-2024.", "detalle": "Notificado el 04/11/2024 por la Secretaria de Sala Jessie Anabell Pari Neyra.", "estado_firma": "Firma Digital SINOE — Secretaria de Sala Pari Neyra", "cvd": "CVD-2024-00530-028", "hito": False},
    {"id": 29, "archivo": "29_oficio_devuelve_el_juzgado.pdf.pdf", "paginas": 1, "fojas": "130", "fecha": "31/10/2024", "hora": "11:12:30", "instancia": "2° Instancia -> 1° Instancia", "tipo": "OFICIO DE DEVOLUCIÓN", "titulo": "Constancia Electrónica de Devolución al 3° Juzgado Civil", "sumilla": "Registro EJE de devolución de actuados tras quedar firme el Auto de Vista.", "detalle": "Remisión electrónica oficial desde la Secretaría de la Sala Civil de Puno.", "estado_firma": "Firma Digital SINOE — Secretaria de Sala Pari Neyra", "cvd": "CVD-2024-00530-029", "hito": False},
    {"id": 30, "archivo": "30_oficio_de_recepcion.pdf.pdf", "paginas": 1, "fojas": "131", "fecha": "04/11/2024", "hora": "09:20:00", "instancia": "1° Instancia - 3° Juzgado Civil", "tipo": "OFICIO N° 925 / RECEPCIÓN", "titulo": "Oficio N° 925 — Recepción de Expediente Devuelto (186 Fojas)", "sumilla": "Ingreso formal del expediente devuelto al 3° Juzgado Civil - Sede Central Puno.", "detalle": "Registra el retorno de los actuados con 186 fojas para prosecución de ejecución.", "estado_firma": "Firma Digital — Mesa de Partes 3° Juzgado Civil", "cvd": "CVD-2024-00530-030", "hito": False},
    {"id": 31, "archivo": "31_resolucion_15.pdf.pdf", "paginas": 1, "fojas": "132", "fecha": "19/12/2024", "hora": "15:05:14", "instancia": "1° Instancia - 3° Juzgado Civil", "tipo": "RESOLUCIÓN JUDICIAL", "titulo": "Resolución N° 15 — Bajada de Autos y Paso a Despacho", "sumilla": "Pone a conocimiento la bajada de autos y ordena autos a despacho para resolver.", "detalle": "Notificada el 27/12/2024 (Esp. Legal Mary Elenia Tapia Sánchez).", "estado_firma": "Firma Digital SINOE — Juez Chevarría Tisnado", "cvd": "CVD-2024-00530-031", "hito": False},
    {"id": 32, "archivo": "32_resolucion_16.pdf.pdf", "paginas": 2, "fojas": "133 - 134", "fecha": "20/12/2024", "hora": "16:40:22", "instancia": "1° Instancia - 3° Juzgado Civil", "tipo": "AUTO FINAL DE EJECUCIÓN", "titulo": "Resolución N° 16 — Ordena Llevar Adelante la Ejecución Forzada", "sumilla": "Ordena ejecución forzada hasta el pago de S/ 128,961.12 más intereses, costas y costos.", "detalle": "Notificada el 27/12/2024. Al amparo del art. 690-E del CPC, ordena la ejecución forzada contra los ejecutados.", "estado_firma": "Firma Digital SINOE — Juez Chevarría Tisnado", "cvd": "CVD-2024-00530-032", "hito": True},
    {"id": 33, "archivo": "33_homologacion.pdf.pdf", "paginas": 1, "fojas": "135", "fecha": "30/12/2024", "hora": "11:30:10", "instancia": "1° Instancia - 3° Juzgado Civil", "tipo": "ESCRITO", "titulo": "Escrito N° 09 — Solicita Homologación de Transacción Extrajudicial", "sumilla": "Pone en conocimiento Acuerdo de Pago y Reconocimiento de Deuda del 27/11/2024.", "detalle": "Banco BBVA Perú solicita aprobación y homologación conforme al art. 337° del CPC.", "estado_firma": "Firmado Digitalmente — Abog. Elizabeth Patricia Flores Ortiz", "cvd": "CVD-2024-00530-033", "hito": False},
    {"id": 34, "archivo": "34_reitero_homologacion.pdf.pdf", "paginas": 1, "fojas": "136", "fecha": "07/01/2025", "hora": "14:12:08", "instancia": "1° Instancia - 3° Juzgado Civil", "tipo": "ESCRITO", "titulo": "Escrito N° 10 — Reitera Homologación y Adjunta Tasas", "sumilla": "Reitera proveído de transacción extrajudicial (Reg. 319-2025).", "detalle": "Banco BBVA Perú adjunta arancel judicial por formas especiales de conclusión del proceso.", "estado_firma": "Firmado Digitalmente — Abog. Elizabeth Patricia Flores Ortiz", "cvd": "CVD-2025-00530-034", "hito": False},
    {"id": 35, "archivo": "35_resolucion_17.pdf.pdf", "paginas": 1, "fojas": "137", "fecha": "09/01/2025", "hora": "15:50:33", "instancia": "1° Instancia - 3° Juzgado Civil", "tipo": "RESOLUCIÓN JUDICIAL", "titulo": "Resolución N° 17 — Provee Escrito Reg. 319-2025", "sumilla": "Dispone estese a lo resuelto y requiere vigencias de poder inscritas en SUNARP.", "detalle": "Notificada el 10/01/2025. Requiere acreditar facultades especiales para transigir vigentes en SUNARP.", "estado_firma": "Firma Digital SINOE — Juez Chevarría Tisnado / Esp. Tapia Sánchez", "cvd": "CVD-2025-00530-035", "hito": False},
    {"id": 36, "archivo": "36_resolucion_18.pdf.pdf", "paginas": 1, "fojas": "138", "fecha": "09/01/2025", "hora": "15:52:10", "instancia": "1° Instancia - 3° Juzgado Civil", "tipo": "RESOLUCIÓN JUDICIAL", "titulo": "Resolución N° 18 — Decreto de Trámite", "sumilla": "Dispone estese a lo dispuesto en la resolución que antecede.", "detalle": "Notificada el 10/01/2025. Ordena estar a la espera de la subsanación de vigencias de poder.", "estado_firma": "Firma Digital SINOE — Juez Chevarría Tisnado", "cvd": "CVD-2025-00530-036", "hito": False},
    {"id": 37, "archivo": "37_cumple_requerimiento.pdf.pdf", "paginas": 30, "fojas": "139 - 168", "fecha": "13/01/2025", "hora": "10:45:19", "instancia": "1° Instancia - 3° Juzgado Civil", "tipo": "ESCRITO / ANEXOS SUNARP", "titulo": "Escrito N° 11 — Cumple Requerimiento con Vigencias de Poder SUNARP", "sumilla": "Adjunta Certificados de Vigencia de Poder de Intiqa Hotel E.I.R.L. y Banco BBVA Perú (Reg. 872-2025).", "detalle": "Presenta Vigencia de Poder Partida N° 11052346 y Partida N° 11014915 más aranceles de notificación.", "estado_firma": "Firmado Digitalmente — Abog. Elizabeth Patricia Flores Ortiz", "cvd": "CVD-2025-00530-037", "hito": False},
    {"id": 38, "archivo": "38_reitero_homologacion.pdf.pdf", "paginas": 38, "fojas": "169 - 206", "fecha": "20/01/2025", "hora": "11:25:00", "instancia": "1° Instancia - 3° Juzgado Civil", "tipo": "ESCRITO / INSTRUMENTOS", "titulo": "Escrito N° 12 — Reitera Homologación y Adjunta Antecedentes", "sumilla": "Adjunta Acuerdo de Pago del 27/11/2024, vigencias de poder y resoluciones análogas (Reg. 1394-2025).", "detalle": "Acompaña acuerdo con firmas legalizadas y tasa Págalo.pe Ticket 250000647052.", "estado_firma": "Firmado Digitalmente — Abog. Elizabeth Patricia Flores Ortiz", "cvd": "CVD-2025-00530-038", "hito": False},
    {"id": 39, "archivo": "39_resolucion_19.pdf.pdf", "paginas": 2, "fojas": "207 - 208", "fecha": "20/01/2025", "hora": "16:18:44", "instancia": "1° Instancia - 3° Juzgado Civil", "tipo": "RESOLUCIÓN JUDICIAL", "titulo": "Resolución N° 19 — Tiene por Presente Acto Jurídico Posterior y Suspende Ejecución", "sumilla": "Aplica art. 339° CPC al Acuerdo de Pago (S/ 66,448.36 en 60 cuotas) y suspende ejecución forzada.", "detalle": "Reconoce el acuerdo del 27/11/2024 como Acto Jurídico Posterior a la Resolución Final (Res. 16), suspende provisionalmente la ejecución y mantiene vigentes medidas cautelares.", "estado_firma": "Firma Digital SINOE — Juez Chevarría Tisnado", "cvd": "CVD-2025-00530-039", "hito": True},
    {"id": 40, "archivo": "40_solicita_conclusion_definitiva.pdf.pdf", "paginas": 2, "fojas": "209 - 210", "fecha": "23/07/2025", "hora": "10:45:00", "instancia": "1° Instancia - 3° Juzgado Civil", "tipo": "ESCRITO / CONSTANCIA NO ADEUDO", "titulo": "Escrito N° 02-2025 — Solicita Conclusión Definitiva por Pago Íntegro", "sumilla": "Acredita cancelación total de S/ 45,000.00 mediante Constancia de No Adeudo del BBVA Perú.", "detalle": "Intiqa Hotel E.I.R.L. adjunta Constancia de No Adeudo emitida el 16/07/2025 por Banco BBVA Perú S.A. certificando la extinción total de la deuda.", "estado_firma": "Presentado ante Mesa de Partes 3° Juzgado Civil (23/07/2025)", "cvd": "CVD-2025-00530-040", "hito": True},
    {"id": 41, "archivo": "41_resolucion_20.pdf.pdf", "paginas": 3, "fojas": "211 - 213", "fecha": "24/07/2025", "hora": "16:40:12", "instancia": "1° Instancia - 3° Juzgado Civil", "tipo": "AUTO DE CONCLUSIÓN Y ARCHIVO", "titulo": "Resolución N° 20 — Conclusión Definitiva del Proceso y Archivo", "sumilla": "Declara conclusión definitiva sin declaración sobre el fondo (art. 322 inc. 1 CPC) y levanta medidas cautelares.", "detalle": "Verifica la cancelación del 100% de la deuda según Constancia de No Adeudo del 16/07/2025. Ordena conclusión definitiva, levantamiento de embargos, devolución del pagaré y archivo definitivo.", "estado_firma": "Firma Digital SINOE — Juez Chevarría Tisnado / Esp. Tapia Sánchez", "cvd": "CVD-2025-00530-041", "hito": True}
]

# ==============================================================================
# BASES SIMULADAS DE INTEROPERABILIDAD RENIEC / SUNAT (PIDE - D. LEG. 1412)
# ==============================================================================
RENIEC_DB = {
    "01285695": {"dni": "01285695", "digito_ver": "4", "nombres": "FRANCISCO GERARDO", "apellido_paterno": "AQUISE", "apellido_materno": "AQUISE", "genero": "M", "fecha_nac": "14/05/1974", "estado_civil": "CASADO", "ubigeo": "210101 - PUNO / PUNO / PUNO", "direccion": "JR. TARAPACÁ N° 272 - BARRIO PORTEÑO", "restricciones": "NINGUNA - HÁBIL PARA ACTOS CIVILES"},
    "01287042": {"dni": "01287042", "digito_ver": "9", "nombres": "JULIANA JUDHY", "apellido_paterno": "GONZALES", "apellido_materno": "AZA", "genero": "F", "fecha_nac": "22/08/1976", "estado_civil": "CASADA", "ubigeo": "210101 - PUNO / PUNO / PUNO", "direccion": "JR. TARAPACÁ N° 272 - BARRIO PORTEÑO", "restricciones": "NINGUNA - HÁBIL PARA ACTOS CIVILES"}
}

SUNAT_DB = {
    "20100130204": {"ruc": "20100130204", "razon_social": "BANCO BBVA PERU", "tipo_contribuyente": "SOCIEDAD ANONIMA ABIERTA", "estado": "ACTIVO", "condicion": "HABIDO", "fecha_inscripcion": "09/10/1951", "actividad_economica": "6419 - OTROS TIPOS DE INTERMEDIACIÓN MONETARIA", "domicilio_fiscal": "AV. REPÚBLICA DE PANAMÁ N° 3055 - SAN ISIDRO - LIMA", "representante": "FLORES ORTIZ ELIZABETH PATRICIA (APODERADA JUDICIAL PUNO)"},
    "20447892153": {"ruc": "20447892153", "razon_social": "INTIQA HOTEL EMPRESA INDIVIDUAL DE RESPONSABILIDAD LIMITADA", "tipo_contribuyente": "EMPRESA INDIVIDUAL DE RESP. LTDA.", "estado": "ACTIVO", "condicion": "HABIDO", "fecha_inscripcion": "18/03/2011", "actividad_economica": "5510 - ACTIVIDADES DE ALOJAMIENTO PARA ESTANCIAS CORTAS", "domicilio_fiscal": "JR. TARAPACÁ N° 272 - PUNO - PUNO - PUNO", "representante": "AQUISE AQUISE FRANCISCO GERARDO (TITULAR - GERENTE)"}
}

NOTIFICACIONES_CUD = [
    {"id": "NOT-2025-88412", "resolucion": "Resolución N° 20 (Auto de Archivo Definitivo)", "fecha_deposito": "24/07/2025 16:42:05", "dia_habil_sig": "25/07/2025", "vencimiento_plazo": "01/08/2025 (5 días hábiles - Consentida)", "estado": "LEÍDA Y CONSENTIDA"},
    {"id": "NOT-2025-10419", "resolucion": "Resolución N° 19 (Suspensión por Acuerdo Art. 339 CPC)", "fecha_deposito": "20/01/2025 16:20:11", "dia_habil_sig": "21/01/2025", "vencimiento_plazo": "24/01/2025 (3 días hábiles)", "estado": "NOTIFICADA VÁLIDAMENTE"},
    {"id": "NOT-2024-99210", "resolucion": "Resolución N° 16 (Ordena Ejecución Forzada)", "fecha_deposito": "27/12/2024 10:15:00", "dia_habil_sig": "30/12/2024", "vencimiento_plazo": "03/01/2025 (3 días hábiles)", "estado": "NOTIFICADA VÁLIDAMENTE"},
    {"id": "NOT-2024-65104", "resolucion": "Resolución N° 014-2024 (Auto de Vista N° 249-2024)", "fecha_deposito": "31/07/2024 22:56:08", "dia_habil_sig": "01/08/2024", "vencimiento_plazo": "15/08/2024 (10 días hábiles)", "estado": "EJECUTORIADA"}
]

AUDIT_LOGS = [
    {"timestamp": "24/07/2025 16:40:12", "actor": "Sistema EJE / IOFE - 3° Juzgado Civil Puno", "accion": "CIERRE DE ÍNDICE DIGITAL FIRMADO (41 ACTUADOS / 335 FOLIOS)", "norma": "Arts. 40–43 D.S. 029-2021-PCM", "hash_integridad": "SHA256-9F84C2B10E77A1D3"},
    {"timestamp": "23/07/2025 10:45:00", "actor": "Mesa Digital Perú — Intiqa Hotel E.I.R.L.", "accion": "INGRESO ESCRITO N° 02-2025 Y CONSTANCIA DE NO ADEUDO BBVA", "norma": "Arts. 46–47 D.S. 029-2021-PCM", "hash_integridad": "SHA256-4A19E8D05B21C9F0"},
    {"timestamp": "20/01/2025 15:18:44", "actor": "Juez Guido Armando Chevarría Tisnado (DNIe NCA 3)", "accion": "EMISIÓN RES. N° 19 — ACTO JURÍDICO POSTERIOR (ART. 339 CPC)", "norma": "Art. 16.2 D.S. 029-2021-PCM", "hash_integridad": "SHA256-7C31B9A22D48E6A1"}
]


def resolver_ruta_real(nombre_archivo):
    ruta = os.path.join(PDF_FOLDER, nombre_archivo)
    if os.path.exists(ruta):
        return nombre_archivo
    alt = nombre_archivo[:-4] if nombre_archivo.endswith(".pdf.pdf") else nombre_archivo + ".pdf"
    if os.path.exists(os.path.join(PDF_FOLDER, alt)):
        return alt
    return None


def calcular_hash_archivo(nombre_archivo):
    nombre_real = resolver_ruta_real(nombre_archivo)
    if nombre_real:
        ruta = os.path.join(PDF_FOLDER, nombre_real)
        sha256 = hashlib.sha256()
        with open(ruta, "rb") as f:
            for chunk in iter(lambda: f.read(8192), b""):
                sha256.update(chunk)
        return sha256.hexdigest().upper()
    return "E3B0C44298FC1C149AFBF4C8996FB92427AE41E4649B934CA495991B7852B855"


@app.route("/")
def index():
    return render_template("index.html", exp=EXPEDIENTE_DATA, total_actuados=len(ACTUADOS))


@app.route("/api/buscar_expediente", methods=["POST"])
def api_buscar_expediente():
    data = request.get_json() or {}
    nca = int(data.get("nca", 1))
    modo = data.get("modo", "codigo")
    codigo = data.get("codigo", "").strip().upper()
    distrito = data.get("distrito", "").strip().upper()
    anio = data.get("anio", "").strip()
    numero = data.get("numero", "").strip()
    parte = data.get("parte", "").strip().upper()

    coincide = False
    if modo == "codigo":
        if codigo in ["00530-2023-0-2101-JR-CI-03", "00530-2023", "530-2023"]:
            coincide = True
    else:
        if (not distrito or distrito == "PUNO") and (not anio or anio == "2023") and (not numero or numero in ["00530", "530"]):
            if not parte or any(k in parte for k in ["BBVA", "INTIQA", "AQUISE", "GONZALES"]):
                coincide = True

    if not coincide:
        return jsonify({"encontrado": False, "resultados": []})

    partes_resp = []
    for p in EXPEDIENTE_DATA["partes"]:
        partes_resp.append({
            "rol": p["rol"],
            "nombre": p["nombre_anon"] if nca == 1 else p["nombre"],
            "documento": "PROTEGIDO (LEY 29733 - NCA 1)" if nca == 1 else p["documento"],
            "representante": "RESERVADO (NCA 1)" if nca == 1 else p["representante"],
            "domicilio_procesal": "PUNO (ANONIMIZADO)" if nca == 1 else p["domicilio_procesal"],
            "casilla_sinoe": p["casilla_sinoe"]
        })

    AUDIT_LOGS.insert(0, {
        "timestamp": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        "actor": f"Usuario Autenticado ID GOB.PE (Nivel NCA {nca})",
        "accion": f"CONSULTA DE EXPEDIENTE N° {EXPEDIENTE_DATA['codigo_expediente']}",
        "norma": "Art. 17 D. Leg. 1412 / Art. 16.2 D.S. 029-2021-PCM",
        "hash_integridad": "SHA256-IDGOBPE88412A"
    })

    return jsonify({
        "encontrado": True,
        "nca": nca,
        "expediente": EXPEDIENTE_DATA,
        "partes": partes_resp,
        "total_actuados": len(ACTUADOS)
    })


@app.route("/api/actuados")
def api_actuados():
    q = request.args.get("q", "").strip().lower()
    instancia = request.args.get("instancia", "TODAS")
    solo_hitos = request.args.get("hitos", "false").lower() == "true"

    resultados = []
    for item in ACTUADOS:
        if solo_hitos and not item["hito"]:
            continue
        if instancia != "TODAS" and instancia.lower() not in item["instancia"].lower():
            continue
        if q:
            texto = f"{item['id']} {item['fecha']} {item['tipo']} {item['titulo']} {item['sumilla']} {item['detalle']}".lower()
            if q not in texto:
                continue
        copia = dict(item)
        copia["existe_archivo"] = resolver_ruta_real(item["archivo"]) is not None
        copia["hash_corto"] = calcular_hash_archivo(item["archivo"])[:20]
        resultados.append(copia)
    return jsonify(resultados)


@app.route("/api/actuado/<int:actuado_id>")
def api_actuado_detalle(actuado_id):
    actuado = next((a for a in ACTUADOS if a["id"] == actuado_id), None)
    if not actuado:
        abort(404)
    nombre_real = resolver_ruta_real(actuado["archivo"])
    hash_full = calcular_hash_archivo(actuado["archivo"])
    copia = dict(actuado)
    copia["existe_archivo"] = nombre_real is not None
    copia["sha256_completo"] = hash_full
    copia["url_pdf"] = f"/pdfs/{nombre_real or actuado['archivo']}"
    copia["resumen_ia_actuado"] = (
        f"Actuado procesal número {actuado['id']} de fecha {actuado['fecha']}, correspondiente a {actuado['titulo']} "
        f"emitido en {actuado['instancia']}. En síntesis: {actuado['sumilla']} {actuado['detalle']}"
    )
    return jsonify(copia)


@app.route("/api/validar_cvd", methods=["POST"])
def api_validar_cvd():
    data = request.get_json() or {}
    cvd = data.get("cvd", "").strip().upper()
    actuado = next((a for a in ACTUADOS if a["cvd"] == cvd), None)
    if not actuado:
        return jsonify({"valido": False, "mensaje": "El Código de Verificación Digital (CVD) no figura en el Índice Digital Firmado IOFE."})
    return jsonify({
        "valido": True,
        "actuado": actuado,
        "sha256": calcular_hash_archivo(actuado["archivo"]),
        "sello_tiempo": f"{actuado['fecha']} {actuado['hora']} PET (TSA INDECOPI)"
    })


@app.route("/api/reniec",methods=["POST"])
def api_reniec():
    data = request.get_json(silent=True) or {}
    dni = re.sub(r"\D", "", str(data.get("dni", "")))
    genero = str(data.get("genero", "M")).upper()

    if len(dni) != 8:
        return jsonify({"ok": False, "error": "Debe ingresar exactamente 8 dígitos numéricos para el DNI."}), 400

    # Retratos fotográficos realistas generados (Masculino y Femenino) indexados por el último dígito del DNI
    fotos_masculinas = [
        "https://randomuser.me/api/portraits/men/32.jpg",
        "https://randomuser.me/api/portraits/men/45.jpg",
        "https://randomuser.me/api/portraits/men/52.jpg",
        "https://randomuser.me/api/portraits/men/64.jpg",
        "https://randomuser.me/api/portraits/men/71.jpg",
        "https://randomuser.me/api/portraits/men/18.jpg",
        "https://randomuser.me/api/portraits/men/29.jpg",
        "https://randomuser.me/api/portraits/men/41.jpg",
        "https://randomuser.me/api/portraits/men/55.jpg",
        "https://randomuser.me/api/portraits/men/83.jpg",
    ]
    fotos_femeninas = [
        "https://randomuser.me/api/portraits/women/44.jpg",
        "https://randomuser.me/api/portraits/women/65.jpg",
        "https://randomuser.me/api/portraits/women/28.jpg",
        "https://randomuser.me/api/portraits/women/33.jpg",
        "https://randomuser.me/api/portraits/women/50.jpg",
        "https://randomuser.me/api/portraits/women/68.jpg",
        "https://randomuser.me/api/portraits/women/19.jpg",
        "https://randomuser.me/api/portraits/women/37.jpg",
        "https://randomuser.me/api/portraits/women/54.jpg",
        "https://randomuser.me/api/portraits/women/79.jpg",
    ]

    idx_foto = int(dni[-1])
    foto_url = fotos_femeninas[idx_foto] if genero == "F" else fotos_masculinas[idx_foto]

    # Base de registros reales conocidos del expediente
    base_reniec = {
        "01285695": {
            "dni": "01285695",
            "digito_ver": "4",
            "apellido_paterno": "AQUISE",
            "apellido_materno": "AQUISE",
            "nombres": "FRANCISCO GERARDO",
            "fecha_nac": "14/05/1971",
            "estado_civil": "CASADO",
            "ubigeo": "210101 - PUNO / PUNO / PUNO",
            "direccion": "JR. LIBERTAD N° 345 - BARRIO CERRO COLORADO - PUNO",
            "restricciones": "NINGUNA",
            "genero": "M",
        },
        "01287042": {
            "dni": "01287042",
            "digito_ver": "9",
            "apellido_paterno": "GONZALES",
            "apellido_materno": "AZA",
            "nombres": "JULIANA JUDHY",
            "fecha_nac": "22/08/1975",
            "estado_civil": "CASADA",
            "ubigeo": "210101 - PUNO / PUNO / PUNO",
            "direccion": "JR. LIBERTAD N° 345 - BARRIO CERRO COLORADO - PUNO",
            "restricciones": "NINGUNA",
            "genero": "F",
        },
    }

    if dni in base_reniec:
        persona = dict(base_reniec[dni])
        # Si el usuario cambió manualmente el selector de género en la consulta, respetar su selección visual
        persona["genero"] = genero
        persona["foto_url"] = fotos_femeninas[idx_foto] if genero == "F" else fotos_masculinas[idx_foto]
        return jsonify({"ok": True, "persona": persona})

    # Generación determinista realista para cualquier otro DNI de 8 dígitos
    apellidos = [
        "MAMANI", "QUISPE", "CONDORI", "APAZA", "CHURA", "TICONA", "CHAMBI", "HUANCA",
        "CCAMA", "FLORES", "PARI", "SUCASACA", "VELASQUEZ", "DELGADO", "RODRIGUEZ", "MENDOZA"
    ]
    nombres_m = [
        "CARLOS ALBERTO", "LUIS MIGUEL", "JOSE ANTONIO", "EDGAR ROLANDO",
        "MARCO ANTONIO", "CESAR AUGUSTO", "HECTOR DANIEL", "RODRIGO ALEJANDRO"
    ]
    nombres_f = [
        "MARIA ELENA", "ROSA MERCEDES", "CARMEN PATRICIA", "VALERIA SOFIA",
        "ANDREA LUCIA", "CLAUDIA BEATRIZ", "GABRIELA ALEJANDRA", "PAOLA FERNANDA"
    ]
    calles_puno = [
        "JR. LIMA N° 418 - CERCADO - PUNO",
        "AV. EL SOL N° 842 - BARRIO PORTEÑO - PUNO",
        "JR. DEUSTUA N° 512 - PUNO",
        "AV. TITIQAQA N° 230 - PUNO",
        "JR. TACNA N° 615 - PUNO",
        "AV. SIMON BOLIVAR N° 1140 - PUNO",
    ]

    seed = int(dni)
    ap_pat = apellidos[seed % len(apellidos)]
    ap_mat = apellidos[(seed // 7) % len(apellidos)]
    nom = nombres_f[seed % len(nombres_f)] if genero == "F" else nombres_m[seed % len(nombres_m)]
    dia = str((seed % 27) + 1).zfill(2)
    mes = str(((seed // 3) % 12) + 1).zfill(2)
    anio = 1968 + (seed % 36)
    estado_civ = ("SOLTERA" if genero == "F" else "SOLTERO") if seed % 2 == 0 else ("CASADA" if genero == "F" else "CASADO")

    persona_gen = {
        "dni": dni,
        "digito_ver": str(seed % 10),
        "apellido_paterno": ap_pat,
        "apellido_materno": ap_mat,
        "nombres": nom,
        "fecha_nac": f"{dia}/{mes}/{anio}",
        "estado_civil": estado_civ,
        "ubigeo": "210101 - PUNO / PUNO / PUNO",
        "direccion": calles_puno[seed % len(calles_puno)],
        "restricciones": "NINGUNA",
        "genero": genero,
        "foto_url": foto_url,
    }
    return jsonify({"ok": True, "persona": persona_gen})


@app.route("/api/sunat", methods=["POST"])
def api_sunat():
    data = request.get_json(silent=True) or {}
    num = re.sub(r"\D", "", str(data.get("ruc", "")))

    # Permite búsqueda de 8 dígitos (DNI asociado a RUC 10) o RUC completo de 11 dígitos
    if len(num) not in (8, 11):
        return jsonify({"ok": False, "error": "Ingrese un número válido de 8 dígitos (DNI/RUC 10) u 11 dígitos (RUC)."}), 400

    ruc_completo = f"10{num}{int(num) % 10}" if len(num) == 8 else num

    base_sunat = {
        "20100130204": {
            "ruc": "20100130204",
            "razon_social": "BANCO BBVA PERU",
            "tipo_contribuyente": "SOCIEDAD ANONIMA",
            "estado": "ACTIVO",
            "condicion": "HABIDO",
            "domicilio_fiscal": "AV. REPUBLICA DE PANAMA NRO. 3055 URB. EL PALOMAR - SAN ISIDRO - LIMA",
            "actividad_economica": "6419 - OTROS TIPOS DE INTERMEDIACION MONETARIA",
            "representante": "APODERADO JUDICIAL / GERENTE DE RECUPERACIONES",
        },
        "20447892153": {
            "ruc": "20447892153",
            "razon_social": "INTIQA HOTEL E.I.R.L.",
            "tipo_contribuyente": "EMPRESA INDIVIDUAL DE RESP. LTDA",
            "estado": "ACTIVO",
            "condicion": "HABIDO",
            "domicilio_fiscal": "JR. LIBERTAD NRO. 345 BARRIO CERRO COLORADO - PUNO - PUNO",
            "actividad_economica": "5510 - ACTIVIDADES DE ALOJAMIENTO PARA ESTANCIAS CORTAS",
            "representante": "AQUISE AQUISE FRANCISCO GERARDO (TITULAR GERENTE)",
        },
    }

    if ruc_completo in base_sunat:
        return jsonify({"ok": True, "empresa": base_sunat[ruc_completo]})

    rubros = [
        "6910 - ACTIVIDADES JURIDICAS Y CONSULTORIA LEGAL",
        "5510 - SERVICIOS DE HOTELERIA Y TURISMO",
        "4711 - COMERCIO AL POR MENOR EN ALMACENES NO ESPECIALIZADOS",
        "6201 - PROGRAMACION INFORMATICA Y GOBIERNO DIGITAL",
        "4100 - CONSTRUCCION DE EDIFICIOS Y OBRAS CIVILES",
    ]
    razones = [
        "CORPORACION ANDINA DEL ALTIPLANO S.A.C.",
        "INVERSIONES TURISTICAS TITICACA E.I.R.L.",
        "CONSORCIO JURIDICO & EMPRESARIAL DEL SUR S.A.C.",
        "SERVICIOS INTEGRALES PUNO S.R.L.",
        "NEGOCIOS E INVERSIONES ALTIPLANICAS S.A.C.",
    ]
    seed = int(ruc_completo[-8:])
    es_persona_nat = ruc_completo.startswith("10")

    return jsonify({
        "ok": True,
        "empresa": {
            "ruc": ruc_completo,
            "razon_social": f"CONTRIBUYENTE PERSONA NATURAL CON NEGOCIO (DNI {num})" if es_persona_nat else razones[seed % len(razones)],
            "tipo_contribuyente": "PERSONA NATURAL CON NEGOCIO" if es_persona_nat else "SOCIEDAD ANONIMA CERRADA",
            "estado": "ACTIVO",
            "condicion": "HABIDO",
            "domicilio_fiscal": f"JR. LIMA NRO. {(seed % 890) + 100} CERCADO - PUNO - PUNO",
            "actividad_economica": rubros[seed % len(rubros)],
            "representante": "TITULAR REGISTRADO EN PADRON RUC - PIDE SUNAT",
        },
    })


@app.route("/api/ingresar_escrito", methods=["POST"])
def api_ingresar_escrito():
    data = request.get_json() or {}
    sumilla = data.get("sumilla", "ESCRITO DIGITAL PRESENTADO POR MESA DIGITAL PERÚ").strip()
    ahora = datetime.now()
    es_habil = (ahora.weekday() < 5) and (8 <= ahora.hour < 17)
    cargo = {
        "numero_cargo": f"MDP-2026-{ahora.strftime('%H%M%S')}",
        "fecha_recepcion": ahora.strftime("%d/%m/%Y %H:%M:%S"),
        "condicion_horaria": "HORARIO HÁBIL (08:00 - 16:45)" if es_habil else "HORARIO INHÁBIL — SE TIENE POR PRESENTADO AL DÍA HÁBIL SIGUIENTE (ART. 46.3 D.S. 029-2021-PCM)",
        "sumilla": sumilla,
        "firma_agente": "FIRMADO DIGITALMENTE POR AGENTE AUTOMATIZADO — MESA DIGITAL PERÚ (PJ-PUNO)",
        "hash_cargo": hashlib.sha256(f"{sumilla}{ahora}".encode()).hexdigest()[:28].upper()
    }
    AUDIT_LOGS.insert(0, {
        "timestamp": cargo["fecha_recepcion"],
        "actor": "Mesa Digital Perú (Agente Automatizado Art. 47)",
        "accion": f"CARGO ELECTRÓNICO {cargo['numero_cargo']}: {sumilla[:45]}",
        "norma": "Arts. 46–47 D.S. 029-2021-PCM",
        "hash_integridad": f"SHA256-{cargo['hash_cargo'][:16]}"
    })
    return jsonify({"ok": True, "cargo": cargo})


@app.route("/api/notificaciones_cud")
def api_notificaciones_cud():
    return jsonify(NOTIFICACIONES_CUD)


@app.route("/api/auditoria")
def api_auditoria():
    return jsonify(AUDIT_LOGS[:25])


@app.route("/pdfs/<path:filename>")
def servir_pdf(filename):
    nombre_real = resolver_ruta_real(filename)
    if not nombre_real:
        abort(404, description=f"El archivo {filename} no se encuentra en static/pdfs/")
    return send_from_directory(PDF_FOLDER, nombre_real, mimetype="application/pdf")

if __name__ == "__main__":
    import os
    os.makedirs(PDF_FOLDER, exist_ok=True)
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)