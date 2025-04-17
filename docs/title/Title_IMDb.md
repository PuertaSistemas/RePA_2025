```
# Estructura de Datos de IMDb para la Gestión de Títulos Audiovisuales

La Base de Datos de Películas de Internet (IMDb) proporciona una colección exhaustiva de datos relacionados con títulos audiovisuales y las personas involucradas en su creación. Para uso personal y no comercial, IMDb ofrece un subconjunto de estos extensos datos como una colección de archivos comprimidos en formato de valores separados por tabulaciones (TSV).[1] Este formato es un estándar para la distribución de grandes conjuntos de datos debido a su eficiencia en almacenamiento y procesamiento.[2, 3] Cada archivo comienza con una fila de encabezado que define las columnas, y los valores faltantes o nulos dentro de los datos se representan con el símbolo '\N'.[1, 4, 5, 6, 7] Los siete conjuntos de datos principales disponibles son `title.akas`, `title.basics`, `title.crew`, `title.episode`, `title.principals`, `title.ratings` y `name.basics`.[1, 4, 7] Dado que estos datos se actualizan diariamente [4], la estructura subyacente debe ser robusta y estar diseñada para adaptarse a actualizaciones frecuentes y nueva información, lo que sugiere una arquitectura de base de datos bien diseñada.

En el núcleo de la estructura de datos de IMDb se encuentran dos identificadores fundamentales: `tconst` y `nconst`. El `tconst` es una cadena alfanumérica que identifica de forma única un título dentro de la base de datos de IMDb, abarcando películas, series de televisión, episodios individuales y videojuegos.[1, 2, 3, 4, 5, 6, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23] Este identificador generalmente comienza con el prefijo 'tt', lo que indica claramente que la entidad es un título.[11, 24] El `tconst` sirve como clave primaria en la tabla `title.basics` y actúa como clave foránea en varias otras tablas relacionadas con títulos, estableciendo vínculos cruciales en todo el conjunto de datos. Su uso constante garantiza que la información sobre un título específico se pueda recuperar y unir de manera eficiente desde diversas fuentes dentro de la base de datos. De manera similar, el `nconst` es una cadena alfanumérica que identifica de forma única un nombre o persona involucrada en los títulos, como actores, directores y escritores.[1, 2, 3, 5, 8, 12, 14, 15, 20, 21, 22, 23, 24, 25, 26, 27, 28] El prefijo 'nm' generalmente denota una entidad de nombre.[11, 24] El `nconst` es la clave primaria para la tabla `name.basics` y funciona como clave foránea en tablas como `title.crew` y `title.principals`, vinculando así a las personas con los títulos en los que han trabajado. La aplicación consistente de estos identificadores únicos sustenta la estructura relacional de los datos de IMDb. También es importante destacar que IMDb otorga un derecho no exclusivo para usar y mostrar estos ID de título de IMDb (`tconst`) e ID de nombre de IMDb (`nconst`), lo que facilita su uso en aplicaciones externas e investigación.[26]

El archivo `title.akas` proporciona títulos alternativos para cada título, a menudo localizados para diferentes regiones e idiomas.[1, 3, 5, 14, 15, 20, 23, 29] El campo `titleId`, que corresponde directamente a un `tconst` de la tabla `title.basics` [1, 5, 14, 15, 20, 22, 23, 29], actúa como clave foránea, vinculando cada entrada de título alternativo a la información central del título. El campo `ordering`, un entero, sirve para identificar de forma única cada fila para un `titleId` dado, ya que un solo título puede tener múltiples títulos alternativos.[1, 5, 14, 15, 20, 23, 29] El título alternativo real se encuentra dentro del campo `title` (cadena) [1, 5, 14, 15, 20, 22, 23, 29], y su aplicabilidad a un área geográfica específica se indica mediante el campo `region` (cadena).[1, 5, 14, 15, 20, 22, 23, 29] El campo `language` (cadena) especifica el idioma del título alternativo.[1, 5, 14, 15, 20, 22, 23, 29] El campo `types` (array) proporciona más contexto sobre la naturaleza del título alternativo, que contiene un conjunto enumerado de atributos como "alternative", "dvd", "festival", "tv", "video", "working", "original" e "imdbDisplay".[1, 5, 14, 20, 22, 23, 29] Es importante tener en cuenta que se pueden agregar nuevos valores a este conjunto en el futuro.[1, 5] El campo `attributes` (array) ofrece términos adicionales no enumerados para describir el título alternativo, como "informal" o "transliterated".[1, 5, 14, 20, 22, 23, 29, 30] Finalmente, el campo `isOriginalTitle` (booleano) indica si la entrada de título alternativo actual es el título original de la obra audiovisual, con '0' representando falso y '1' representando verdadero.[1, 5, 20, 22, 23, 29]

El archivo `title.basics` contiene la información fundamental de cada título en la base de datos de IMDb.[1, 2, 4, 5, 12, 14, 16, 17, 18, 19, 20, 23, 29, 31, 32] A menudo se considera la tabla central para los datos relacionados con los títulos.[4, 5] El campo `tconst` (cadena), como se mencionó anteriormente, es el identificador alfanumérico único para el título.[1, 2, 4, 5, 12, 14, 16, 17, 18, 19, 20, 23, 31, 32] El campo `titleType` (cadena) especifica el formato del título, como "movie", "short", "tvSeries", "tvEpisode" o "video".[1, 2, 4, 5, 12, 14, 17, 18, 19, 20, 23, 31, 32] El `primaryTitle` (cadena) representa el título más popular o el título utilizado en los materiales promocionales [1, 2, 4, 5, 12, 14, 17, 18, 19, 20, 23, 32], mientras que `originalTitle` (cadena) contiene el título en su idioma original.[1, 2, 4, 5, 12, 14, 17, 18, 19, 20, 23, 32] El campo `isAdult` (booleano) indica si el título se clasifica como contenido para adultos, con '0' para no adultos y '1' para adultos.[1, 2, 4, 5, 12, 14, 17, 18, 19, 20, 22, 23, 31, 32] El `startYear` (AAAA) representa el año de lanzamiento de un título, o el año de inicio para las series de televisión [1, 2, 4, 5, 12, 14, 17, 18, 19, 20, 22, 23, 31, 32], mientras que `endYear` (AAAA) indica el año de finalización para las series de televisión, con '\N' para todos los demás tipos de títulos.[1, 2, 4, 5, 12, 14, 17, 18, 19, 20, 22, 23, 32] El campo `runtimeMinutes` proporciona la duración principal del título en minutos.[1, 2, 4, 5, 12, 14, 17, 18, 19, 20, 22, 23, 32] Por último, el campo `genres` (array de cadenas) enumera hasta tres géneros asociados con el título, generalmente como una cadena separada por comas.[1, 2, 4, 5, 12, 14, 16, 17, 18, 19, 20, 22, 23, 31, 32]

El archivo `title.crew` detalla los directores y escritores asociados con cada título.[1, 3, 4, 6, 7, 14, 20, 21, 23, 29, 32, 33, 34] Incluye el `tconst` (cadena) [1, 3, 4, 6, 7, 14, 20, 21, 23, 29, 32, 33, 34], que sirve como clave foránea para `title.basics`. El campo `directors` (array de `nconst`s) contiene una lista de identificadores `nconst` para el (los) director(es) del título dado [1, 3, 4, 6, 7, 14, 20, 21, 23, 29, 32, 33, 34], probablemente separados por comas si hay varios directores. De manera similar, el campo `writers` (array de `nconst`s) proporciona los identificadores `nconst` para el (los) escritor(es) del título [1, 3, 4, 6, 7, 14, 20, 21, 23, 29, 32, 33, 34], también potencialmente separados por comas.

Para los episodios de televisión, el archivo `title.episode` ofrece información específica, vinculando cada episodio a su serie de televisión principal.[1, 3, 4, 6, 11, 14, 15, 20, 21, 23, 29, 32] El campo `tconst` (cadena) aquí identifica de forma única el episodio.[1, 3, 4, 6, 11, 14, 15, 20, 21, 23, 29, 32] El campo `parentTconst` (cadena) es una clave foránea que hace referencia al `tconst` de la serie de televisión principal en el archivo `title.basics`, donde el `titleType` probablemente sea 'tvSeries'.[1, 3, 4, 6, 11, 14, 15, 20, 21, 23, 29, 32, 35] Este campo establece la relación jerárquica entre una serie de televisión y sus episodios constituyentes. El `seasonNumber` (entero) indica la temporada a la que pertenece el episodio [1, 3, 4, 6, 11, 14, 15, 20, 21, 23, 29, 32], y el `episodeNumber` (entero) especifica el número del episodio dentro de esa temporada.[1, 3, 4, 6, 11, 14, 15, 20, 21, 23, 29, 32]

El archivo `title.principals` contiene información sobre los miembros principales del reparto y del equipo para cada título.[1, 3, 4, 5, 12, 14, 16, 20, 21, 22, 23, 33] Esta tabla es crucial para vincular los títulos con las personas involucradas en ellos.[3, 12] Incluye el `tconst` (cadena) [1, 3, 4, 5, 12, 14, 16, 20, 21, 22, 23, 33], nuevamente como clave foránea para `title.basics`. El campo `ordering` (entero) indica el orden de rango de la persona en los créditos del título.[1, 4, 5, 12, 14, 20, 21, 22, 23, 33] El campo `nconst` (cadena) proporciona el identificador único para el nombre/persona [1, 3, 4, 5, 12, 14, 20, 21, 22, 23, 33], actuando como clave foránea para `name.basics`. El campo `category` (cadena) especifica la categoría de trabajo general de la persona, como "actor", "director", "writer" o "producer".[1, 4, 5, 12, 14, 20, 21, 22, 23, 33] El campo `job` (cadena) ofrece un título de trabajo más específico, si corresponde, de lo contrario contiene '\N'.[1, 4, 5, 14, 20, 21, 22, 23, 33] Para aquellos en roles de actuación, el campo `characters` (cadena) contiene el nombre del (los) personaje(s) interpretado(s), o '\N' si no corresponde.[1, 4, 5, 14, 20, 21, 22, 23, 33]

El archivo `title.ratings` proporciona la calificación de IMDb y el número de votos recibidos para cada título.[1, 2, 3, 4, 5, 6, 12, 14, 15, 17, 18, 20, 21, 23, 36] Incluye el `tconst` (cadena) [1, 2, 3, 4, 5, 6, 12, 14, 15, 17, 18, 20, 21, 23, 36] como clave foránea para `title.basics`. El campo `averageRating` proporciona el promedio ponderado de todas las calificaciones de usuarios individuales para el título [1, 2, 3, 4, 5, 6, 12, 14, 15, 17, 18, 20, 21, 23, 36], y el campo `numVotes` indica el número total de votos que ha recibido el título.[1, 2, 3, 4, 5, 6, 12, 14, 15, 17, 18, 20, 21, 23, 36]

Finalmente, el archivo `name.basics` contiene información fundamental sobre las personas involucradas en la industria cinematográfica.[1, 2, 3, 4, 5, 7, 12, 14, 15, 20, 21, 23, 25, 31] El `nconst` (cadena) es el identificador alfanumérico único para el nombre/persona.[1, 2, 3, 4, 5, 12, 14, 15, 20, 21, 23, 25, 31] El `primaryName` (cadena) es el nombre por el cual la persona es más a menudo acreditada.[1, 2, 3, 4, 5, 12, 14, 15, 20, 21, 23, 25, 31] El `birthYear` proporciona el año de nacimiento en formato AAAA [1, 2, 3, 4, 5, 12, 14, 15, 20, 21, 23, 25], y `deathYear` indica el año de fallecimiento en el mismo formato, si corresponde, de lo contrario es '\N'.[1, 2, 3, 4, 5, 12, 14, 15, 20, 21, 23, 25] El campo `primaryProfession` (array de cadenas) enumera las tres profesiones principales de la persona, probablemente como una cadena separada por comas.[1, 2, 3, 4, 5, 12, 14, 15, 20, 21, 23, 25] Por último, el campo `knownForTitles` (array de `tconst`s) proporciona una lista de identificadores `tconst` para los títulos por los que la persona es más conocida, probablemente como una cadena separada por comas.[1, 2, 3, 4, 5, 12, 14, 15, 20, 21, 23, 25]

El conjunto de datos de IMDb está estructurado como una base de datos relacional, con tablas vinculadas mediante el uso consistente de `tconst` y `nconst` como claves primarias y foráneas.[8] Este diseño facilita la recuperación eficiente de información interconectada sobre títulos e individuos. La tabla `title.basics` sirve como centro principal para toda la información relacionada con los títulos, con su identificador `tconst` referenciado en `title.akas` (como `titleId`), `title.crew`, `title.episode`, `title.principals` y `title.ratings`.[1] De manera similar, `nconst` en `name.basics` actúa como el identificador principal para las personas, referenciado en `title.crew` (para directores y escritores) y `title.principals`.[1] La tabla `title.episode` establece una relación padre-hijo al usar `parentTconst` para vincular los episodios a sus respectivas series en `title.basics`.[1, 4, 14, 20, 21, 22, 23] La tabla `title.principals` actúa como un intermediario crucial, conectando títulos (`tconst`) con personas (`nconst`) y proporcionando detalles sobre sus roles y orden de crédito.[1] Además, el campo `knownForTitles` en `name.basics` ofrece un enlace directo de las personas a los títulos por los que son más famosas.[1] Esta estructura interconectada permite una amplia gama de consultas y análisis, aprovechando la gran cantidad de información almacenada dentro de la base de datos de IMDb.

```
+-----------------+      +-----------------+      +-----------------+
| title.basics |----->| title.akas | | title.ratings |
|-----------------+ | |-----------------+ |-----------------|
| tconst (PK) | | | titleId (FK) | | tconst (FK) |
| titleType | | | ordering | | averageRating |
| primaryTitle | | | title | | numVotes |
| originalTitle | | | region | | |
| isAdult | | | language | +-----------------+
| startYear | | | types |
| endYear | | | attributes | +-----------------+
| runtimeMinutes | | | isOriginalTitle |----->| title.crew |
| genres | | +-----------------+ |-----------------|
+-----------------+ | | tconst (FK) |
| +-----------------+ | directors (FK) |
                     +----->| title.episode | | writers (FK) |
