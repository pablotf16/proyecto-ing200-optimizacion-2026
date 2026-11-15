# =============================================================================
# DATOS DEL PROYECTO 2026-2: FIESTA DE VERANO DE VILLA PEUMAYÉN
# ING200: Optimización
#
# Este archivo contiene los datos del proyecto y dos funciones de apoyo:
#   - demanda(artistas): estima el público que convoca un conjunto de artistas.
#   - mostrar_parrilla(parrilla): muestra una parrilla y su público por noche.
# Puede copiar todo su contenido directamente en su script.
#
# Los montos están en millones de pesos (MM$).
# =============================================================================

# -----------------------------------------------------------------------------
# NOCHES DEL FESTIVAL
# FACTOR_NOCHE[n]: fracción de la demanda que asiste la noche n.
# -----------------------------------------------------------------------------
NOCHES = ['Viernes', 'Sábado', 'Domingo']
FACTOR_NOCHE = {'Viernes': 0.90, 'Sábado': 1.00, 'Domingo': 0.85}

# -----------------------------------------------------------------------------
# RECINTOS
# recinto: capacidad (personas) y costo de arriendo por noche (MM$).
# Todos los recintos están disponibles las tres noches.
# -----------------------------------------------------------------------------
RECINTOS = {
    'Plaza de Armas':     {'capacidad': 12000, 'costo': 30},
    'Medialuna':          {'capacidad': 7500,  'costo': 18},
    'Gimnasio Municipal': {'capacidad': 4200,  'costo': 8},
}

# -----------------------------------------------------------------------------
# ARTISTAS
# nombre: género, nivel ('G' grande, 'M' mediano, 'P' pequeño),
#         popularidad (índice individual), costo (MM$) y noches disponibles.
# -----------------------------------------------------------------------------
ARTISTAS = {
    'La Sonora Copihue':           {'genero': 'Cumbia',  'nivel': 'G', 'popularidad': 1.08, 'costo': 52, 'noches': ['Viernes', 'Sábado', 'Domingo']},
    'Los Volcanes':                {'genero': 'Rock',    'nivel': 'G', 'popularidad': 0.97, 'costo': 40, 'noches': ['Viernes', 'Sábado', 'Domingo']},
    'Camila Arrebol':              {'genero': 'Pop',     'nivel': 'G', 'popularidad': 1.03, 'costo': 48, 'noches': ['Viernes', 'Sábado', 'Domingo']},
    'Kevo Flow':                   {'genero': 'Urbano',  'nivel': 'G', 'popularidad': 1.12, 'costo': 58, 'noches': ['Viernes', 'Sábado']},
    'Los Cumbiancheros del Ñuble': {'genero': 'Cumbia',  'nivel': 'M', 'popularidad': 0.94, 'costo': 18, 'noches': ['Viernes', 'Sábado', 'Domingo']},
    'Grupo Tierra Sur':            {'genero': 'Folclor', 'nivel': 'M', 'popularidad': 1.06, 'costo': 15, 'noches': ['Viernes', 'Sábado', 'Domingo']},
    'La Nena Real':                {'genero': 'Urbano',  'nivel': 'M', 'popularidad': 1.01, 'costo': 22, 'noches': ['Viernes', 'Sábado', 'Domingo']},
    'Las Hermanas Quintral':       {'genero': 'Pop',     'nivel': 'M', 'popularidad': 0.92, 'costo': 17, 'noches': ['Viernes', 'Sábado', 'Domingo']},
    'Ruta Cinco':                  {'genero': 'Rock',    'nivel': 'M', 'popularidad': 1.04, 'costo': 16, 'noches': ['Viernes', 'Sábado', 'Domingo']},
    'Banda Fogata':                {'genero': 'Cumbia',  'nivel': 'P', 'popularidad': 1.11, 'costo': 7,  'noches': ['Viernes', 'Sábado', 'Domingo']},
    'Conjunto Raíces del Valle':   {'genero': 'Folclor', 'nivel': 'P', 'popularidad': 0.98, 'costo': 5,  'noches': ['Viernes', 'Sábado', 'Domingo']},
    'Las Cantoras de Peumayén':    {'genero': 'Folclor', 'nivel': 'P', 'popularidad': 0.89, 'costo': 4,  'noches': ['Viernes', 'Sábado', 'Domingo']},
    'Niebla Austral':              {'genero': 'Rock',    'nivel': 'P', 'popularidad': 0.95, 'costo': 6,  'noches': ['Viernes', 'Sábado', 'Domingo']},
    'Tomás del Lago':              {'genero': 'Pop',     'nivel': 'P', 'popularidad': 1.09, 'costo': 8,  'noches': ['Viernes', 'Sábado', 'Domingo']},
    'Yisus Beat':                  {'genero': 'Urbano',  'nivel': 'P', 'popularidad': 0.91, 'costo': 6,  'noches': ['Viernes', 'Sábado', 'Domingo']},
}

