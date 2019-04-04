#   CLASE BASE
class Humano:
    def __init__(self, edad):
        self.edad = edad
        print('Soy Humano, de ',edad, 'años')
        
    def hablar(self, mensaje):
        print (mensaje)
        
# CLASES DERIVADAS
class Profesor(Humano):
    def __init__(self):
        print('Soy Profesor, heredo de humano')
    def darClases(self, tema):
        print( 'La clase de hoy es de:', tema)
        
class Estudiante(Humano):
    def __init__(self, escuela):
        self.escuela = escuela
        print('Soy Estudiante, heredo de humano, y del colegio', escuela)
    def realizarPregunta(self, pregunta):
        print( 'Profe, ¿', pregunta, '?')
       
#   CLASES DE HERENCIA MULTIPLE, IMPORTA EL ORDEN PARA EL __init___
class ComunidadEdu(Profesor, Estudiante):
    pass

class ComunidadEdu2(Estudiante, Profesor):
    pass


pedro = Estudiante('Badia')
raul = Profesor()

pedro.hablar('Hola, soy Pedro')
raul.hablar( 'Hola, soy Raul')

raul.darClases('Análisis de señales y sistemas')
pedro.realizarPregunta('Copaimos')


flor = ComunidadEdu()
flor.hablar('Tengo herencia multiple y la inicialización la lleva a cabo Profesor')
flor.darClases( 'FLOR' )
flor.realizarPregunta( 'FLOR' )

ana = ComunidadEdu2('Badia')
flor.hablar('Tengo herencia multiple y la inicialización la lleva a cabo Estudiante')