|-----------------+      +-----------------+
| tconst (PK) |
| parentTconst (FK)|
| seasonNumber | +-------------------+
| episodeNumber |----->| title.principals |
                            +-----------------+ |-------------------|
| tconst (FK) |
| ordering |
| nconst (FK) |
| category |
| job |
| characters |
                                                   +-------------------+

+-----------------+
| name.basics |
|-----------------|
| nconst (PK) |
| primaryName |
| birthYear |
| deathYear |
| primaryProfession|
| knownForTitles (FK)|
+-----------------+
```

El modelo de datos conceptual ilustra las relaciones entre las siete tablas principales del conjunto de datos de IMDb. La tabla `title.basics`, que contiene información central sobre cada título, es fundamental para el modelo. Está vinculada a `title.akas` a través de `titleId` (que es un `tconst`), a `title.episode` a través de `parentTconst` (para series de televisión y sus episodios), a `title.crew` y `title.principals` a través de `tconst`, y a `title.ratings` también a través de `tconst`. De manera similar, `nconst` en `name.basics` actúa como el identificador principal para las personas, referenciado en `title.crew` (para directores y escritores) y `title.principals`. La tabla `title.episode` establece una relación padre-hijo utilizando `parentTconst` para vincular los episodios a sus respectivas series en `title.basics`.[1, 4, 14, 20, 21, 22, 23] La tabla `title.principals` actúa como una tabla de unión que conecta títulos (`tconst`) con personas (`nconst`) y detalla sus roles. Además, `name.basics` tiene un campo `knownForTitles` que hace referencia a `tconst` en `title.basics`, creando un enlace directo de una persona a sus obras notables. Esta estructura interconectada, construida sobre la base de los identificadores `tconst` y `nconst`, permite la gestión y consulta exhaustiva de la gran cantidad de datos audiovisuales dentro del sistema IMDb.

En conclusión, la estructura de datos de IMDb para la gestión de títulos audiovisuales se basa en un modelo relacional bien definido. El uso de identificadores únicos, `tconst` para títulos y `nconst` para nombres, es fundamental para vincular información a través de los siete archivos TSV proporcionados. La tabla `title.basics` sirve como repositorio central para la información principal del título, mientras que `name.basics` desempeña un papel similar para las personas. Tablas como `title.akas`, `title.crew`, `title.episode`, `title.principals` y `title.ratings` extienden esta información central, proporcionando detalles sobre títulos alternativos, miembros del equipo, detalles de episodios, roles de reparto y equipo, y calificaciones de usuarios, respectivamente. Las relaciones entre estas tablas, establecidas principalmente a través de restricciones de clave foránea en `tconst` y `nconst`, permiten consultas complejas y una comprensión holística de los datos. Para aquellos que trabajan con este conjunto de datos, es importante tener en cuenta los campos tipo array, como géneros y títulos conocidos, que pueden requerir análisis, así como el uso consistente de '\N' para denotar valores faltantes. Los puntos fuertes de este modelo de datos radican en su capacidad para gestionar y consultar una colección grande y diversa de información audiovisual de manera eficiente, lo que lo convierte en un recurso valioso para el desarrollo de software y el análisis de datos en el ámbito del entretenimiento.
```
### Estructura de Datos de IMDb: Descripción Detallada

