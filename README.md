# A Fervenza Tinta

Bienvenido al proyecto "A Fervenza Tinta". Este documento sirve como punto de partida para entender la arquitectura, el stack tecnológico y el estado actual del proyecto.

##  Estado del Proyecto

**Fase Actual: Diseño Arquitectónico y Fundamentación**

El proyecto se encuentra en una etapa inicial de desarrollo, con un fuerte enfoque en establecer una arquitectura limpia, robusta y escalable.

-   [x] Principios arquitectónicos definidos (Clean Architecture, TDD, Vertical Slices).
-   [x] Stack tecnológico seleccionado y configurado en Docker.
-   [] Diseño de la entidad `User`.
-   [] Diseño de la entidad `Tokens`.
-   [x] Diseño de las interfaces y abstracciones para servicios compartidos (`IEmailService`).
-   [ ] Implementación del primer slice de negocio (`users`).
-   [ ] Implementación de los flujos de autenticación.

## Descripción

`Afervenzatinta` es una aplicación web full-stack diseñada para gestionar via web la Banda Marinera A Fervenza Tinta. Consta de un backend API desarrollado en Python (FastAPI) y un frontend en JavaScript (React), todo ello orquestado y containerizado con Docker.

## Arquitectura y Principios de Diseño

La arquitectura de este proyecto es su pilar fundamental. Seguimos una combinación de principios modernos para asegurar que el sistema sea mantenible, testeable y escalable.

-   **Clean Architecture:** Se respeta una estricta separación de capas. Las dependencias siempre apuntan hacia el interior, protegiendo el núcleo del negocio de los detalles de la infraestructura.
-   **DDD-Driven Design (DDD):** El núcleo de la aplicación es el **Dominio**. Las entidades y value objects se modelan con **Pydantic**, convirtiéndose en la fuente única de la verdad para la lógica de negocio.
-   **Vertical Slices:** La funcionalidad se organiza en "slices" o módulos verticales por característica de negocio (ej. `users`, `tokens`). Cada slice es autocontenido y expone su funcionalidad a través de casos de uso.
-   **Test-Driven Development (TDD):** Se fomenta el desarrollo guiado por pruebas para garantizar la robustez y correctitud del código.

## Tech Stack

| Categoría         | Tecnología                                       |
| ----------------- | ------------------------------------------------ |
| **Backend**       | Python 3.12, FastAPI, Uvicorn                    |
| **Persistencia**  | SQLAlchemy (ORM), Alembic (Migraciones), asyncpg |
| **Frontend**      | React.js, npm                                    |
| **Base de Datos** | PostgreSQL 16                                    |
| **Containerización** | Docker, Docker Compose                           |
| **Dependencias (Python)** | Poetry                                           |

## Estructura del Proyecto

El proyecto está organizado en tres directorios principales en la raíz: `backend/`, `frontend/`, y `docker/`. La estructura interna del backend sigue los principios de Clean Architecture:

```
backend/app/
│
├── {slice_name}/          # Directorio para un slice de negocio (ej. users, tokens)
│   └── domain/            # Lógica y modelos de dominio (Pydantic)
│   └── application/       # Casos de uso (lógica de aplicación)
│   └── infrastructure/    # Implementacion Especifica
│   └── presentation/      # Routers y DTOs de la API
│
├── shared/                # Componentes compartidos (interfaces, utilidades base)
│
└── infrastructure/        # Implementaciones concretas (repositorios, servicios externos)
```

## Cómo Ejecutar el Proyecto

### Requisitos

-   Docker
-   Docker Compose

### Pasos para la Ejecución

1.  Clona el repositorio.
2.  Asegúrate de que no haya otros servicios corriendo en los puertos listados abajo.
3.  Desde la raíz del proyecto, ejecuta el siguiente comando:

    ```bash
    docker-compose -f docker/docker-compose.yml up --build
    ```

### Acceso a los Servicios

Una vez levantado, los servicios estarán disponibles en:

-   **Frontend:** `http://localhost:5173`
-   **Backend API:** `http://localhost:8000`
-   **Documentación de la API (Swagger):** `http://localhost:8000/api/v1/docs`
-   **Base de Datos (PostgreSQL):** `localhost:5432`

## Próximos Pasos

La hoja de ruta inmediata se centra en implementar las capas fundacionales:

1.  Implementar el slice Users.
2.  Implementar el caso de uso de tokens y su implementacion especcifica.
3.  Crear el endpoint `POST /users` para  usuarios y tokens.
4.  Implementar policies y guards.
5.  Una vez implementado estos slices, desarrollar el frontend para estos slices


