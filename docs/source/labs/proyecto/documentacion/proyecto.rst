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

En este laboratorio se implementará un sistema eieManager 2.0, el cual tendrá algunos cambios, ya que se necesita que este tenga una estructura, la cual permite cubrir despliegues a gran escala y con posibilidad de expansión, ya que se quiere manejar una cantidad grande de dispositivos a nivel industrial, para esto, se utilizara un protocolo llamado MQTT, usando el patrón publish/suscribe y como broker el Eclipse Mosquito.
Para el diseño de los modelos virtuales de los dispositivos de la fábrica se utilizará el concepto de digital twin, que para este proyecto se encontró un framework open-source llamado Eclipse Ditto, junto con el proxy para analizar el estado del sistema sin tener que acudir directamente a los dispositivos, el mismo, cumple ciertos atributos como: modificabilidad dado que se puede modificar el código de forma simple y añadir o eliminar dispositivos, y la testeabilidad dado que tiene que ser sometido a una serie de pruebas para que se muestre su efectividad.
Ahora bien, con respecto al patrón broker este tiene básicamente la misma estructura, que consta de un cliente, un broker, y los servers, donde en este caso para el cliente se tiene un cliente, en cuanto el broker correspondería al eie manager 2.0, el cual lo compone el Ditto, MQTT y eie manager config, y de último en lugar de los servers, se encuentran los eie devices los cuales son los dispositivos que se van a controlar.

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

**REQ.1** Se debe tener soporte de la estructura Thing para albergar los features, configuration y status de los objetos.

**REQ.2** Se debe soportar callbacks para modificar la propiedad configuration en un feature del twin.

**REQ.3** El programa debe soportar la recepcion de mensajes Ditto para poder actualizar los Twin

**REQ.4** Para facilitar el mantenimiento del sistema, se debe contar de un Device discovery

Requerimientos funcionales para eie-manager:
============================================

**REQ.5** El eie manager debe contar de un Rest API que contenga el Ditto, MQTT y el eie manager config.

**REQ.6** El programa debe poder administrar dispositivos con un Rest API y un protocolo Ditto.

**REQ.7** El programa debe garantizar la seguridad de acceso.

**REQ.8** El programa debe estar bien documentado para su legibilidad.

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

  @enduml


*2.* Modificacion de ``status``

.. uml::

  @startuml
  eieDevice->Mosquitto: update request to update the status sent
  Mosquitto-> Ditto: request packed into a JSON
  Ditto-> Client: MQTT process the new status request and sent it to Cliente
  
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

  
    