---

#### **1. Campos de Datos por Archivo**

##### **title.akas**
- **titleId**: Identificador único (tconst) del título principal.
- **ordering**: Número para distinguir múltiples entradas del mismo `titleId`.
- **title**: Título localizado para una región o idioma específico.
- **region**: Código de región (ej: "US", "FR").
- **language**: Idioma del título (ej: "en", "es").
- **types**: Tipos de título alternativo (ej: "alternative", "original").
- **attributes**: Atributos adicionales no estandarizados (ej: "Literal Title").
- **isOriginalTitle**: `1` si es el título original, `0` en caso contrario.

##### **title.basics**
- **tconst**: Identificador único del título.
- **titleType**: Tipo de contenido (ej: "movie", "tvSeries").
- **primaryTitle**: Título principal usado en promoción.
- **originalTitle**: Título en el idioma original.
- **isAdult**: `1` si es contenido adulto, `0` si no.
- **startYear**: Año de lanzamiento o inicio de una serie.
- **endYear**: Año de finalización de una serie (`\N` para otros tipos).
- **runtimeMinutes**: Duración en minutos.
- **genres**: Hasta tres géneros asociados (ej: "Action,Drama").

##### **title.crew**
- **tconst**: Identificador del título.
- **directors**: Lista de `nconst` (IDs de personas) de directores.
- **writers**: Lista de `nconst` (IDs de personas) de guionistas.