# -----------------------------------------------------------------------------
# REGLAS ENTRE ARTISTAS
# TELONEROS: si se contrata al primero, el segundo debe presentarse la misma noche.
# EXCLUSIONES: no pueden ser contratados ambos.
# -----------------------------------------------------------------------------
TELONEROS = [('La Sonora Copihue', 'Banda Fogata')]
EXCLUSIONES = [('La Nena Real', 'Yisus Beat')]

# -----------------------------------------------------------------------------
# PARÁMETROS GENERALES
# -----------------------------------------------------------------------------
PRESUPUESTO = 250              # MM$: artistas + arriendo de recintos + plan de seguridad
UMBRAL_SEGURIDAD = 20000       # personas: si el público total del festival lo supera, se exige el plan
COSTO_SEGURIDAD = 25           # MM$

# -----------------------------------------------------------------------------
# PARÁMETROS DE LA FUNCIÓN DE DEMANDA (usados por la función demanda)
# -----------------------------------------------------------------------------
BASE_NIVEL = {'G': 4200, 'M': 1900, 'P': 750}
FACTOR_GENERO = {'Cumbia': 1.20, 'Urbano': 1.10, 'Pop': 1.00, 'Rock': 0.95, 'Folclor': 0.65}
ARRASTRE = 0.20                # aumento de la base de artistas M y P si en la noche hay un artista G
MISMO_GENERO = -0.15           # por cada par de artistas del mismo género
DOS_GRANDES = -0.10            # por cada par de artistas grandes
AFINIDAD = {('Cumbia', 'Urbano'): 0.06, ('Pop', 'Rock'): 0.05, ('Pop', 'Urbano'): 0.03}


def demanda(artistas):
    """Demanda esperada (personas) de un conjunto de artistas que se presentan la misma noche.

    No considera la noche ni el recinto: el público esperado de la noche n en el recinto r es
        min(FACTOR_NOCHE[n] * demanda(artistas), capacidad del recinto r),
    redondeado al entero más cercano.

    Ejemplo: demanda(['Kevo Flow', 'Ruta Cinco', 'Banda Fogata'])
    También acepta conjuntos de uno o dos artistas (útil, por ejemplo, para analizar cancelaciones).
    """
    artistas = list(artistas)
    hay_grande = any(ARTISTAS[a]['nivel'] == 'G' for a in artistas)
    base = 0.0
    for a in artistas:
        datos = ARTISTAS[a]
        b = BASE_NIVEL[datos['nivel']] * FACTOR_GENERO[datos['genero']] * datos['popularidad']
        if hay_grande and datos['nivel'] != 'G':
            b *= 1 + ARRASTRE
        base += b
    interaccion = 0.0
    for i in range(len(artistas)):
        for j in range(i + 1, len(artistas)):
            a1, a2 = ARTISTAS[artistas[i]], ARTISTAS[artistas[j]]
            if a1['genero'] == a2['genero']:
                interaccion += MISMO_GENERO
            interaccion += AFINIDAD.get((a1['genero'], a2['genero']), AFINIDAD.get((a2['genero'], a1['genero']), 0))
            if a1['nivel'] == 'G' and a2['nivel'] == 'G':
                interaccion += DOS_GRANDES
    return base * (1 + interaccion)


def mostrar_parrilla(parrilla, titulo='Parrilla del festival'):
    """Muestra una parrilla con su público y su costo por noche.

    parrilla: lista de tuplas (noche, recinto, [artista1, artista2, artista3]), por ejemplo
        [('Viernes', 'Medialuna', ['Kevo Flow', 'Ruta Cinco', 'Banda Fogata']), ...]
    El costo mostrado incluye artistas y recinto, pero no el plan de seguridad.
    """
    import matplotlib.pyplot as plt
    orden = {n: i for i, n in enumerate(NOCHES)}
    parrilla = sorted(parrilla, key=lambda t: orden[t[0]])
    print(f'{titulo}\n' + '-' * 100)
    total_pub, total_costo, publicos = 0, 0, []
    for noche, recinto, artistas in parrilla:
        pub = round(min(FACTOR_NOCHE[noche] * demanda(artistas), RECINTOS[recinto]['capacidad']))
        costo = sum(ARTISTAS[a]['costo'] for a in artistas) + RECINTOS[recinto]['costo']
        total_pub += pub; total_costo += costo; publicos.append(pub)
        nombres = ', '.join(f"{a} ({ARTISTAS[a]['nivel']})" for a in artistas)
        print(f'{noche:8s} | {recinto:18s} | {pub:6,d} personas | {costo:4d} MM$ | {nombres}')
    print('-' * 100 + f'\nTotal: {total_pub:,} personas | {total_costo} MM$ (sin plan de seguridad)')
    plt.figure(figsize=(7, 3.5))
    barras = plt.bar([p[0] for p in parrilla], publicos, color=['#1565c0', '#c62828', '#2e7d32'][:len(parrilla)])
    for b, (noche, recinto, _) in zip(barras, parrilla):
        plt.text(b.get_x() + b.get_width() / 2, b.get_height(), recinto, ha='center', va='bottom', fontsize=9)
    plt.ylabel('Público esperado'); plt.title(titulo); plt.tight_layout(); plt.show()
