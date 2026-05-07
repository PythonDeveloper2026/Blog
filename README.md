# Django Blog Loyihasi

Bu yerda to'liq ishlangan Django Blog loyihasi taqdim etilgan. Ushbu loyiha barcha talablarga javob beradigan qilib tayyorlangan (Autentifikatsiya, Postlarni CRUD qilish, Qidirish, Saralash, Paginatsiya va Profil tizimlari).

## O'rnatish va ishga tushirish

1. Virtual muhitni ishga tushirish:
```bash
.\venv\Scripts\activate
```

2. Kerakli kutubxonalarni o'rnatish (agarda o'rnatilmagan bo'lsa):
```bash
pip install django==4.2.* Pillow django-crispy-forms crispy-bootstrap5
```

3. Migratsiyalarni amalga oshirish (allaqachon qilingan):
```bash
python manage.py makemigrations
python manage.py migrate
```

4. Superuser yaratish (Admin panelga kirish uchun):
```bash
python manage.py createsuperuser
```

5. Loyihani ishga tushirish:
```bash
python manage.py runserver
```
Shundan so'ng, loyihani `http://127.0.0.1:8000/` manzilidan ko'rishingiz mumkin.

## Xususiyatlar
- Tizimga kirish / Ro'yxatdan o'tish (Login/Register)
- Shaxsiy profil va uni tahrirlash
- Postlar yozish, tahrirlash va o'chirish (Faqat post egasi yoki Admin uchun)
- Postlarni qidirish (Sarlavha va matn bo'yicha)
- Bosh sahifada postlarni saralash
- Barcha sahifalarda Pagination tizimi ishlaydi
- Zamonaviy va moslashuvchan (Responsive) interfeys (Bootstrap 5 yordamida)
