# Proyecto: Battleship IA

**Materia:** Inteligencia Artificial  
**Fecha:** 12 de mayo de 2025  
**Integrantes:**
- Barragán Osorio Diego José María
- Garduño Sánchez Moisés
- Moreno Barranco Ulises

---

## 🎯 Descripción del Proyecto

Este proyecto consiste en el desarrollo de un agente inteligente capaz de jugar al clásico juego de **Battleship** (Hundir la Flota). El entorno se modela con dos tableros (propio y enemigo), donde el agente toma decisiones para disparar, registrar resultados y adaptarse al comportamiento del oponente.

---

## 🧠 Objetivo del Agente

El objetivo principal del agente es **hundir todos los barcos del oponente**, utilizando estrategias basadas en:
- Razonamiento bajo incertidumbre
- Planeación secuencial
- Inferencia sobre el entorno parcial

---

## ⚙️ Características del Entorno

| Característica         | Descripción                                                                 |
|------------------------|-----------------------------------------------------------------------------|
| Observabilidad         | Parcial. Solo se conocen los resultados de disparos (agua, tocado, hundido) |
| Determinismo           | Determinista. Las acciones tienen resultados predecibles                    |
| Secuencialidad         | Secuencial. Cada disparo influye en los próximos                            |
| Dinamicidad            | Estático. El entorno solo cambia con las acciones del jugador               |
| Discretización         | Discreto. El entorno es una grilla finita de celdas                         |
| Número de agentes      | Multiagente competitivo (2 jugadores)                                       |

---

## 🧩 Justificación del Entorno

- **Relevancia didáctica:** Permite explorar temas clave de IA como inferencia, planeación y entornos parcialmente observables.
- **Aplicabilidad:** Modela escenarios reales de defensa, exploración y toma de decisiones con información incompleta.
- **Complejidad adecuada:** Tiene suficiente reto sin ser inmanejable, ideal para estrategias de IA.

---