##### **title.episode**
- **tconst**: Identificador del episodio.
- **parentTconst**: Identificador de la serie a la que pertenece.
- **seasonNumber**: Número de temporada.
- **episodeNumber**: Número del episodio en la temporada.

##### **title.principals**
- **tconst**: Identificador del título.
- **ordering**: Orden de importancia del rol en el título.
- **nconst**: Identificador de la persona.
- **category**: Categoría del rol (ej: "actor", "producer").
- **job**: Trabajo específico (ej: "director", `\N` si no aplica).
- **characters**: Nombre del personaje interpretado (ej: "James Bond", `\N` si no aplica).

##### **title.ratings**
- **tconst**: Identificador del título.
- **averageRating**: Puntuación promedio ponderada (ej: 8.5).
- **numVotes**: Número total de votos recibidos.

##### **name.basics**
- **nconst**: Identificador único de la persona.
- **primaryName**: Nombre principal de la persona.
- **birthYear**: Año de nacimiento (ej: "1975").
- **deathYear**: Año de fallecimiento (`\N` si no aplica).
- **primaryProfession**: Hasta tres profesiones principales (ej: "actor,producer").
- **knownForTitles**: Lista de `tconst` de títulos destacados.

---

#### **2. Relaciones entre Tablas**

| **Tabla A**           | **Campo**      | **Tabla B**           | **Relación**                                                                 |
|-----------------------|----------------|-----------------------|------------------------------------------------------------------------------|
| `title.akas`          | titleId        | `title.basics`        | Un título puede tener múltiples nombres alternativos.                       |
| `title.crew`          | tconst         | `title.basics`        | Un título tiene un equipo de directores y guionistas.                       |
| `title.crew`          | directors      | `name.basics`         | Los directores guinistasson personas registradas en `name.basics`.         |
| `title.episode`       | parentTconst   | `title.basics`        | Un episodio pertenece a una serie (parentTconst).                          |
| `title.principals`    | tconst         | `title.basics`        | Los roles principales están asociados a un título.                         |
| `title.principals`    | nconst         | `name.basics`         | Las personas en roles principales están registradas en `name.basics`.       |
| `title.ratings`       | tconst         | `title.basics`        | Las calificaciones están vinculadas a un título específico.                |
| `name.basics`         | knownForTitles | `title.basics`        | Los títulos destacados de una persona son registros en `title.basics`.      |

