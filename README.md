# == DESCRIPCIÓN DE gDNA CRISPR-Cas9 DESIGNER ==
# Herramienta ligera diseñada para escanear una secuencia diana de ADN y obtener gRNA candidatos para edición génica mediante el sistema CRISPR-Cas9 (Streptococcus pyogenes).
# El programa permite la entrada de la secuencia de ADN manualmente o leyendo un documento directamente desde archivo de texto plano (.txt). A continuación, identifica los motivos PAM (NGG) y aplica criterios de calidad biológica para seleccionar todas las posibles guías que garantizan la estabilidad del complejo gRNA-Cas9.
# Finalmente, se genera una guía con los gRNA posibles, permitiendo además la opción de exportar un archivo de texto (.txt) con el informe completo.

# El control de calidad se basa en dos criterios fundamentales:
#  - Porcentaje de pares de bases GC: Para asegurar la especificidad de la unión y una actividad de Cas9 adecuada, se recomienda que la secuencia guía contenga entre un 40 y un 60% de pares GC, reduciendo la probabilidad de off-targets.
#  - Ausencia de secuencias de poli-T: Una secuencia de cuatro o más T seguidas pueden interferir en la transcripción haciendo que la RNA Polimerasa III termine según encuentra esta secuencia. Por ende, se seleccionan guias que no contengan esta señal.

# == PRÓXIMOS PASOS ==
# - Creación de una matriz de puntuación y adición de nuevos criterios y recomendaciones para otorgar un resultado más gradual y consistente.
# - Cálculo de puntajes de especificidad e interacciones off-target mediante alineamiento con el genoma de referencia.

# == LICENCIA ==
# Este proyecto se distribuye bajo la licencia MIT. Consulta el archivo LICENSE para más información.

