*************
Avance de proyecto 1
*************
+---------------+--------------+
| Estudiante    |  Carnet      |
+---------------+--------------+
|| Oscar Fallas | B92861       |
+---------------+--------------+
|| Steven Mora  | B95109       |
+---------------+--------------+


**Aspectos importantes**
================

En este laboratorio se implementara un sistema eieManager 2.0, el cual tendra algunos cambios ya que se necesita que este 
tenga una estructura la cual permite curbir despliegues a gran escala y con posibilidad de expansion, ya que se quiere manejar 
una cantidad grande de dispositivos a nivel industrial, para esto, se utilizara una nueva arquitectura llamada MQTT, usando 
el patron publish/suscribe y como broker el Eclipse Mosquito, para el diseno de loa modelos virtuales de los dispositivos de la
fabrica se utilizara el concepto de digital twin, que para este proyecto se encontro un framework open-source llamado Eclipse
Ditto, junto con el proxy para analizar el estado del sistema sin tener que acudir directamente a los dispositivos.

Caracteristicas utiles de Ditto que serviran para el proyecto:
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
* Para la administracion de dispositivos se utilizara un REST API y un Ditto Protocolo.
* Se utilizara el concepto Thing para abstraer el hardware.
* En cuanto a la seguridad, se utilizara Policy para que solo los sistemas autorizados puedan leer o modificar los dispositivos.


EIE manager
===========

La secuencia del handshake para el eieManager-config seria el siguiente:

* Se suscribe al topic eie-manager/config/device_discovery/request, para poder recibir solicitudes desde los dispositivos. Nóte que esto se debe hacer una sola vez al iniciar el servicio.

* Al recibir un mensaje de solicitud desde un dispositivo:

* Generar un identificador único tipo string (Thing ID) a partir del namespace indicado. Para esto puede utilizar un número secuencial (ej: temp_sensor:5). Debe almacenar estos identificadores o la secuencia en alguna estructura de datos para no repetirlos en el futuro.

* Registrar el nuevo Thing con el REST API de Ditto.

* Una vez registrado, se publica el mensaje de respuesta para el dispositivo en el topic eie-manager/config/device_discovery/response, utilizando el mismo correlation-id del mensaje de solicitud.

EIE device
==========

Para la comunicacion de eieDevice con eieManager, se utilizara una secuencia handshake la cual consta de lo siguiente:

* Al iniciar un dispositivo, se recibe un archivo JSON el cual posee la estructura del Thing.

* Suscribirse al topic eie-manager/config/device_discovery/response.

* Publicar el mensaje JSON con la configuración del dispositivo en el topic eie-manager/config/device_discovery/request. 
   Como parte de este mensaje, se debe generar y enviar un número aleatorio llamado correlation-id, que permita correlacionar la solicitud y la respuesta.

* Esperar por la respuesta del mensaje con el mismo correlation-id. Si la misma no se recibe luego de un período de timeout,
   se puede volver a enviar el mismo mensaje con otro correlation-id.

* Al recibir el mensaje de respuesta correspondiente, se extrae y guarda el identificador del dispositivo generado por eie-manager-config, llamado Thing ID.

Para la comunicacion con Mosquitto, se utilizara el cliente Paho MQTT C, tambien, en la instalacion del cmake va a contener los archivos binarios y aplicaciones, 
los headers, el archivo pkg-config.
Es importante mencionar que la estructura de Thing contiene features y propiedades de configuracion y status, las cuales a como su traduccion lo dice, almacena las 
caracteristicas de cada dispositivo.

+--------------------------------------------------+
|| **Estimacion en el tiempo de trabajo**          |
+===========================+======================+
|| Tarea                    | Estimacion de tiempo |
+---------------------------+----------------------+
|| Crear documentacion      | 3 semanas            |
||                          |                      |
+---------------------------+----------------------+
|| Implementar eie Device   | 2 semanas            |
||                          |                      |
+---------------------------+----------------------+
|| Implementar eie manager  | 2 semanas            |
||                          |                      |
+---------------------------+----------------------+
|| Implementar unit testing | 2 semanas            |
||                          |                      |
+---------------------------+----------------------+
|| Implementar API          | 2 semanas            |
||                          |                      |
+---------------------------+----------------------+