---

#### **3. Diagrama de Relaciones (Descripción Textual)**

```
title.basics (tconst)
│
├─ title.akas (titleId)
├─ title.crew (tconst)
│  ├─ directors (nconst) → name.basics
│  └─ writers (nconst) → name.basics
├─ title.episode (parentTconst)
├─ title.principals (tconst)
│  └─ nconst → name.basics
├─ title.ratings (tconst)
│
name.basics (nconst)
└─ knownForTitles → title.basics (tconst)
```

- **Clave Primaria**: `tconst` (títulos) y `nconst` (personas).
- **Relaciones 1:N**: Un título puede tener múltiples registros en `title.akas`, `title.crew`, `title.episode`, etc.
- **Arrays**: Campos como `genres`, `directors` o `knownForTitles` se almacenan como listas separadas por comas.

#### Relación de las tablas de datos:

title.basics (tconst) -- Tiene 1 a N title.akas (titleId)
title.basics (tconst) -- Tiene 1 a N title.crew (tconst)
title.basics (tconst) -- Tiene 1 a N title.episode (parentTconst)
title.basics (tconst) -- Tiene 1 a N title.principals (tconst)

---

#### **4. Consideraciones Técnicas**
- **Formato**: Archivos TSV comprimidos en GZIP, codificación UTF-8.
- **Valores Nulos**: Representados con `\N`.
- **Arreglos**: Campos como `genres` o `types` usan comas para separar elementos (ej: "Action,Drama").
- **Identificadores Únicos**: `tconst` y `nconst` son claves para joins entre tablas.

---

## Análisis de la Estructura de Datos para Obras Audiovisuales

---

#### **1. Campos de Datos y sus Funciones**

##### **Sección: Datos de la Obra**
- **Estado de la obra**: Indica la fase de producción (ej: preproducción, rodaje).
- **Nombre completo**: Título oficial de la obra.
- **Formato**: Tipo de obra (cortometraje, serie, etc.).
- **Tipo de producción**: Clasifica el enfoque productivo (comunitario, industrial).
- **Género**: Categoría artística principal (ficción, documental, etc.).
- **Clasificación**: Edad recomendada para la audiencia (ej: ATP, +18).
- **Lugar de pertenencia**: Origen geográfico de la obra (Misiones, internacional).
- **Duración**: Duración total en minutos.
- **Idioma original**: Idioma principal de la obra.
- **Subtítulos y doblaje**: Detalles de accesibilidad lingüística.
- **Datos específicos de series**: Número de capítulos y duración promedio por episodio.
- **Resolución y audio**: Calidad técnica del video y configuración de sonido.
- **Fecha de estreno**: Fecha de lanzamiento oficial.
- **Sinopsis y Storyline**: Descripción narrativa breve y resumen extendido.
- **Temática**: Palabras clave que definen el contenido (ej: ecología, derechos humanos).

##### **Sección: Gráfica**
- **Enlaces de gráficas**: URLs para imágenes promocionales (horizontal/vertical).
- **Material de prensa/fotogramas**: Archivos adjuntos para difusión.
- **Tráiler**: Enlace al avance promocional.

##### **Sección: Datos de Producción**
- **Producción colaborativa**: Indica si fue creada por un colectivo.
- **Equipo clave**: Director/a, guionista, productor/a.
- **Equipo técnico y actores**: Lista de roles y participantes.
- **Financiamiento**: Fuentes de fondos (ej: fondos propios, coproducción).

##### **Sección: Otros Datos**
- **Avant Premiere**: Detalles de estreno y financiamiento (ej: apoyo del IAAviM).
- **Tipo de exhibición**: Modalidad de distribución (tradicional/no tradicional).
- **Certificado de exhibición**: Documento oficial validando el circuito de exhibición.

---

#### **2. Relaciones entre Campos y Secciones**

