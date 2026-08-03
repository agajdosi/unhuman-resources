

# Unhuman Resources

Este es el código original para la intervención artística Unhuman Resources.
Espeja los servidores de noticias idnes.cz y lidovky.cz en sitios web falsos https://lidov.ky y https://l-dnes.cz, que contienen menciones alteradas de Andrej Babis, primer ministro checo y dueño de idnes.cz y lidovky.cz.
Para ver algunos de los artículos editados, visite la página que redirige aleatoriamente: https://babis.media.

Para ver la versión en inglés, consulte una de las cinco capturas de pantalla traducidas:
- https://babis.media/12
- https://babis.media/18
- https://babis.media/29
- https://babis.media/37
- https://babis.media/43

## Código feo

Este no es código limpio, es código feo.
Difícil de leer, difícil de entender.
No es agradable.
Caótico.
Fue el trabajo de una sola persona.
Y era un artista.
Perseguido por la fecha límite.
Y por eso es feo.
Se aprecia la presión del tiempo en la arquitectura de toda la aplicación y en el estilo del código.
Y lo siento por eso.

Se publica "tal cual":
- para archivar el proyecto,
- para compartirlo con cualquier persona interesada en la obra de arte y su contexto exacto,
- para evitar que sea comprado y encerrado en alguna estúpida colección privada,
- para apoyar a la comunidad y no a quienes la arruinan y quieren lavarse las manos sucias,
- para salvarme de tentaciones futuras.

Comparte, reutiliza, modifica, disfruta <3

## Fork limpiado

Si te interesa reutilizar este proyecto para tus fines, probablemente deberías esperar unas semanas, ya que publicaré el fork limpiado pronto.


El enlace al fork limpiado se publicará aquí pronto.
Lo haré.
Lo prometo.
Bombardéame con correos electrónicos para acelerar el proceso.

## Ejecutar el proyecto

### Requisitos previos

1. Python3 y pip3 instalados
2. Tener el puerto 8080 disponible (o usar otro puerto disponible)

Alternativamente:

- usa un entorno virtual `venv`, actívalo con: `source ./venv/bin/activate` y luego continúa

### Uso local

1. Instala los paquetes necesarios con pip3:
   ```
    pip3 install -r requirements.txt
   ```
2. Ejecuta la aplicación:
   1. para falsificar idnes.cz usa: `python3 main.py -p 8080 -s localhost=idnes.cz -d True`
   2. para falsificar lidovky.cz usa: `python3 main.py -p 8080 -s localhost=lidovky.cz -d True`
3. abre el navegador y accede a la dirección http://localhost:8080
   
### Problemas
En caso de cualquier problema, abre un issue en este repositorio o envíame un correo electrónico a andreas.gajdosik( a t )gmail.com.
