from datetime import date, datetime
from app.processors.motor_asistencia import Punch, reconstruir, fecha_operativa

def p(s,t): return Punch(datetime.fromisoformat(s),t)
def test_mario_doble_salida_usa_ultima():
    j=reconstruir(date(2026,8,3),"Diurno",[p("2026-08-03 07:10","Entrada"),p("2026-08-03 14:30","Salida"),p("2026-08-03 15:35","Salida")])
    assert j.salida.hour==15 and j.salida.minute==35
    assert j.horas==7.92 and "MARCACION_INCOMPLETA" not in j.incidencias
def test_entrada_entrada_salida():
    j=reconstruir(date(2026,8,3),"Diurno",[p("2026-08-03 06:58","Entrada"),p("2026-08-03 07:02","Entrada"),p("2026-08-03 15:30","Salida")])
    assert j.entrada.minute==58
def test_comida_exceso_suma_retraso():
    j=reconstruir(date(2026,8,3),"Diurno",[p("2026-08-03 07:20","Entrada"),p("2026-08-03 12:00","Salida"),p("2026-08-03 12:50","Entrada"),p("2026-08-03 15:30","Salida")])
    assert j.retraso_entrada==20 and j.retraso_comida==20 and j.total_retraso==40 and j.estado=="AUTOMATICO"
def test_limites_salida_temprana():
    def early(m): return reconstruir(date(2026,8,3),"Diurno",[p("2026-08-03 07:00","Entrada"),Punch(datetime(2026,8,3,15,30)-__import__("datetime").timedelta(minutes=m),"Salida")])
    assert early(10).salida_temprana_auto==0
    assert early(11).salida_temprana_auto==11
    assert early(30).salida_temprana_auto==30
    assert early(31).salida_temprana_pendiente==31
def test_total_60_61():
    j60=reconstruir(date(2026,8,3),"Diurno",[p("2026-08-03 08:00","Entrada"),p("2026-08-03 15:30","Salida")])
    j61=reconstruir(date(2026,8,3),"Diurno",[p("2026-08-03 08:01","Entrada"),p("2026-08-03 15:30","Salida")])
    assert j60.estado=="AUTOMATICO" and j61.estado=="PENDIENTE"
def test_salida_tardia_informativa():
    j=reconstruir(date(2026,8,3),"Diurno",[p("2026-08-03 07:00","Entrada"),p("2026-08-03 16:01","Salida")])
    assert j.impacto=="INFORMATIVO" and j.consecuencia=="NORMAL"
def test_nocturno_fecha_operativa():
    assert fecha_operativa(datetime(2026,8,4,5,30),"Nocturno")==date(2026,8,3)
def test_incompleta_y_ausencia():
    assert reconstruir(date(2026,8,3),"Diurno",[p("2026-08-03 07:00","Entrada")]).consecuencia=="FALTA_INJUSTIFICADA"
    assert reconstruir(date(2026,8,3),"Diurno",[]).consecuencia=="FALTA_INJUSTIFICADA"

if __name__ == "__main__":
    tests=[v for k,v in sorted(globals().items()) if k.startswith("test_") and callable(v)]
    for test in tests: test()
    print(f"{len(tests)} pruebas OK")