| **Campo Principal**       | **Campos Relacionados**                          | **Dependencia**                                                                 |
|----------------------------|--------------------------------------------------|---------------------------------------------------------------------------------|
| **Formato = "Serie"**      | Número de capítulos, duración por episodio       | Campos obligatorios solo si el formato es "Serie".                              |
| **Posee subtítulos = "Sí"**| Idiomas de subtítulos                            | Los idiomas se registran solo si hay subtítulos.                                |
| **Producción colaborativa**| Nombre del colectivo                             | El nombre del colectivo es requerido si la obra fue colaborativa.               |
| **Temática = "Otros"**     | Descripción de temática adicional               | Campo habilitado para especificar temas no listados.                            |

---

#### **3. Diagrama de Estructura (Jerarquía)**

```
Obra Audiovisual (Entidad Principal)
├─ Datos Básicos
│  ├─ Estado, Formato, Género, Clasificación, Duración
│  ├─ Detalles Técnicos (Idioma, Subtítulos, Resolución, Audio)
│  └─ Narrativa (Sinopsis, Storyline, Temática)
├─ Gráfica
│  ├─ Enlaces de imágenes
│  ├─ Archivos adjuntos (prensa, fotogramas)
│  └─ Tráiler
├─ Producción
│  ├─ Equipo clave (Director, Guionista, Productor)
│  ├─ Equipo técnico y actores
│  └─ Financiamiento
└─ Otros Datos
   ├─ Avant Premiere
   ├─ Exhibición
   └─ Certificados
```

---

#### **4. Consideraciones Clave**
1. **Campos Condicionales**:
   - Algunos campos solo son relevantes bajo ciertas condiciones (ej: "Número de capítulos" solo aplica a series).
   - Los valores como "Otros" en listas habilitan campos de texto adicionales.

2. **Tipos de Datos**:
   - **Listas**: Usadas para opciones predefinidas (ej: género, temática).
   - **Archivos**: Límites de tamaño (ej: 10 MB para material de prensa).
   - **Fechas y Números**: Validación de formato (ej: `date` para estreno, `int` para duración).

3. **Normalización Potencial**:
   - **Tabla "Equipo"**: Podría separarse en subtablas para roles específicos (directores, actores, técnicos).
   - **Tabla "Financiamiento"**: Registro estructurado de fuentes y montos.

4. **Integridad de Datos**:
   - Validar que campos como "Fecha de estreno" sean posteriores al "Estado de la obra = Finalizada".
   - Asegurar que los enlaces de gráficas y tráiler sean URLs válidos.

---

#### **5. Diagrama Relacional Sugerido (Si se Implementa en Base de Datos)**

```
Obras (ID_Obra)
│
├─ DatosBasicos (ID_Obra, Estado, Formato, Género...)
├─ Produccion (ID_Obra, Director, Guionista, Financiamiento...)
│  ├─ EquipoTecnico (ID_Produccion, Rol, Nombre)
│  └─ Actores (ID_Produccion, Nombre, Personaje)
├─ Grafica (ID_Obra, EnlaceHorizontal, EnlaceVertical, Trailer...)
└─ Exhibicion (ID_Obra, LugarAvantPremiere, TipoExhibicion...)
```

- **Clave Primaria**: `ID_Obra` vincula todas las tablas secundarias.
- **Relaciones 1:N**: Una obra tiene múltiples registros en tablas como `EquipoTecnico` o `Actores`.

---

## Definición de la estructúra de datos de Títulos para RePA-IAAViM

Describe las tablas relacionadas con la información de títulos en el sistema de RePA del IAAViM.

##### **title.basics**
- **tconst**: Identificador único del título.
- **primaryTitle**: Título principal usado en promoción.
- **originalTitle**: Título en el idioma original.
- **startYear**: Año de lanzamiento o inicio de una serie o producción en curso.
- **endYear**: Año de finalización de una serie (`\Null` para producción en curso )
- **runtimeMinutes**: Duración en minutos.
- **statusTitle**: Estado actual del título (ej: "En Desarrollo", "Preproducción", "Rodaje", "En Producción", "Postproducción", "En Estreno","Finalizada","Cancelada").
- **productionType**: Tipo de producción (ej: "Comunitaria", "Independiente", "Industrial").
- **originTitle**: Origen del título (ej: "Misiones", "Región", "Argentina","Internacional").
- **numberChapterTitle**: Número de capítulos del título (ej: "1", "2", "3", etc.).
- **audioType**: Tipo de audio (ej: "Mono", "Stereo", "5.1", "7.1", etc.).
- **sinopsisTitle**: Sinopsis del título (ej: "Una historia de amor...", "Una aventura épica...", etc.).
- **storyLineTitle**: Sinopsis del título (ej: "Una historia de amor...", "Una aventura épica...", etc.).
- **avantPremiereSite**: Sitio de la primera preestreno del título (ej: "Netflix", "Amazon Prime", "Disney+", etc.).
- **avantPremiereIaavim**: Booleano que indica si el título tiene una primera preestreno financiado por el IAAViM (ej: "true", "false").

### **title.type**
- **tconst**: Identificador del título.
- **yconst**: Identificador del tipo de contenido.

