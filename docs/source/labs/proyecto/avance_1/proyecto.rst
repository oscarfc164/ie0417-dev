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


**Justificacion**
================

En este laboratorio se implementara un sistema eieManager 2.0, el cual tendra algunos cambios ya que se necesita que este 
tenga una estructura la cual permite curbir despliegues a gran escala y con posibilidad de expansion, ya que se quiere manejar 
una cantidad grande de dispositivos a nivel industrial, para esto, se utilizara una nueva arquitectura llamada MQTT, usando 
el patron publish/suscribe y como broker el Eclipse Mosquito, para el diseno de loa modelos virtuales de los dispositivos de la
fabrica se utilizara el concepto de digital twin, que para este proyecto se encontro un framework open-source llamado Eclipse
Ditto, junto con el proxy para analizar el estado del sistema sin tener que acudir directamente a los dispositivos, esta arquitectura
cumple ciertos atributos como: modificabilidad dado que se puede modificar el codigo de forma simple y anadir o eliminar dispositivos, y la testeabilidad 
dado que tiene que ser sometido a una serie de pruebas para que se muestre su efectividad, ahora bien, con respecto al patron broker este tiene basicamente la misma estructura, que consta de un cliente, un broker, y los servers, donde en este caso para el cliente se tiene un cliente, en cuanto el broker corresponderia al eie manager 2.0, el cual lo compone el Ditto, MQTT y eie manager config, y de ultimo en lugar de los servers, se encuentran los eie devices los cuales son los dispositivos que se van a controlar.

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


Requerimientos funcionales para eie-device:
===========================================

**REQ.1** se debe tener soporte de la estructura Thing para albergar los features, configuration y status de los objetos.

**REQ.2** Se debe soportar callbacks para modificar la propiedad configuration en un feature del twin.

**REQ.3** El programa debe soportar la recepcion de mensajes Ditto para actualizar el el Twin del dispositivo mediante MQTT.

**REQ.4** El eie device debe contar de un Device discovery, el cual facilita el mantenimiento del sistema.

Requerimientos funcionales para eie-manager:
============================================

**REQ.5** El eie manager debe contar de un Rest API que contenga el Ditto, MQTT y el eie manager config.

**REQ.6** El programa debe poder administrar dispositivos mediante el uso de un Rest API y un protocolo Ditto.

**REQ.7** El programa debe garantizar la seguridad de acceso a los dispositivos, donde solo los sistemas autorizados puedan acceder o modificar los dispositivos.

**REQ.8** El programa debe ser escalable, para poder administrar muchos dispositivos y tambien, tener la posibilidad de expandirse con el tiempo.

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

Diagramas
=========

*1.* Modificacion de ``configuration``

.. uml::

  @startuml
  client->Ditto: update request to configuration sent
  Ditto-> Mosquitto: request packed into a JSON
  Mosquitto-> eieDevice: MQTT process the configuration 
  eieDevice->eieDevice: Internal to Proccess to implement the request
  eieDevice-> Mosquitto: Request Respond
  Mosquitto->Ditto: Request Respond
  Ditto->client: Request Respond
  @enduml

*2.* Modificacion de ``status``

.. uml::

  @startuml
  client->Ditto: update request to update the status sent
  Ditto-> Mosquitto: request packed into a JSON
  Mosquitto-> eieDevice: MQTT process the new status request and sent it to eieDevice
  eieDevice->eieDevice: Internal to Proccess to implement the request
  eieDevice-> Mosquitto: Request Respond
  Mosquitto->Ditto: Request Respond about status
  Ditto->client: Request Respond status
  @enduml

*3.* ``eie-device`` publica configuracion incial

.. uml::

  @startuml
  eieDevice-> Ditto: MQTT Topic get the initial configuration
  Ditto->Ditto: Convert the initial into a JSON
  Ditto->eieConfiguration: Get information about the device
  eieConfiguration->eieConfiguration: Convert it into a hash table
  eieConfiguration->eieConfiguration: Register completed
  eieConfiguration->Ditto: device register msg
  Ditto->eieDevice: device register msg
  @enduml

  
    
