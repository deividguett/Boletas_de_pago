# Documentación del Proyecto: Sistema de Planillas (Casino & Entertainment S.A.)

Este repositorio contiene el sistema automatizado para el control y generación de boletas de pago de la empresa **Casino & Entertainment S.A.** El proyecto implementa un flujo de trabajo profesional utilizando **Git** y **GitHub** para garantizar la continuidad operativa y mitigar riesgos en el entorno de producción.

## 📋 Descripción del Script
El archivo principal `generar_boletas.py` es un script desarrollado en **Python** encargado de procesar la información del personal y estructurar los cálculos de haberes, descuentos y aportes legales de la organización de manera automatizada.

## 🚀 Nuevas Implementaciones (Control de Versiones)
Para cumplir con las políticas laborales de la empresa sin alterar la estabilidad del sistema, se estructuró el desarrollo en base a ramas de trabajo independientes:
*   **Rama `main` (Producción):** Aloja exclusivamente el código estable y auditado que opera actualmente en la empresa.
*   **Rama `feature/add-bonus` (Desarrollo):** Línea de trabajo aislada utilizada para programar, probar e integrar de forma segura el **Bono de S/ 200** destinado a todo el personal, previniendo caídas o corrupción de datos operativos en producción.

## 🛠️ Requisitos del Sistema
Para ejecutar y colaborar en este proyecto, se requiere contar con las siguientes herramientas instaladas:
1.  **Python 3.x** o superior.
2.  **Git** (para el control de versiones local).
3.  Una cuenta activa en **GitHub** (para el respaldo remoto).

## 💻 Instrucciones de Ejecución Local
Para probar el script en tu computadora, sigue estos pasos desde tu terminal de comandos:

1.  **Clonar el repositorio:**
    ```bash
    git clone https://github.com
    ```
2.  **Acceder a la carpeta del proyecto:**
    ```bash
    cd boletas_de_pago
    ```
3.  **Ejecutar el script de boletas:**
    ```bash
    python generar_boletas.py
    ```