### **type.content**
- **yconst**: Identificador del tipo de contenido.
- **type_content**: Descripción tipo de contenido (ej: "Cortometraje", "Largometraje", "Serie","Videoclips", etc.).

### **title.clasifi**
- **tconst**: Identificador del título.
- **sconst**: Identificador de la Clasificación

### **clasifi**
- **sconst**: Identificador de la Clasificación
- **clasifi_name**: Nombre de la Clasificación. (ej: "APT", "+13", "+16", "+18", "C", etc.)

### **title.genere**
- **tconst**: Identificador del título.
- **gconst**: Identificador del género.

### **generes**
- **gconst**: Identificador del género.
- **genera_name**: Nombre del género. (ej: "Action,Drama,Ficción,Documental,Animación,Televisivo,Videodanza,Experimental,etc.").

### **title.language**
- **tconst**: Identificador del título.
- **lconst**: Identificador del idioma.

### **title.language.subtitle**
- **tconst**: Identificador del título.
- **lconst**: Identificador del idioma.

### **title.Language.Dubbing**
- **tconst**: Identificador del título.
- **lconst**: Identificador del idioma.

### **language**
- **lconst**: Identificador del idioma.
- **languageDescription**: Descripción del idioma del doblaje (ej: "Español", "Inglés", "Francés", etc.).

### **title.theme**
- **hconst**: Identificador de tema del título.
- **tconst**: Identificador del título.

### **themes**
- **hconst**: Identificador de tema del título.
- **themeDescription**: Descripción del tema del título (ej: "Aventura", "Comedia", "Drama", "Fantasía", "Romance", etc.).

#### **title.funding.sources**
- **tconst**: Identificador del título.
- **fconst**: Identificador de financiamiento del título.
- **foundingAmount**: Monto de financiamiento del título ("Total" o "Parcial").

#### **funding.sources**
- **fconst**: Identificador de financiamiento del título.
- **titlefunding**: Descripción de fuentes de financiamiento del título. (ej: "Banco", "Inversión", "Patrocinio", etc.).

##### **title.resolution**
- **tconst**: Identificador del título.
- **rconst**: Identificador de Resolución.

##### **resolution**
- **rconst**: Identificador de Resolución.
- **resolution**: Descripción de resolución (ej: "480p", "720p", "1080p", "4K", etc.).
- **aspectRatio**: Descripción de relación de aspecto del título (ej: "16:9", "4:3", "2.35:1", etc.).

### **crew.category**
- **cconst**: Identificador de la categoría de equipo.
- **crewType_name**: Nombre del tipo de equipo. (ej: "Director", "Guionista", "Actor", "Productor", "Editor", etc.)

##### **title.episode**
- **tconst**: Identificador del episodio.
- **parentTconst**: Identificador de la serie a la que pertenece.
- **seasonNumber**: Número de temporada.
- **episodeNumber**: Número del episodio en la temporada.

##### **title.principals**
- **tconst**: Identificador del título.
- **nconst**: Identificador de la persona.
- **cconst**: Identificador de la categoría de equipo.
- **ordering**: Orden de importancia del rol en el título.
- **job**: Trabajo específico (ej: "director", `\N` si no aplica).
- **characters**: Nombre del personaje interpretado (ej: "James Bond", `\N` si no aplica).

##### **name.basics**
- **nconst**: Identificador único de la persona.
- **primaryName**: Nombre principal de la persona.
- **birthYear**: Año de nacimiento (ej: "1975").
- **deathYear**: Año de fallecimiento (`\N` si no aplica).
- **primaryProfession**: Hasta tres profesiones principales (ej: "actor,producer").
- **knownForTitles**: Lista de `tconst` de títulos destacados.

Analizada la propuesta, verifica si la misma cumple con la normalización del sistema estructurado.
Realiza una propuesta superadora, que mantenga las mejores prácticas de normalización para bases de datos estructuradas con SQL.

**Recomendaciones adicionales:**
    * Divide el prompt en secciones claras para facilitar la comprensión.
    * Utiliza viñetas o listas para organizar la información.
    * Sé conciso y preciso en tu lenguaje.
    * Prueba diferentes variaciones del prompt para obtener los mejores resultados.

---

**Análisis de la propuesta original**

1. **Observaciones generales**
   - Hay abundantes tablas de enlace (`title.type`, `title.clasifi`, `title.genere`, etc.) que replican el patrón de “tabla de entidad + tabla de asociación”.
   - Varios campos repiten nombres muy largos y poco estandarizados (e.g. `sinopsisTitle` vs `storyLineTitle`).
   - Se mezclan datos atómicos (ej. `startYear`) con listas o descripciones libres (ej. `genres` en `generes` que incluye “Action,Drama…”).
   - Algunas tablas (como `title.language`, `title.language.subtitle` y `title.Language.Dubbing`) duplican la misma relación: título ↔ idioma.
   - La tabla `title.funding.sources` incluye el atributo `foundingAmount` con valores semánticos (“Total”/“Parcial”), mejor modelados como un enumerado.

