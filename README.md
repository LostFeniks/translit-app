# 🔄 Транслитератор

<div align="center">

![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![Flask](https://img.shields.io/badge/Flask-3.0.0-green)
![SQLite](https://img.shields.io/badge/SQLite-3-blue)
![License](https://img.shields.io/badge/license-MIT-green)
[![CI/CD Pipeline](https://github.com/LostFeniks/translit-app/actions/workflows/ci.yml/badge.svg)](https://github.com/LostFeniks/translit-app/actions/workflows/ci.yml)

**Веб-приложение для транслитерации текста с русского на латиницу в реальном времени**

[🚀 Демо](#-демонстрация) • [📖 О проекте](#-о-проекте) • [🛠️ Технологии](#-технологии) • [🚀 Установка](#-установка-и-запуск)

</div>

---

## 📺 Демонстрация

### Главная страница
![Главная страница](https://via.placeholder.com/800x400/667eea/ffffff?text=Translit+App+-+Main+Page)

### Работа приложения в браузере

<table>
<tr>
<td width="50%">

#### 1. Ввод текста
Введите текст на русском в первое поле

![Ввод текста](https://via.placeholder.com/400x200/4CAF50/ffffff?text=Ввод:+%22вода%22)

</td>
<td width="50%">

#### 2. Мгновенная транслитерация
Транслитерация появляется автоматически

![Транслитерация](https://via.placeholder.com/400x200/2196F3/ffffff?text=Результат:+%22voda%22)

</td>
</tr>
<tr>
<td width="50%">

#### 3. История переводов
Нажмите "Показать историю"

![История](https://via.placeholder.com/400x200/FF9800/ffffff?text=История+переводов)

</td>
<td width="50%">

#### 4. API запросы
Работа через curl/Postman

![API](https://via.placeholder.com/400x200/9C27B0/ffffff?text=REST+API)

</td>
</tr>
</table>

### Демонстрация API

**Запрос:**
```bash
curl -X POST http://localhost:8080/api \
  -H "Content-Type: application/json" \
  -d '{"data": "апишка"}'