2. **Cumplimiento de la normalización**
   - **1NF (Atomicidad):**
     - **Incumple**: en tablas de entidad se ven campos con listas o cadenas separadas por comas (p.ej. `generes.genera_name`).
   - **2NF (Dependencia total de clave primaria):**
     - Listas de atributos en tablas de asociación como `title.funding.sources` usan descripciones en lugar de `fconst`→`funding.sources`.
   - **3NF (No dependencia transitiva):**
     - Ej. en `title.basics` existen campos redundantes (`sinopsisTitle` y `storyLineTitle` parecen sinónimos).
   - **BCNF:**
     - Duplicación de relaciones título–idioma en tres tablas distintas rompe la forma normal más estricta.

---

## Propuesta superadora: Modelo relacional normalizado

### 1. Entidades principales

- **titles**
  - `id` (PK, UUID)
  - `primary_title` (VARCHAR)
  - `original_title` (VARCHAR)
  - `start_year` (SMALLINT)
  - `end_year` (SMALLINT, NULL)
  - `runtime_minutes` (INTEGER, NULL)
  - `status` (ENUM: desarrollo, preproducción, rodaje, producción, postproducción, estreno, finalizada, cancelada)
  - `production_type` (ENUM: comunitaria, independiente, industrial)
  - `origin` (ENUM: Misiones, Región, Argentina, Internacional)
  - `synopsis` (TEXT)
  - `storyline` (VARCHAR(250))
  - `avant_site` (VARCHAR, NULL)
  - `avant_iaavim` (BOOLEAN)

- **content_types**
  - `id` (PK, SERIAL)
  - `name` (VARCHAR: cortometraje, largometraje, serie, videoclip, etc.)

- **classifications**
  - `id` (PK, SERIAL)
  - `code` (ENUM: ATP, +13, +16, +18, C)

- **genres**
  - `id` (PK, SERIAL)
  - `name` (VARCHAR)

- **languages**
  - `id` (PK, SERIAL)
  - `name` (VARCHAR)

- **themes**
  - `id` (PK, SERIAL)
  - `name` (VARCHAR)

- **resolutions**
  - `id` (PK, SERIAL)
  - `label` (ENUM: 480p, 720p, 1080p, 4K, etc.)
  - `aspect_ratio` (VARCHAR: “16:9”, “4:3”,…)

- **funding_sources**
  - `id` (PK, SERIAL)
  - `name` (VARCHAR: banco, patrocinio, IAAviM, INCAA, propios, etc.)

- **crew_categories**
  - `id` (PK, SERIAL)
  - `name` (VARCHAR: director, guionista, actor, productor, editor,…)

- **people**
  - `nconst` (PK, VARCHAR)
  - `name` (VARCHAR)
  - `birth_year` (SMALLINT, NULL)
  - `death_year` (SMALLINT, NULL)
  - `professions` (VARCHAR[], NULL)

### 2. Tablas de relación (Muchos a Muchos y 1:1 donde corresponda)

- **title_content_types**
  - `title_id` (FK → titles.id)
  - `content_type_id` (FK → content_types.id)

- **title_classifications**
  - `title_id` (FK → titles.id)
  - `classification_id` (FK → classifications.id)

- **title_genres**
  - `title_id` (FK → titles.id)
  - `genre_id` (FK → genres.id)

- **title_languages**
  - `title_id` (FK → titles.id)
  - `language_id` (FK → languages.id)
  - `subtitles` (BOOLEAN)
  - `dubbing` (BOOLEAN)

- **title_themes**
  - `title_id` (FK → titles.id)
  - `theme_id` (FK → themes.id)

- **title_resolutions**
  - `title_id` (FK → titles.id)
  - `resolution_id` (FK → resolutions.id)

- **title_funding**
  - `title_id` (FK → titles.id)
  - `funding_source_id` (FK → funding_sources.id)
  - `contribution` (ENUM: total, parcial)

- **title_episodes**
  - `episode_id` (PK, FK → titles.id)
  - `series_id` (FK → titles.id)
  - `season_number` (SMALLINT)
  - `episode_number` (SMALLINT)

- **title_crew**
  - `title_id` (FK → titles.id)
  - `person_id` (FK → people.nconst)
  - `crew_category_id` (FK → crew_categories.id)
  - `ordering` (SMALLINT)
  - `job` (VARCHAR, NULL)
  - `characters` (VARCHAR, NULL)

### 3. Ventajas de la propuesta

- **1NF**: todos los campos son atómicos; las listas pasan a tablas de relación.
- **2NF**: cada atributo depende de la PK completa; no hay columnas que dependan sólo de parte de la clave.
- **3NF**: no existen dependencias transitivas; e.g. `code`→`classification.name` está aislado en su propia tabla.
- **Escalabilidad**: se pueden agregar nuevos géneros, idiomas o estados sin alterar esquemas existentes.
- **Claridad**: cada tabla tiene un propósito único, nombres consistentes y tipos estándar (ENUM, VARCHAR, INTEGER, BOOLEAN).

---

> Con este diseño, la base de datos queda **completamente normalizada**, modular y de fácil mantenimiento, ajustada a las mejores prácticas relacionales para sistemas de gestión de títulos audiovisuales.

---
